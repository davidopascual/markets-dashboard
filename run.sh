#!/bin/bash

# Daily Markets Dashboard - Quick Start Script

echo "=========================================="
echo "Daily Markets Dashboard"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if dependencies are installed
echo "Checking dependencies..."
python3 -c "import tkinter; import yfinance; import requests; import pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing dependencies..."
    python3 -m pip install -r requirements.txt --quiet
    if [ $? -eq 0 ]; then
        echo "✓ Dependencies installed successfully"
    else
        echo "❌ Failed to install dependencies"
        echo "Try running: python3 -m pip install -r requirements.txt"
        exit 1
    fi
else
    echo "✓ All dependencies are installed"
fi

echo ""
echo "Starting Daily Markets Dashboard..."
echo "=========================================="
echo ""

# Launch the application
python3 src/main.py

exit $?
