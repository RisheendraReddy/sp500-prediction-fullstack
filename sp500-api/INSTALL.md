# Installation Guide

## macOS/Linux

On macOS and Linux, Python 3 is typically installed as `python3`:

```bash
# Check Python version
python3 --version

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Windows

On Windows, you may use `python` or `py`:

```bash
# Check Python version
python --version
# or
py --version

# Create virtual environment
python -m venv venv
# or
py -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Troubleshooting

### "command not found: python"

**On macOS/Linux:**
- Use `python3` instead of `python`
- Install Python 3 if not available: `brew install python3` (macOS)

**On Windows:**
- Use `py` command: `py -m venv venv`
- Or install Python from python.org

### "command not found: pip"

**On macOS/Linux:**
- Use `pip3` instead of `pip`
- Or use: `python3 -m pip install -r requirements.txt`

**On Windows:**
- Use: `python -m pip install -r requirements.txt`
- Or: `py -m pip install -r requirements.txt`

## Verify Installation

```bash
# Check Python
python3 --version  # Should show Python 3.8+

# Check pip
pip3 --version  # Should show pip version

# Check virtual environment
which python3  # Should point to venv/bin/python3
```

## Quick Setup Script

For macOS/Linux, you can use:

```bash
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Setup complete! Activate with: source venv/bin/activate"
```

Save as `setup.sh` and run: `chmod +x setup.sh && ./setup.sh`

