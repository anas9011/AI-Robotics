"""
Perception Data Model

This module defines the data model for perception and vision processing.
"""
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from datetime import datetime


class ObjectInfo(BaseModel):
    """
    Model representing information about a detected object
    """
    name: str
    pose: Dict[str, float]  # Position and orientation {x, y, z, roll, pitch, yaw}
    confidence: float
    bounding_box: Optional[Dict[str, float]] = None  # {x, y, width, height}


class PerceptionData(BaseModel):
    """
    Model representing perception data from sensors
    """
    timestamp: datetime
    image_data: Optional[str] = None  # Base64 encoded image data
    depth_data: Optional[Dict[str, Any]] = None
    point_cloud: Optional[List[Dict[str, float]]] = None
    detected_objects: List[ObjectInfo] = []
    spatial_relationships: Dict[str, Any] = {}
    status: str = "processed"  # raw, processed, analyzed

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"
        # Enable datetime serialization
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }