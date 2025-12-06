#!/bin/bash

echo "🚀 Quick Upload to GitHub"
echo ""

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: S&P 500 Returns Prediction Full Stack Application"
fi

# Add remote
REPO_NAME="sp500-prediction-fullstack"
if git remote | grep -q "origin"; then
    git remote remove origin
fi
git remote add origin https://github.com/RisheendraReddy/${REPO_NAME}.git
git branch -M main

echo ""
echo "⚠️  IMPORTANT: Create the repository on GitHub first!"
echo "   Go to: https://github.com/new"
echo "   Repository name: ${REPO_NAME}"
echo "   Then press Enter to continue..."
read

# Push
echo "⬆️  Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Repository: https://github.com/RisheendraReddy/${REPO_NAME}"
else
    echo ""
    echo "❌ Push failed. Check authentication and repository exists."
fi

