"""Integration utilities between UI and core functionality."""

import os
import json
from typing import Dict, Any, Optional, List

import streamlit as st
from src.core.scaffolding import ScaffoldingEngine
from src.core.config import Config
from src.core.logging import get_logger

logger = get_logger()

def generate_project_from_ui(config_data: Dict[str, Any]) -> Optional[str]:
    """Generate a project using the configuration from the UI.
    
    Args:
        config_data: Project configuration dictionary
        
    Returns:
        str: Path to the generated project, or None if generation failed
    """
    try:
        logger.info(f"Generating project with config: {config_data}")
        
        # Create scaffolding engine
        output_dir = config_data.get("output_dir", "./output")
        engine = ScaffoldingEngine(output_dir=output_dir)
        
        # Generate the project
        project_path = engine.generate_project(config_data)
        
        return project_path
    except Exception as e:
        logger.error(f"Error generating project: {e}")
        return None


def prepare_config_from_ui(ui_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert UI form data to the format expected by the scaffolding engine.
    
    Args:
        ui_data: UI form data
        
    Returns:
        dict: Configuration in the format expected by the scaffolding engine
    """
    # Extract selections from session state
    selections = ui_data.get("selections", {})
    
    config = {
        "project_name": ui_data.get("projectName", "app"),
        "base_package": ui_data.get("basePackageName", "com.example"),
        
        "framework": {
            "name": selections.get("framework", {}).get("id") if selections.get("framework") else "spring-boot",
            "version": selections.get("frameworkVersion", {}).get("id") if selections.get("frameworkVersion") else "latest"
        },
        
        "language": {
            "name": selections.get("language", {}).get("id") if selections.get("language") else "java",
            "version": selections.get("languageVersion", {}).get("id") if selections.get("languageVersion") else "latest"
        },
        
        "build_system": {
            "name": selections.get("buildTool", {}).get("id") if selections.get("buildTool") else "maven"
        },
        
        "service_type": selections.get("serviceType", {}).get("id") if selections.get("serviceType") else "domain-driven"
    }
    
    # Add gradle DSL if applicable
    if config["build_system"]["name"] == "gradle" and selections.get("gradleDsl"):
        config["build_system"]["dsl"] = selections["gradleDsl"]["id"]
    
    # Add database if selected
    if selections.get("database") and selections["database"]["id"] != "none":
        config["database"] = {
            "name": selections["database"]["id"]
        }
    
    # Add entities and relationships
    if "entities" in ui_data and ui_data["entities"]:
        config["entities"] = ui_data["entities"]
        
    if "relationships" in ui_data and ui_data["relationships"]:
        config["relationships"] = ui_data["relationships"]
    
    # Add output directory
    if "output_dir" in ui_data:
        config["output_dir"] = ui_data["output_dir"]
    
    # Add pipeline
    if selections.get("pipeline"):
        config["pipeline"] = {
            "name": selections["pipeline"]["id"]
        }
    
    # Add features
    if selections.get("features"):
        config["features"] = [feature["id"] for feature in selections["features"]]
    
    # Add swagger/openapi spec if provided
    if selections.get("swagger"):
        config["swagger"] = selections["swagger"]
        
    # Add DDL if provided
    if selections.get("ddl"):
        config["ddl"] = selections["ddl"]
    
    return config


def get_available_templates() -> Dict[str, Any]:
    """Get information about available templates in the system.
    
    Returns:
        dict: Dictionary with information about available templates
    """
    config = Config()
    config.load()
    
    templates_info = {
        "frameworks": config.get("generators.frameworks", ["spring-boot", "micronaut", "graphql"]),
        "languages": config.get("generators.languages", ["java", "kotlin"]),
        "build_systems": config.get("generators.build_systems", ["maven", "gradle"]),
        "databases": config.get("generators.databases", ["mysql", "postgresql", "h2", "mongodb", "none"]),
        "pipelines": config.get("generators.pipelines", ["github-actions", "jenkins", "azure-devops", "gitlab-ci"])
    }
    
    return templates_info


def save_ui_settings(settings: Dict[str, Any]) -> bool:
    """Save UI settings to a configuration file.
    
    Args:
        settings: Dictionary of settings to save
        
    Returns:
        bool: True if settings were saved successfully, False otherwise
    """
    try:
        config_dir = os.path.expanduser("~/.microgenesis")
        os.makedirs(config_dir, exist_ok=True)
        
        config_path = os.path.join(config_dir, "ui_settings.json")
        
        with open(config_path, "w") as f:
            json.dump(settings, f, indent=2)
            
        return True
    except Exception as e:
        logger.error(f"Error saving UI settings: {e}")
        return False


def load_ui_settings() -> Dict[str, Any]:
    """Load UI settings from configuration file.
    
    Returns:
        dict: Loaded settings or default settings
    """
    default_settings = {
        "default_output_dir": "./output",
        "default_author": "",
        "default_email": "",
        "custom_template_dir": "",
        "enable_debug": False,
        "template_reload": True
    }
    
    try:
        config_path = os.path.expanduser("~/.microgenesis/ui_settings.json")
        
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                loaded_settings = json.load(f)
                
            # Merge with defaults in case new settings are added
            for key, value in default_settings.items():
                if key not in loaded_settings:
                    loaded_settings[key] = value
                    
            return loaded_settings
        else:
            return default_settings
    except Exception as e:
        logger.error(f"Error loading UI settings: {e}")
        return default_settings


def parse_ddl_file(file_content: str) -> List[Dict[str, Any]]:
    """Parse DDL file content to extract entity information.
    
    Args:
        file_content: Content of the DDL file
        
    Returns:
        list: List of entity dictionaries
    """
    try:
        from src.generators.schema.ddl_parser import DDLParser
        
        parser = DDLParser()
        entities = parser.parse_ddl(file_content)
        
        return entities
    except Exception as e:
        logger.error(f"Error parsing DDL file: {e}")
        return []
