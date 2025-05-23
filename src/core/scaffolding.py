"""Scaffolding module for generating application code."""

import os
import json
import shutil
from typing import Dict, List, Any, Optional

from src.core.logging import get_logger

logger = get_logger()


class ScaffoldingEngine:
    """Core engine for generating application scaffolding."""
    
    def __init__(self, output_dir: str = None):
        """Initialize the scaffolding engine.
        
        Args:
            output_dir: Directory where the generated code will be placed
        """
        self.output_dir = output_dir
        self.logger = get_logger()
    
    def generate_project(self, config: Dict[str, Any]) -> str:
        """Generate a project based on the provided configuration.
        
        Args:
            config: Project configuration dictionary
            
        Returns:
            str: Path to the generated project
        """
        self.logger.info(f"Starting project generation with config: {config}")
        
        # Extract basic project info
        project_name = config.get("project_name", "app")
        base_package = config.get("base_package", "com.example")
        
        # Handle different formats for language (flat or nested)
        language_config = config.get("language", {})
        if isinstance(language_config, dict):
            language = language_config.get("name", "java")
            language_version = language_config.get("version", "11")
        else:
            language = language_config or "java"
            language_version = config.get("language_version", "11")
        
        # Handle different formats for framework (flat or nested)
        framework_config = config.get("framework", {})
        if isinstance(framework_config, dict):
            framework = framework_config.get("name", "spring-boot")
            framework_version = framework_config.get("version", "2.7.0")
        else:
            framework = framework_config or "spring-boot"
            framework_version = config.get("framework_version", "2.7.0")
        
        service_type = config.get("service_type", "domain-driven")
        
        # Handle different formats for build system (flat or nested)
        build_system_config = config.get("build_system", {})
        if isinstance(build_system_config, dict):
            build_system = build_system_config.get("name", "maven")
        else:
            build_system = build_system_config or "maven"
            
        # Handle different formats for database (flat or nested)
        database_config = config.get("database", {})
        if not isinstance(database_config, dict):
            # Convert string to dict format
            database_name = database_config
            config["database"] = {"name": database_name}
        
        # Create project directory
        if not self.output_dir:
            self.output_dir = os.path.join(os.getcwd(), project_name)
        
        project_dir = os.path.join(self.output_dir, project_name)
        os.makedirs(project_dir, exist_ok=True)
        self.logger.info(f"Project will be generated at: {project_dir}")
        
        # Process DDL file if provided
        entities = []
        if "ddl_file" in config and config["ddl_file"]:
            try:
                from src.generators.schema.ddl_parser import DDLParser
                ddl_parser = DDLParser()
                ddl_file = config["ddl_file"]
                self.logger.info(f"Parsing DDL file: {ddl_file}")
                entities = ddl_parser.parse_ddl_file(ddl_file)
                config["entities"] = entities
                self.logger.info(f"Found {len(entities)} entities in DDL file")
            except Exception as e:
                self.logger.error(f"Error parsing DDL file: {e}")
        
        # Generate code based on framework and language
        generator = self._get_generator(framework, language)
        generator.generate(project_dir, config)
        
        # Return the path to the generated project
        return project_dir
        
    def _get_generator(self, framework: str, language: str):
        """Get the appropriate generator for the framework and language.
        
        Args:
            framework: Name of the framework (spring-boot, micronaut, etc.)
            language: Name of the language (java, kotlin, etc.)
            
        Returns:
            Generator implementation for the specified framework and language
        """
        # Import generator implementations based on framework and language
        if framework == "spring-boot":
            if language == "java":
                from src.generators.spring_boot.java import SpringBootJavaGenerator
                return SpringBootJavaGenerator()
            elif language == "kotlin":
                from src.generators.spring_boot.kotlin import SpringBootKotlinGenerator
                return SpringBootKotlinGenerator()
        elif framework == "micronaut":
            if language == "java":
                from src.generators.micronaut.java import MicronautJavaGenerator
                return MicronautJavaGenerator()
            elif language == "kotlin":
                from src.generators.micronaut.kotlin import MicronautKotlinGenerator
                return MicronautKotlinGenerator()
        elif framework == "graphql":
            if language == "java":
                from src.generators.graphql.java import GraphQLJavaGenerator
                return GraphQLJavaGenerator()
            elif language == "kotlin":
                from src.generators.graphql.kotlin import GraphQLKotlinGenerator
                return GraphQLKotlinGenerator()
        
        # Default fallback
        from src.generators.base import BaseGenerator
        self.logger.warning(f"No specific generator found for {framework}/{language}. Using base generator.")
        return BaseGenerator()
