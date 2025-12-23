"""
Action Execution Result Model

This module defines the data model for action execution results and feedback.
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime


class ActionResult(BaseModel):
    """
    Model representing the result of an action execution
    """
    action_id: str
    status: str  # success, failure, partial, timeout
    execution_time: float  # in seconds
    feedback: Optional[Dict[str, Any]] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    recovery_needed: bool = False
    timestamp: datetime

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"
        # Enable datetime serialization
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }