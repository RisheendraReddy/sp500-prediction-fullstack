"""
Health check endpoints
"""
from fastapi import APIRouter
from pathlib import Path
from app.config import settings
from app.schemas import HealthResponse, ModelInfo
from loguru import logger

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    # Get available models
    models_available = []
    if settings.MODEL_DIR.exists():
        for model_file in settings.MODEL_DIR.glob("*.pkl"):
            model_type = model_file.stem.replace("model_", "")
            models_available.append(model_type)
    
    return HealthResponse(
        status="healthy",
        version=settings.API_VERSION,
        models_available=models_available
    )


@router.get("/models", response_model=list[ModelInfo])
async def list_models():
    """List all available models"""
    models = []
    if settings.MODEL_DIR.exists():
        for model_file in settings.MODEL_DIR.glob("*.pkl"):
            model_type = model_file.stem.replace("model_", "")
            try:
                import joblib
                data = joblib.load(model_file)
                features = data.get('feature_cols', [])
                models.append(ModelInfo(
                    model_type=model_type,
                    model_path=str(model_file),
                    features=features
                ))
            except Exception as e:
                logger.error(f"Error loading model {model_file}: {e}")
    
    return models

