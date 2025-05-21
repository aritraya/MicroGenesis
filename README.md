# MicroGenesis

MicroGenesis is a powerful code scaffolding tool that generates application code based on user specifications. It allows users to quickly generate project structures for various frameworks like Spring Boot, Micronaut, and GraphQL with customizable configurations.

![MicroGenesis UI](https://via.placeholder.com/800x450.png?text=MicroGenesis+UI)

## Features

### Modern Streamlit UI
- Graphical interface for configuring and generating projects
- Visual entity designer for data modeling
- Drag-and-drop relationship mapping
- DDL import for database schemas
- Project history and quick access to recent projects

- Generate project structures for Spring Boot, Micronaut, and GraphQL (Java/Kotlin)
- Support for multiple languages (Java, Kotlin) across all frameworks
- Build system configuration (Maven, Gradle)
- CI/CD pipeline setup (GitHub Actions, Jenkins, Azure DevOps, GitLab CI)
- Database integration (MySQL, PostgreSQL, H2, MongoDB)
- Schema relationship mapping with advanced entity relationships
- Additional features like logging, Swagger/OpenAPI, AWS integration, etc.
- Generate code from OpenAPI/Swagger definitions
- Support for different architectural styles (Domain-Driven Design, Entity-Driven)
- Customizable templates for all code generation needs

## Installation

```bash
# Install the package
pip install -e .

# Install UI dependencies
pip install streamlit>=1.27.0
```

## Usage

### Graphical UI (Recommended)

The fastest way to get started is using the graphical UI:

```powershell
# On Windows, simply run:
.\run_ui.bat

# Alternatively:
python setup_ui.py --run
```

This will open the MicroGenesis UI in your default browser. See [UI Documentation](docs/UI_DOCUMENTATION.md) for details.

### Interactive Mode (Command Line)

```bash
python -m microgenesis.main --interactive
```

### Command Line Mode

```bash
python -m microgenesis.main \
    --project-name MyProject \
    --base-package com.example.myproject \
    --framework spring-boot \
    --framework-version 2.7.0 \
    --language java \
    --language-version 17 \
    --build-system maven \
    --pipeline github-actions \
    --database mysql \
    --features logging swagger \
    --service-type domain-driven \
    --output-dir ./output
```

### Configuration File Mode

Create a JSON configuration file:

```json
{
  "project_name": "MyProject",
  "base_package": "com.example.myproject",
  "description": "My awesome project",
  "framework": {
    "name": "spring-boot",
    "version": "2.7.0"
  },
  "language": {
    "name": "java",
    "version": "17"
  },
  "build_system": {
    "name": "maven"
  },
  "pipeline": {
    "name": "github-actions"
  },
  "database": {
    "name": "mysql"
  },
  "features": ["logging", "swagger", "data"],
  "service_type": "domain-driven",
  "output_dir": "./output"
}
```

Then run:

```bash
python -m microgenesis.main --config-file my_config.json
```

## Development

### Setup Development Environment

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
python tests/run_tests.py
```

## Supported Implementations

| Framework   | Java | Kotlin |
|-------------|------|--------|
| Spring Boot | ✅    | ✅      |
| Micronaut   | ✅    | ✅      |
| GraphQL     | ✅    | ✅      |

### Architecture Patterns

| Pattern Type        | Support |
|---------------------|---------|
| Domain-Driven       | ✅       |
| Entity-Driven       | ✅       |
| Technical-Layered   | ✅       |
| Data-Driven         | ✅       |
| Function-Oriented   | ✅       |

For more details on specific architectures, see:
- [Domain-Driven Architecture](docs/DOMAIN_DRIVEN_ARCHITECTURE.md)
- [Entity-Driven Architecture](docs/ENTITY_DRIVEN_ARCHITECTURE.md) 
- [Technical-Layered Architecture](docs/TECHNICAL_LAYERED_ARCHITECTURE.md)
- [GraphQL Kotlin Architecture](docs/GRAPHQL_KOTLIN_ARCHITECTURE.md)

## Extending MicroGenesis

MicroGenesis is designed to be extensible. You can add new generators for different frameworks, languages, or customize the templates to fit your needs.