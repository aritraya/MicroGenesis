"""
MicroGenesis Streamlit Application Entry Point

This script serves as the entry point for the Streamlit-based UI of MicroGenesis.
"""

import os
import sys
import streamlit as st

# Ensure the project root is in the path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

# Import and run the UI main module
from src.ui.ui_main import *

# The UI is already rendered by importing the ui_main module
