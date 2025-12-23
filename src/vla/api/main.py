"""
FastAPI Server for VLA Integration

This module sets up the main FastAPI server for handling VLA pipeline requests.
"""
import asyncio
import logging
from typing import Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.vla.config import settings
from src.vla.services.vla_service import vla_service


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Vision-Language-Action (VLA) Integration API",
    description="API for processing voice, text, and vision-language commands for ROS 2 humanoid robots",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from src.vla.api import voice_router, text_router, vision_router, health_router

app.include_router(voice_router.router, prefix="/api/v1/voice", tags=["voice"])
app.include_router(text_router.router, prefix="/api/v1/text", tags=["text"])
app.include_router(vision_router.router, prefix="/api/v1/vision", tags=["vision"])
app.include_router(health_router.router, prefix="/api/v1/health", tags=["health"])


@app.on_event("startup")
async def startup_event():
    """Perform startup tasks"""
    logger.info("VLA API server starting up...")

    # Perform any initialization tasks
    # Skip health check on startup to avoid immediate API calls
    logger.info("VLA service initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Perform cleanup tasks"""
    logger.info("VLA API server shutting down...")
    # Add any cleanup code here if needed


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint for basic information"""
    return {
        "message": "Vision-Language-Action (VLA) Integration API",
        "version": "0.1.0",
        "status": "running",
        "documentation": "/docs"
    }


@app.post("/api/v1/process_voice")
async def process_voice_command(audio_file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Process a voice command through the VLA pipeline

    Args:
        audio_file: Audio file containing the voice command

    Returns:
        Processing result from the VLA pipeline
    """
    try:
        logger.info(f"Processing voice command: {audio_file.filename}")

        # Read audio file content
        audio_data = await audio_file.read()

        # Validate file type (basic check)
        if not audio_file.content_type or not any(
            ext in audio_file.filename.lower()
            for ext in ['.wav', '.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.webm']
        ):
            raise HTTPException(
                status_code=400,
                detail="Unsupported audio file format. Supported formats: WAV, MP3, MP4, M4A, WebM"
            )

        # Process the voice command through the VLA service
        result = await vla_service.process_voice_command(audio_data)

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing voice command: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing voice command: {str(e)}"
        )


@app.post("/api/v1/process_text")
async def process_text_command(text: str = Form(...)) -> Dict[str, Any]:
    """
    Process a text command through the VLA pipeline

    Args:
        text: Natural language command as text

    Returns:
        Processing result from the VLA pipeline
    """
    try:
        logger.info(f"Processing text command: {text[:50]}...")

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
        logger.error(f"Error processing text command: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing text command: {str(e)}"
        )


@app.post("/api/v1/process_vision_language")
async def process_vision_language_command(
    image_file: UploadFile = File(...),
    text: str = Form(...)
) -> Dict[str, Any]:
    """
    Process a vision-language command combining image and text

    Args:
        image_file: Image file for vision processing
        text: Natural language command referencing the image

    Returns:
        Processing result from the VLA pipeline
    """
    try:
        logger.info(f"Processing vision-language command: {text[:50]}...")

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
        logger.error(f"Error processing vision-language command: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing vision-language command: {str(e)}"
        )


# Additional utility endpoints
@app.get("/api/v1/status")
async def get_status() -> Dict[str, Any]:
    """
    Get the current status of the VLA service

    Returns:
        Status information about all VLA components
    """
    try:
        health_status = await vla_service.health_check()
        return health_status
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")


@app.get("/api/v1/config")
async def get_config() -> Dict[str, Any]:
    """
    Get the current configuration of the VLA service

    Returns:
        Configuration information
    """
    try:
        config_info = {
            "service_config": {
                "host": settings.vla_service_host,
                "port": settings.vla_service_port,
                "log_level": settings.log_level,
            },
            "openai_config": {
                "model": settings.openai_model,
                "has_api_key": bool(settings.openai_api_key),  # Don't expose the actual key
            },
            "simulation_config": {
                "type": settings.simulation_type,
                "host": settings.simulation_host,
                "port": settings.simulation_port,
            }
        }
        return config_info
    except Exception as e:
        logger.error(f"Error getting configuration: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error getting configuration: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting VLA API server on {settings.vla_service_host}:{settings.vla_service_port}")

    uvicorn.run(
        "src.vla.api.main:app",
        host=settings.vla_service_host,
        port=settings.vla_service_port,
        reload=True,  # Disable in production
        log_level=settings.log_level.lower()
    )