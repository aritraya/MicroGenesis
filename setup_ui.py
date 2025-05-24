"""
Setup script for installing dependencies and running the MicroGenesis UI.
"""

import os
import sys
import subprocess
import venv
import argparse
import platform

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="MicroGenesis UI Setup")
    parser.add_argument("--no-venv", action="store_true", help="Skip creating a virtual environment")
    parser.add_argument("--no-install", action="store_true", help="Skip installing dependencies")
    parser.add_argument("--run", action="store_true", help="Run the UI after setup")
    return parser.parse_args()

def create_virtual_environment(venv_dir):
    """Create a virtual environment."""
    print(f"Creating virtual environment in {venv_dir}...")
    venv.create(venv_dir, with_pip=True)
    return os.path.join(venv_dir, "Scripts" if platform.system() == "Windows" else "bin")

def install_dependencies(bin_dir):
    """Install required dependencies."""
    pip = os.path.join(bin_dir, "pip")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    req_ui_path = os.path.join(script_dir, "requirements-ui.txt")
    
    print("Installing required dependencies...")
    # Install the package itself
    subprocess.check_call([pip, "install", "-e", "."])
    
    # Install UI-specific requirements
    if os.path.exists(req_ui_path):
        print("Installing UI dependencies from requirements-ui.txt...")
        subprocess.check_call([pip, "install", "-r", req_ui_path])
    else:
        print("requirements-ui.txt not found, installing minimal UI dependencies...")
        subprocess.check_call([pip, "install", "streamlit>=1.27.0"])
    
    print("Dependencies installed successfully.")

def run_ui(bin_dir):
    """Run the UI."""
    python = os.path.join(bin_dir, "python")
    
    print("Starting MicroGenesis UI...")
    try:
        subprocess.check_call([python, "run_ui.py"])
    except KeyboardInterrupt:
        print("\nUI shutdown requested. Exiting...")

def main():
    """Main function."""
    args = parse_arguments()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(script_dir, "venv")
    
    if not args.no_venv and not os.path.exists(venv_dir):
        bin_dir = create_virtual_environment(venv_dir)
    else:
        bin_dir = os.path.join(venv_dir, "Scripts" if platform.system() == "Windows" else "bin")
    
    if not args.no_install:
        install_dependencies(bin_dir)
    
    if args.run:
        run_ui(bin_dir)
    else:
        print("\nSetup completed successfully.")
        print(f"\nTo activate the virtual environment, run:")
        if platform.system() == "Windows":
            print(f"    {os.path.join(venv_dir, 'Scripts', 'activate')}")
        else:
            print(f"    source {os.path.join(venv_dir, 'bin', 'activate')}")
        
        print("\nTo run the UI, execute:")
        print("    python run_ui.py")

if __name__ == "__main__":
    main()
