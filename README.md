# MicroGenesis

MicroGenesis is a powerful code scaffolding tool that generates application code based on user specifications. It allows users to quickly generate project structures for various frameworks like Spring Boot, Micronaut, and GraphQL with customizable configurations.

## Features

- Generate project structures for Spring Boot, Micronaut, and GraphQL
- Support for multiple languages (Java, Kotlin)
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
pip install -e .
```

## Usage

### Interactive Mode

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

## Extending MicroGenesis

MicroGenesis is designed to be extensible. You can add new generators for different frameworks, languages, or customize the templates to fit your needs.