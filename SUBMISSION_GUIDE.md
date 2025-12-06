# Kaggle Submission Guide

## What to Submit

For this competition, you need to submit **code** (not a CSV file) that implements the evaluation API. Here's exactly what to include:

## Required Files

### 1. Main Inference Server File
**File**: `inference_server.py` (or convert to a notebook)

This is the main file that Kaggle will run. It contains:
- Your `predict` function
- Model loading logic
- Server setup

### 2. Trained Model File(s)
**Directory**: `models/`

Include your trained model file(s):
- `models/model_lightgbm.pkl` (or whichever model you trained)
- Make sure the model file is included in your submission

### 3. Source Code
**Directory**: `src/`

Include all your source code:
- `src/__init__.py`
- `src/data_loader.py`
- `src/models.py`
- `src/evaluate.py`

### 4. Kaggle Evaluation Framework
**Directory**: `kaggle_evaluation/`

This is provided by the competition and must be included:
- `kaggle_evaluation/__init__.py`
- `kaggle_evaluation/default_inference_server.py`
- `kaggle_evaluation/default_gateway.py`
- `kaggle_evaluation/core/` (entire directory)

## Submission Options

### Option 1: Python Script Submission (Recommended)

Create a zip file containing:
```
submission.zip
├── inference_server.py          # Main file
├── models/
│   └── model_lightgbm.pkl       # Your trained model
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── models.py
│   └── evaluate.py
└── kaggle_evaluation/
    ├── __init__.py
    ├── default_inference_server.py
    ├── default_gateway.py
    └── core/
        └── ... (all files)
```

### Option 2: Kaggle Notebook Submission

Convert `inference_server.py` to a Jupyter notebook (`.ipynb`) and include all dependencies.

## Step-by-Step Submission Process

### Step 1: Train Your Model

```bash
# Train your best model
python3 train.py --model-type lightgbm

# This creates: models/model_lightgbm.pkl
```

### Step 2: Prepare Submission Files

Create a submission directory:

```bash
mkdir submission
cp inference_server.py submission/
cp -r models submission/
cp -r src submission/
cp -r kaggle_evaluation submission/
```

### Step 3: Verify Your Submission

Make sure your `inference_server.py` can find the model:

```python
# In inference_server.py, the model path should work
# It looks for models in: models/model_{model_type}.pkl
```

### Step 4: Test Locally (Important!)

Before submitting, test that everything works:

```bash
# Make sure test.csv is in data/ directory
python3 inference_server.py
```

This should run without errors and show predictions.

### Step 5: Create Submission Package

**For Kaggle Notebook:**
- Upload all files to Kaggle
- Create a notebook that runs `inference_server.py`
- Or paste the code directly into a notebook cell

**For Code Submission:**
- Create a zip file with all required files
- Upload to Kaggle

## File Structure for Submission

```
your_submission/
├── inference_server.py          # REQUIRED: Main entry point
├── models/
│   └── model_lightgbm.pkl       # REQUIRED: Your trained model
├── src/                         # REQUIRED: Your source code
│   ├── __init__.py
│   ├── data_loader.py
│   ├── models.py
│   └── evaluate.py
└── kaggle_evaluation/           # REQUIRED: Competition framework
    ├── __init__.py
    ├── default_inference_server.py
    ├── default_gateway.py
    └── core/
        └── ... (all files)
```

## Important Notes

### 1. Model File Size
- Kaggle has file size limits
- If your model is too large, consider:
  - Using a smaller model
  - Compressing the model
  - Using model quantization

### 2. Dependencies
Kaggle should have most packages pre-installed, but if you need custom packages, you can:
- Add a `requirements.txt` file
- Or install in your notebook/code

### 3. Model Path
Make sure the model path in `inference_server.py` matches where you place the model:
```python
# Default: looks for models/model_{model_type}.pkl
# Make sure this path exists in your submission
```

### 4. Testing
**Always test locally first!** Use:
```bash
python3 inference_server.py
```

## Quick Checklist

Before submitting, verify:

- [ ] `inference_server.py` exists and runs
- [ ] Trained model file exists in `models/` directory
- [ ] All `src/` files are included
- [ ] `kaggle_evaluation/` directory is included
- [ ] Code runs locally without errors
- [ ] Model can be loaded successfully
- [ ] Predictions are generated correctly

## Example Submission Script

Create a script to prepare your submission:

```bash
#!/bin/bash
# prepare_submission.sh

# Create submission directory
mkdir -p submission

# Copy required files
cp inference_server.py submission/
cp -r models submission/
cp -r src submission/
cp -r kaggle_evaluation submission/

# Create zip file
cd submission
zip -r ../submission.zip .
cd ..

echo "Submission package created: submission.zip"
```

## Troubleshooting

### "Model not found" error
- Check that model file is in `models/` directory
- Verify model filename matches what's expected
- Check file permissions

### Import errors
- Make sure all `src/` files are included
- Verify `kaggle_evaluation/` is complete
- Check that all dependencies are available

### Timeout errors
- Optimize your `predict` function
- Use faster models
- Pre-compute heavy operations

## Final Steps

1. **Train your best model**
2. **Test locally** - Make sure everything works
3. **Package files** - Create submission package
4. **Upload to Kaggle** - Submit via Kaggle interface
5. **Monitor** - Check for any errors in submission

Good luck with your submission! 🚀

