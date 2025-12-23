"""
Validation Service

This module provides validation for inputs, intents, and action plans to ensure safety and feasibility.
"""
import logging
from typing import Dict, Any, Tuple, List
from datetime import datetime, timedelta

from src.vla.config import settings
from src.vla.models.intent import Intent
from src.vla.models.action_plan import ROS2ActionPlan
from src.vla.models.voice_command import VoiceCommand


logger = logging.getLogger(__name__)


class ValidationService:
    """
    Service for validating inputs, intents, and action plans for safety and feasibility
    """

    def __init__(self):
        """Initialize the validation service with validation rules"""
        self.confidence_threshold = 0.7
        self.max_action_timeout = 60.0  # seconds
        self.max_plan_timeout = 300.0  # seconds (5 minutes)

        logger.info("Validation service initialized")

    def validate_voice_command(self, voice_command: VoiceCommand) -> Tuple[bool, str]:
        """
        Validate a voice command for basic requirements

        Args:
            voice_command: Voice command to validate

        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Check confidence score
            if voice_command.confidence < self.confidence_threshold:
                return False, f"Voice command confidence too low: {voice_command.confidence} < {self.confidence_threshold}"

            # Check that we have a transcript
            if not voice_command.transcript.strip():
                return False, "Voice command has no transcript"

            # Check timestamp is not too old (within 1 minute)
            if voice_command.timestamp:
                time_diff = datetime.now() - voice_command.timestamp
                if time_diff > timedelta(minutes=1):
                    return False, "Voice command is too old"

            # Check audio data is present
            if not voice_command.audio_data:
                logger.warning("Voice command has no audio data, but proceeding with validation")

            return True, "Voice command is valid"

        except Exception as e:
            logger.error(f"Error validating voice command: {str(e)}")
            return False, f"Error validating voice command: {str(e)}"

    def validate_intent(self, intent: Intent) -> Tuple[bool, str]:
        """
        Validate an intent for safety and feasibility

        Args:
            intent: Intent to validate

        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Check intent type is valid
            if not intent.intent_type:
                return False, "Intent type is required"

            # Check parameters are valid
            if not isinstance(intent.parameters, dict):
                return False, "Intent parameters must be a dictionary"

            # Check for potentially unsafe intent types
            unsafe_keywords = ["destroy", "damage", "harm", "break", "kill"]
            if hasattr(intent, 'context') and intent.context:
                context_lower = intent.context.lower()
                for keyword in unsafe_keywords:
                    if keyword in context_lower:
                        return False, f"Intent contains potentially unsafe keyword: {keyword}"

            # Validate action sequence
            if not isinstance(intent.action_sequence, list):
                return False, "Intent action sequence must be a list"

            # Check for empty or invalid intents
            if not intent.action_sequence and not intent.parameters:
                logger.warning("Intent has no action sequence or parameters")

            return True, "Intent is valid"

        except Exception as e:
            logger.error(f"Error validating intent: {str(e)}")
            return False, f"Error validating intent: {str(e)}"

    def validate_action_plan(self, action_plan: ROS2ActionPlan) -> Tuple[bool, str]:
        """
        Validate an action plan for safety and feasibility

        Args:
            action_plan: Action plan to validate

        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Check plan has actions
            if not action_plan.actions:
                return False, "Action plan has no actions"

            # Check plan timeout is reasonable
            if action_plan.timeout <= 0 or action_plan.timeout > self.max_plan_timeout:
                return False, f"Action plan timeout is invalid: {action_plan.timeout}s (max: {self.max_plan_timeout}s)"

            # Validate each action in the plan
            for i, action in enumerate(action_plan.actions):
                is_valid, message = self.validate_action(action)
                if not is_valid:
                    return False, f"Action {i} in plan is invalid: {message}"

            # Check dependencies are valid
            action_ids = [f"action_{j}" for j in range(len(action_plan.actions))]
            for dep in action_plan.dependencies:
                if dep not in action_ids:
                    return False, f"Dependency {dep} does not exist in action plan"

            # Check recovery steps are valid
            for i, recovery_action in enumerate(action_plan.recovery_steps):
                is_valid, message = self.validate_action(recovery_action)
                if not is_valid:
                    return False, f"Recovery action {i} is invalid: {message}"

            # Check for potentially unsafe action types
            unsafe_actions = ["emergency_stop", "shutdown_system", "self_destruct"]
            for action in action_plan.actions:
                if action.action_type.lower() in unsafe_actions:
                    return False, f"Action plan contains potentially unsafe action: {action.action_type}"

            # Check for physically impossible parameters
            for action in action_plan.actions:
                if action.action_type == "move_arm":
                    # Check for physically impossible positions
                    params = action.parameters
                    if 'x' in params and abs(params['x']) > 2.0:  # Arm can't reach beyond 2m
                        return False, f"Arm movement to x={params['x']} is physically impossible"
                    if 'y' in params and abs(params['y']) > 2.0:
                        return False, f"Arm movement to y={params['y']} is physically impossible"
                    if 'z' in params and params['z'] < -1.0:  # Below ground
                        return False, f"Arm movement to z={params['z']} is below ground level"

            return True, "Action plan is valid"

        except Exception as e:
            logger.error(f"Error validating action plan: {str(e)}")
            return False, f"Error validating action plan: {str(e)}"

    def validate_action(self, action: 'ROS2Action') -> Tuple[bool, str]:
        """
        Validate a single action for safety and feasibility

        Args:
            action: Action to validate

        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Check action type is provided
            if not action.action_type:
                return False, "Action type is required"

            # Check parameters are valid
            if not isinstance(action.parameters, dict):
                return False, "Action parameters must be a dictionary"

            # Check timeout is reasonable
            if action.timeout <= 0 or action.timeout > self.max_action_timeout:
                return False, f"Action timeout is invalid: {action.timeout}s (max: {self.max_action_timeout}s)"

            # Validate specific action types
            if action.action_type == "move_base":
                # Check for valid navigation parameters
                if 'x' not in action.parameters or 'y' not in action.parameters:
                    return False, "Move base action requires x and y coordinates"

                # Check for reasonable coordinates (not too far)
                x, y = action.parameters['x'], action.parameters['y']
                if abs(x) > 100 or abs(y) > 100:  # Robot shouldn't move more than 100m
                    return False, f"Navigation coordinates too far: ({x}, {y})"

            elif action.action_type == "move_arm":
                # Check for valid arm movement parameters
                required_params = ['x', 'y', 'z']
                for param in required_params:
                    if param not in action.parameters:
                        return False, f"Move arm action requires '{param}' parameter"

                # Check for physically reasonable positions
                x, y, z = action.parameters['x'], action.parameters['y'], action.parameters['z']
                if abs(x) > 2.0 or abs(y) > 2.0:  # Arm reach limit
                    return False, f"Arm position too far: ({x}, {y}, {z})"

            elif action.action_type == "grasp_object":
                # Check for valid object reference
                if 'object_name' not in action.parameters:
                    return False, "Grasp object action requires 'object_name' parameter"

            elif action.action_type == "speak":
                # Check for valid message
                if 'text' not in action.parameters or not action.parameters['text'].strip():
                    return False, "Speak action requires non-empty 'text' parameter"

                # Check for potentially inappropriate content
                text_lower = action.parameters['text'].lower()
                inappropriate_keywords = ["shutdown", "stop", "error", "emergency"]
                for keyword in inappropriate_keywords:
                    if keyword in text_lower:
                        logger.warning(f"Speak action contains keyword '{keyword}': {action.parameters['text']}")

            return True, "Action is valid"

        except Exception as e:
            logger.error(f"Error validating action: {str(e)}")
            return False, f"Error validating action: {str(e)}"

    def validate_language_command(self, text: str) -> Tuple[bool, str]:
        """
        Validate a natural language command for basic safety and feasibility

        Args:
            text: Natural language command to validate

        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Check if text is empty
            if not text or not text.strip():
                return False, "Command text is empty"

            # Check length
            if len(text.strip()) < 3:
                return False, "Command text is too short (minimum 3 characters)"

            # Check for potentially unsafe commands
            unsafe_patterns = [
                "shutdown", "terminate", "kill", "destroy", "break", "damage",
                "emergency stop", "panic", "self destruct", "harm"
            ]

            text_lower = text.lower()
            for pattern in unsafe_patterns:
                if pattern in text_lower:
                    return False, f"Command contains potentially unsafe pattern: '{pattern}'"

            # Check for excessive length
            if len(text) > 1000:  # Arbitrary limit
                return False, "Command text is too long (maximum 1000 characters)"

            return True, "Language command is valid"

        except Exception as e:
            logger.error(f"Error validating language command: {str(e)}")
            return False, f"Error validating language command: {str(e)}"

    def validate_vision_language_request(self, image_data: bytes, text: str) -> Tuple[bool, str]:
        """
        Validate a vision-language request for safety and feasibility

        Args:
            image_data: Image data for validation
            text: Natural language command to validate

        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Validate the text component
            text_valid, text_message = self.validate_language_command(text)
            if not text_valid:
                return False, f"Text validation failed: {text_message}"

            # Check if image data is provided
            if not image_data:
                return False, "Image data is required for vision-language request"

            # Check image data size (not too large)
            if len(image_data) > 10 * 1024 * 1024:  # 10MB limit
                return False, "Image data is too large (maximum 10MB)"

            # Check for potential privacy/security issues in text
            privacy_keywords = ["password", "secret", "private", "confidential", "personal"]
            text_lower = text.lower()
            for keyword in privacy_keywords:
                if keyword in text_lower:
                    logger.warning(f"Vision-language request contains privacy keyword: '{keyword}'")

            return True, "Vision-language request is valid"

        except Exception as e:
            logger.error(f"Error validating vision-language request: {str(e)}")
            return False, f"Error validating vision-language request: {str(e)}"

    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check of the validation service

        Returns:
            Dictionary containing health status
        """
        try:
            # Test basic validation functionality
            test_intent = Intent(
                intent_type="navigation",
                action_sequence=["move_base"],
                parameters={"x": 1.0, "y": 1.0},
                context="Move to location",
                validation_status="pending"
            )

            is_valid, message = self.validate_intent(test_intent)

            if is_valid:
                return {
                    "status": "healthy",
                    "validation_rules": {
                        "confidence_threshold": self.confidence_threshold,
                        "max_action_timeout": self.max_action_timeout,
                        "max_plan_timeout": self.max_plan_timeout
                    }
                }
            else:
                return {"status": "warning", "message": f"Basic validation test failed: {message}"}

        except Exception as e:
            logger.error(f"Validation service health check failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    def add_custom_validation_rule(self, rule_name: str, rule_function) -> bool:
        """
        Add a custom validation rule to the service

        Args:
            rule_name: Name of the validation rule
            rule_function: Function that takes an object and returns (is_valid, message)

        Returns:
            True if rule was added successfully
        """
        try:
            # In a real implementation, we would store the rule function
            # For now, we'll just log that a custom rule was added
            logger.info(f"Custom validation rule added: {rule_name}")
            return True
        except Exception as e:
            logger.error(f"Error adding custom validation rule: {str(e)}")
            return False