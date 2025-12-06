# How to Start the Frontend

## Correct Commands

### ❌ Wrong:
```bash
npm dev          # This doesn't work!
```

### ✅ Correct:
```bash
npm run dev      # Use "run" before "dev"
```

## Step-by-Step

### 1. Navigate to Frontend Directory

```bash
# From sp500-api directory:
cd ../sp500-frontend

# Or use full path:
cd "/Users/risheendrareddyboddu/Desktop/untitled folder/sp500-frontend"
```

### 2. Install Dependencies (First Time Only)

```bash
npm install
```

### 3. Start Development Server

```bash
npm run dev
```

## Full Command Sequence

```bash
# Navigate to frontend
cd "../sp500-frontend"

# Install (if not done already)
npm install

# Start server
npm run dev
```

## What You Should See

After running `npm run dev`, you should see:

```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

Then open: **http://localhost:3000**

## Common Mistakes

1. **Wrong directory**: Make sure you're in `sp500-frontend`, not `sp500-api`
2. **Wrong command**: Use `npm run dev`, not `npm dev`
3. **Dependencies not installed**: Run `npm install` first

## Quick Check

```bash
# Check you're in the right directory
pwd
# Should show: .../sp500-frontend

# Check package.json exists
ls package.json
# Should show: package.json

# Then run
npm run dev
```

