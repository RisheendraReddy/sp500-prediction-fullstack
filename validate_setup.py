"""
Simple validation script to check if the project setup is correct.
This script checks imports and basic functionality without requiring data files.
"""
import sys
from pathlib import Path

def check_imports():
    """Check if all required modules can be imported."""
    print("Checking imports...")
    try:
        from src import data_loader, models, evaluate
        print("✓ All source modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def check_structure():
    """Check if project structure is correct."""
    print("\nChecking project structure...")
    required_dirs = ['src', 'data', 'models', 'notebooks']
    required_files = [
        'src/__init__.py',
        'src/data_loader.py',
        'src/models.py',
        'src/evaluate.py',
        'train.py',
        'predict.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_good = True
    base_path = Path(__file__).parent
    
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"✓ Directory '{dir_name}' exists")
        else:
            print(f"✗ Directory '{dir_name}' missing")
            all_good = False
    
    for file_name in required_files:
        file_path = base_path / file_name
        if file_path.exists() and file_path.is_file():
            print(f"✓ File '{file_name}' exists")
        else:
            print(f"✗ File '{file_name}' missing")
            all_good = False
    
    return all_good

def check_model_initialization():
    """Check if models can be initialized."""
    print("\nChecking model initialization...")
    try:
        from src.models import BaselineModel
        
        # Test each model type
        for model_type in ['lightgbm', 'xgboost', 'rf', 'gbm']:
            try:
                model = BaselineModel(model_type)
                print(f"✓ {model_type} model initialized")
            except Exception as e:
                print(f"✗ {model_type} model failed: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Model initialization check failed: {e}")
        return False

def main():
    """Run all validation checks."""
    print("=" * 50)
    print("Project Setup Validation")
    print("=" * 50)
    
    structure_ok = check_structure()
    imports_ok = check_imports()
    models_ok = check_model_initialization()
    
    print("\n" + "=" * 50)
    if structure_ok and imports_ok and models_ok:
        print("✓ All checks passed! Project setup looks good.")
        print("\nNote: This script doesn't check for data files.")
        print("Make sure to place train.csv and test.csv in the data/ directory.")
        return 0
    else:
        print("✗ Some checks failed. Please review the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

