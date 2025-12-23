"""
Health Check Router

This module defines the API endpoints for health checking functionality.
"""
from fastapi import APIRouter
from typing import Dict, Any

from src.vla.services.vla_service import vla_service


router = APIRouter()


@router.get("/status")
async def get_status() -> Dict[str, Any]:
    """
    Get the current status of the VLA service

    Returns:
        Status information about all VLA components
    """
    health_status = await vla_service.health_check()
    return health_status


@router.get("/ping")
async def ping() -> Dict[str, str]:
    """
    Simple ping endpoint to check if the service is running

    Returns:
        Simple response indicating service is running
    """
    return {"status": "ok", "message": "VLA service is running"}


@router.get("/components")
async def get_component_health() -> Dict[str, Any]:
    """
    Get health status of individual VLA components

    Returns:
        Health status of each component
    """
    health_status = await vla_service.health_check()

    # Extract just the components part
    components = health_status.get("components", {})

    return {
        "timestamp": health_status.get("timestamp"),
        "components": components
    }