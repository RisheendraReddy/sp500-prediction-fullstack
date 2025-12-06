# How to Train Your Model

## The Problem

You don't have `model_lightgbm.pkl` yet because you haven't trained a model!

## Solution: Train a Model First

### Step 1: Get the Training Data

You need `train.csv` in your `data/` directory. 

**Option A: If you have the data in the hull-tactical-market-prediction folder:**

```bash
# Copy the data files
cp hull-tactical-market-prediction/train.csv data/
cp hull-tactical-market-prediction/test.csv data/
```

**Option B: Download from Kaggle:**

1. Go to the competition page on Kaggle
2. Download `train.csv` and `test.csv`
3. Place them in the `data/` directory

### Step 2: Train the Model

Once you have `train.csv` in the `data/` directory, run:

```bash
python3 train.py --model-type lightgbm
```

This will:
- Load the training data
- Train a LightGBM model
- Save it as `models/model_lightgbm.pkl`

### Step 3: Verify the Model Was Created

Check that the file exists:

```bash
ls -lh models/model_lightgbm.pkl
```

You should see the file with a size (usually a few MB to tens of MB).

## Quick Start Commands

```bash
# 1. Copy data (if you have it in hull-tactical-market-prediction folder)
cp hull-tactical-market-prediction/train.csv data/
cp hull-tactical-market-prediction/test.csv data/

# 2. Train the model
python3 train.py --model-type lightgbm

# 3. Verify it was created
ls models/
```

## What Happens When You Train

The training script will:
1. Load `data/train.csv`
2. Split it into train/validation sets
3. Prepare features
4. Train a LightGBM model
5. Evaluate on validation set
6. **Save the model to `models/model_lightgbm.pkl`** ← This is what you need!

## After Training

Once you have `models/model_lightgbm.pkl`, you can:
1. Upload it to Kaggle as a dataset
2. Use it in your notebook
3. Make predictions

## Troubleshooting

### "FileNotFoundError: Training data not found"
- Make sure `train.csv` is in the `data/` directory
- Check the file path: `data/train.csv`

### "No module named 'lightgbm'"
- Install dependencies: `pip install -r requirements.txt`

### Model file is very small (< 1 MB)
- This might indicate an error during training
- Check the training output for errors
- Try training again

## Next Steps After Training

1. ✅ Train model: `python3 train.py --model-type lightgbm`
2. ✅ Verify: `ls models/model_lightgbm.pkl`
3. ✅ Upload to Kaggle as dataset
4. ✅ Use in your notebook

