"""
Check if all required dependencies are installed.
"""
import sys

def check_package(package_name, import_name=None, min_version=None):
    """Check if a package is installed and optionally verify version."""
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        
        if min_version:
            # Simple version comparison (basic check)
            try:
                from packaging import version as pkg_version
                if pkg_version.parse(version) >= pkg_version.parse(min_version):
                    status = "✓"
                else:
                    status = "⚠"
                    version += f" (required: >={min_version})"
            except:
                status = "✓"
                version += f" (version check skipped)"
        else:
            status = "✓"
        
        print(f"{status} {package_name:20s} - {version}")
        return True
    except ImportError:
        print(f"✗ {package_name:20s} - NOT INSTALLED")
        return False

def main():
    """Check all required dependencies."""
    print("=" * 60)
    print("Dependency Check")
    print("=" * 60)
    print()
    
    required_packages = [
        ('pandas', 'pandas', '1.5.0'),
        ('numpy', 'numpy', '1.23.0'),
        ('scikit-learn', 'sklearn', '1.2.0'),
        ('xgboost', 'xgboost', '1.7.0'),
        ('lightgbm', 'lightgbm', '3.3.0'),
        ('joblib', 'joblib', '1.2.0'),
    ]
    
    results = []
    for package_name, import_name, min_version in required_packages:
        installed = check_package(package_name, import_name, min_version)
        results.append(installed)
    
    print()
    print("=" * 60)
    
    if all(results):
        print("✓ All dependencies are installed!")
        return 0
    else:
        missing = [pkg[0] for pkg, installed in zip(required_packages, results) if not installed]
        print(f"✗ Missing dependencies: {', '.join(missing)}")
        print()
        print("To install missing dependencies, run:")
        print("  pip install -r requirements.txt")
        print("  or")
        print("  pip3 install -r requirements.txt")
        return 1

if __name__ == '__main__':
    sys.exit(main())

