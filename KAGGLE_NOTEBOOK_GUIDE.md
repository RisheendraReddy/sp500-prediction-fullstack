# Kaggle Notebook Submission Guide

## Overview

This guide explains how to create and submit a Kaggle notebook for the S&P 500 Returns Prediction competition.

## Step 1: Create the Notebook

I've created `inference_server.ipynb` for you. This notebook contains all the code needed for the evaluation API.

## Step 2: Prepare Your Model

### Option A: Upload Model as Dataset (Recommended)

1. **Create a dataset on Kaggle:**
   - Go to Kaggle → Datasets → New Dataset
   - Upload your `models/model_lightgbm.pkl` file
   - Name it something like "sp500-prediction-model"
   - Make it public or private (your choice)

2. **Add dataset to notebook:**
   - In your notebook, click "Add Data" (top right)
   - Search for your dataset
   - Click "Add"

3. **Update the model path in the notebook:**
   - Find the `load_model` function
   - Update the path to: `/kaggle/input/your-dataset-name/models/model_lightgbm.pkl`

### Option B: Include Model in Notebook Output

1. Train your model locally
2. Upload the model file directly to the notebook
3. Update paths accordingly

## Step 3: Include Source Code

You have two options:

### Option A: Upload src/ as Dataset (Recommended)

1. **Create a dataset with your src/ directory:**
   - Zip your `src/` folder
   - Upload as a Kaggle dataset
   - Add to your notebook

2. **Uncomment the path addition in the notebook:**
   ```python
   sys.path.insert(0, '/kaggle/input/your-src-dataset/src')
   ```

### Option B: Copy Functions Directly

The notebook already includes the essential functions (`get_feature_columns`, `prepare_features`, etc.) directly in the cells. You can use these or import from your src/ dataset.

## Step 4: Configure the Notebook

### Update Model Path

In the `load_model` function, update the paths to match where your model is located:

```python
possible_paths = [
    Path('/kaggle/input/your-model-dataset/models/model_lightgbm.pkl'),
    Path('/kaggle/working/models/model_lightgbm.pkl'),
    # ... etc
]
```

### Update Dataset Names

Replace `your-model-dataset` and `your-src-dataset` with your actual dataset names.

## Step 5: Test Locally (Optional)

Before submitting, you can test the notebook:

1. Download the notebook
2. Run it locally with test data
3. Verify it works correctly

## Step 6: Submit to Kaggle

1. **Save the notebook:**
   - Click "Save Version" in Kaggle
   - Choose "Save & Run All"
   - Wait for it to complete

2. **Submit for evaluation:**
   - Go to the competition page
   - Click "Submit Predictions"
   - Select your notebook
   - Click "Submit"

## Important Notes

### File Structure in Kaggle

When you add datasets, the structure will be:
```
/kaggle/input/
├── hull-tactical-market-prediction/  (competition data)
│   ├── train.csv
│   └── test.csv
├── your-model-dataset/               (your model)
│   └── models/
│       └── model_lightgbm.pkl
└── your-src-dataset/                 (your source code, optional)
    └── src/
        ├── __init__.py
        ├── data_loader.py
        ├── models.py
        └── evaluate.py
```

### Dependencies

The notebook includes a cell to install dependencies:
```python
!pip install -q polars grpcio protobuf
```

Kaggle should have most packages pre-installed, but this ensures everything is available.

### Time Limits

- **Startup**: 15 minutes (server must start)
- **Per batch**: 5 minutes (each prediction batch)
- **First call**: Can take longer (model loading)

The notebook uses lazy loading to stay within these limits.

## Troubleshooting

### Model Not Found

**Error**: `FileNotFoundError: No trained model found`

**Solution**:
- Verify your model dataset is added to the notebook
- Check the path in `load_model` function
- Ensure the model file name matches

### Import Errors

**Error**: `ModuleNotFoundError`

**Solution**:
- Run the pip install cell
- Verify all datasets are added
- Check that src/ path is correct if using Option A

### Timeout Errors

**Error**: `GRPC_DEADLINE_EXCEEDED`

**Solution**:
- Optimize your predict function
- Use faster models
- Pre-compute heavy operations

## Quick Checklist

Before submitting:

- [ ] Model dataset is uploaded and added to notebook
- [ ] Model path is updated in `load_model` function
- [ ] Source code is included (either as dataset or in cells)
- [ ] All cells run successfully
- [ ] Notebook is saved with "Save & Run All"
- [ ] No errors in the notebook output

## Example Workflow

1. **Train model locally:**
   ```bash
   python3 train.py --model-type lightgbm
   ```

2. **Upload model to Kaggle:**
   - Create dataset with `models/model_lightgbm.pkl`
   - Note the dataset name

3. **Create notebook:**
   - Use `inference_server.ipynb` as template
   - Update model path with your dataset name
   - Add the model dataset to notebook

4. **Test:**
   - Run all cells
   - Verify no errors

5. **Submit:**
   - Save version
   - Submit for evaluation

## Alternative: Simplified Notebook

If you want a simpler version without separate datasets, you can:

1. Copy all code directly into notebook cells
2. Upload model file directly to notebook
3. Use relative paths

The provided notebook is flexible and supports both approaches.

Good luck with your submission! 🚀

