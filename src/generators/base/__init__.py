"""Base generator module for application scaffolding."""

import os
import shutil
import json
import yaml
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import jinja2
import re

from src.core.logging import get_logger

logger = get_logger()


class BaseGenerator(ABC):
    """Base class for all generators."""
    
    def __init__(self):
        """Initialize the base generator."""
        self.logger = get_logger()
        # Set up Jinja2 template environment
        templates_dir = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "..",
            "templates"
        )
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add utility functions to templates
        self.template_env.filters['camelcase'] = self._to_camel_case
        self.template_env.filters['pascalcase'] = self._to_pascal_case
        self.template_env.filters['snakecase'] = self._to_snake_case
        self.template_env.filters['kebabcase'] = self._to_kebab_case
        
        # Add custom tests
        self.template_env.tests['match'] = self._match_test
        
    def generate(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate a project based on the provided configuration.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        self.logger.info(f"Starting generation in {project_dir}")
        
        # Basic project setup
        self._create_project_structure(project_dir, config)
        
        # Generate build configuration
        self._generate_build_config(project_dir, config)
        
        # Generate source code
        self._generate_source_code(project_dir, config)
        
        # Generate tests
        self._generate_tests(project_dir, config)
        
        # Generate CI/CD pipeline configs
        self._generate_pipeline_config(project_dir, config)
        
        # Generate documentation
        self._generate_documentation(project_dir, config)
        
        self.logger.info(f"Project generation completed in {project_dir}")
    
    def _create_project_structure(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Create the basic project structure.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        os.makedirs(project_dir, exist_ok=True)
        
        # Create standard directories
        src_dir = os.path.join(project_dir, "src")
        os.makedirs(src_dir, exist_ok=True)
        
        main_dir = os.path.join(src_dir, "main")
        os.makedirs(main_dir, exist_ok=True)
        
        test_dir = os.path.join(src_dir, "test")
        os.makedirs(test_dir, exist_ok=True)
        
        # Create language-specific directories
        language = config.get("language", {}).get("name", "java")
        base_package_path = config.get("base_package", "com.example").replace(".", os.path.sep)
        
        main_code_dir = os.path.join(main_dir, language, base_package_path)
        os.makedirs(main_code_dir, exist_ok=True)
        
        test_code_dir = os.path.join(test_dir, language, base_package_path)
        os.makedirs(test_code_dir, exist_ok=True)
        
        # Create resource directories
        main_resources = os.path.join(main_dir, "resources")
        os.makedirs(main_resources, exist_ok=True)
        
        test_resources = os.path.join(test_dir, "resources")
        os.makedirs(test_resources, exist_ok=True)
        
        # Create docs directory
        docs_dir = os.path.join(project_dir, "docs")
        os.makedirs(docs_dir, exist_ok=True)
    
    @abstractmethod
    def _generate_build_config(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate build configuration files (e.g., pom.xml, build.gradle).
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        pass
    
    @abstractmethod
    def _generate_source_code(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate source code files.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        pass
    
    @abstractmethod
    def _generate_tests(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate test files.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        pass
    
    def _generate_pipeline_config(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate CI/CD pipeline configuration files.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        pipeline = config.get("pipeline", {}).get("name", "")
        
        if pipeline == "github-actions":
            self._generate_github_actions(project_dir, config)
        elif pipeline == "jenkins":
            self._generate_jenkins(project_dir, config)
        elif pipeline == "azure-devops":
            self._generate_azure_devops(project_dir, config)
        elif pipeline == "gitlab-ci":
            self._generate_gitlab_ci(project_dir, config)
            
    def _generate_github_actions(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate GitHub Actions workflow files.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        github_dir = os.path.join(project_dir, ".github", "workflows")
        os.makedirs(github_dir, exist_ok=True)
        
        build_system = config.get("build_system", {}).get("name", "maven")
        language = config.get("language", {}).get("name", "java")
        
        # Generate CI workflow
        template = self.template_env.get_template(f"github-actions-{build_system}-{language}.yml.j2")
        ci_content = template.render(config=config)
        
        with open(os.path.join(github_dir, "ci.yml"), "w") as f:
            f.write(ci_content)
    
    def _generate_jenkins(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate Jenkinsfile.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        build_system = config.get("build_system", {}).get("name", "maven")
        template = self.template_env.get_template(f"Jenkinsfile-{build_system}.j2")
        jenkinsfile_content = template.render(config=config)
        
        with open(os.path.join(project_dir, "Jenkinsfile"), "w") as f:
            f.write(jenkinsfile_content)
    
    def _generate_azure_devops(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate Azure DevOps pipeline YAML.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        build_system = config.get("build_system", {}).get("name", "maven")
        template = self.template_env.get_template(f"azure-pipelines-{build_system}.yml.j2")
        pipeline_content = template.render(config=config)
        
        with open(os.path.join(project_dir, "azure-pipelines.yml"), "w") as f:
            f.write(pipeline_content)
    
    def _generate_gitlab_ci(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate GitLab CI YAML.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        build_system = config.get("build_system", {}).get("name", "maven")
        template = self.template_env.get_template(f"gitlab-ci-{build_system}.yml.j2")
        ci_content = template.render(config=config)
        
        with open(os.path.join(project_dir, ".gitlab-ci.yml"), "w") as f:
            f.write(ci_content)
    def _generate_documentation(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate project documentation.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        docs_dir = os.path.join(project_dir, "docs")
        os.makedirs(docs_dir, exist_ok=True)
          # Generate README
        template = self.template_env.get_template("common/docs/README.md.j2")
        readme_content = template.render(**config)
        
        with open(os.path.join(project_dir, "README.md"), "w") as f:
            f.write(readme_content)
        
        # Generate Getting Started guide
        template = self.template_env.get_template("common/docs/GETTING-STARTED.md.j2")
        getting_started_content = template.render(**config)
        
        with open(os.path.join(docs_dir, "GETTING-STARTED.md"), "w") as f:
            f.write(getting_started_content)
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a template with the given context.
        
        Args:
            template_name: Name of the template file
            context: Context data for template rendering
            
        Returns:
            str: Rendered template content
        """
        template = self.template_env.get_template(template_name)
        return template.render(**context)
    
    def get_safe_database_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Get the database configuration, ensuring it's a dictionary.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Dict[str, Any]: Database configuration as a dictionary
        """
        database = config.get("database", {})
        if not isinstance(database, dict):
            # Convert string to dict format
            return {"name": database}
        return database
    
    def parse_swagger_file(self, swagger_path: str) -> Dict[str, Any]:
        """Parse an OpenAPI/Swagger file and extract API information.
        
        Args:
            swagger_path: Path to the Swagger/OpenAPI definition file
            
        Returns:
            Dict[str, Any]: Parsed API information
        """
        if not os.path.exists(swagger_path):
            self.logger.error(f"Swagger file not found: {swagger_path}")
            return {}
        
        try:
            with open(swagger_path, 'r') as f:
                
                # Determine the file type and parse accordingly
                file_extension = os.path.splitext(swagger_path)[1].lower()
                if file_extension in ['.yaml', '.yml']:
                    swagger_data = yaml.safe_load(f)
                else:
                    swagger_data = json.load(f)
                
                
            api_info = {
                'info': swagger_data.get('info', {}),
                'endpoints': [],
                'models': {},
            }
            
            # Extract endpoints
            paths = swagger_data.get('paths', {})
            for path, methods in paths.items():
                for method, details in methods.items():
                    if method in ['get', 'post', 'put', 'delete', 'patch']:
                        endpoint_info = {
                            'path': path,
                            'method': method,
                            'operation_id': details.get('operationId', ''),
                            'summary': details.get('summary', ''),
                            'description': details.get('description', ''),
                            'tags': details.get('tags', []),
                            'parameters': details.get('parameters', []),
                            'request_body': details.get('requestBody', {}),
                            'responses': details.get('responses', {})
                        }
                        api_info['endpoints'].append(endpoint_info)
            
            # Extract models
            schemas = swagger_data.get('components', {}).get('schemas', {})
            for schema_name, schema in schemas.items():
                properties = schema.get('properties', {})
                required = schema.get('required', [])
                
                model_info = {
                    'name': schema_name,
                    'properties': [],
                    'type': 'entity' if 'Entity' in schema_name else 'dto'
                }
                
                for prop_name, prop_details in properties.items():
                    property_info = {
                        'name': prop_name,
                        'type': prop_details.get('type', 'string'),
                        'format': prop_details.get('format', ''),
                        'description': prop_details.get('description', ''),
                        'required': prop_name in required
                    }
                    model_info['properties'].append(property_info)
                
                api_info['models'][schema_name] = model_info
            
            return api_info
            
        except Exception as e:
            self.logger.error(f"Error parsing Swagger file: {e}")
            return {}
    
    def _match_test(self, value: str, pattern: str) -> bool:
        """Custom test to match a value against a regex pattern.
        
        Args:
            value: The value to test
            pattern: The regex pattern to match against
            
        Returns:
            bool: True if the value matches the pattern, False otherwise
        """
        if not isinstance(value, str) or not isinstance(pattern, str):
            return False
        
        try:
            regex = re.compile(pattern)
            return bool(regex.match(value))
        except re.error:
            return False
