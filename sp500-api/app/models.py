"""
Machine Learning model implementations
"""
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any
import joblib

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler


class BaselineModel:
    """Baseline model using tree-based algorithms"""
    
    def __init__(self, model_type: str = 'lightgbm', **kwargs):
        """Initialize baseline model"""
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.feature_cols = None
        
        if model_type == 'lightgbm':
            if not LIGHTGBM_AVAILABLE:
                raise ImportError("LightGBM is not available. Install with: pip install lightgbm")
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
                raise ImportError("XGBoost is not available. Install with: pip install xgboost")
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
        """Train the model"""
        self.feature_cols = X.columns.tolist()
        
        if self.model_type == 'lightgbm':
            if val_X is not None and val_y is not None:
                self.model.fit(X, y, 
                              eval_set=[(val_X, val_y)],
                              callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False)])
            else:
                self.model.fit(X, y)
        elif self.model_type == 'xgboost':
            if val_X is not None and val_y is not None:
                self.model.fit(X, y, eval_set=[(val_X, val_y)], verbose=False)
            else:
                self.model.fit(X, y, verbose=False)
        else:
            self.model.fit(X, y)
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions"""
        if self.feature_cols is None:
            raise ValueError("Model has not been trained yet")
        
        X = X[self.feature_cols]
        return self.model.predict(X)
    
    def save(self, filepath: str):
        """Save model to disk"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_cols': self.feature_cols,
            'model_type': self.model_type
        }, filepath)
    
    def load(self, filepath: str):
        """Load model from disk"""
        data = joblib.load(filepath)
        self.model = data['model']
        self.scaler = data['scaler']
        self.feature_cols = data['feature_cols']
        self.model_type = data['model_type']


def get_feature_columns(df: pd.DataFrame) -> list:
    """Extract feature column names"""
    exclude_cols = [
        'date_id',
        'forward_returns',
        'risk_free_rate',
        'market_forward_excess_returns',
        'is_scored',
        'lagged_forward_returns',
        'lagged_risk_free_rate',
        'lagged_market_forward_excess_returns'
    ]
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    return feature_cols


def prepare_features(df: pd.DataFrame, feature_cols: Optional[list] = None) -> pd.DataFrame:
    """Prepare features for modeling"""
    if feature_cols is None:
        feature_cols = get_feature_columns(df)
    
    X = df[feature_cols].copy()
    X = X.ffill().bfill()
    X = X.fillna(0)
    
    return X

