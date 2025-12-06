"""
Main training script for S&P 500 returns prediction.
"""
import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import (
    load_train_data,
    get_feature_columns,
    prepare_features,
    prepare_target,
    split_train_val
)
from src.models import BaselineModel, EnsembleModel
from src.evaluate import evaluate_predictions


def main():
    parser = argparse.ArgumentParser(description='Train S&P 500 returns prediction model')
    parser.add_argument('--data-dir', type=str, default='data', 
                       help='Directory containing train.csv')
    parser.add_argument('--model-type', type=str, default='lightgbm',
                       choices=['lightgbm', 'xgboost', 'rf', 'gbm', 'ensemble'],
                       help='Type of model to train')
    parser.add_argument('--val-size', type=float, default=0.2,
                       help='Proportion of data to use for validation')
    parser.add_argument('--model-dir', type=str, default='models',
                       help='Directory to save trained model')
    parser.add_argument('--no-save', action='store_true',
                       help='Do not save the trained model')
    
    args = parser.parse_args()
    
    # Load data
    print("Loading training data...")
    train_df = load_train_data(data_dir=args.data_dir)
    
    # Split into train and validation
    print("\nSplitting data into train and validation sets...")
    train_df_split, val_df = split_train_val(train_df, val_size=args.val_size)
    
    # Prepare features
    print("\nPreparing features...")
    feature_cols = get_feature_columns(train_df)
    print(f"Number of features: {len(feature_cols)}")
    
    X_train = prepare_features(train_df_split, feature_cols)
    X_val = prepare_features(val_df, feature_cols)
    
    # Prepare target
    y_train = prepare_target(train_df_split)
    y_val = prepare_target(val_df)
    
    # Initialize and train model
    print(f"\nTraining {args.model_type} model...")
    if args.model_type == 'ensemble':
        model = EnsembleModel([
            BaselineModel('lightgbm', n_estimators=100),
            BaselineModel('xgboost', n_estimators=100),
            BaselineModel('rf', n_estimators=100)
        ])
    else:
        model = BaselineModel(args.model_type)
    
    model.fit(X_train, y_train, X_val, y_val)
    
    # Evaluate on validation set
    print("\nEvaluating on validation set...")
    val_pred = model.predict(X_val)
    val_metrics = evaluate_predictions(y_val.values, val_pred, prefix="Validation")
    
    # Save model
    if not args.no_save:
        model_dir = Path(args.model_dir)
        model_dir.mkdir(exist_ok=True)
        model_path = model_dir / f"model_{args.model_type}.pkl"
        model.save(str(model_path))
        print(f"\nModel saved to {model_path}")
    
    print("\nTraining completed!")


if __name__ == '__main__':
    main()

