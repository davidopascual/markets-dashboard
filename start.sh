#!/bin/bash

# Daily Markets Dashboard - Start Script
# Suppresses deprecation warnings and launches the app

# Activate virtual environment
source venv/bin/activate

# Suppress Tk deprecation warning on macOS
export TK_SILENCE_DEPRECATION=1

# Launch the application
python3 src/main.py
