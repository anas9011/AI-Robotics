"""
Vision Processing Router

This module defines the API endpoints for vision processing functionality.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Dict, Any

from src.vla.services.vla_service import vla_service


router = APIRouter()


@router.post("/process_language_with_vision")
async def process_vision_language_command(
    image_file: UploadFile = File(...),
    text: str = Form(...)
) -> Dict[str, Any]:
    """
    Process a command that combines vision and language input

    Args:
        image_file: Image file for vision processing
        text: Natural language command referencing the image

    Returns:
        Processing result from the VLA pipeline
    """
    try:
        # Read image file content
        image_data = await image_file.read()

        # Validate inputs
        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text command cannot be empty")

        if len(text) > 1000:  # Arbitrary limit
            raise HTTPException(status_code=400, detail="Text command is too long (max 1000 characters)")

        if len(image_data) == 0:
            raise HTTPException(status_code=400, detail="Image file cannot be empty")

        if len(image_data) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="Image file is too large (max 10MB)")

        # Validate image file type (basic check)
        if not image_file.content_type or not any(
            ext in image_file.filename.lower()
            for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
        ):
            raise HTTPException(
                status_code=400,
                detail="Unsupported image format. Supported formats: JPG, JPEG, PNG, BMP, WebP"
            )

        # Process the vision-language command through the VLA service
        result = await vla_service.process_vision_language_command(image_data, text)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing vision-language command: {str(e)}"
        )


@router.post("/detect_objects")
async def detect_objects(image_file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Detect objects in an image

    Args:
        image_file: Image file to analyze

    Returns:
        Detected objects and their information
    """
    try:
        # Read image file content
        image_data = await image_file.read()

        if len(image_data) == 0:
            raise HTTPException(status_code=400, detail="Image file cannot be empty")

        # Process image through ROS bridge (simulated)
        vision_result = await vla_service.ros_bridge.process_vision_data(image_data)

        return {
            "objects": vision_result.get("objects", []),
            "spatial_relationships": vision_result.get("spatial_relationships", {}),
            "status": vision_result.get("status", "processed")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error detecting objects: {str(e)}"
        )


@router.post("/analyze_scene")
async def analyze_scene(image_file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Analyze a scene in an image

    Args:
        image_file: Image file to analyze

    Returns:
        Scene analysis results
    """
    try:
        # Read image file content
        image_data = await image_file.read()

        if len(image_data) == 0:
            raise HTTPException(status_code=400, detail="Image file cannot be empty")

        # For now, return the same as object detection
        # In a real implementation, this would do more sophisticated scene analysis
        vision_result = await vla_service.ros_bridge.process_vision_data(image_data)

        return {
            "objects": vision_result.get("objects", []),
            "spatial_relationships": vision_result.get("spatial_relationships", {}),
            "scene_description": "Scene analysis not fully implemented in simulation",
            "status": vision_result.get("status", "processed")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing scene: {str(e)}"
        )