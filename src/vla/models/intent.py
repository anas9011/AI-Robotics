"""
Intent Model

This module defines the data model for intent extraction and representation.
"""
from enum import Enum
from typing import Dict, List, Any, Optional
from pydantic import BaseModel


class IntentType(str, Enum):
    """Enumeration of possible intent types"""
    navigation = "navigation"
    manipulation = "manipulation"
    query = "query"
    other = "other"


class Intent(BaseModel):
    """
    Model representing an extracted intent from natural language processing
    """
    intent_type: IntentType
    action_sequence: List[str]
    parameters: Dict[str, Any]
    context: str
    validation_status: str  # pending, valid, invalid, error

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"

    def dict(self, *args, **kwargs):
        """Override dict method to properly serialize the Enum"""
        result = super().dict(*args, **kwargs)
        result['intent_type'] = self.intent_type.value
        return result