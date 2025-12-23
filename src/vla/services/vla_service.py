"""
Base VLA Service Class

This class provides the core functionality for the Vision-Language-Action integration system.
It handles the orchestration between voice input, language processing, vision processing,
and action execution.
"""
import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple

from src.vla.config import settings
from src.vla.models.intent import Intent
from src.vla.models.voice_command import VoiceCommand
from src.vla.models.action_plan import ROS2ActionPlan
from src.vla.services.whisper_client import WhisperAPIClient
from src.vla.services.llm_client import LLMClient
from src.vla.services.validation_service import ValidationService
from src.vla.services.ros_bridge import ROSBridge
from src.vla.utils.error_handler import error_handler, handle_speech_recognition_error, handle_intent_extraction_error, handle_action_execution_error, handle_validation_error


logger = logging.getLogger(__name__)


class VLABaseService:
    """
    Base service class that orchestrates the VLA pipeline:
    Voice → Whisper → LLM → Action Planning → ROS 2 Execution
    """

    def __init__(self):
        """Initialize the VLA service with required clients and services"""
        self.whisper_client = WhisperAPIClient()
        self.llm_client = LLMClient()
        self.validation_service = ValidationService()
        self.ros_bridge = ROSBridge()

        # Configure logging
        logging.basicConfig(
            level=getattr(logging, settings.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(settings.log_file),
                logging.StreamHandler()
            ]
        )

    async def process_voice_command(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Process a voice command through the full VLA pipeline

        Args:
            audio_data: Raw audio data in bytes

        Returns:
            Dictionary containing the processing result
        """
        # Step 1: Convert speech to text using Whisper
        from src.vla.utils.error_handler import ErrorType
        transcription_result = await error_handler.safe_execute(
            self.whisper_client.transcribe_audio, audio_data,
            error_type=ErrorType.SPEECH_RECOGNITION_ERROR,
            component="whisper_client",
            operation_name="transcribe_audio"
        )

        if not transcription_result.success:
            logger.error(f"Speech recognition failed: {transcription_result.message}")
            return {
                "status": "error",
                "message": f"Speech recognition failed: {transcription_result.message}"
            }

        transcript_data = transcription_result.recovered_data
        transcript = transcript_data.get("text", "")
        confidence = transcript_data.get("confidence", 0.0)

        if confidence < 0.7:
            logger.warning(f"Low confidence transcription: {confidence}")
            return {
                "status": "error",
                "message": "Unclear audio input. Please try again.",
                "confidence": confidence
            }

        logger.info(f"Transcribed: '{transcript}' with confidence {confidence}")

        # Step 2: Extract intent from the transcribed text
        intent_result = await error_handler.safe_execute(
            self.llm_client.extract_intent, transcript,
            error_type=ErrorType.INTENT_EXTRACTION_ERROR,
            component="llm_client",
            operation_name="extract_intent"
        )

        if not intent_result.success:
            logger.error(f"Intent extraction failed: {intent_result.message}")
            return {
                "status": "error",
                "message": f"Intent extraction failed: {intent_result.message}"
            }

        intent = intent_result.recovered_data
        logger.info(f"Extracted intent: {intent.intent_type}")

        # Step 3: Validate the intent
        is_valid, validation_message = self.validation_service.validate_intent(intent)
        if not is_valid:
            logger.warning(f"Invalid intent: {validation_message}")
            return {
                "status": "error",
                "message": validation_message,
                "intent": intent.dict()
            }

        # Step 4: Decompose complex goals into action sequence if needed
        action_plan_result = await error_handler.safe_execute(
            self.llm_client.plan_actions, intent,
            error_type=ErrorType.ACTION_PLANNING_ERROR,
            component="llm_client",
            operation_name="plan_actions"
        )

        if not action_plan_result.success:
            logger.error(f"Action planning failed: {action_plan_result.message}")
            return {
                "status": "error",
                "message": f"Action planning failed: {action_plan_result.message}"
            }

        action_plan = action_plan_result.recovered_data
        logger.info(f"Generated action plan with {len(action_plan.actions)} actions")

        # Step 5: Validate the action plan
        is_valid, validation_message = self.validation_service.validate_action_plan(action_plan)
        if not is_valid:
            logger.warning(f"Invalid action plan: {validation_message}")
            return {
                "status": "error",
                "message": validation_message,
                "action_plan": action_plan.dict()
            }

        # Step 6: Execute the action plan via ROS bridge
        execution_result = await error_handler.safe_execute(
            self.ros_bridge.execute_action_plan, action_plan,
            error_type=ErrorType.ACTION_EXECUTION_ERROR,
            component="ros_bridge",
            operation_name="execute_action_plan"
        )

        if not execution_result.success:
            logger.error(f"Action execution failed: {execution_result.message}")
            return {
                "status": "error",
                "message": f"Action execution failed: {execution_result.message}",
                "action_plan": action_plan.dict()
            }

        logger.info("Voice command processing completed successfully")
        return {
            "status": "success",
            "transcript": transcript,
            "confidence": confidence,
            "intent": intent.dict(),
            "action_plan": action_plan.dict(),
            "execution_result": execution_result.recovered_data
        }

    async def process_text_command(self, text: str) -> Dict[str, Any]:
        """
        Process a text command through the VLA pipeline (without speech recognition)

        Args:
            text: Natural language command as text

        Returns:
            Dictionary containing the processing result
        """
        from src.vla.utils.error_handler import ErrorType

        logger.info(f"Processing text command: '{text}'")

        # Step 1: Extract intent from the text
        intent_result = await error_handler.safe_execute(
            self.llm_client.extract_intent, text,
            error_type=ErrorType.INTENT_EXTRACTION_ERROR,
            component="llm_client",
            operation_name="extract_intent"
        )

        if not intent_result.success:
            logger.error(f"Intent extraction failed: {intent_result.message}")
            return {
                "status": "error",
                "message": f"Intent extraction failed: {intent_result.message}"
            }

        intent = intent_result.recovered_data
        logger.info(f"Extracted intent: {intent.intent_type}")

        # Step 2: Validate the intent
        is_valid, validation_message = self.validation_service.validate_intent(intent)
        if not is_valid:
            logger.warning(f"Invalid intent: {validation_message}")
            return {
                "status": "error",
                "message": validation_message,
                "intent": intent.dict()
            }

        # Step 3: Decompose complex goals into action sequence
        action_plan_result = await error_handler.safe_execute(
            self.llm_client.plan_actions, intent,
            error_type=ErrorType.ACTION_PLANNING_ERROR,
            component="llm_client",
            operation_name="plan_actions"
        )

        if not action_plan_result.success:
            logger.error(f"Action planning failed: {action_plan_result.message}")
            return {
                "status": "error",
                "message": f"Action planning failed: {action_plan_result.message}"
            }

        action_plan = action_plan_result.recovered_data
        logger.info(f"Generated action plan with {len(action_plan.actions)} actions")

        # Step 4: Validate the action plan
        is_valid, validation_message = self.validation_service.validate_action_plan(action_plan)
        if not is_valid:
            logger.warning(f"Invalid action plan: {validation_message}")
            return {
                "status": "error",
                "message": validation_message,
                "action_plan": action_plan.dict()
            }

        # Step 5: Execute the action plan via ROS bridge
        execution_result = await error_handler.safe_execute(
            self.ros_bridge.execute_action_plan, action_plan,
            error_type=ErrorType.ACTION_EXECUTION_ERROR,
            component="ros_bridge",
            operation_name="execute_action_plan"
        )

        if not execution_result.success:
            logger.error(f"Action execution failed: {execution_result.message}")
            return {
                "status": "error",
                "message": f"Action execution failed: {execution_result.message}",
                "action_plan": action_plan.dict()
            }

        logger.info("Text command processing completed successfully")
        return {
            "status": "success",
            "text": text,
            "intent": intent.dict(),
            "action_plan": action_plan.dict(),
            "execution_result": execution_result.recovered_data
        }

    async def process_vision_language_command(self, image_data: bytes, text: str) -> Dict[str, Any]:
        """
        Process a command that combines vision and language input

        Args:
            image_data: Image data for vision processing
            text: Natural language command that references the image

        Returns:
            Dictionary containing the processing result
        """
        from src.vla.utils.error_handler import ErrorType

        logger.info(f"Processing vision-language command: '{text}'")

        # Step 1: Process the image to extract visual information
        vision_result = await error_handler.safe_execute(
            self.ros_bridge.process_vision_data, image_data,
            error_type=ErrorType.ACTION_EXECUTION_ERROR,  # Vision processing is part of action execution
            component="ros_bridge",
            operation_name="process_vision_data"
        )

        if not vision_result.success:
            logger.error(f"Vision processing failed: {vision_result.message}")
            return {
                "status": "error",
                "message": f"Vision processing failed: {vision_result.message}"
            }

        vision_data = vision_result.recovered_data
        logger.info(f"Vision processing result: {len(vision_data.get('objects', []))} objects detected")

        # Step 2: Extract intent from the text with vision context
        intent_result = await error_handler.safe_execute(
            self.llm_client.extract_vision_language_intent, text, vision_data,
            error_type=ErrorType.INTENT_EXTRACTION_ERROR,
            component="llm_client",
            operation_name="extract_vision_language_intent"
        )

        if not intent_result.success:
            logger.error(f"Vision-language intent extraction failed: {intent_result.message}")
            return {
                "status": "error",
                "message": f"Vision-language intent extraction failed: {intent_result.message}"
            }

        intent = intent_result.recovered_data
        logger.info(f"Extracted vision-language intent: {intent.intent_type}")

        # Step 3: Validate the intent
        is_valid, validation_message = self.validation_service.validate_intent(intent)
        if not is_valid:
            logger.warning(f"Invalid intent: {validation_message}")
            return {
                "status": "error",
                "message": validation_message,
                "intent": intent.dict()
            }

        # Step 4: Decompose complex goals into action sequence
        action_plan_result = await error_handler.safe_execute(
            self.llm_client.plan_vision_language_actions, intent, vision_data,
            error_type=ErrorType.ACTION_PLANNING_ERROR,
            component="llm_client",
            operation_name="plan_vision_language_actions"
        )

        if not action_plan_result.success:
            logger.error(f"Vision-language action planning failed: {action_plan_result.message}")
            return {
                "status": "error",
                "message": f"Vision-language action planning failed: {action_plan_result.message}"
            }

        action_plan = action_plan_result.recovered_data
        logger.info(f"Generated vision-language action plan with {len(action_plan.actions)} actions")

        # Step 5: Validate the action plan
        is_valid, validation_message = self.validation_service.validate_action_plan(action_plan)
        if not is_valid:
            logger.warning(f"Invalid action plan: {validation_message}")
            return {
                "status": "error",
                "message": validation_message,
                "action_plan": action_plan.dict()
            }

        # Step 6: Execute the action plan via ROS bridge
        execution_result = await error_handler.safe_execute(
            self.ros_bridge.execute_action_plan, action_plan,
            error_type=ErrorType.ACTION_EXECUTION_ERROR,
            component="ros_bridge",
            operation_name="execute_action_plan"
        )

        if not execution_result.success:
            logger.error(f"Action execution failed: {execution_result.message}")
            return {
                "status": "error",
                "message": f"Action execution failed: {execution_result.message}",
                "action_plan": action_plan.dict()
            }

        logger.info("Vision-language command processing completed successfully")
        return {
            "status": "success",
            "text": text,
            "vision_result": vision_data,
            "intent": intent.dict(),
            "action_plan": action_plan.dict(),
            "execution_result": execution_result.recovered_data
        }

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check of all VLA service components

        Returns:
            Dictionary containing health status of all components
        """
        health_status = {
            "service": "running",
            "timestamp": asyncio.get_event_loop().time(),
            "components": {}
        }

        # Check Whisper API client
        try:
            whisper_health = await self.whisper_client.health_check()
            health_status["components"]["whisper"] = whisper_health
        except Exception as e:
            health_status["components"]["whisper"] = {"status": "error", "message": str(e)}

        # Check LLM client
        try:
            llm_health = await self.llm_client.health_check()
            health_status["components"]["llm"] = llm_health
        except Exception as e:
            health_status["components"]["llm"] = {"status": "error", "message": str(e)}

        # Check ROS bridge
        try:
            ros_health = await self.ros_bridge.health_check()
            health_status["components"]["ros"] = ros_health
        except Exception as e:
            health_status["components"]["ros"] = {"status": "error", "message": str(e)}

        # Check validation service
        try:
            validation_health = self.validation_service.health_check()
            health_status["components"]["validation"] = validation_health
        except Exception as e:
            health_status["components"]["validation"] = {"status": "error", "message": str(e)}

        return health_status


# Global instance of the VLA service
vla_service = VLABaseService()