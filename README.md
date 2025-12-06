# S&P 500 Returns Prediction - Full Stack Application

A complete full-stack application for predicting S&P 500 daily returns using machine learning, featuring a REST API backend and modern React frontend.

## 🚀 Features

- **Backend API**: FastAPI-based REST API with multiple ML models
- **Frontend**: Modern React application with beautiful UI
- **ML Models**: LightGBM, XGBoost, Random Forest, Gradient Boosting
- **Real-time Predictions**: Single and batch prediction endpoints
- **Model Training**: Train models via API or CLI
- **Modern UI**: Black & green theme with animations

## 📁 Project Structure

```
.
├── sp500-api/          # Backend API (FastAPI)
│   ├── app/            # Application code
│   ├── api/            # API routes
│   ├── models/         # Trained models
│   ├── data/           # Data files
│   └── scripts/        # Utility scripts
│
└── sp500-frontend/     # Frontend (React)
    ├── src/            # Source code
    ├── public/         # Static files
    └── package.json    # Dependencies
```

## 🛠️ Setup

### Backend Setup

```bash
cd sp500-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
python3 -m app.main
```

API will be available at: http://localhost:8000

### Frontend Setup

```bash
cd sp500-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:3000

## 📚 Documentation

- **Backend API Docs**: http://localhost:8000/docs (Swagger UI)
- **Frontend README**: See `sp500-frontend/README.md`
- **API README**: See `sp500-api/README.md`

## 🎨 UI Features

- Modern black & green color scheme
- Smooth animations and transitions
- Responsive design
- Interactive components
- Real-time status updates

## 🤖 ML Models

Supported models:
- LightGBM
- XGBoost
- Random Forest
- Gradient Boosting

## 📝 Usage

### Train a Model

```bash
# Via CLI
cd sp500-api
python3 scripts/train_model.py --model-type lightgbm

# Via API
curl -X POST "http://localhost:8000/api/v1/train" \
  -H "Content-Type: application/json" \
  -d '{"model_type": "lightgbm"}'
```

### Make Predictions

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"date_id": 1, "features": {...}}'
```

## 🐳 Docker

```bash
# Build and run with Docker Compose
docker-compose up
```

## 📦 Technologies

**Backend:**
- FastAPI
- LightGBM, XGBoost
- Scikit-learn
- Pandas

**Frontend:**
- React
- Vite
- Axios
- React Router

## 📄 License

MIT License

## 👤 Author

RisheendraReddy

## 🔗 Links

- GitHub: https://github.com/RisheendraReddy/sp500-prediction-fullstack
