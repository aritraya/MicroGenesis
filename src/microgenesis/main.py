"""Main module for MicroGenesis application."""

import argparse
import json
import os
import sys
from typing import Dict, Any, List, Optional

from microgenesis.scaffolding import ScaffoldingEngine
from microgenesis.logging import get_logger
from microgenesis.config import Config

logger = get_logger()

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="MicroGenesis - Application Scaffolding Generator"
    )
    
    # Basic project info
    parser.add_argument(
        "--project-name",
        type=str,
        help="Name of the project"
    )
    
    parser.add_argument(
        "--base-package",
        type=str,
        help="Base package name (e.g., com.example.myapp)"
    )
    
    parser.add_argument(
        "--description",
        type=str,
        default="",
        help="Project description"
    )
    
    # Framework selection
    parser.add_argument(
        "--framework",
        type=str,
        choices=["spring-boot", "micronaut", "graphql"],
        help="Framework to use for the project"
    )
    
    parser.add_argument(
        "--framework-version",
        type=str,
        help="Version of the framework to use"
    )
    
    # Language selection
    parser.add_argument(
        "--language",
        type=str,
        choices=["java", "kotlin"],
        help="Programming language to use"
    )
    
    parser.add_argument(
        "--language-version",
        type=str,
        help="Version of the language to use"
    )
    
    # Build system
    parser.add_argument(
        "--build-system",
        type=str,
        choices=["maven", "gradle"],
        help="Build system to use"
    )
    
    # CI/CD pipeline
    parser.add_argument(
        "--pipeline",
        type=str,
        choices=["github-actions", "jenkins", "azure-devops", "gitlab-ci"],
        help="CI/CD pipeline to configure"
    )
    
    # Database
    parser.add_argument(
        "--database",
        type=str,
        choices=["mysql", "postgresql", "h2", "mongodb", "none"],
        help="Database to configure"
    )
    
    # Additional features
    parser.add_argument(
        "--features",
        type=str,
        nargs="+",
        choices=["logging", "swagger", "aws", "data", "config", "integration", "yaml-config", "generate-dtos"],
        help="Additional features to add"
    )
    
    # Service type
    parser.add_argument(
        "--service-type",
        type=str,
        choices=["domain-driven", "entity-driven"],
        help="Type of service architecture to generate"
    )
    
    # Swagger file
    parser.add_argument(
        "--swagger-file",
        type=str,
        help="Path to Swagger/OpenAPI definition file"
    )
    
    # Schema mapping file
    parser.add_argument(
        "--schema-mapping",
        type=str,
        help="Path to schema relationship mapping file"
    )
    
    # Output directory
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Directory where the generated code will be placed"
    )
    
    # Config file
    parser.add_argument(
        "--config-file",
        type=str,
        help="Path to JSON configuration file with all settings"
    )
    
    # Interactive mode
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode to prompt for all options"
    )
    
    parser.add_argument(
        "--version", 
        action="store_true",
        help="Show version information and exit"
    )
    
    return parser.parse_args()

def get_config_from_file(config_file: str) -> Dict[str, Any]:
    """Load configuration from a JSON file.
    
    Args:
        config_file: Path to the JSON configuration file
        
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading configuration file: {e}")
        return {}

def prompt_for_config() -> Dict[str, Any]:
    """Prompt the user for configuration options.
    
    Returns:
        Dict[str, Any]: Configuration dictionary based on user input
    """
    print("MicroGenesis - Application Scaffolding Generator")
    print("-----------------------------------------------")
    print("Please enter the following information:")
    
    config = {}
    
    # Basic project info
    config["project_name"] = input("Project Name: ")
    config["base_package"] = input("Base Package (e.g., com.example.myapp): ")
    config["description"] = input("Project Description (optional): ")
    
    # Framework selection
    framework_options = ["spring-boot", "micronaut", "graphql"]
    print("\nFramework options:")
    for i, option in enumerate(framework_options):
        print(f"{i+1}. {option}")
    
    framework_choice = int(input("Select a framework (1-3): "))
    framework = framework_options[framework_choice - 1]
    framework_version = input(f"{framework} version (leave empty for latest): ")
    
    config["framework"] = {
        "name": framework,
        "version": framework_version if framework_version else "latest"
    }
    
    # Language selection
    language_options = ["java", "kotlin"]
    print("\nLanguage options:")
    for i, option in enumerate(language_options):
        print(f"{i+1}. {option}")
    
    language_choice = int(input("Select a language (1-2): "))
    language = language_options[language_choice - 1]
    language_version = input(f"{language} version (leave empty for latest): ")
    
    config["language"] = {
        "name": language,
        "version": language_version if language_version else "latest"
    }
    
    # Build system
    build_options = ["maven", "gradle"]
    print("\nBuild system options:")
    for i, option in enumerate(build_options):
        print(f"{i+1}. {option}")
    
    build_choice = int(input("Select a build system (1-2): "))
    build_system = build_options[build_choice - 1]
    
    config["build_system"] = {
        "name": build_system
    }
    
    # CI/CD pipeline
    pipeline_options = ["github-actions", "jenkins", "azure-devops", "gitlab-ci", "none"]
    print("\nCI/CD pipeline options:")
    for i, option in enumerate(pipeline_options):
        print(f"{i+1}. {option}")
    
    pipeline_choice = int(input("Select a CI/CD pipeline (1-5): "))
    pipeline = pipeline_options[pipeline_choice - 1]
    
    if pipeline != "none":
        config["pipeline"] = {
            "name": pipeline
        }
    
    # Database
    db_options = ["mysql", "postgresql", "h2", "mongodb", "none"]
    print("\nDatabase options:")
    for i, option in enumerate(db_options):
        print(f"{i+1}. {option}")
    
    db_choice = int(input("Select a database (1-5): "))
    database = db_options[db_choice - 1]
    
    if database != "none":
        config["database"] = {
            "name": database
        }
    
    # Additional features
    feature_options = ["logging", "swagger", "aws", "data", "config", "integration", "yaml-config", "generate-dtos"]
    print("\nAdditional features (select multiple by separating with spaces):")
    for i, option in enumerate(feature_options):
        print(f"{i+1}. {option}")
    
    feature_choices = input("Select features (e.g., '1 3 4'): ").split()
    features = [feature_options[int(choice) - 1] for choice in feature_choices if 0 < int(choice) <= len(feature_options)]
    
    config["features"] = features
    
    # Service type
    service_options = ["domain-driven", "entity-driven"]
    print("\nService architecture type:")
    for i, option in enumerate(service_options):
        print(f"{i+1}. {option}")
    
    service_choice = int(input("Select a service architecture (1-2): "))
    service_type = service_options[service_choice - 1]
    
    config["service_type"] = service_type
    
    # Swagger file
    swagger_file = input("\nPath to Swagger/OpenAPI definition file (optional): ")
    if swagger_file:
        config["swagger_file"] = swagger_file
    
    # Schema mapping file
    schema_mapping = input("Path to schema relationship mapping file (optional): ")
    if schema_mapping:
        config["schema_mapping"] = schema_mapping
    
    # Output directory
    output_dir = input("\nOutput directory (leave empty for current directory): ")
    if output_dir:
        config["output_dir"] = output_dir
    
    return config

def merge_configs(config1: Dict[str, Any], config2: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two configuration dictionaries, with config2 taking precedence.
    
    Args:
        config1: Base configuration dictionary
        config2: Override configuration dictionary
        
    Returns:
        Dict[str, Any]: Merged configuration dictionary
    """
    result = config1.copy()
    
    for key, value in config2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    
    return result

def prepare_config(args) -> Dict[str, Any]:
    """Prepare configuration from command line arguments and/or interactive input.
    
    Args:
        args: Command line arguments
        
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    config = {}
    
    # Load from config file if specified
    if args.config_file:
        file_config = get_config_from_file(args.config_file)
        config = merge_configs(config, file_config)
    
    # Interactive mode
    if args.interactive:
        interactive_config = prompt_for_config()
        config = merge_configs(config, interactive_config)
    
    # Command line arguments override
    cli_config = {}
    
    if args.project_name:
        cli_config["project_name"] = args.project_name
    
    if args.base_package:
        cli_config["base_package"] = args.base_package
    
    if args.description:
        cli_config["description"] = args.description
    
    if args.framework:
        cli_config["framework"] = {
            "name": args.framework,
            "version": args.framework_version if args.framework_version else "latest"
        }
    
    if args.language:
        cli_config["language"] = {
            "name": args.language,
            "version": args.language_version if args.language_version else "latest"
        }
    
    if args.build_system:
        cli_config["build_system"] = {
            "name": args.build_system
        }
    
    if args.pipeline:
        cli_config["pipeline"] = {
            "name": args.pipeline
        }
    
    if args.database and args.database != "none":
        cli_config["database"] = {
            "name": args.database
        }
    
    if args.features:
        cli_config["features"] = args.features
    
    if args.service_type:
        cli_config["service_type"] = args.service_type
    
    if args.swagger_file:
        cli_config["swagger_file"] = args.swagger_file
    
    if args.schema_mapping:
        cli_config["schema_mapping"] = args.schema_mapping
    
    if args.output_dir:
        cli_config["output_dir"] = args.output_dir
    
    # Merge CLI config (highest priority)
    config = merge_configs(config, cli_config)
    
    return config

def validate_config(config: Dict[str, Any]) -> List[str]:
    """Validate the configuration and return any errors.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List[str]: List of validation error messages (empty if valid)
    """
    errors = []
    
    # Required fields
    if not config.get("project_name"):
        errors.append("Project name is required")
    
    if not config.get("base_package"):
        errors.append("Base package is required")
    
    if not config.get("framework", {}).get("name"):
        errors.append("Framework is required")
    
    if not config.get("language", {}).get("name"):
        errors.append("Language is required")
    
    if not config.get("build_system", {}).get("name"):
        errors.append("Build system is required")
    
    # Validate swagger file path if specified
    swagger_file = config.get("swagger_file")
    if swagger_file and not os.path.exists(swagger_file):
        errors.append(f"Swagger file not found: {swagger_file}")
    
    # Validate schema mapping file path if specified
    schema_mapping = config.get("schema_mapping")
    if schema_mapping and not os.path.exists(schema_mapping):
        errors.append(f"Schema mapping file not found: {schema_mapping}")
    
    return errors

def main():
    """Run the main application."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Show version and exit if requested
    if args.version:
        from microgenesis import __version__
        print(f"MicroGenesis version {__version__}")
        return 0
    
    try:
        # Prepare configuration
        if args.interactive or args.config_file or any([
            args.project_name, args.base_package, args.framework, 
            args.language, args.build_system
        ]):
            config = prepare_config(args)
            
            # Validate configuration
            errors = validate_config(config)
            if errors:
                for error in errors:
                    print(f"Error: {error}")
                return 1
            
            # Initialize scaffolding engine
            engine = ScaffoldingEngine(output_dir=config.get("output_dir"))
            
            # Generate project
            project_dir = engine.generate_project(config)
            
            print(f"\nProject generated successfully at: {project_dir}")
            print("\nNext steps:")
            print(f"  1. Navigate to the project directory: cd {project_dir}")
            
            if config.get("build_system", {}).get("name") == "maven":
                print("  2. Build the project: mvn clean install")
                print("  3. Run the application: mvn spring-boot:run")
            elif config.get("build_system", {}).get("name") == "gradle":
                print("  2. Build the project: ./gradlew build")
                print("  3. Run the application: ./gradlew bootRun")
            
            return 0
        else:
            print("MicroGenesis - Application Scaffolding Generator")
            print("-----------------------------------------------")
            print("Run with --interactive for guided setup")
            print("Run with --help to see all options")
            return 0
            
    except Exception as e:
        logger.error(f"Error generating project: {e}")
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
