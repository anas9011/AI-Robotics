"""
Voice Processing Router

This module defines the API endpoints for voice processing functionality.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any

from src.vla.services.vla_service import vla_service


router = APIRouter()


@router.post("/process")
async def process_voice_command(audio_file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Process a voice command through the VLA pipeline

    Args:
        audio_file: Audio file containing the voice command

    Returns:
        Processing result from the VLA pipeline
    """
    try:
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
        raise HTTPException(
            status_code=500,
            detail=f"Error processing voice command: {str(e)}"
        )


@router.post("/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)) -> Dict[str, str]:
    """
    Transcribe audio to text using Whisper API

    Args:
        audio_file: Audio file to transcribe

    Returns:
        Transcribed text
    """
    try:
        # Read audio file content
        audio_data = await audio_file.read()

        # Transcribe using Whisper client
        transcription_result = await vla_service.whisper_client.transcribe_audio(audio_data)

        return {
            "transcript": transcription_result["text"],
            "confidence": transcription_result["confidence"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error transcribing audio: {str(e)}"
        )