# Kaggle Evaluation API Setup

## Overview

This competition uses a **server-based evaluation API** instead of the traditional CSV submission format. Kaggle will run your code in a container and call a `predict` function with test data batches.

## How It Works

1. **Server Setup**: Your code runs an inference server that listens for requests
2. **Batch Processing**: Kaggle's gateway sends test data in batches (one `date_id` at a time)
3. **Real-time Prediction**: Your `predict` function receives each batch and returns predictions
4. **Time Limits**:
   - Server must start within **15 minutes** of notebook execution
   - Each batch (except the first) must respond within **5 minutes**
   - The first `predict` call can take longer to load your model

## Key Files

- `inference_server.py` - Main inference server implementation
- `kaggle_evaluation/` - Kaggle evaluation API framework (provided by competition)

## Implementation Details

### The `predict` Function

The `predict` function signature:
```python
def predict(test: pl.DataFrame) -> pl.DataFrame:
    """
    Args:
        test: Polars DataFrame with test features for one date_id
        
    Returns:
        Polars DataFrame with columns:
        - date_id: Trading day identifier
        - forward_returns: Predicted returns (float)
    """
```

### Model Loading Strategy

The implementation uses **lazy loading**:
- Model is loaded on the **first** `predict` call
- This avoids exceeding the 15-minute startup limit
- First call can take longer (no 5-minute deadline)

### Local Testing

To test locally before submission:

```python
# Set environment variable to use local data
export DATA_PATH=/path/to/your/data

# Run the inference server
python inference_server.py
```

Or in Python:
```python
import os
os.environ['DATA_PATH'] = 'data'  # Your local data directory
exec(open('inference_server.py').read())
```

## Usage

### 1. Train Your Model First

```bash
python3 train.py --model-type lightgbm
```

This creates: `models/model_lightgbm.pkl`

### 2. Test Inference Server Locally

```bash
# Make sure test.csv is in the data directory
python3 inference_server.py
```

### 3. Submit to Kaggle

Upload your notebook/code to Kaggle. The evaluation system will:
1. Run your code
2. Call `inference_server.serve()` automatically
3. Send test data batches to your `predict` function
4. Collect predictions and score them

## Environment Variables

- `KAGGLE_IS_COMPETITION_RERUN`: Set by Kaggle during evaluation
- `MODEL_TYPE`: Optional - specify which model to use (default: 'lightgbm')
- `DATA_PATH`: For local testing - path to data directory

## Important Notes

1. **Model Path**: The inference server looks for models in the `models/` directory
   - Tries: `lightgbm` → `ensemble` → `xgboost` → `rf` → `gbm`
   - Or set `MODEL_TYPE` environment variable

2. **Data Format**: 
   - Input: Polars DataFrame with feature columns
   - Output: Polars DataFrame with `date_id` and `forward_returns`

3. **Performance**:
   - First prediction may be slow (model loading)
   - Subsequent predictions should be fast (< 1 second per batch)

4. **Error Handling**:
   - Make sure your model file exists before submission
   - Test locally first to catch any issues

## Troubleshooting

### Model Not Found
```
FileNotFoundError: No trained model found
```
**Solution**: Train a model first using `train.py`

### Import Errors
```
ModuleNotFoundError: No module named 'polars'
```
**Solution**: Install dependencies: `pip install -r requirements.txt`

### Timeout Errors
If you see timeout errors, your `predict` function is taking too long:
- Optimize feature preparation
- Consider using a faster model
- Pre-compute any heavy operations

## Example Workflow

```bash
# 1. Train model
python3 train.py --model-type lightgbm

# 2. Test locally (optional)
python3 inference_server.py

# 3. Prepare for submission
# - Ensure inference_server.py is in your submission
# - Ensure models/ directory with trained model is included
# - Upload to Kaggle
```

## Differences from CSV Submission

| CSV Submission | Evaluation API |
|---------------|----------------|
| Generate CSV file | Implement `predict` function |
| Submit file | Submit code |
| Batch processing | Real-time processing |
| No time limits | 5-minute per-batch limit |

The Evaluation API allows for more dynamic predictions and can handle streaming data, but requires your code to be more robust and efficient.

