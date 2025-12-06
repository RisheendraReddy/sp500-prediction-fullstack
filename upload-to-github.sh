#!/bin/bash

echo "🚀 Uploading S&P 500 Prediction Project to GitHub..."
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

# Add all files
echo "📦 Adding files..."
git add .

# Commit
echo "💾 Committing changes..."
git commit -m "Initial commit: S&P 500 Returns Prediction Full Stack Application

- Backend API with FastAPI
- React frontend with modern UI
- ML models (LightGBM, XGBoost, RF, GBM)
- Black & green theme
- Complete documentation"

# Check if remote exists
if git remote | grep -q "origin"; then
    echo "⚠️  Remote 'origin' already exists. Removing..."
    git remote remove origin
fi

# Add remote
echo "🔗 Setting up remote..."
REPO_NAME="sp500-prediction-fullstack"
git remote add origin https://github.com/RisheendraReddy/${REPO_NAME}.git

# Create main branch
git branch -M main

echo ""
echo "⚠️  IMPORTANT: Create the repository on GitHub first!"
echo "   Go to: https://github.com/new"
echo "   Repository name: ${REPO_NAME}"
echo "   Then press Enter to continue..."
read

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully uploaded to GitHub!"
    echo "   Repository: https://github.com/RisheendraReddy/${REPO_NAME}"
else
    echo ""
    echo "❌ Push failed. Make sure:"
    echo "   1. Repository exists on GitHub"
    echo "   2. You have push access"
    echo "   3. You're authenticated (use GitHub CLI or SSH keys)"
fi

