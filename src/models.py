"""
Model implementations for S&P 500 returns prediction.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from typing import Optional, Dict, Any
import joblib

# Try importing XGBoost and LightGBM, but handle gracefully if they fail
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    xgb = None

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    lgb = None


class BaselineModel:
    """
    Baseline model using simple ensemble of tree-based models.
    """
    
    def __init__(self, model_type: str = 'lightgbm', **kwargs):
        """
        Initialize baseline model.
        
        Args:
            model_type: Type of model ('lightgbm', 'xgboost', 'rf', 'gbm')
            **kwargs: Additional parameters for the model
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.feature_cols = None
        
        if model_type == 'lightgbm':
            if not LIGHTGBM_AVAILABLE:
                raise ImportError("LightGBM is not available. Please install it with: pip install lightgbm")
            default_params = {
                'objective': 'regression',
                'metric': 'rmse',
                'boosting_type': 'gbdt',
                'num_leaves': 31,
                'learning_rate': 0.05,
                'feature_fraction': 0.9,
                'bagging_fraction': 0.8,
                'bagging_freq': 5,
                'verbose': -1,
                'random_state': 42
            }
            default_params.update(kwargs)
            self.model = lgb.LGBMRegressor(**default_params)
            
        elif model_type == 'xgboost':
            if not XGBOOST_AVAILABLE:
                raise ImportError("XGBoost is not available. Please install it with: pip install xgboost. On macOS, you may also need: brew install libomp")
            default_params = {
                'objective': 'reg:squarederror',
                'eval_metric': 'rmse',
                'max_depth': 6,
                'learning_rate': 0.05,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'random_state': 42,
                'n_jobs': -1
            }
            default_params.update(kwargs)
            self.model = xgb.XGBRegressor(**default_params)
            
        elif model_type == 'rf':
            default_params = {
                'n_estimators': 100,
                'max_depth': 10,
                'min_samples_split': 5,
                'min_samples_leaf': 2,
                'random_state': 42,
                'n_jobs': -1
            }
            default_params.update(kwargs)
            self.model = RandomForestRegressor(**default_params)
            
        elif model_type == 'gbm':
            default_params = {
                'n_estimators': 100,
                'max_depth': 5,
                'learning_rate': 0.05,
                'random_state': 42
            }
            default_params.update(kwargs)
            self.model = GradientBoostingRegressor(**default_params)
            
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    def fit(self, X: pd.DataFrame, y: pd.Series, 
            val_X: Optional[pd.DataFrame] = None, 
            val_y: Optional[pd.Series] = None):
        """
        Train the model.
        
        Args:
            X: Training features
            y: Training target
            val_X: Validation features (optional)
            val_y: Validation target (optional)
        """
        self.feature_cols = X.columns.tolist()
        
        # For tree-based models, scaling is optional but we'll do it for consistency
        if self.model_type == 'lightgbm':
            # LightGBM supports eval_set
            if val_X is not None and val_y is not None:
                self.model.fit(X, y, 
                              eval_set=[(val_X, val_y)],
                              callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False)])
            else:
                self.model.fit(X, y)
        elif self.model_type == 'xgboost':
            # XGBoost supports eval_set
            if val_X is not None and val_y is not None:
                self.model.fit(X, y,
                              eval_set=[(val_X, val_y)],
                              verbose=False)
            else:
                self.model.fit(X, y, verbose=False)
        elif self.model_type in ['rf', 'gbm']:
            # Random Forest and GBM don't support eval_set
            self.model.fit(X, y)
        else:
            X_scaled = self.scaler.fit_transform(X)
            if val_X is not None:
                val_X_scaled = self.scaler.transform(val_X)
                self.model.fit(X_scaled, y)
            else:
                self.model.fit(X_scaled, y)
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            X: Features to predict on
            
        Returns:
            Array of predictions
        """
        if self.feature_cols is None:
            raise ValueError("Model has not been trained yet")
        
        # Ensure columns are in the same order
        X = X[self.feature_cols]
        
        if self.model_type in ['lightgbm', 'xgboost', 'rf', 'gbm']:
            return self.model.predict(X)
        else:
            X_scaled = self.scaler.transform(X)
            return self.model.predict(X_scaled)
    
    def save(self, filepath: str):
        """Save model to disk."""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_cols': self.feature_cols,
            'model_type': self.model_type
        }, filepath)
    
    def load(self, filepath: str):
        """Load model from disk."""
        data = joblib.load(filepath)
        self.model = data['model']
        self.scaler = data['scaler']
        self.feature_cols = data['feature_cols']
        self.model_type = data['model_type']


class EnsembleModel:
    """
    Ensemble of multiple models.
    """
    
    def __init__(self, models: list):
        """
        Initialize ensemble with list of models.
        
        Args:
            models: List of model instances
        """
        self.models = models
    
    def fit(self, X: pd.DataFrame, y: pd.Series,
            val_X: Optional[pd.DataFrame] = None,
            val_y: Optional[pd.Series] = None):
        """Train all models in the ensemble."""
        for model in self.models:
            model.fit(X, y, val_X, val_y)
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Average predictions from all models."""
        predictions = np.array([model.predict(X) for model in self.models])
        return np.mean(predictions, axis=0)
    
    def save(self, filepath: str):
        """Save ensemble to disk."""
        joblib.dump(self.models, filepath)
    
    def load(self, filepath: str):
        """Load ensemble from disk."""
        self.models = joblib.load(filepath)


