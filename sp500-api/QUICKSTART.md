# Quick Start Guide

## 1. Setup

```bash
# Clone and navigate
cd sp500-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Prepare Data

Place your data files:
- `data/train.csv` - Training data with `forward_returns` column
- `data/test.csv` - Test data (optional)

## 3. Train a Model

```bash
# Using CLI
python3 scripts/train_model.py --model-type lightgbm

# Or using the API (after starting server)
curl -X POST "http://localhost:8000/api/v1/train" \
  -H "Content-Type: application/json" \
  -d '{"model_type": "lightgbm"}'
```

## 4. Start the API

```bash
python3 -m app.main
```

The API will be available at: http://localhost:8000

## 5. Make Predictions

### Single Prediction
```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "date_id": 1,
    "features": {
      "M1": 0.5,
      "M2": 0.3,
      "E1": 0.2
    }
  }'
```

### Batch Predictions
```bash
curl -X POST "http://localhost:8000/api/v1/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "predictions": [
      {"date_id": 1, "features": {"M1": 0.5}},
      {"date_id": 2, "features": {"M1": 0.6}}
    ]
  }'
```

### From CSV File
```bash
curl -X POST "http://localhost:8000/api/v1/predict/file" \
  -F "file=@test.csv" \
  -F "model_type=lightgbm"
```

## 6. View API Documentation

Visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker

```bash
# Build and run
docker-compose up

# Or build manually
docker build -t sp500-api .
docker run -p 8000:8000 sp500-api
```

## Next Steps

- Check `README.md` for full documentation
- Explore the API at `/docs`
- Train different model types
- Deploy to production

