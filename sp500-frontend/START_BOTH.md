# Starting Both Backend and Frontend

## Yes, You Need Both Running!

The frontend needs the backend API to work. You need **two terminals**:

## Terminal 1: Backend API

```bash
# Navigate to API directory
cd sp500-api

# Start the API server
python3 -m app.main
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

API will be at: **http://localhost:8000**

## Terminal 2: Frontend

```bash
# Navigate to frontend directory
cd sp500-frontend

# Start the frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:3000/
```

Frontend will be at: **http://localhost:3000**

## Quick Start Script

You can also create a script to start both:

### macOS/Linux: `start-all.sh`
```bash
#!/bin/bash
# Start backend in background
cd sp500-api
python3 -m app.main &
BACKEND_PID=$!

# Wait a moment
sleep 2

# Start frontend
cd ../sp500-frontend
npm run dev

# Kill backend when frontend stops
kill $BACKEND_PID
```

## Order of Starting

1. **Start Backend First** (Terminal 1)
   - API needs to be running for frontend to connect

2. **Then Start Frontend** (Terminal 2)
   - Frontend will connect to backend automatically

## Verify Both Are Running

- **Backend**: Visit http://localhost:8000/docs (should show API docs)
- **Frontend**: Visit http://localhost:3000 (should show the app)

## If Frontend Shows "API Offline"

- Make sure backend is running
- Check backend is on port 8000
- Check browser console for connection errors

