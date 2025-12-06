# Frontend Quick Start

## Correct Navigation

The frontend is in the **parent directory** of `sp500-api`:

```bash
# From sp500-api directory, go up one level first
cd ..
cd sp500-frontend

# Or from the root directory
cd "untitled folder"
cd sp500-frontend
```

## Setup Steps

### 1. Navigate to Frontend Directory

```bash
cd "/Users/risheendrareddyboddu/Desktop/untitled folder/sp500-frontend"
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start Development Server

```bash
npm run dev
```

The frontend will be available at: **http://localhost:3000**

## Full Path

If you're in `sp500-api`, use:

```bash
cd ../sp500-frontend
npm install
npm run dev
```

## Make Sure API is Running

Before using the frontend, make sure your API is running:

```bash
# In a separate terminal
cd sp500-api
python3 -m app.main
```

API should be at: **http://localhost:8000**

## Troubleshooting

### "cd: no such file or directory"
- Make sure you're in the right directory
- Use: `cd "../sp500-frontend"` from `sp500-api`
- Or use the full path

### "npm: command not found"
- Install Node.js: https://nodejs.org/
- Or use: `brew install node` (macOS)

### "Cannot find module"
- Run `npm install` first
- Make sure you're in the `sp500-frontend` directory

