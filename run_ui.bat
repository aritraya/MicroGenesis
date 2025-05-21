@echo off
REM MicroGenesis UI Launcher
REM This script launches the MicroGenesis UI with Streamlit

echo Starting MicroGenesis UI...

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -e .
    pip install streamlit>=1.27.0
) else (
    call venv\Scripts\activate.bat
)

REM Run the UI
python run_ui.py

REM Keep the console window open if there was an error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred while running the UI.
    echo Press any key to exit...
    pause > nul
)
