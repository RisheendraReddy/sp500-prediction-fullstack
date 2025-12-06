"""
Evaluation utilities for S&P 500 returns prediction.
"""
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import Tuple


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """
    Calculate evaluation metrics.
    
    Args:
        y_true: True target values
        y_pred: Predicted values
        
    Returns:
        Dictionary of metrics
    """
    metrics = {
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'mse': mean_squared_error(y_true, y_pred),
        'mae': mean_absolute_error(y_true, y_pred),
        'r2': r2_score(y_true, y_pred),
        'correlation': np.corrcoef(y_true, y_pred)[0, 1]
    }
    return metrics


def print_metrics(metrics: dict, prefix: str = ""):
    """
    Print evaluation metrics in a readable format.
    
    Args:
        metrics: Dictionary of metrics
        prefix: Optional prefix for the output
    """
    if prefix:
        print(f"\n{prefix} Metrics:")
    else:
        print("\nEvaluation Metrics:")
    print("-" * 40)
    for metric_name, metric_value in metrics.items():
        print(f"{metric_name.upper()}: {metric_value:.6f}")
    print("-" * 40)


def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray, 
                        prefix: str = "") -> dict:
    """
    Evaluate predictions and print metrics.
    
    Args:
        y_true: True target values
        y_pred: Predicted values
        prefix: Optional prefix for the output
        
    Returns:
        Dictionary of metrics
    """
    metrics = calculate_metrics(y_true, y_pred)
    print_metrics(metrics, prefix)
    return metrics

