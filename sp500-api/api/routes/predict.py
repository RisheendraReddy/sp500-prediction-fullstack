"""
Prediction endpoints
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Optional
from loguru import logger

from app.config import settings
from app.schemas import (
    PredictionRequest, PredictionResponse,
    BatchPredictionRequest, BatchPredictionResponse
)
from app.models import BaselineModel, prepare_features

router = APIRouter()

# Global model cache
_model_cache: dict[str, BaselineModel] = {}


def load_model(model_type: str) -> BaselineModel:
    """Load model from cache or disk"""
    if model_type in _model_cache:
        return _model_cache[model_type]
    
    model_path = settings.MODEL_DIR / f"model_{model_type}.pkl"
    if not model_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Model {model_type} not found. Train a model first."
        )
    
    try:
        model = BaselineModel(model_type)
        model.load(str(model_path))
        _model_cache[model_type] = model
        logger.info(f"Loaded model: {model_type}")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")


@router.post("/predict", response_model=PredictionResponse)
async def predict_single(request: PredictionRequest, model_type: Optional[str] = None):
    """Make a single prediction"""
    if model_type is None:
        model_type = settings.DEFAULT_MODEL_TYPE
    
    try:
        # Load model
        model = load_model(model_type)
        
        # Convert features to DataFrame
        features_df = pd.DataFrame([request.features])
        
        # Ensure all required features are present
        missing_features = set(model.feature_cols) - set(features_df.columns)
        if missing_features:
            # Fill missing features with 0
            for feat in missing_features:
                features_df[feat] = 0.0
        
        # Prepare features
        X = prepare_features(features_df, model.feature_cols)
        
        # Make prediction
        prediction = model.predict(X)[0]
        
        return PredictionResponse(
            date_id=request.date_id,
            forward_returns=float(prediction)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest, model_type: Optional[str] = None):
    """Make batch predictions"""
    if model_type is None:
        model_type = settings.DEFAULT_MODEL_TYPE
    
    try:
        # Load model
        model = load_model(model_type)
        
        # Convert to DataFrame
        data = []
        for pred_req in request.predictions:
            row = {"date_id": pred_req.date_id, **pred_req.features}
            data.append(row)
        
        features_df = pd.DataFrame(data)
        
        # Ensure all required features are present
        missing_features = set(model.feature_cols) - set(features_df.columns)
        if missing_features:
            for feat in missing_features:
                features_df[feat] = 0.0
        
        # Prepare features
        X = prepare_features(features_df, model.feature_cols)
        
        # Make predictions
        predictions = model.predict(X)
        
        # Format response
        results = [
            PredictionResponse(
                date_id=request.predictions[i].date_id,
                forward_returns=float(pred)
            )
            for i, pred in enumerate(predictions)
        ]
        
        return BatchPredictionResponse(
            predictions=results,
            total=len(results)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/file")
async def predict_from_file(
    file: UploadFile = File(...),
    model_type: Optional[str] = None
):
    """Make predictions from CSV file"""
    if model_type is None:
        model_type = settings.DEFAULT_MODEL_TYPE
    
    try:
        # Load model
        model = load_model(model_type)
        
        # Read CSV
        df = pd.read_csv(file.file)
        
        # Check for date_id
        if 'date_id' not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'date_id' column")
        
        # Prepare features
        X = prepare_features(df, model.feature_cols)
        
        # Make predictions
        predictions = model.predict(X)
        
        # Create result DataFrame
        result_df = pd.DataFrame({
            'date_id': df['date_id'].values,
            'forward_returns': predictions
        })
        
        # Return as CSV
        from fastapi.responses import Response
        return Response(
            content=result_df.to_csv(index=False),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=predictions.csv"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

