# Submission Checklist

## Quick Reference: What to Submit to Kaggle

### ✅ Required Files

1. **`inference_server.py`** - Main entry point with `predict` function
2. **`models/model_*.pkl`** - Your trained model file
3. **`src/`** - All source code files
4. **`kaggle_evaluation/`** - Competition evaluation framework

### 📦 Submission Format

**Option 1: Kaggle Notebook** (Recommended for beginners)
- Create a `.ipynb` notebook
- Paste code from `inference_server.py`
- Upload model and dependencies as dataset or include in notebook

**Option 2: Code Files** (Recommended for advanced users)
- Create a zip file with all required files
- Upload to Kaggle
- Use the submission script: `./prepare_submission.sh`

### 🔍 Pre-Submission Checklist

- [ ] Model is trained and saved: `models/model_lightgbm.pkl`
- [ ] `inference_server.py` runs locally without errors
- [ ] All files are included in submission package
- [ ] Model path is correct in `inference_server.py`
- [ ] Tested locally with: `python3 inference_server.py`

### 📝 Step-by-Step

1. **Train Model**
   ```bash
   python3 train.py --model-type lightgbm
   ```

2. **Test Locally**
   ```bash
   python3 inference_server.py
   ```

3. **Prepare Submission**
   ```bash
   ./prepare_submission.sh
   ```

4. **Upload to Kaggle**
   - Go to competition page
   - Click "Submit Predictions"
   - Upload `submission.zip` or notebook

### ⚠️ Common Mistakes to Avoid

- ❌ Forgetting to include the model file
- ❌ Missing `src/` or `kaggle_evaluation/` directories
- ❌ Wrong model path in code
- ❌ Not testing locally first
- ❌ Model file too large (check Kaggle limits)

### 📊 File Sizes

- Model file: Usually 1-100 MB
- Source code: < 1 MB
- Total submission: Check Kaggle's limits (usually 500 MB - 1 GB)

### 🚀 Ready to Submit?

Run the preparation script and upload the resulting zip file to Kaggle!

```bash
./prepare_submission.sh
# Then upload submission.zip to Kaggle
```

