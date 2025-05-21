"""
MicroGenesis UI Runner

This script runs the Streamlit UI for MicroGenesis.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_ui():
    """Run the Streamlit UI for MicroGenesis."""
    # Ensure the current directory is in the Python path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.append(script_dir)

    # Get the path to the UI main app
    ui_module_path = os.path.join(script_dir, "streamlit_app.py")
    
    if not os.path.exists(ui_module_path):
        print(f"Error: UI module not found at {ui_module_path}")
        return 1
    
    try:
        print("Starting MicroGenesis UI...")
        subprocess.run(
            ["streamlit", "run", ui_module_path, "--server.headless", "true"],
            check=True
        )
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
        return e.returncode
    except KeyboardInterrupt:
        print("\nUI shutdown requested. Exiting...")
        return 0

if __name__ == "__main__":
    sys.exit(run_ui())
