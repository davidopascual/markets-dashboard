#!/bin/bash

# Build standalone executable for Daily Markets Dashboard
# Requires PyInstaller: pip install pyinstaller

echo "=========================================="
echo "Building Daily Markets Dashboard"
echo "=========================================="
echo ""

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "Installing PyInstaller..."
    python3 -m pip install PyInstaller --quiet
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist *.spec

# Build executable
echo "Building executable..."
python3 -m PyInstaller \
    --onefile \
    --windowed \
    --name "MarketsDashboard" \
    --icon assets/icon.ico 2>/dev/null || \
    python3 -m PyInstaller \
    --onefile \
    --windowed \
    --name "MarketsDashboard" \
    src/main.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Build successful!"
    echo "=========================================="
    echo ""
    echo "Executable location:"
    echo "  dist/MarketsDashboard"
    echo ""
    echo "To run:"
    echo "  ./dist/MarketsDashboard"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "✗ Build failed"
    echo "=========================================="
    echo ""
    echo "Make sure you have PyInstaller installed:"
    echo "  python3 -m pip install PyInstaller"
    exit 1
fi
