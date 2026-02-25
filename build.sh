#!/bin/bash

# Build macOS .app for Daily Markets Dashboard

echo "=========================================="
echo "Building Daily Markets Dashboard (.app)"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# Use venv python if available
if [ -f "venv/bin/python3" ]; then
    PYTHON="venv/bin/python3"
else
    PYTHON="python3"
fi

# Ensure PyInstaller is installed
if ! $PYTHON -c "import PyInstaller" 2>/dev/null; then
    echo "Installing PyInstaller..."
    $PYTHON -m pip install PyInstaller --quiet
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist *.spec

# Build .app bundle
echo "Building macOS app..."
$PYTHON -m PyInstaller \
    --onedir \
    --windowed \
    --name "Markets Dashboard" \
    --icon assets/icon.icns \
    --add-data "src:src" \
    --add-data ".env:.env_data" \
    --hidden-import tkinter \
    --hidden-import yfinance \
    --hidden-import requests \
    --hidden-import pandas \
    --hidden-import dotenv \
    --hidden-import feedparser \
    --hidden-import bs4 \
    --hidden-import plyer \
    --osx-bundle-identifier com.davidpascual.marketsdashboard \
    src/main.py

if [ $? -eq 0 ]; then
    # Copy .env into the app bundle
    if [ -f ".env" ]; then
        cp .env "dist/Markets Dashboard.app/Contents/Resources/.env"
    fi

    echo ""
    echo "=========================================="
    echo "Build successful!"
    echo "=========================================="
    echo ""
    echo "App location:"
    echo "  dist/Markets Dashboard.app"
    echo ""
    echo "To install, run:"
    echo "  cp -r \"dist/Markets Dashboard.app\" /Applications/"
    echo ""
    echo "Then find 'Markets Dashboard' in Launchpad or Spotlight."
    echo ""
else
    echo ""
    echo "Build failed!"
    echo "Make sure dependencies are installed: pip install -r requirements.txt"
    exit 1
fi
