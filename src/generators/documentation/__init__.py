"""Documentation generator for MicroGenesis projects.

This module provides utilities for generating comprehensive technical documentation
for projects generated with MicroGenesis.
"""

import os
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader


class DocumentationGenerator:
    """Generate comprehensive documentation for MicroGenesis projects."""
    
    def __init__(self, templates_dir: str):
        """Initialize the documentation generator.
        
        Args:
            templates_dir: Directory containing documentation templates
        """
        self.template_env = Environment(
            loader=FileSystemLoader(templates_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def generate_documentation(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate documentation for a project.
        
        Args:
            project_dir: Project directory
            config: Project configuration
        """
        docs_dir = os.path.join(project_dir, "docs")
        os.makedirs(docs_dir, exist_ok=True)
        
        # Generate README
        self._generate_readme(project_dir, config)
        
        # Generate architecture documentation
        self._generate_architecture_docs(docs_dir, config)
        
        # Generate API documentation
        self._generate_api_docs(docs_dir, config)
        
        # Generate deployment documentation
        self._generate_deployment_docs(docs_dir, config)
        
        # Generate development guide
        self._generate_development_guide(docs_dir, config)
    
    def _generate_readme(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate project README.
        
        Args:
            project_dir: Project directory
            config: Project configuration
        """
        template = self.template_env.get_template("README.md.j2")
        content = template.render(
            project_name=config.get("project_name", ""),
            description=config.get("description", ""),
            features=config.get("features", []),
            framework=config.get("framework", {}),
            language=config.get("language", {}),
            service_type=config.get("service_type", ""),
            build_system=config.get("build_system", {})
        )
        
        with open(os.path.join(project_dir, "README.md"), "w") as f:
            f.write(content)
    
    def _generate_architecture_docs(self, docs_dir: str, config: Dict[str, Any]) -> None:
        """Generate architecture documentation.
        
        Args:
            docs_dir: Documentation directory
            config: Project configuration
        """
        # Get service type for architecture-specific documentation
        service_type = config.get("service_type", "domain-driven")
        
        # Generate architecture overview
        template = self.template_env.get_template(f"architecture/{service_type}.md.j2")
        content = template.render(
            project_name=config.get("project_name", ""),
            base_package=config.get("base_package", ""),
            framework=config.get("framework", {}),
            language=config.get("language", {})
        )
        
        with open(os.path.join(docs_dir, "ARCHITECTURE.md"), "w") as f:
            f.write(content)
        
        # Generate component diagram if PlantUML is available
        self._generate_component_diagram(docs_dir, config)
    
    def _generate_component_diagram(self, docs_dir: str, config: Dict[str, Any]) -> None:
        """Generate component diagram using PlantUML.
        
        Args:
            docs_dir: Documentation directory
            config: Project configuration
        """
        service_type = config.get("service_type", "domain-driven")
        template = self.template_env.get_template(f"diagrams/{service_type}_components.puml.j2")
        content = template.render(
            project_name=config.get("project_name", ""),
            base_package=config.get("base_package", "")
        )
        
        with open(os.path.join(docs_dir, "component_diagram.puml"), "w") as f:
            f.write(content)
    
    def _generate_api_docs(self, docs_dir: str, config: Dict[str, Any]) -> None:
        """Generate API documentation.
        
        Args:
            docs_dir: Documentation directory
            config: Project configuration
        """
        template = self.template_env.get_template("api_documentation.md.j2")
        content = template.render(
            project_name=config.get("project_name", ""),
            base_package=config.get("base_package", ""),
            endpoints=self._get_sample_endpoints(config)
        )
        
        with open(os.path.join(docs_dir, "API.md"), "w") as f:
            f.write(content)
    
    def _generate_deployment_docs(self, docs_dir: str, config: Dict[str, Any]) -> None:
        """Generate deployment documentation.
        
        Args:
            docs_dir: Documentation directory
            config: Project configuration
        """
        template = self.template_env.get_template("deployment.md.j2")
        content = template.render(
            project_name=config.get("project_name", ""),
            framework=config.get("framework", {}),
            features=config.get("features", []),
            database=config.get("database", {})
        )
        
        with open(os.path.join(docs_dir, "DEPLOYMENT.md"), "w") as f:
            f.write(content)
        
        # Generate Kubernetes configuration if Kubernetes is a feature
        if "kubernetes" in config.get("features", []):
            k8s_dir = os.path.join(docs_dir, "kubernetes")
            os.makedirs(k8s_dir, exist_ok=True)
            
            self._generate_kubernetes_docs(k8s_dir, config)
    
    def _generate_kubernetes_docs(self, k8s_dir: str, config: Dict[str, Any]) -> None:
        """Generate Kubernetes documentation and manifests.
        
        Args:
            k8s_dir: Kubernetes documentation directory
            config: Project configuration
        """
        # Generate Kubernetes README
        template = self.template_env.get_template("kubernetes/README.md.j2")
        content = template.render(
            project_name=config.get("project_name", ""),
            database=config.get("database", {})
        )
        
        with open(os.path.join(k8s_dir, "README.md"), "w") as f:
            f.write(content)
        
        # Generate sample Kubernetes manifests
        for manifest in ["deployment", "service", "configmap", "secret"]:
            template = self.template_env.get_template(f"kubernetes/{manifest}.yaml.j2")
            content = template.render(
                project_name=config.get("project_name", ""),
                container_port=8080,
                database=config.get("database", {})
            )
            
            with open(os.path.join(k8s_dir, f"{manifest}.yaml"), "w") as f:
                f.write(content)
    
    def _generate_development_guide(self, docs_dir: str, config: Dict[str, Any]) -> None:
        """Generate development guide.
        
        Args:
            docs_dir: Documentation directory
            config: Project configuration
        """
        template = self.template_env.get_template("development_guide.md.j2")
        content = template.render(
            project_name=config.get("project_name", ""),
            framework=config.get("framework", {}),
            language=config.get("language", {}),
            build_system=config.get("build_system", {}),
            database=config.get("database", {}),
            features=config.get("features", [])
        )
        
        with open(os.path.join(docs_dir, "DEVELOPMENT.md"), "w") as f:
            f.write(content)
    
    def _get_sample_endpoints(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate sample API endpoints based on configuration.
        
        Args:
            config: Project configuration
            
        Returns:
            List of sample endpoints
        """
        project_name = config.get("project_name", "app")
        resource_name = project_name.lower()
        if resource_name.endswith("s"):
            resource_name = resource_name[:-1]
            
        # Create sample endpoints
        return [
            {
                "path": f"/api/{resource_name}s",
                "method": "GET",
                "description": f"Get all {resource_name}s",
                "params": [
                    {"name": "page", "type": "integer", "description": "Page number (zero-based)", "required": False},
                    {"name": "size", "type": "integer", "description": "Page size", "required": False}
                ],
                "response": {
                    "status": 200,
                    "type": f"List<{resource_name.capitalize()}DTO>",
                    "description": f"List of {resource_name}s"
                }
            },
            {
                "path": f"/api/{resource_name}s/{{id}}",
                "method": "GET",
                "description": f"Get {resource_name} by ID",
                "params": [
                    {"name": "id", "type": "integer", "description": f"{resource_name.capitalize()} ID", "required": True}
                ],
                "response": {
                    "status": 200,
                    "type": f"{resource_name.capitalize()}DTO",
                    "description": f"The {resource_name} details"
                }
            },
            {
                "path": f"/api/{resource_name}s",
                "method": "POST",
                "description": f"Create a new {resource_name}",
                "request_body": {
                    "type": f"{resource_name.capitalize()}DTO",
                    "description": f"{resource_name.capitalize()} details"
                },
                "response": {
                    "status": 201,
                    "type": f"{resource_name.capitalize()}DTO",
                    "description": f"The created {resource_name}"
                }
            },
            {
                "path": f"/api/{resource_name}s/{{id}}",
                "method": "PUT",
                "description": f"Update {resource_name} by ID",
                "params": [
                    {"name": "id", "type": "integer", "description": f"{resource_name.capitalize()} ID", "required": True}
                ],
                "request_body": {
                    "type": f"{resource_name.capitalize()}DTO",
                    "description": f"Updated {resource_name} details"
                },
                "response": {
                    "status": 200,
                    "type": f"{resource_name.capitalize()}DTO",
                    "description": f"The updated {resource_name}"
                }
            },
            {
                "path": f"/api/{resource_name}s/{{id}}",
                "method": "DELETE",
                "description": f"Delete {resource_name} by ID",
                "params": [
                    {"name": "id", "type": "integer", "description": f"{resource_name.capitalize()} ID", "required": True}
                ],
                "response": {
                    "status": 204,
                    "type": "void",
                    "description": "No content"
                }
            }
        ]
