"""
Text Processing Router

This module defines the API endpoints for text processing functionality.
"""
from fastapi import APIRouter, Form, HTTPException
from typing import Dict, Any

from src.vla.services.vla_service import vla_service


router = APIRouter()


@router.post("/process")
async def process_text_command(text: str = Form(...)) -> Dict[str, Any]:
    """
    Process a text command through the VLA pipeline

    Args:
        text: Natural language command as text

    Returns:
        Processing result from the VLA pipeline
    """
    try:
        # Validate input
        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text command cannot be empty")

        if len(text) > 1000:  # Arbitrary limit
            raise HTTPException(status_code=400, detail="Text command is too long (max 1000 characters)")

        # Process the text command through the VLA service
        result = await vla_service.process_text_command(text)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing text command: {str(e)}"
        )


@router.post("/extract_intent")
async def extract_intent(text: str = Form(...)) -> Dict[str, Any]:
    """
    Extract intent from natural language text

    Args:
        text: Natural language text to extract intent from

    Returns:
        Extracted intent information
    """
    try:
        # Validate input
        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        # Extract intent using LLM client
        intent = await vla_service.llm_client.extract_intent(text)

        return intent.dict()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting intent: {str(e)}"
        )


@router.post("/plan_actions")
async def plan_actions(text: str = Form(...)) -> Dict[str, Any]:
    """
    Plan actions based on natural language text

    Args:
        text: Natural language text describing desired actions

    Returns:
        Planned sequence of actions
    """
    try:
        # Validate input
        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        # Extract intent first
        intent = await vla_service.llm_client.extract_intent(text)

        # Plan actions based on intent
        action_plan = await vla_service.llm_client.plan_actions(intent)

        return action_plan.dict()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error planning actions: {str(e)}"
        )