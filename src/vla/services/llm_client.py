"""
LLM Client Interface

This module provides an interface to OpenAI GPT models for intent extraction,
task decomposition, and action planning.
"""
import asyncio
import json
import logging
from typing import Dict, Any, List, Optional

import openai
from openai import AsyncOpenAI

from src.vla.config import settings
from src.vla.models.intent import Intent, IntentType
from src.vla.models.action_plan import ROS2Action, ROS2ActionPlan


logger = logging.getLogger(__name__)


class LLMClient:
    """
    Client for interacting with OpenAI GPT models for language understanding and planning
    """

    def __init__(self):
        """Initialize the LLM client with configuration from settings"""
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for LLM client")

        # Initialize the OpenAI client
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

        logger.info(f"LLM client initialized with model: {self.model}")

    async def extract_intent(self, text: str) -> Intent:
        """
        Extract intent from natural language text using LLM

        Args:
            text: Natural language text to extract intent from

        Returns:
            Intent object with extracted information
        """
        try:
            logger.info(f"Extracting intent from text: '{text}'")

            # Define the system message to guide the LLM
            system_message = """
            You are an AI assistant that extracts structured intent information from natural language commands for a robotics system.
            Your task is to analyze the command and extract the following:
            1. Intent type (navigation, manipulation, query, etc.)
            2. Action sequence (if any)
            3. Parameters (coordinates, object names, etc.)
            4. Context (environmental context needed)

            Respond in JSON format with the following structure:
            {
                "intent_type": "navigation|manipulation|query|other",
                "action_sequence": ["action1", "action2", ...],
                "parameters": {"param1": "value1", ...},
                "context": "environmental context"
            }

            Only respond with the JSON object, nothing else.
            """

            # Create the chat completion
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Extract intent from: {text}"}
                ],
                temperature=0.1,  # Low temperature for more consistent extraction
                response_format={"type": "json_object"}  # Ensure JSON response
            )

            # Parse the response
            response_content = response.choices[0].message.content
            intent_data = json.loads(response_content)

            # Create and return Intent object
            intent = Intent(
                intent_type=IntentType(intent_data.get("intent_type", "other")),
                action_sequence=intent_data.get("action_sequence", []),
                parameters=intent_data.get("parameters", {}),
                context=intent_data.get("context", ""),
                validation_status="pending"  # Will be validated by validation service
            )

            logger.info(f"Extracted intent: {intent.intent_type}")
            return intent

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing LLM response as JSON: {str(e)}")
            # Return a default intent if parsing fails
            return Intent(
                intent_type=IntentType.other,
                action_sequence=[],
                parameters={"original_text": text},
                context="",
                validation_status="invalid"
            )
        except Exception as e:
            logger.error(f"Error extracting intent: {str(e)}", exc_info=True)
            # Return a default intent if LLM call fails
            return Intent(
                intent_type=IntentType.other,
                action_sequence=[],
                parameters={"original_text": text},
                context="",
                validation_status="error"
            )

    async def plan_actions(self, intent: Intent) -> ROS2ActionPlan:
        """
        Plan ROS 2 actions based on the extracted intent using LLM

        Args:
            intent: Intent object with extracted information

        Returns:
            ROS2ActionPlan with sequence of actions to execute
        """
        try:
            logger.info(f"Planning actions for intent: {intent.intent_type}")

            # Define the system message to guide the LLM for action planning
            system_message = """
            You are an AI planning assistant for a robotics system. Your task is to decompose high-level goals into sequences of specific ROS 2 actions.
            Given an intent, generate a plan with specific actions that can be executed by a humanoid robot in simulation.
            Each action should be a specific ROS 2 action with parameters.

            Available action types:
            - move_base: Move the robot to a specific location [x, y, theta]
            - move_arm: Move the robot's arm to a specific position [x, y, z, roll, pitch, yaw]
            - grasp_object: Grasp an object [object_name]
            - release_object: Release an object
            - look_at: Turn the robot's head to look at a location [x, y, z]
            - speak: Make the robot speak a message [text]
            - detect_objects: Detect objects in the environment

            Respond in JSON format with the following structure:
            {
                "id": "unique_plan_id",
                "actions": [
                    {
                        "action_type": "move_base|move_arm|grasp_object|etc.",
                        "parameters": {"param1": "value1", ...},
                        "timeout": 10.0
                    }
                ],
                "dependencies": [],
                "timeout": 30.0,
                "recovery_steps": []
            }

            Only respond with the JSON object, nothing else.
            """

            # Create the chat completion for action planning
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Plan actions for intent: {intent.dict()}"}
                ],
                temperature=0.2,  # Slightly higher for planning creativity
                response_format={"type": "json_object"}
            )

            # Parse the response
            response_content = response.choices[0].message.content
            plan_data = json.loads(response_content)

            # Convert action data to ROS2Action objects
            actions = []
            for action_data in plan_data.get("actions", []):
                action = ROS2Action(
                    action_type=action_data["action_type"],
                    parameters=action_data.get("parameters", {}),
                    timeout=action_data.get("timeout", 10.0)
                )
                actions.append(action)

            # Create and return ROS2ActionPlan object
            action_plan = ROS2ActionPlan(
                id=plan_data.get("id", "default_plan_id"),
                actions=actions,
                dependencies=plan_data.get("dependencies", []),
                timeout=plan_data.get("timeout", 30.0),
                recovery_steps=plan_data.get("recovery_steps", []),
                validation_rules=[]  # Will be set by validation service
            )

            logger.info(f"Planned {len(action_plan.actions)} actions")
            return action_plan

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing LLM action plan response as JSON: {str(e)}")
            # Return a default empty plan if parsing fails
            return ROS2ActionPlan(
                id="default_plan_id",
                actions=[],
                dependencies=[],
                timeout=30.0,
                recovery_steps=[],
                validation_rules=[]
            )
        except Exception as e:
            logger.error(f"Error planning actions: {str(e)}", exc_info=True)
            # Return a default empty plan if LLM call fails
            return ROS2ActionPlan(
                id="default_plan_id",
                actions=[],
                dependencies=[],
                timeout=30.0,
                recovery_steps=[],
                validation_rules=[]
            )

    async def extract_vision_language_intent(self, text: str, vision_result: Dict[str, Any]) -> Intent:
        """
        Extract intent from text with vision context using LLM

        Args:
            text: Natural language text that references visual information
            vision_result: Result from vision processing with object information

        Returns:
            Intent object with extracted information considering visual context
        """
        try:
            logger.info(f"Extracting vision-language intent from text: '{text}' with vision context")

            # Define the system message to guide the LLM for vision-language understanding
            system_message = """
            You are an AI assistant that extracts structured intent information from natural language commands that reference visual information.
            Your task is to analyze the command and the visual context to extract the following:
            1. Intent type (navigation, manipulation, query, etc.)
            2. Action sequence (if any)
            3. Parameters (coordinates, specific object references, etc.)
            4. Context (using the visual information provided)

            The visual context contains information about detected objects and their spatial relationships.
            Use this information to resolve references like "the object to the left", "the red cube", etc.

            Respond in JSON format with the following structure:
            {
                "intent_type": "navigation|manipulation|query|other",
                "action_sequence": ["action1", "action2", ...],
                "parameters": {"param1": "value1", ...},
                "context": "environmental context with visual information"
            }

            Only respond with the JSON object, nothing else.
            """

            # Create the chat completion for vision-language intent extraction
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Command: {text}\nVisual context: {json.dumps(vision_result, indent=2)}"}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )

            # Parse the response
            response_content = response.choices[0].message.content
            intent_data = json.loads(response_content)

            # Create and return Intent object
            intent = Intent(
                intent_type=IntentType(intent_data.get("intent_type", "other")),
                action_sequence=intent_data.get("action_sequence", []),
                parameters=intent_data.get("parameters", {}),
                context=intent_data.get("context", ""),
                validation_status="pending"
            )

            logger.info(f"Extracted vision-language intent: {intent.intent_type}")
            return intent

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing LLM vision-language response as JSON: {str(e)}")
            # Return a default intent if parsing fails
            return Intent(
                intent_type=IntentType.other,
                action_sequence=[],
                parameters={"original_text": text, "vision_context": vision_result},
                context="",
                validation_status="invalid"
            )
        except Exception as e:
            logger.error(f"Error extracting vision-language intent: {str(e)}", exc_info=True)
            # Return a default intent if LLM call fails
            return Intent(
                intent_type=IntentType.other,
                action_sequence=[],
                parameters={"original_text": text, "vision_context": vision_result},
                context="",
                validation_status="error"
            )

    async def plan_vision_language_actions(self, intent: Intent, vision_result: Dict[str, Any]) -> ROS2ActionPlan:
        """
        Plan ROS 2 actions based on vision-language intent using LLM

        Args:
            intent: Intent object with vision-language information
            vision_result: Result from vision processing with object information

        Returns:
            ROS2ActionPlan with sequence of actions considering visual context
        """
        try:
            logger.info(f"Planning vision-language actions for intent: {intent.intent_type}")

            # Define the system message to guide the LLM for vision-language action planning
            system_message = """
            You are an AI planning assistant for a robotics system that integrates vision and language.
            Your task is to decompose high-level goals that reference visual information into sequences of specific ROS 2 actions.
            Use the visual context to ground the actions in specific objects and spatial relationships.

            Available action types:
            - move_base: Move the robot to a specific location [x, y, theta]
            - move_arm: Move the robot's arm to a specific position [x, y, z, roll, pitch, yaw]
            - grasp_object: Grasp a specific object [object_name, position]
            - release_object: Release an object
            - look_at: Turn the robot's head to look at a location [x, y, z]
            - speak: Make the robot speak a message [text]
            - detect_objects: Detect objects in the environment

            Respond in JSON format with the following structure:
            {
                "id": "unique_plan_id",
                "actions": [
                    {
                        "action_type": "move_base|move_arm|grasp_object|etc.",
                        "parameters": {"param1": "value1", ...},
                        "timeout": 10.0
                    }
                ],
                "dependencies": [],
                "timeout": 30.0,
                "recovery_steps": []
            }

            Only respond with the JSON object, nothing else.
            """

            # Create the chat completion for vision-language action planning
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Intent: {intent.dict()}\nVisual context: {json.dumps(vision_result, indent=2)}"}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )

            # Parse the response
            response_content = response.choices[0].message.content
            plan_data = json.loads(response_content)

            # Convert action data to ROS2Action objects
            actions = []
            for action_data in plan_data.get("actions", []):
                action = ROS2Action(
                    action_type=action_data["action_type"],
                    parameters=action_data.get("parameters", {}),
                    timeout=action_data.get("timeout", 10.0)
                )
                actions.append(action)

            # Create and return ROS2ActionPlan object
            action_plan = ROS2ActionPlan(
                id=plan_data.get("id", "vision_language_plan_id"),
                actions=actions,
                dependencies=plan_data.get("dependencies", []),
                timeout=plan_data.get("timeout", 30.0),
                recovery_steps=plan_data.get("recovery_steps", []),
                validation_rules=[]
            )

            logger.info(f"Planned {len(action_plan.actions)} vision-language actions")
            return action_plan

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing LLM vision-language action plan response as JSON: {str(e)}")
            # Return a default empty plan if parsing fails
            return ROS2ActionPlan(
                id="vision_language_plan_id",
                actions=[],
                dependencies=[],
                timeout=30.0,
                recovery_steps=[],
                validation_rules=[]
            )
        except Exception as e:
            logger.error(f"Error planning vision-language actions: {str(e)}", exc_info=True)
            # Return a default empty plan if LLM call fails
            return ROS2ActionPlan(
                id="vision_language_plan_id",
                actions=[],
                dependencies=[],
                timeout=30.0,
                recovery_steps=[],
                validation_rules=[]
            )

    async def enhance_command_with_context(self, text: str, context: str) -> str:
        """
        Enhance a command with additional context using LLM

        Args:
            text: Original command text
            context: Additional context to incorporate

        Returns:
            Enhanced command text with context incorporated
        """
        try:
            logger.info(f"Enhancing command with context: '{text[:50]}...'")

            system_message = """
            You are an AI assistant that enhances natural language commands by incorporating additional context.
            Your task is to refine the command based on the provided context to make it more specific and actionable.
            """

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Command: {text}\nContext: {context}\n\nEnhanced command:"}
                ],
                temperature=0.3
            )

            enhanced_text = response.choices[0].message.content.strip()
            logger.info(f"Command enhanced: '{enhanced_text[:50]}...'")
            return enhanced_text

        except Exception as e:
            logger.error(f"Error enhancing command with context: {str(e)}", exc_info=True)
            # Return original text if enhancement fails
            return text

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check of the LLM client

        Returns:
            Dictionary containing health status
        """
        try:
            # Test with a simple API call
            if not settings.openai_api_key:
                return {"status": "error", "message": "OpenAI API key not configured"}

            # Test the API with a minimal request
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )

            if response:
                return {
                    "status": "healthy",
                    "model": self.model,
                    "api_key_valid": True
                }
            else:
                return {"status": "error", "message": "API test failed"}

        except Exception as e:
            logger.error(f"LLM client health check failed: {str(e)}")
            return {"status": "error", "message": str(e)}