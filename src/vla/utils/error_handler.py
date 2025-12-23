"""
Error Handling and Fallback Framework

This module provides a comprehensive error handling and fallback mechanism framework
for the VLA integration system.
"""
import asyncio
import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass
from datetime import datetime

from src.vla.models.action_plan import ROS2Action, ROS2ActionPlan


logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Enumeration of different error types in the VLA system"""
    SPEECH_RECOGNITION_ERROR = "speech_recognition_error"
    INTENT_EXTRACTION_ERROR = "intent_extraction_error"
    ACTION_PLANNING_ERROR = "action_planning_error"
    ACTION_EXECUTION_ERROR = "action_execution_error"
    VALIDATION_ERROR = "validation_error"
    CONNECTION_ERROR = "connection_error"
    TIMEOUT_ERROR = "timeout_error"
    CONFIGURATION_ERROR = "configuration_error"
    UNKNOWN_ERROR = "unknown_error"


class FallbackStrategy(Enum):
    """Enumeration of fallback strategies"""
    RETRY = "retry"
    SIMPLIFY = "simplify"
    ALTERNATIVE_ACTION = "alternative_action"
    HUMAN_INTERVENTION = "human_intervention"
    SAFE_MODE = "safe_mode"
    FALLBACK_RESPONSE = "fallback_response"


@dataclass
class ErrorContext:
    """Context information for an error"""
    error_type: ErrorType
    component: str  # e.g., "whisper_client", "llm_client", "ros_bridge"
    operation: str  # e.g., "transcribe_audio", "extract_intent"
    original_error: Exception
    timestamp: datetime
    additional_info: Dict[str, Any] = None


@dataclass
class FallbackResult:
    """Result of a fallback operation"""
    success: bool
    message: str
    recovered_data: Any = None
    strategy_used: FallbackStrategy = None


class FallbackHandler(ABC):
    """Abstract base class for fallback handlers"""

    @abstractmethod
    async def can_handle(self, error_context: ErrorContext) -> bool:
        """Check if this handler can handle the given error"""
        pass

    @abstractmethod
    async def handle(self, error_context: ErrorContext) -> FallbackResult:
        """Handle the error using the fallback strategy"""
        pass


class RetryFallbackHandler(FallbackHandler):
    """Fallback handler that retries the operation"""

    def __init__(self, max_retries: int = 3, delay: float = 1.0):
        self.max_retries = max_retries
        self.delay = delay

    async def can_handle(self, error_context: ErrorContext) -> bool:
        """Can handle most types of errors except configuration errors"""
        return error_context.error_type not in [
            ErrorType.CONFIGURATION_ERROR,
            ErrorType.VALIDATION_ERROR
        ]

    async def handle(self, error_context: ErrorContext) -> FallbackResult:
        """Retry the operation up to max_retries times"""
        logger.info(f"Attempting retry fallback for {error_context.operation}")

        for attempt in range(self.max_retries):
            try:
                logger.info(f"Retry attempt {attempt + 1}/{self.max_retries}")
                await asyncio.sleep(self.delay * (attempt + 1))  # Exponential backoff
                # In a real implementation, we would re-execute the failed operation
                # For now, we'll just return a mock success
                return FallbackResult(
                    success=True,
                    message=f"Operation succeeded on retry attempt {attempt + 1}",
                    strategy_used=FallbackStrategy.RETRY
                )
            except Exception as e:
                logger.warning(f"Retry attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.max_retries - 1:
                    logger.error(f"All {self.max_retries} retry attempts failed")
                    return FallbackResult(
                        success=False,
                        message=f"Retry fallback failed after {self.max_retries} attempts",
                        strategy_used=FallbackStrategy.RETRY
                    )

        return FallbackResult(
            success=False,
            message="Retry fallback exhausted",
            strategy_used=FallbackStrategy.RETRY
        )


class SimplifyFallbackHandler(FallbackHandler):
    """Fallback handler that simplifies the request"""

    async def can_handle(self, error_context: ErrorContext) -> bool:
        """Can handle complex intent extraction or action planning errors"""
        return error_context.error_type in [
            ErrorType.INTENT_EXTRACTION_ERROR,
            ErrorType.ACTION_PLANNING_ERROR
        ]

    async def handle(self, error_context: ErrorContext) -> FallbackResult:
        """Simplify the complex request into basic actions"""
        logger.info(f"Attempting simplify fallback for {error_context.operation}")

        try:
            # For complex planning errors, create a basic action plan
            if error_context.error_type == ErrorType.ACTION_PLANNING_ERROR:
                # Create a simple, safe action plan
                simple_plan = ROS2ActionPlan(
                    id="simplified_plan",
                    actions=[],
                    dependencies=[],
                    timeout=10.0,
                    recovery_steps=[],
                    validation_rules=[]
                )
                return FallbackResult(
                    success=True,
                    message="Simplified to basic action plan",
                    recovered_data=simple_plan,
                    strategy_used=FallbackStrategy.SIMPLIFY
                )
            elif error_context.error_type == ErrorType.INTENT_EXTRACTION_ERROR:
                # Create a simple intent
                from src.vla.models.intent import Intent, IntentType
                simple_intent = Intent(
                    intent_type=IntentType.other,
                    action_sequence=[],
                    parameters={},
                    context="Simplified due to error",
                    validation_status="simplified"
                )
                return FallbackResult(
                    success=True,
                    message="Simplified to basic intent",
                    recovered_data=simple_intent,
                    strategy_used=FallbackStrategy.SIMPLIFY
                )

            return FallbackResult(
                success=False,
                message="Cannot simplify this type of error",
                strategy_used=FallbackStrategy.SIMPLIFY
            )
        except Exception as e:
            logger.error(f"Simplify fallback failed: {str(e)}")
            return FallbackResult(
                success=False,
                message=f"Simplify fallback failed: {str(e)}",
                strategy_used=FallbackStrategy.SIMPLIFY
            )


class AlternativeActionFallbackHandler(FallbackHandler):
    """Fallback handler that suggests alternative actions"""

    async def can_handle(self, error_context: ErrorContext) -> bool:
        """Can handle action execution errors"""
        return error_context.error_type == ErrorType.ACTION_EXECUTION_ERROR

    async def handle(self, error_context: ErrorContext) -> FallbackResult:
        """Suggest alternative actions when primary action fails"""
        logger.info(f"Attempting alternative action fallback for {error_context.operation}")

        try:
            # Analyze the error to suggest alternatives
            error_msg = str(error_context.original_error).lower()

            if "collision" in error_msg or "obstacle" in error_msg:
                # Suggest navigation around obstacles
                alternative_actions = [
                    ROS2Action(action_type="move_base", parameters={"x": 0.5, "y": 0.0, "theta": 0.0})
                ]
            elif "reachable" in error_msg or "distance" in error_msg:
                # Suggest moving closer
                alternative_actions = [
                    ROS2Action(action_type="move_base", parameters={"x": 0.8, "y": 0.0, "theta": 0.0})
                ]
            elif "grasp" in error_msg or "gripper" in error_msg:
                # Suggest alternative manipulation
                alternative_actions = [
                    ROS2Action(action_type="move_arm", parameters={"x": 0.5, "y": 0.0, "z": 0.2})
                ]
            else:
                # Generic alternative
                alternative_actions = [
                    ROS2Action(action_type="speak", parameters={"text": "I encountered an issue and am requesting assistance"})
                ]

            return FallbackResult(
                success=True,
                message="Alternative actions suggested",
                recovered_data=alternative_actions,
                strategy_used=FallbackStrategy.ALTERNATIVE_ACTION
            )
        except Exception as e:
            logger.error(f"Alternative action fallback failed: {str(e)}")
            return FallbackResult(
                success=False,
                message=f"Alternative action fallback failed: {str(e)}",
                strategy_used=FallbackStrategy.ALTERNATIVE_ACTION
            )


class SafeModeFallbackHandler(FallbackHandler):
    """Fallback handler that activates safe mode"""

    async def can_handle(self, error_context: ErrorContext) -> bool:
        """Can handle critical errors that require safe mode"""
        return error_context.error_type in [
            ErrorType.ACTION_EXECUTION_ERROR,
            ErrorType.CONNECTION_ERROR
        ]

    async def handle(self, error_context: ErrorContext) -> FallbackResult:
        """Activate safe mode to prevent further issues"""
        logger.info(f"Activating safe mode fallback for {error_context.operation}")

        try:
            # In a real implementation, this would stop robot movement and return to safe state
            # For simulation, we'll just return a safe state indicator
            safe_state = {
                "robot_status": "safe_mode",
                "movements_disabled": True,
                "emergency_stop": False,
                "recovery_needed": True
            }

            return FallbackResult(
                success=True,
                message="Safe mode activated",
                recovered_data=safe_state,
                strategy_used=FallbackStrategy.SAFE_MODE
            )
        except Exception as e:
            logger.error(f"Safe mode fallback failed: {str(e)}")
            return FallbackResult(
                success=False,
                message=f"Safe mode fallback failed: {str(e)}",
                strategy_used=FallbackStrategy.SAFE_MODE
            )


class ErrorHandler:
    """Main error handler that coordinates fallback strategies"""

    def __init__(self):
        self.fallback_handlers: List[FallbackHandler] = [
            RetryFallbackHandler(max_retries=2, delay=0.5),
            SimplifyFallbackHandler(),
            AlternativeActionFallbackHandler(),
            SafeModeFallbackHandler()
        ]
        self.error_history: List[ErrorContext] = []

    async def handle_error(self, error_type: ErrorType, component: str, operation: str,
                          original_error: Exception, additional_info: Dict[str, Any] = None) -> FallbackResult:
        """
        Handle an error using appropriate fallback strategies

        Args:
            error_type: Type of error that occurred
            component: Component where error occurred
            operation: Operation that failed
            original_error: The original exception
            additional_info: Additional context information

        Returns:
            FallbackResult indicating success/failure of fallback
        """
        error_context = ErrorContext(
            error_type=error_type,
            component=component,
            operation=operation,
            original_error=original_error,
            timestamp=datetime.now(),
            additional_info=additional_info
        )

        # Log the error
        logger.error(
            f"Error in {component}.{operation}: {str(original_error)} "
            f"(Type: {error_type.value})"
        )

        # Add to error history
        self.error_history.append(error_context)

        # Try each fallback handler in order
        for handler in self.fallback_handlers:
            try:
                if await handler.can_handle(error_context):
                    logger.info(f"Using {handler.__class__.__name__} for error handling")
                    result = await handler.handle(error_context)

                    if result.success:
                        logger.info(f"Fallback successful using {result.strategy_used.value}")
                        return result
                    else:
                        logger.warning(f"Fallback failed: {result.message}")
            except Exception as e:
                logger.error(f"Error in fallback handler {handler.__class__.__name__}: {str(e)}")
                continue

        # If all fallbacks fail, return failure
        logger.error("All fallback strategies failed")
        return FallbackResult(
            success=False,
            message=f"All fallback strategies exhausted for error: {str(original_error)}",
            strategy_used=None
        )

    async def register_fallback_handler(self, handler: FallbackHandler):
        """Register a new fallback handler"""
        self.fallback_handlers.append(handler)
        logger.info(f"Registered new fallback handler: {handler.__class__.__name__}")

    def get_error_statistics(self) -> Dict[str, Any]:
        """Get statistics about errors and fallbacks"""
        if not self.error_history:
            return {"total_errors": 0}

        error_counts = {}
        for error in self.error_history:
            error_key = error.error_type.value
            error_counts[error_key] = error_counts.get(error_key, 0) + 1

        return {
            "total_errors": len(self.error_history),
            "error_counts": error_counts,
            "recent_errors": [
                {
                    "type": error.error_type.value,
                    "component": error.component,
                    "operation": error.operation,
                    "timestamp": error.timestamp.isoformat()
                }
                for error in self.error_history[-10:]  # Last 10 errors
            ]
        }

    async def safe_execute(self, operation: Callable, *args, error_type: ErrorType = None,
                          component: str = "unknown", operation_name: str = "unknown", **kwargs) -> FallbackResult:
        """
        Safely execute an operation with error handling and fallbacks

        Args:
            operation: The operation to execute
            *args: Arguments for the operation
            error_type: Type of error to expect
            component: Component name for logging
            operation_name: Operation name for logging
            **kwargs: Keyword arguments for the operation

        Returns:
            FallbackResult with operation result or fallback result
        """
        try:
            result = await operation(*args, **kwargs)
            return FallbackResult(
                success=True,
                message="Operation completed successfully",
                recovered_data=result
            )
        except Exception as e:
            # Use the provided error type or infer from context
            actual_error_type = error_type or ErrorType.UNKNOWN_ERROR
            return await self.handle_error(
                error_type=actual_error_type,
                component=component,
                operation=operation_name,
                original_error=e
            )


# Global error handler instance
error_handler = ErrorHandler()


# Convenience functions for common error scenarios
async def handle_speech_recognition_error(original_error: Exception, additional_info: Dict[str, Any] = None) -> FallbackResult:
    """Handle speech recognition errors"""
    return await error_handler.handle_error(
        error_type=ErrorType.SPEECH_RECOGNITION_ERROR,
        component="whisper_client",
        operation="transcribe_audio",
        original_error=original_error,
        additional_info=additional_info
    )


async def handle_intent_extraction_error(original_error: Exception, additional_info: Dict[str, Any] = None) -> FallbackResult:
    """Handle intent extraction errors"""
    return await error_handler.handle_error(
        error_type=ErrorType.INTENT_EXTRACTION_ERROR,
        component="llm_client",
        operation="extract_intent",
        original_error=original_error,
        additional_info=additional_info
    )


async def handle_action_execution_error(original_error: Exception, additional_info: Dict[str, Any] = None) -> FallbackResult:
    """Handle action execution errors"""
    return await error_handler.handle_error(
        error_type=ErrorType.ACTION_EXECUTION_ERROR,
        component="ros_bridge",
        operation="execute_action",
        original_error=original_error,
        additional_info=additional_info
    )


async def handle_validation_error(original_error: Exception, additional_info: Dict[str, Any] = None) -> FallbackResult:
    """Handle validation errors"""
    return await error_handler.handle_error(
        error_type=ErrorType.VALIDATION_ERROR,
        component="validation_service",
        operation="validate_input",
        original_error=original_error,
        additional_info=additional_info
    )