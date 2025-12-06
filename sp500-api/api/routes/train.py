"""
Model training endpoints
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pathlib import Path
import pandas as pd
from loguru import logger

from app.config import settings
from app.schemas import TrainRequest, TrainResponse
from app.models import BaselineModel, get_feature_columns, prepare_features

router = APIRouter()


def prepare_target(df: pd.DataFrame, target_col: str = 'forward_returns') -> pd.Series:
    """Extract target variable"""
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found")
    return df[target_col].copy()


def split_train_val(df: pd.DataFrame, val_size: float = 0.2, date_col: str = 'date_id'):
    """Split data into train and validation sets"""
    df_sorted = df.sort_values(date_col)
    split_idx = int(len(df_sorted) * (1 - val_size))
    return df_sorted.iloc[:split_idx].copy(), df_sorted.iloc[split_idx:].copy()


def train_model_task(
    model_type: str,
    val_size: float,
    save_model: bool,
    train_file: Path
):
    """Background task for training model"""
    try:
        logger.info(f"Starting training: {model_type}")
        
        # Load data
        train_df = pd.read_csv(train_file)
        logger.info(f"Loaded {len(train_df)} training samples")
        
        # Split data
        train_df_split, val_df = split_train_val(train_df, val_size)
        
        # Prepare features
        feature_cols = get_feature_columns(train_df)
        X_train = prepare_features(train_df_split, feature_cols)
        X_val = prepare_features(val_df, feature_cols)
        
        # Prepare target
        y_train = prepare_target(train_df_split)
        y_val = prepare_target(val_df)
        
        # Train model
        model = BaselineModel(model_type)
        model.fit(X_train, y_train, X_val, y_val)
        
        # Evaluate
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        val_pred = model.predict(X_val)
        metrics = {
            'rmse': float((mean_squared_error(y_val, val_pred) ** 0.5)),
            'mae': float(mean_absolute_error(y_val, val_pred)),
            'r2': float(r2_score(y_val, val_pred))
        }
        
        # Save model
        model_path = None
        if save_model:
            model_path = settings.MODEL_DIR / f"model_{model_type}.pkl"
            model.save(str(model_path))
            logger.info(f"Model saved to {model_path}")
        
        logger.info(f"Training completed: {model_type}")
        return {"status": "completed", "metrics": metrics, "model_path": str(model_path) if model_path else None}
        
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise


@router.post("/train", response_model=TrainResponse)
async def train_model(request: TrainRequest, background_tasks: BackgroundTasks):
    """Train a new model"""
    # Validate model type
    if request.model_type not in settings.MODEL_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model type. Must be one of: {settings.MODEL_TYPES}"
        )
    
    # Check if training data exists
    train_file = settings.DATA_DIR / "train.csv"
    if not train_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Training data not found at {train_file}"
        )
    
    try:
        # Train model (synchronous for now, can be made async)
        result = train_model_task(
            request.model_type,
            request.val_size,
            request.save_model,
            train_file
        )
        
        return TrainResponse(
            status="success",
            message=f"Model {request.model_type} trained successfully",
            model_type=request.model_type,
            model_path=result.get("model_path"),
            metrics=result.get("metrics")
        )
        
    except Exception as e:
        logger.error(f"Training error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

