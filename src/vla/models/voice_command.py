"""
Voice Command Model

This module defines the data model for voice command processing.
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

from src.vla.models.intent import Intent


class VoiceCommand(BaseModel):
    """
    Model representing a voice command with all associated data
    """
    id: str
    audio_data: Optional[str] = None  # Base64 encoded audio data
    transcript: str = ""
    timestamp: datetime
    confidence: float = 0.0
    intent: Optional[Intent] = None
    entities: Dict[str, Any] = {}
    status: str = "received"  # received, transcribing, intent_processing, task_decomposing, validating, executing, completed, failed

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"
        # Enable datetime serialization
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }