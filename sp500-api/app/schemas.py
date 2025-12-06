"""
Pydantic schemas for API requests and responses
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class TrainRequest(BaseModel):
    """Request schema for model training"""
    model_type: str = Field(default="lightgbm", description="Type of model to train")
    val_size: float = Field(default=0.2, ge=0.0, le=1.0, description="Validation set size")
    save_model: bool = Field(default=True, description="Whether to save the trained model")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model_type": "lightgbm",
                "val_size": 0.2,
                "save_model": True
            }
        }


class TrainResponse(BaseModel):
    """Response schema for model training"""
    status: str
    message: str
    model_type: str
    model_path: Optional[str] = None
    metrics: Optional[Dict[str, float]] = None
    job_id: Optional[str] = None


class PredictionRequest(BaseModel):
    """Request schema for single prediction"""
    date_id: int = Field(description="Trading day identifier")
    features: Dict[str, float] = Field(description="Feature values")
    
    class Config:
        json_schema_extra = {
            "example": {
                "date_id": 1,
                "features": {
                    "M1": 0.5,
                    "M2": 0.3,
                    "E1": 0.2
                }
            }
        }


class BatchPredictionRequest(BaseModel):
    """Request schema for batch predictions"""
    predictions: List[PredictionRequest] = Field(description="List of prediction requests")
    
    class Config:
        json_schema_extra = {
            "example": {
                "predictions": [
                    {"date_id": 1, "features": {"M1": 0.5}},
                    {"date_id": 2, "features": {"M1": 0.6}}
                ]
            }
        }


class PredictionResponse(BaseModel):
    """Response schema for predictions"""
    date_id: int
    forward_returns: float
    confidence: Optional[float] = None


class BatchPredictionResponse(BaseModel):
    """Response schema for batch predictions"""
    predictions: List[PredictionResponse]
    total: int


class HealthResponse(BaseModel):
    """Response schema for health check"""
    status: str
    version: str
    models_available: List[str]


class ModelInfo(BaseModel):
    """Model information"""
    model_type: str
    model_path: str
    features: List[str]
    created_at: Optional[str] = None

