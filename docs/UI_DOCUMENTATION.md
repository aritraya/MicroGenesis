# MicroGenesis UI Documentation

## Overview

MicroGenesis provides a modern web-based UI built with Streamlit that makes it easy to generate, configure, and manage microservice projects without having to use the command line interface.

## Features

- **Project Generator**: Visually configure and generate microservice projects
- **Entity Designer**: Create and manage data models visually
- **Relationship Mapper**: Define relationships between entities
- **DDL Import**: Import database schemas from SQL files
- **Settings Management**: Configure application preferences

## Running the UI

### Using Setup Script (Recommended)

The easiest way to run the UI is using the provided setup script:

```powershell
# Navigate to the MicroGenesis directory
cd F:\MicroGenesis

# Run the setup script with the --run flag
python setup_ui.py --run
```

This will:
1. Create a virtual environment if needed
2. Install required dependencies
3. Start the Streamlit server

### Manual Setup

If you prefer to set up manually:

```powershell
# Navigate to the MicroGenesis directory
cd F:\MicroGenesis

# Create a virtual environment
python -m venv venv

# Activate the environment
.\venv\Scripts\Activate

# Install dependencies
pip install -e .
pip install streamlit>=1.27.0

# Run the UI
python run_ui.py
```

### Development Mode

For development with hot-reloading:

```powershell
cd F:\MicroGenesis
streamlit run src\ui\app.py
```

## UI Navigation

Once the UI is running, you'll see:

1. **Home Page**: Overview of features and recent projects
2. **Project Generator**: Configure and generate projects
3. **Entity Designer**: Design data models
4. **Settings**: Configure application preferences

## Generating Your First Project

1. Click on the "Project Generator" in the sidebar
2. Fill in the project details:
   - Project name
   - Base package
   - Framework (Spring Boot, Micronaut, GraphQL)
   - Language (Java, Kotlin)
   - Build system (Maven, Gradle)
3. Configure architecture style
4. Add entities (optional)
5. Click "Generate Project"

## Designing Entities

1. Navigate to "Entity Designer" in the sidebar
2. Create entities manually or import from DDL
3. Define fields with types and constraints
4. Create relationships between entities

## Customization

The UI settings page allows you to customize:

- Default output directory
- Author information
- Custom template directories
- Debug settings

## Requirements

- Python 3.8+
- Streamlit 1.27+
- Modern web browser

## Troubleshooting

If you encounter issues:

1. Check that you're running the latest version of Python
2. Ensure all dependencies are installed
3. Verify that the MicroGenesis core is properly installed
4. Check the browser console for errors

For additional help, please check the GitHub repository or submit an issue.
