#!/bin/bash
# Script to prepare Kaggle submission package

echo "Preparing Kaggle submission package..."

# Create submission directory
mkdir -p submission
rm -rf submission/*

# Copy required files
echo "Copying inference server..."
cp inference_server.py submission/

echo "Copying models..."
mkdir -p submission/models
cp -r models/*.pkl submission/models/ 2>/dev/null || echo "Warning: No model files found. Train a model first!"

echo "Copying source code..."
cp -r src submission/

echo "Copying Kaggle evaluation framework..."
cp -r kaggle_evaluation submission/

# Create requirements.txt for submission (optional)
echo "Creating requirements.txt..."
cat > submission/requirements.txt << EOF
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.2.0
xgboost>=1.7.0
lightgbm>=3.3.0
joblib>=1.2.0
polars>=0.19.0
grpcio>=1.50.0
protobuf>=4.0.0
EOF

# Create zip file
echo "Creating zip file..."
cd submission
zip -r ../submission.zip . -q
cd ..

echo ""
echo "✓ Submission package created: submission.zip"
echo ""
echo "Files included:"
ls -lh submission.zip
echo ""
echo "Contents:"
unzip -l submission.zip | head -20
echo ""
echo "Next steps:"
echo "1. Verify the package contains all required files"
echo "2. Test locally: python3 inference_server.py"
echo "3. Upload submission.zip to Kaggle"

