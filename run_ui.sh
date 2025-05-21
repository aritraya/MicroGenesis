#!/bin/bash
# MicroGenesis UI Launcher
# This script launches the MicroGenesis UI with Streamlit

echo "Starting MicroGenesis UI..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -e .
    pip install streamlit>=1.27.0
else
    source venv/bin/activate
fi

# Run the UI
python run_ui.py "$@"
