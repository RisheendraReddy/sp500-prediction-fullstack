# S&P 500 Prediction Frontend

A modern, beautiful React frontend for the S&P 500 Returns Prediction API.

## Features

- 🎨 Modern, responsive UI
- 📊 Train ML models
- 🔮 Make predictions (single or batch)
- 📈 View available models
- 📁 Upload CSV files for batch predictions
- 🚀 Fast and lightweight

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The frontend will be available at: http://localhost:3000

### 3. Make Sure API is Running

The frontend expects the API to be running at: http://localhost:8000

Start the API server:
```bash
cd ../sp500-api
python3 -m app.main
```

## Configuration

Create a `.env` file to configure the API URL:

```env
VITE_API_URL=http://localhost:8000
```

## Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Project Structure

```
sp500-frontend/
├── src/
│   ├── components/     # Reusable components
│   ├── pages/          # Page components
│   │   ├── Home.jsx    # Home page
│   │   ├── Train.jsx   # Train model page
│   │   ├── Predict.jsx # Prediction page
│   │   └── Models.jsx  # Models list page
│   ├── services/       # API service functions
│   │   └── api.js      # API client
│   ├── styles/         # CSS files
│   ├── App.jsx         # Main app component
│   └── main.jsx        # Entry point
├── public/             # Static files
└── package.json        # Dependencies
```

## Pages

### Home
- API status check
- Overview of features
- Quick navigation

### Train Model
- Select model type (LightGBM, XGBoost, RF, GBM)
- Set validation size
- View training metrics

### Predict
- Single prediction with feature input
- Batch prediction from CSV file
- View prediction results

### Models
- List all available models
- View model details
- See feature lists

## Technologies

- React 18
- React Router
- Axios
- Vite
- Modern CSS

## License

MIT License

