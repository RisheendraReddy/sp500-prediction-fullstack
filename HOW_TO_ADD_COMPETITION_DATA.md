# How to Add Competition Data to Your Kaggle Notebook

## Where to Add: In Your Kaggle Notebook

The `hull-tactical-market-prediction` dataset is the **competition's test data**. You need to add it to your notebook so the evaluation API can access it.

## Step-by-Step Instructions

### 1. Open Your Notebook on Kaggle
- Go to your notebook on Kaggle (the one with `inference_server.ipynb`)

### 2. Click "Add Data" Button
- Look for the **"Add Data"** button in the top right corner of your notebook
- It's usually next to the "Save Version" button
- Click it

### 3. Search for the Competition Dataset
- In the search box, type: `hull-tactical-market-prediction`
- Or search for: `hull tactical market prediction`
- You should see the official competition dataset

### 4. Add the Dataset
- Click on the competition dataset
- Click the **"Add"** button
- The dataset will be added to your notebook

### 5. Verify It's Added
- You should see the dataset listed in the "Data" section (usually on the right side)
- The path will be: `/kaggle/input/hull-tactical-market-prediction/`

## Visual Guide

```
┌─────────────────────────────────────────┐
│  Your Notebook                          │
│                                         │
│  [Code cells...]                        │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Data                            │   │
│  │  ┌───────────────────────────┐   │   │
│  │  │ sp500-lightgbm-mode       │   │   │ ← Your model
│  │  └───────────────────────────┘   │   │
│  │  ┌───────────────────────────┐   │   │
│  │  │ hull-tactical-market-     │   │   │ ← Competition data
│  │  │ prediction                │   │   │
│  │  └───────────────────────────┘   │   │
│  └─────────────────────────────────┘   │
│                                         │
│  [Add Data] ← Click here to add        │
└─────────────────────────────────────────┘
```

## What's in the Competition Dataset?

The `hull-tactical-market-prediction` dataset contains:
- `test.csv` - The test data that will be used for evaluation
- `train.csv` - Training data (for reference)
- `kaggle_evaluation/` - Evaluation API framework

## Why You Need It

Your notebook's inference server needs access to:
1. **Your model** (`sp500-lightgbm-mode`) - To make predictions
2. **Competition data** (`hull-tactical-market-prediction`) - To get test data batches

## After Adding

Once you add both datasets, your notebook will have access to:
- `/kaggle/input/sp500-lightgbm-mode/model_lightgbm.pkl` (your model)
- `/kaggle/input/hull-tactical-market-prediction/test.csv` (test data)

## Quick Checklist

- [ ] Open your notebook on Kaggle
- [ ] Click "Add Data" button (top right)
- [ ] Search for "hull-tactical-market-prediction"
- [ ] Click "Add"
- [ ] Verify it appears in the Data section
- [ ] Both datasets should now be listed:
  - [x] sp500-lightgbm-mode (your model)
  - [x] hull-tactical-market-prediction (competition data)

## Troubleshooting

### Can't Find the Dataset?
- Make sure you're searching in the correct competition
- Try searching for just "hull tactical"
- Check if you're in the right competition page

### Dataset Already Added?
- If you see it in the Data section, you're good!
- No need to add it again

### Multiple Versions?
- Use the official competition dataset
- It should be from the competition organizers

## You're All Set!

Once both datasets are added, your notebook is ready to run! 🚀

