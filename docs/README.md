# MicroGenesis Documentation

This directory contains the project documentation.

## Building the Documentation

To build the documentation:

1. Install documentation dependencies:
   ```
   pip install -r requirements-dev.txt
   ```

2. Build the documentation:
   ```
   cd docs
   sphinx-quickstart  # Only the first time
   make html
   ```

3. View the documentation in your browser:
   ```
   open _build/html/index.html
   ```
