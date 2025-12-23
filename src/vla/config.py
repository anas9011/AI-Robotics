"""
Configuration module for VLA Integration Service
"""
import os
from typing import Optional
try:
    from pydantic import BaseSettings
except ImportError:
    from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo")

    # Whisper API Configuration
    whisper_model: str = os.getenv("WHISPER_MODEL", "whisper-1")

    # Service Configuration
    vla_service_host: str = os.getenv("VLA_SERVICE_HOST", "0.0.0.0")
    vla_service_port: int = int(os.getenv("VLA_SERVICE_PORT", "8000"))

    # Simulation Configuration
    simulation_type: str = os.getenv("SIMULATION_TYPE", "gazebo")
    simulation_host: str = os.getenv("SIMULATION_HOST", "localhost")
    simulation_port: int = int(os.getenv("SIMULATION_PORT", "11345"))

    # Logging Configuration
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "vla_service.log")

    # ROS Configuration
    ros_domain_id: int = int(os.getenv("ROS_DOMAIN_ID", "0"))
    ros_hostname: str = os.getenv("ROS_HOSTNAME", "localhost")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


# Create a global settings instance
settings = Settings()


def validate_settings():
    """Validate that required settings are present"""
    errors = []

    if not settings.openai_api_key:
        errors.append("OPENAI_API_KEY is required")

    if settings.openai_model not in ["gpt-4-turbo", "gpt-3.5-turbo", "gpt-4", "gpt-4o"]:
        errors.append(f"Invalid OPENAI_MODEL: {settings.openai_model}")

    if settings.simulation_type not in ["gazebo", "unity"]:
        errors.append(f"Invalid SIMULATION_TYPE: {settings.simulation_type}")

    if settings.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        errors.append(f"Invalid LOG_LEVEL: {settings.log_level}")

    return errors


if __name__ == "__main__":
    # Validate settings on direct execution
    validation_errors = validate_settings()
    if validation_errors:
        print("Configuration validation errors:")
        for error in validation_errors:
            print(f"  - {error}")
    else:
        print("Configuration is valid")