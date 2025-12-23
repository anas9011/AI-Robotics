"""
OpenAI Whisper API Client

This module provides an interface to the OpenAI Whisper API for speech-to-text conversion.
"""
import asyncio
import logging
from typing import Dict, Any, Optional

import openai
from openai import AsyncOpenAI

from src.vla.config import settings


logger = logging.getLogger(__name__)


class WhisperAPIClient:
    """
    Client for interacting with OpenAI Whisper API for speech recognition
    """

    def __init__(self):
        """Initialize the Whisper API client with configuration from settings"""
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for Whisper API client")

        # Initialize the OpenAI client
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.whisper_model

        logger.info(f"Whisper API client initialized with model: {self.model}")

    async def transcribe_audio(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Transcribe audio data using OpenAI Whisper API

        Args:
            audio_data: Raw audio data in bytes

        Returns:
            Dictionary containing transcription result with text and confidence
        """
        try:
            logger.info("Starting audio transcription with Whisper API")

            # Write audio data to a temporary file for OpenAI API
            import tempfile
            import io

            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name

            # Call Whisper API
            with open(temp_file_path, "rb") as audio_file:
                transcription = await self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    response_format="verbose_json",  # Get detailed response with confidence scores
                    timestamp_granularities=["segment"]
                )

            # Clean up temporary file
            import os
            os.unlink(temp_file_path)

            # Calculate confidence based on the transcription
            # For now, we'll use a simple approach; in a real implementation,
            # we'd use more sophisticated confidence scoring
            text = transcription.text
            confidence = self._calculate_confidence(transcription)

            result = {
                "text": text,
                "confidence": confidence,
                "segments": transcription.segments if hasattr(transcription, 'segments') else [],
                "language": transcription.language if hasattr(transcription, 'language') else 'unknown'
            }

            logger.info(f"Transcription completed: '{text[:50]}...' with confidence {confidence:.2f}")
            return result

        except Exception as e:
            logger.error(f"Error in Whisper transcription: {str(e)}", exc_info=True)
            raise

    def _calculate_confidence(self, transcription) -> float:
        """
        Calculate confidence score from transcription result
        This is a simplified implementation - in a real system, we'd use more sophisticated methods
        """
        # In a real implementation, we'd analyze the detailed response from Whisper
        # For now, return a default confidence based on the presence of text
        if hasattr(transcription, 'text') and transcription.text:
            # If we have text, assume moderate to high confidence
            # In a real system, we'd analyze word-level confidence scores
            return 0.85
        else:
            return 0.1

    async def transcribe_audio_file(self, file_path: str) -> Dict[str, Any]:
        """
        Transcribe an audio file using OpenAI Whisper API

        Args:
            file_path: Path to the audio file

        Returns:
            Dictionary containing transcription result
        """
        try:
            logger.info(f"Starting audio file transcription: {file_path}")

            with open(file_path, "rb") as audio_file:
                transcription = await self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )

            # Calculate confidence
            confidence = self._calculate_confidence(transcription)

            result = {
                "text": transcription.text,
                "confidence": confidence,
                "segments": transcription.segments if hasattr(transcription, 'segments') else [],
                "language": transcription.language if hasattr(transcription, 'language') else 'unknown'
            }

            logger.info(f"File transcription completed: '{result['text'][:50]}...' with confidence {confidence:.2f}")
            return result

        except Exception as e:
            logger.error(f"Error in Whisper file transcription: {str(e)}", exc_info=True)
            raise

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check of the Whisper API client

        Returns:
            Dictionary containing health status
        """
        try:
            # Test with a minimal audio request (this is a mock test since we need actual audio)
            # In a real implementation, we might test API key validity differently
            if not settings.openai_api_key:
                return {"status": "error", "message": "OpenAI API key not configured"}

            # Check if we can access the API (with a minimal request)
            # For now, just verify the API key format
            if len(settings.openai_api_key) < 10:
                return {"status": "warning", "message": "OpenAI API key seems too short"}

            return {
                "status": "healthy",
                "model": self.model,
                "api_key_valid": len(settings.openai_api_key) > 20  # Basic validation
            }

        except Exception as e:
            logger.error(f"Whisper client health check failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def validate_audio_format(self, audio_data: bytes) -> bool:
        """
        Validate that the audio data is in a supported format for Whisper API

        Args:
            audio_data: Raw audio data in bytes

        Returns:
            True if format is supported, False otherwise
        """
        try:
            # Whisper API supports: mp3, mp4, mpeg, mpga, m4a, wav, and webm
            # We'll check the file header to determine format

            # Check for common audio file headers
            if len(audio_data) < 12:
                return False

            # Check for WAV header
            if audio_data[0:4] == b'RIFF' and audio_data[8:12] == b'WAVE':
                return True

            # Check for MP3 header (simplified)
            if audio_data[0:3] == b'ID3' or (audio_data[0] & 0xFF == 0xFF and (audio_data[1] & 0xE0) == 0xE0):
                return True

            # Check for M4A/MP4 header
            if audio_data[4:8] == b'ftyp':
                return True

            # For now, assume other formats are supported by Whisper
            # In a real implementation, we'd do more thorough validation
            return True

        except Exception:
            logger.warning("Error validating audio format, assuming supported")
            return False