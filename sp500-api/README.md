# S&P 500 Returns Prediction API

A production-ready REST API for predicting S&P 500 daily returns using machine learning models.

## Features

- 🚀 RESTful API with FastAPI
- 📊 Multiple ML models (LightGBM, XGBoost, Random Forest, Gradient Boosting)
- 🔄 Model training endpoints
- 📈 Prediction endpoints
- 📝 Comprehensive documentation
- 🧪 Unit tests
- 🐳 Docker support
- 📦 Easy deployment

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/RisheendraReddy/sp500-prediction-api.git
cd sp500-prediction-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Data

Place your training data in the `data/` directory:
- `data/train.csv` - Training data with `forward_returns` column
- `data/test.csv` - Test data (optional)

### 3. Train a Model

```bash
# Train using the CLI
python3 scripts/train_model.py --model-type lightgbm

# Or use the API
curl -X POST "http://localhost:8000/api/v1/train" \
  -H "Content-Type: application/json" \
  -d '{"model_type": "lightgbm"}'
```

### 4. Start the API Server

```bash
# Development mode
python3 -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Make Predictions

```bash
# Using curl
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"date_id": 1, "features": {...}}'

# Or use the interactive docs
# Visit: http://localhost:8000/docs
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
sp500-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # ML model implementations
│   ├── schemas.py           # Pydantic schemas
│   └── config.py            # Configuration
├── api/
│   ├── __init__.py
│   └── routes/
│       ├── __init__.py
│       ├── train.py         # Training endpoints
│       ├── predict.py       # Prediction endpoints
│       └── health.py        # Health check endpoints
├── models/                  # Saved trained models
├── data/                    # Data files
├── config/                  # Configuration files
├── scripts/                 # Utility scripts
│   └── train_model.py       # CLI training script
├── tests/                   # Unit tests
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
└── README.md              # This file
```

## API Endpoints

### Health Check
- `GET /api/v1/health` - Check API health
- `GET /api/v1/models` - List available models

### Training
- `POST /api/v1/train` - Train a new model
- `GET /api/v1/train/status/{job_id}` - Check training status

### Predictions
- `POST /api/v1/predict` - Make single prediction
- `POST /api/v1/predict/batch` - Make batch predictions
- `POST /api/v1/predict/file` - Predict from CSV file

## Configuration

Create a `.env` file in the root directory:

```env
MODEL_DIR=models
DATA_DIR=data
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
```

## Docker Deployment

```bash
# Build image
docker build -t sp500-api .

# Run container
docker run -p 8000:8000 sp500-api

# Or use docker-compose
docker-compose up
```

## Development

```bash
# Run tests
pytest tests/

# Format code
black app/ api/ scripts/

# Lint code
flake8 app/ api/ scripts/
```

## Repository

GitHub: https://github.com/RisheendraReddy/sp500-prediction-api

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

RisheendraReddy
