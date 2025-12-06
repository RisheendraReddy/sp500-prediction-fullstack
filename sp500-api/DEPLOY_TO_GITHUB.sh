#!/bin/bash
# Quick script to deploy to GitHub

echo "🚀 Deploying S&P 500 API to GitHub..."

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

# Add all files
echo "Adding files..."
git add .

# Commit
echo "Committing changes..."
git commit -m "Initial commit: S&P 500 Returns Prediction API"

# Add remote (update if exists)
echo "Setting up remote..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/RisheendraReddy/sp500-prediction-api.git

# Create main branch
git branch -M main

# Push to GitHub
echo "Pushing to GitHub..."
echo ""
echo "⚠️  Make sure you've created the repository on GitHub first!"
echo "   Go to: https://github.com/new"
echo "   Repository name: sp500-prediction-api"
echo "   Then press Enter to continue..."
read

git push -u origin main

echo ""
echo "✅ Done! Your repository is at:"
echo "   https://github.com/RisheendraReddy/sp500-prediction-api"

