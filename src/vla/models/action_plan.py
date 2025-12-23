"""
Action Plan Model

This module defines the data models for ROS 2 action planning and execution.
"""
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from datetime import datetime


class ROS2Action(BaseModel):
    """
    Model representing a single ROS 2 action
    """
    action_type: str  # e.g., "move_base", "move_arm", "grasp_object", etc.
    parameters: Dict[str, Any]
    timeout: float = 10.0  # seconds

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"


class ROS2ActionPlan(BaseModel):
    """
    Model representing a sequence of ROS 2 actions to execute
    """
    id: str
    actions: List[ROS2Action]
    dependencies: List[str]  # IDs of dependent actions
    timeout: float = 30.0  # Overall timeout in seconds
    recovery_steps: List[ROS2Action] = []
    validation_rules: List[Dict[str, Any]] = []
    execution_start_time: Optional[datetime] = None
    execution_end_time: Optional[datetime] = None
    status: str = "created"  # created, validating, scheduled, executing, completed, failed, needs_replanning

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"
        # Enable datetime serialization
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }