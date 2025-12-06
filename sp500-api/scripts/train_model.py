#!/usr/bin/env python3
# Use: python3 scripts/train_model.py
"""
CLI script for training models
"""
import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.models import BaselineModel, get_feature_columns, prepare_features
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from loguru import logger


def prepare_target(df: pd.DataFrame, target_col: str = 'forward_returns') -> pd.Series:
    """Extract target variable"""
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataframe")
    return df[target_col].copy()


def split_train_val(df: pd.DataFrame, val_size: float = 0.2, date_col: str = 'date_id'):
    """Split data into train and validation sets"""
    df_sorted = df.sort_values(date_col)
    split_idx = int(len(df_sorted) * (1 - val_size))
    return df_sorted.iloc[:split_idx].copy(), df_sorted.iloc[split_idx:].copy()


def main():
    parser = argparse.ArgumentParser(description='Train S&P 500 returns prediction model')
    parser.add_argument('--model-type', type=str, default='lightgbm',
                       choices=['lightgbm', 'xgboost', 'rf', 'gbm'],
                       help='Type of model to train')
    parser.add_argument('--data-dir', type=str, default=None,
                       help='Directory containing train.csv')
    parser.add_argument('--val-size', type=float, default=0.2,
                       help='Proportion of data to use for validation')
    parser.add_argument('--model-dir', type=str, default=None,
                       help='Directory to save trained model')
    
    args = parser.parse_args()
    
    # Use settings or override
    data_dir = Path(args.data_dir) if args.data_dir else settings.DATA_DIR
    model_dir = Path(args.model_dir) if args.model_dir else settings.MODEL_DIR
    
    # Load data
    train_file = data_dir / "train.csv"
    if not train_file.exists():
        logger.error(f"Training data not found at {train_file}")
        sys.exit(1)
    
    logger.info(f"Loading training data from {train_file}")
    train_df = pd.read_csv(train_file)
    logger.info(f"Loaded {len(train_df)} rows, {len(train_df.columns)} columns")
    
    # Split data
    train_df_split, val_df = split_train_val(train_df, val_size=args.val_size)
    logger.info(f"Train set: {len(train_df_split)} rows")
    logger.info(f"Validation set: {len(val_df)} rows")
    
    # Prepare features
    feature_cols = get_feature_columns(train_df)
    logger.info(f"Number of features: {len(feature_cols)}")
    
    X_train = prepare_features(train_df_split, feature_cols)
    X_val = prepare_features(val_df, feature_cols)
    
    # Prepare target
    y_train = prepare_target(train_df_split)
    y_val = prepare_target(val_df)
    
    # Train model
    logger.info(f"Training {args.model_type} model...")
    model = BaselineModel(args.model_type)
    model.fit(X_train, y_train, X_val, y_val)
    
    # Evaluate
    val_pred = model.predict(X_val)
    rmse = (mean_squared_error(y_val, val_pred) ** 0.5)
    mae = mean_absolute_error(y_val, val_pred)
    r2 = r2_score(y_val, val_pred)
    
    logger.info(f"\nValidation Metrics:")
    logger.info(f"  RMSE: {rmse:.6f}")
    logger.info(f"  MAE: {mae:.6f}")
    logger.info(f"  R²: {r2:.6f}")
    
    # Save model
    model_dir.mkdir(exist_ok=True)
    model_path = model_dir / f"model_{args.model_type}.pkl"
    model.save(str(model_path))
    logger.info(f"\nModel saved to {model_path}")
    
    logger.info("Training completed!")


if __name__ == '__main__':
    main()

