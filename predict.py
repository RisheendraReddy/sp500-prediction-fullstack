"""
Prediction script for S&P 500 returns prediction.
"""
import argparse
import sys
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import load_test_data, prepare_features, get_feature_columns
from src.models import BaselineModel, EnsembleModel


def main():
    parser = argparse.ArgumentParser(description='Make predictions on test data')
    parser.add_argument('--data-dir', type=str, default='data',
                       help='Directory containing test.csv')
    parser.add_argument('--model-path', type=str, required=True,
                       help='Path to trained model file')
    parser.add_argument('--output', type=str, default='submission.csv',
                       help='Output file path for predictions')
    parser.add_argument('--model-type', type=str, default='lightgbm',
                       choices=['lightgbm', 'xgboost', 'rf', 'gbm', 'ensemble'],
                       help='Type of model (must match saved model)')
    
    args = parser.parse_args()
    
    # Load test data
    print("Loading test data...")
    test_df = load_test_data(data_dir=args.data_dir)
    
    # Prepare features
    print("Preparing features...")
    feature_cols = get_feature_columns(test_df)
    X_test = prepare_features(test_df, feature_cols)
    
    # Load model
    print(f"Loading model from {args.model_path}...")
    if args.model_type == 'ensemble':
        model = EnsembleModel([])
    else:
        model = BaselineModel(args.model_type)
    model.load(args.model_path)
    
    # Make predictions
    print("Making predictions...")
    predictions = model.predict(X_test)
    
    # Create submission dataframe
    submission = pd.DataFrame({
        'date_id': test_df['date_id'],
        'forward_returns': predictions
    })
    
    # Save submission
    output_path = Path(args.output)
    submission.to_csv(output_path, index=False)
    print(f"\nPredictions saved to {output_path}")
    print(f"Number of predictions: {len(predictions)}")
    print(f"Prediction statistics:")
    print(f"  Mean: {predictions.mean():.6f}")
    print(f"  Std: {predictions.std():.6f}")
    print(f"  Min: {predictions.min():.6f}")
    print(f"  Max: {predictions.max():.6f}")


if __name__ == '__main__':
    main()

