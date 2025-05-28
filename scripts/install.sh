#!/bin/bash

echo "Installing project dependencies..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg is not installed"
    echo "Install it with:"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo "  Windows: https://ffmpeg.org/download.html"
fi

echo "Installation completed!"
echo "To activate the virtual environment: source venv/bin/activate"
