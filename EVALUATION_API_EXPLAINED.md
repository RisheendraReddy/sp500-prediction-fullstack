# Kaggle Evaluation API - Explained

## What is the Evaluation API?

The **Kaggle Evaluation API** is a server-based evaluation system used by some competitions. Instead of submitting a CSV file with predictions, you submit **code** that runs a server. Kaggle then calls your server with test data and collects predictions in real-time.

## How It Works

### Traditional CSV Submission (Not This Competition)
```
1. Train model locally
2. Generate predictions.csv
3. Upload CSV to Kaggle
4. Kaggle scores the CSV
```

### Evaluation API (This Competition)
```
1. Train model locally
2. Write predict() function
3. Upload code to Kaggle
4. Kaggle runs your code as a server
5. Kaggle sends test data → your server → predictions
6. Kaggle scores the predictions
```

## Architecture

```
┌─────────────────┐
│  Kaggle Gateway │  (Runs in separate container)
│  (Test Data)    │
└────────┬────────┘
         │ gRPC calls
         │ (sends test batches)
         ▼
┌─────────────────┐
│ Your Code       │  (Runs in your container)
│ inference_server│
│   - predict()   │
│   - model       │
└─────────────────┘
         │
         │ returns predictions
         ▼
┌─────────────────┐
│  Kaggle Gateway │
│  (Collects &    │
│   Scores)       │
└─────────────────┘
```

## Key Components

### 1. The `predict` Function

This is the **only function you need to implement**:

```python
def predict(test: pl.DataFrame) -> pl.DataFrame:
    """
    Called by Kaggle with each batch of test data.
    
    Args:
        test: Polars DataFrame with features for one date_id
        
    Returns:
        Polars DataFrame with predictions:
        - date_id: The date identifier
        - forward_returns: Your prediction (float)
    """
    # Your prediction logic here
    return predictions
```

### 2. The Inference Server

The `DefaultInferenceServer` wraps your `predict` function and:
- Starts a gRPC server
- Listens for requests from Kaggle's gateway
- Calls your `predict` function when data arrives
- Returns predictions to the gateway

### 3. The Gateway (Provided by Kaggle)

Kaggle's gateway:
- Loads the hidden test set
- Sends data to your server one batch at a time
- Collects predictions
- Scores them

## Time Limits

### Startup Time: 15 minutes
- Your server must start within 15 minutes
- **Solution**: Use lazy loading - load your model on the first `predict` call

### Response Time: 5 minutes per batch
- Each batch (except the first) must return within 5 minutes
- **Solution**: Keep predictions fast - preprocess efficiently

### First Call Exception
- The first `predict` call can take longer (no 5-minute limit)
- This is when you should load your model

## Data Flow

### Batch Processing

The test data is sent **one date_id at a time**:

```
Batch 1: date_id = 1  → predict() → predictions for date_id 1
Batch 2: date_id = 2  → predict() → predictions for date_id 2
Batch 3: date_id = 3  → predict() → predictions for date_id 3
...
```

Each batch is a Polars DataFrame with:
- All feature columns (M*, E*, I*, P*, V*, S*, MOM*, D*)
- The `date_id` column
- Any lagged columns (lagged_forward_returns, etc.)

## Why Use This System?

### Advantages:
1. **Dynamic Predictions**: Can use information from previous batches
2. **Real-time Processing**: No need to pre-generate all predictions
3. **Streaming Data**: Can handle data that arrives over time
4. **Validation**: Ensures your code actually runs

### Disadvantages:
1. **More Complex**: Requires server setup
2. **Time Constraints**: Must respond quickly
3. **Debugging**: Harder to debug than CSV generation

## Implementation in This Project

### File: `inference_server.py`

This file:
1. Implements the `predict` function
2. Loads your trained model (lazy loading)
3. Prepares features
4. Makes predictions
5. Returns results in the correct format

### Key Features:

```python
# Global model (loaded once)
_model = None

def predict(test: pl.DataFrame) -> pl.DataFrame:
    global _model
    
    # Load model on first call (lazy loading)
    if _model is None:
        load_model()
    
    # Prepare features and predict
    X_test = prepare_features(test)
    predictions = _model.predict(X_test)
    
    # Return in correct format
    return pl.DataFrame({
        'date_id': test['date_id'],
        'forward_returns': predictions
    })
```

## Testing Locally

Before submitting to Kaggle, test locally:

```python
# Set environment variable
os.environ['DATA_PATH'] = 'data'

# Run inference server
python inference_server.py
```

This will:
- Use your local `test.csv`
- Call `predict` with each batch
- Show you the predictions
- Help you debug any issues

## Common Issues

### 1. Model Not Found
**Error**: `FileNotFoundError: No trained model found`

**Solution**: 
- Train a model first: `python train.py`
- Ensure model file is in `models/` directory
- Check model path in `inference_server.py`

### 2. Timeout
**Error**: `GRPC_DEADLINE_EXCEEDED`

**Solution**:
- Optimize your `predict` function
- Pre-compute heavy operations
- Use faster models

### 3. Wrong Output Format
**Error**: Validation errors from gateway

**Solution**:
- Ensure output has `date_id` and `forward_returns` columns
- Check data types (date_id: int, forward_returns: float)
- Verify Polars DataFrame format

## Summary

The Evaluation API is a server-based system where:
- You implement a `predict` function
- Kaggle calls it with test data batches
- You return predictions in real-time
- Kaggle scores the predictions

It's more complex than CSV submission but allows for more dynamic predictions and ensures your code actually works.

