"""
Kaggle Evaluation API Inference Server
This script implements the predict function for the Kaggle evaluation API.
It loads a trained model and makes predictions on test data batches.
"""
import os
import sys
from pathlib import Path

import pandas as pd
import polars as pl

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

import kaggle_evaluation.default_inference_server
from src.data_loader import get_feature_columns, prepare_features
from src.models import BaselineModel, EnsembleModel

# Global model variable - loaded once on first predict call
_model = None
_model_type = None
_feature_cols = None


def load_model(model_path: str = None, model_type: str = 'lightgbm'):
    """
    Load the trained model. This is called lazily on the first predict call
    to avoid exceeding the 15-minute startup time limit.
    
    Args:
        model_path: Path to the trained model file
        model_type: Type of model (lightgbm, xgboost, rf, gbm, ensemble)
    """
    global _model, _model_type, _feature_cols
    
    if _model is not None:
        return  # Model already loaded
    
    # Determine model path if not provided
    if model_path is None:
        # Try to find model in models directory
        models_dir = Path(__file__).parent / 'models'
        # Try different model types in order of preference
        for mt in ['lightgbm', 'ensemble', 'xgboost', 'rf', 'gbm']:
            potential_path = models_dir / f'model_{mt}.pkl'
            if potential_path.exists():
                model_path = str(potential_path)
                model_type = mt
                break
        
        if model_path is None:
            raise FileNotFoundError(
                "No trained model found. Please train a model first using train.py"
            )
    
    print(f"Loading model from {model_path}...")
    
    # Initialize and load model
    if model_type == 'ensemble':
        _model = EnsembleModel([])
    else:
        _model = BaselineModel(model_type)
    
    _model.load(model_path)
    _model_type = model_type
    
    # Get feature columns from the loaded model
    _feature_cols = _model.feature_cols
    
    print(f"Model loaded successfully. Model type: {model_type}")
    print(f"Number of features: {len(_feature_cols)}")


def predict(test: pl.DataFrame) -> pl.DataFrame:
    """
    Predict function for Kaggle Evaluation API.
    
    This function is called by the evaluation API with batches of test data.
    Each batch (except the first) must be returned within 5 minutes.
    The first call can take longer to load the model.
    
    Args:
        test: Polars DataFrame containing test features for a batch
        
    Returns:
        Polars DataFrame with predictions. Must contain 'date_id' and 'forward_returns' columns.
    """
    global _model, _feature_cols
    
    # Load model on first call (lazy loading)
    if _model is None:
        # Try to determine model type from environment or use default
        model_type = os.getenv('MODEL_TYPE', 'lightgbm')
        load_model(model_type=model_type)
    
    # Convert Polars DataFrame to Pandas for compatibility with our models
    test_pd = test.to_pandas()
    
    # Prepare features
    X_test = prepare_features(test_pd, _feature_cols)
    
    # Make predictions
    predictions = _model.predict(X_test)
    
    # Create result DataFrame
    # The competition expects 'forward_returns' as the prediction column
    result = pl.DataFrame({
        'date_id': test_pd['date_id'].values,
        'forward_returns': predictions
    })
    
    return result


# When your notebook is run on the hidden test set, inference_server.serve must be called 
# within 15 minutes of the notebook starting or the gateway will throw an error.
# If you need more than 15 minutes to load your model you can do so during the very
# first `predict` call, which does not have the usual 5 minute response deadline.

inference_server = kaggle_evaluation.default_inference_server.DefaultInferenceServer(predict)

if os.getenv('KAGGLE_IS_COMPETITION_RERUN'):
    # Competition mode: start the server and wait for requests
    inference_server.serve()
else:
    # Local testing mode: run with local gateway
    data_path = os.getenv('DATA_PATH', '/kaggle/input/hull-tactical-market-prediction/')
    if not os.path.exists(data_path):
        # Try local data directory
        data_path = str(Path(__file__).parent / 'data')
    
    inference_server.run_local_gateway((data_path,))

