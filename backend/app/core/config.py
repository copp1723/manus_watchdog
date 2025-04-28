"""
Configuration settings for the Watchdog AI application.
"""
import os
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings

# Base directory for the application
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    API_V1_STR: str = "/v1"
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    
    # File storage settings
    UPLOAD_DIR: Path = BASE_DIR / "data" / "uploads"
    STATIC_DIR: Path = BASE_DIR / "data" / "static"
    CHARTS_DIR: Path = BASE_DIR / "data" / "static" / "charts"
    
    # File size limits (in bytes)
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    
    # Session settings
    SESSION_EXPIRY: int = 60 * 60 * 24  # 24 hours
    
    # Logging settings
    LOG_LEVEL: str = "DEBUG"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.STATIC_DIR, exist_ok=True)
os.makedirs(settings.CHARTS_DIR, exist_ok=True)
