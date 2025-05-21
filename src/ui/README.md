# MicroGenesis UI

This directory contains the Streamlit-based User Interface for MicroGenesis, a powerful microservice generator for Java and Kotlin applications.

## Directory Structure

- `ui_main.py` - Main entry point for the Streamlit wizard-based UI
- `components/` - UI component files
  - `navigation.py` - Contains the render functions for each step of the wizard
- `state/` - State management files
  - `session_state.py` - Manages the application state and data persistence
- `data/` - Data definition files
  - `static_data.py` - Defines static data structures used throughout the UI
- `utils/` - Utility functions
  - `helpers.py` - Helper functions for UI components and actions
  - `core_integration.py` - Integration with the core functionality
- `styles/` - UI styling files
  - `css.py` - Custom CSS styling for the UI
- `static/` - Static resources like images and CSS

## Running the UI

To run the MicroGenesis UI, use the provided script at the project's root:

```bash
# On Windows
run_ui.bat

# On Linux/macOS
./run_ui.sh

# Or manually
cd /path/to/MicroGenesis
python run_ui.py
```

## UI Features

The UI follows a step-by-step wizard approach with four main steps:

### Step 1: Project Configuration
- Configure project name and package
- Select programming language (Java, Kotlin) and version
- Choose framework (Spring Boot, Micronaut, GraphQL)
- Select build tools (Maven, Gradle with DSL options)
- Configure database and CI/CD pipeline options
- Choose service architecture type (Domain-Driven, Entity-Driven, etc.)
- Select additional features

### Step 2: Entity Configuration
- Create and manage entities visually
- Define entity fields with types and properties
- Import entities from DDL scripts
- Configure relationships between entities

### Step 3: API Configuration
- Upload Swagger/OpenAPI specifications
- Configure API endpoints and operations

### Step 4: Generate Project
- Review project configuration summary
- Generate and download the complete project

## Integration with Core

The UI communicates with the MicroGenesis core through the `utils/core_integration.py` module, which provides the following functionality:

- Project generation via `generate_project_from_ui()`
- Configuration preparation via `prepare_config_from_ui()`
- Entity parsing from DDL via `parse_ddl_file()`
- Template and configuration handling

## Requirements

- Python 3.8 or higher
- Streamlit 1.27.0 or higher
- All MicroGenesis core dependencies
