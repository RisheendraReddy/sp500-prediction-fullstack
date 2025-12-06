"""
Data loading utilities for S&P 500 returns prediction competition.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional


def load_train_data(data_dir: str = "data") -> pd.DataFrame:
    """
    Load training data from train.csv.
    
    Args:
        data_dir: Directory containing the data files
        
    Returns:
        DataFrame with training data
    """
    data_path = Path(data_dir) / "train.csv"
    if not data_path.exists():
        raise FileNotFoundError(f"Training data not found at {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"Loaded training data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def load_test_data(data_dir: str = "data") -> pd.DataFrame:
    """
    Load test data from test.csv.
    
    Args:
        data_dir: Directory containing the data files
        
    Returns:
        DataFrame with test data
    """
    data_path = Path(data_dir) / "test.csv"
    if not data_path.exists():
        raise FileNotFoundError(f"Test data not found at {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"Loaded test data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def get_feature_columns(df: pd.DataFrame) -> list:
    """
    Extract feature column names from dataframe.
    Excludes target variables and metadata columns.
    
    Args:
        df: Input dataframe
        
    Returns:
        List of feature column names
    """
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
    """
    Prepare features for modeling.
    
    Args:
        df: Input dataframe
        feature_cols: List of feature columns to use. If None, auto-detect.
        
    Returns:
        DataFrame with prepared features
    """
    if feature_cols is None:
        feature_cols = get_feature_columns(df)
    
    X = df[feature_cols].copy()
    
    # Handle missing values - forward fill then backward fill
    X = X.ffill().bfill()
    
    # Fill any remaining NaN with 0
    X = X.fillna(0)
    
    return X


def prepare_target(df: pd.DataFrame, target_col: str = 'forward_returns') -> pd.Series:
    """
    Extract target variable from training data.
    
    Args:
        df: Training dataframe
        target_col: Name of target column
        
    Returns:
        Series with target values
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataframe")
    
    y = df[target_col].copy()
    return y


def split_train_val(df: pd.DataFrame, val_size: float = 0.2, 
                   date_col: str = 'date_id') -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split training data into train and validation sets by date.
    
    Args:
        df: Training dataframe
        val_size: Proportion of data to use for validation
        date_col: Name of date column
        
    Returns:
        Tuple of (train_df, val_df)
    """
    df_sorted = df.sort_values(date_col)
    split_idx = int(len(df_sorted) * (1 - val_size))
    
    train_df = df_sorted.iloc[:split_idx].copy()
    val_df = df_sorted.iloc[split_idx:].copy()
    
    print(f"Train set: {len(train_df)} rows")
    print(f"Validation set: {len(val_df)} rows")
    
    return train_df, val_df


