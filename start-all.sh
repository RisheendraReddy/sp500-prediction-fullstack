#!/bin/bash
echo "🚀 Starting S&P 500 Prediction System..."
echo ""

# Start backend
echo "📡 Starting Backend API..."
cd sp500-api
python3 -m app.main &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting Frontend..."
cd sp500-frontend
npm run dev

# Cleanup on exit
trap "kill $BACKEND_PID 2>/dev/null" EXIT
