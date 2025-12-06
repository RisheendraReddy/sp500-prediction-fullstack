"""
Application configuration
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "S&P 500 Returns Prediction API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "REST API for predicting S&P 500 daily returns"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    MODEL_DIR: Path = BASE_DIR / "models"
    DATA_DIR: Path = BASE_DIR / "data"
    
    # Model Settings
    DEFAULT_MODEL_TYPE: str = "lightgbm"
    MODEL_TYPES: list = ["lightgbm", "xgboost", "rf", "gbm", "ensemble"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create directories if they don't exist
settings = Settings()
settings.MODEL_DIR.mkdir(exist_ok=True)
settings.DATA_DIR.mkdir(exist_ok=True)

