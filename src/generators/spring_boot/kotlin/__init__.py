"""Spring Boot generator for Kotlin applications."""

import os
import json
from typing import Dict, List, Any, Optional
import re

from src.generators.base import BaseGenerator
from src.core.logging import get_logger


class SpringBootKotlinGenerator(BaseGenerator):
    """Generator for Spring Boot Kotlin applications."""
    
    def __init__(self):
        """Initialize the Spring Boot Kotlin generator."""
        super().__init__()
        self.logger = get_logger()
    
    def _generate_build_config(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate build configuration files.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        build_system = config.get("build_system", {}).get("name", "maven")
        
        if build_system == "maven":
            self._generate_maven_config(project_dir, config)
        elif build_system == "gradle":
            self._generate_gradle_config(project_dir, config)
        else:
            self.logger.warning(f"Unsupported build system: {build_system}")
    
    def _generate_maven_config(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate Maven configuration (pom.xml).
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        # Prepare context for template rendering
        context = {
            "project": config.get("project_name", "app"),
            "group_id": config.get("base_package", "com.example"),
            "artifact_id": config.get("project_name", "app").lower(),
            "version": config.get("project_version", "0.1.0"),
            "spring_boot_version": config.get("framework", {}).get("version", "3.1.0"),
            "kotlin_version": config.get("language", {}).get("version", "1.8.0"),
            "description": config.get("description", "Generated Spring Boot Kotlin application"),
            "database": config.get("database", {}).get("name", ""),
            "features": config.get("features", []),
        }
        
        # Render pom.xml template
        pom_content = self.render_template("spring-boot/kotlin/pom.xml.j2", context)
        with open(os.path.join(project_dir, "pom.xml"), "w") as f:
            f.write(pom_content)
    
    def _generate_gradle_config(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate Gradle configuration (build.gradle.kts).
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        # Prepare context for template rendering
        context = {
            "project": config.get("project_name", "app"),
            "group_id": config.get("base_package", "com.example"),
            "artifact_id": config.get("project_name", "app").lower(),
            "version": config.get("project_version", "0.1.0"),
            "spring_boot_version": config.get("framework", {}).get("version", "3.1.0"),
            "kotlin_version": config.get("language", {}).get("version", "1.8.0"),
            "description": config.get("description", "Generated Spring Boot Kotlin application"),
            "database": config.get("database", {}).get("name", ""),
            "features": config.get("features", []),
        }
        
        # Render build.gradle.kts template
        build_gradle_content = self.render_template("spring-boot/kotlin/build.gradle.kts.j2", context)
        with open(os.path.join(project_dir, "build.gradle.kts"), "w") as f:
            f.write(build_gradle_content)
        
        # Render settings.gradle.kts template
        settings_gradle_content = self.render_template("spring-boot/kotlin/settings.gradle.kts.j2", context)
        with open(os.path.join(project_dir, "settings.gradle.kts"), "w") as f:
            f.write(settings_gradle_content)
    
    def _generate_source_code(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate source code files.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        # Extract configuration
        package_name = config.get("base_package", "com.example")
        
        # Prepare source directories
        src_main_kotlin = os.path.join(project_dir, "src", "main", "kotlin")
        package_path = os.path.join(src_main_kotlin, *package_name.split("."))
        os.makedirs(package_path, exist_ok=True)
        
        # Create subdirectories for different components
        controllers_dir = os.path.join(package_path, "controllers")
        models_dir = os.path.join(package_path, "models")
        repositories_dir = os.path.join(package_path, "repositories")
        services_dir = os.path.join(package_path, "services")
        config_dir = os.path.join(package_path, "config")
        
        for directory in [controllers_dir, models_dir, repositories_dir, services_dir, config_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Create resources directory
        resources_dir = os.path.join(project_dir, "src", "main", "resources")
        os.makedirs(resources_dir, exist_ok=True)
        
        # Generate application class
        self._generate_application_class(package_path, package_name, config)
        
        # Generate model classes
        self._generate_model_classes(models_dir, package_name, config)
        
        # Generate controller classes
        self._generate_controller_classes(controllers_dir, package_name, config)
        
        # Generate service classes
        self._generate_service_classes(services_dir, package_name, config)
        
        # Generate repository interfaces
        self._generate_repository_interfaces(repositories_dir, package_name, config)
        
        # Generate application properties
        self._generate_application_properties(resources_dir, config)
    
    def _generate_application_class(self, package_path: str, package_name: str, config: Dict[str, Any]) -> None:
        """Generate the main application class.
        
        Args:
            package_path: Path to the package directory
            package_name: Package name
            config: Project configuration dictionary
        """
        context = {
            "package": package_name,
            "app_name": config.get("project_name", "app"),
        }
        
        application_content = self.render_template("spring-boot/kotlin/Application.kt.j2", context)
        with open(os.path.join(package_path, "Application.kt"), "w") as f:
            f.write(application_content)
    
    def _generate_model_classes(self, models_dir: str, package_name: str, config: Dict[str, Any]) -> None:
        """Generate model classes.
        
        Args:
            models_dir: Directory for model classes
            package_name: Package name
            config: Project configuration dictionary
        """
        models_package = f"{package_name}.models"
        entities = config.get("entities", [])
        
        if not entities:
            # Generate sample entity if none provided
            sample_entity = {
                "name": "Sample",
                "fields": [
                    {"name": "id", "type": "Long", "annotations": ["@Id", "@GeneratedValue(strategy = GenerationType.IDENTITY)"]},
                    {"name": "name", "type": "String", "annotations": ["@Column(nullable = false)"]},
                    {"name": "description", "type": "String?", "annotations": []},
                    {"name": "createdAt", "type": "LocalDateTime", "annotations": ["@Column(name = \"created_at\")"]},
                ]
            }
            
            context = {
                "package": models_package,
                "entity_name": sample_entity["name"],
                "fields": sample_entity["fields"],
                "imports": ["java.time.LocalDateTime", "jakarta.persistence.*"],
            }
            
            entity_content = self.render_template("spring-boot/kotlin/Entity.kt.j2", context)
            with open(os.path.join(models_dir, f"{sample_entity['name']}.kt"), "w") as f:
                f.write(entity_content)
            
            # Create DTO for sample entity
            if "generate-dtos" in config.get("features", []):
                dto_context = {
                    "package": models_package,
                    "entity_name": sample_entity["name"],
                    "fields": sample_entity["fields"],
                    "imports": ["java.time.LocalDateTime"],
                }
                
                dto_content = self.render_template("spring-boot/kotlin/DTO.kt.j2", dto_context)
                with open(os.path.join(models_dir, f"{sample_entity['name']}DTO.kt"), "w") as f:
                    f.write(dto_content)
        else:
            # Generate entities from configuration
            for entity in entities:
                context = {
                    "package": models_package,
                    "entity_name": entity["name"],
                    "fields": entity["fields"],
                    "imports": self._get_imports_for_kotlin_entity(entity["fields"]),
                }
                
                entity_content = self.render_template("spring-boot/kotlin/Entity.kt.j2", context)
                with open(os.path.join(models_dir, f"{entity['name']}.kt"), "w") as f:
                    f.write(entity_content)
                
                # Create DTOs if needed
                if "generate-dtos" in config.get("features", []):
                    dto_context = {
                        "package": models_package,
                        "entity_name": entity["name"],
                        "fields": entity["fields"],
                        "imports": self._get_imports_for_kotlin_dto(entity["fields"]),
                    }
                    
                    dto_content = self.render_template("spring-boot/kotlin/DTO.kt.j2", dto_context)
                    with open(os.path.join(models_dir, f"{entity['name']}DTO.kt"), "w") as f:
                        f.write(dto_content)
    
    def _generate_controller_classes(self, controllers_dir: str, package_name: str, config: Dict[str, Any]) -> None:
        """Generate controller classes.
        
        Args:
            controllers_dir: Directory for controller classes
            package_name: Package name
            config: Project configuration dictionary
        """
        controllers_package = f"{package_name}.controllers"
        models_package = f"{package_name}.models"
        services_package = f"{package_name}.services"
        entities = config.get("entities", [])
        
        if not entities:
            entities = [{"name": "Sample"}]
        
        for entity in entities:
            context = {
                "package": controllers_package,
                "model_package": models_package,
                "service_package": services_package,
                "entity_name": entity["name"],
                "entity_var": entity["name"][0].lower() + entity["name"][1:],
                "use_dtos": "generate-dtos" in config.get("features", []),
                "rest_base_path": entity["name"].lower() + "s"
            }
            
            controller_content = self.render_template("spring-boot/kotlin/Controller.kt.j2", context)
            with open(os.path.join(controllers_dir, f"{entity['name']}Controller.kt"), "w") as f:
                f.write(controller_content)
    
    def _generate_service_classes(self, services_dir: str, package_name: str, config: Dict[str, Any]) -> None:
        """Generate service classes.
        
        Args:
            services_dir: Directory for service classes
            package_name: Package name
            config: Project configuration dictionary
        """
        services_package = f"{package_name}.services"
        models_package = f"{package_name}.models"
        repositories_package = f"{package_name}.repositories"
        entities = config.get("entities", [])
        
        if not entities:
            entities = [{"name": "Sample"}]
        
        for entity in entities:
            # Generate service interface
            interface_context = {
                "package": services_package,
                "model_package": models_package,
                "entity_name": entity["name"],
                "entity_var": entity["name"][0].lower() + entity["name"][1:],
                "use_dtos": "generate-dtos" in config.get("features", [])
            }
            
            interface_content = self.render_template("spring-boot/kotlin/Service.kt.j2", interface_context)
            with open(os.path.join(services_dir, f"{entity['name']}Service.kt"), "w") as f:
                f.write(interface_content)
            
            # Generate service implementation
            impl_context = {
                "package": services_package,
                "model_package": models_package,
                "repository_package": repositories_package,
                "entity_name": entity["name"],
                "entity_var": entity["name"][0].lower() + entity["name"][1:],
                "use_dtos": "generate-dtos" in config.get("features", [])
            }
            
            impl_content = self.render_template("spring-boot/kotlin/ServiceImpl.kt.j2", impl_context)
            with open(os.path.join(services_dir, f"{entity['name']}ServiceImpl.kt"), "w") as f:
                f.write(impl_content)
    
    def _generate_repository_interfaces(self, repositories_dir: str, package_name: str, config: Dict[str, Any]) -> None:
        """Generate repository interfaces.
        
        Args:
            repositories_dir: Directory for repository interfaces
            package_name: Package name
            config: Project configuration dictionary
        """
        repositories_package = f"{package_name}.repositories"
        models_package = f"{package_name}.models"
        entities = config.get("entities", [])
        
        if not entities:
            entities = [{"name": "Sample", "id_type": "Long"}]
        
        for entity in entities:
            # Determine ID type
            id_type = "Long"  # Default
            if "fields" in entity:
                id_field = next((f for f in entity["fields"] if f.get("name") == "id"), None)
                if id_field:
                    id_type = id_field.get("type", "Long")
                    if id_type.endswith("?"):
                        id_type = id_type[:-1]  # Remove nullable indicator
            
            context = {
                "package": repositories_package,
                "model_package": models_package,
                "entity_name": entity["name"],
                "id_type": entity.get("id_type", id_type)
            }
            
            repository_content = self.render_template("spring-boot/kotlin/Repository.kt.j2", context)
            with open(os.path.join(repositories_dir, f"{entity['name']}Repository.kt"), "w") as f:
                f.write(repository_content)
    
    def _generate_application_properties(self, resources_dir: str, config: Dict[str, Any]) -> None:
        """Generate application properties/yml.
        
        Args:
            resources_dir: Directory for resource files
            config: Project configuration dictionary
        """
        use_yaml = "yaml-config" in config.get("features", [])
        
        if use_yaml:
            # Generate application.yml
            context = {"config": config}
            yaml_content = self.render_template("spring-boot/kotlin/application.yml.j2", context)
            with open(os.path.join(resources_dir, "application.yml"), "w") as f:
                f.write(yaml_content)
        else:
            # Generate application.properties
            context = {"config": config}
            props_content = self.render_template("spring-boot/kotlin/application.properties.j2", context)
            with open(os.path.join(resources_dir, "application.properties"), "w") as f:
                f.write(props_content)
    
    def _generate_tests(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate test files.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        # Extract configuration
        package_name = config.get("base_package", "com.example")
        
        # Prepare test directories
        src_test_kotlin = os.path.join(project_dir, "src", "test", "kotlin")
        test_package_path = os.path.join(src_test_kotlin, *package_name.split("."))
        os.makedirs(test_package_path, exist_ok=True)
        
        # Create subdirectories for different test types
        controllers_test_dir = os.path.join(test_package_path, "controllers")
        services_test_dir = os.path.join(test_package_path, "services")
        repositories_test_dir = os.path.join(test_package_path, "repositories")
        
        for directory in [controllers_test_dir, services_test_dir, repositories_test_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Generate application test
        context = {
            "package": package_name,
            "app_name": config.get("project_name", "app"),
        }
        
        app_test_content = self.render_template("spring-boot/kotlin/ApplicationTests.kt.j2", context)
        with open(os.path.join(test_package_path, "ApplicationTests.kt"), "w") as f:
            f.write(app_test_content)
        
        # Generate entity-specific tests
        entities = config.get("entities", [])
        if not entities:
            entities = [{"name": "Sample"}]
        
        for entity in entities:
            # Controller tests
            controller_test_context = {
                "package": f"{package_name}.controllers",
                "model_package": f"{package_name}.models",
                "service_package": f"{package_name}.services",
                "entity_name": entity["name"],
                "entity_var": entity["name"][0].lower() + entity["name"][1:],
                "use_dtos": "generate-dtos" in config.get("features", [])
            }
            
            controller_test_content = self.render_template("spring-boot/kotlin/ControllerTests.kt.j2", controller_test_context)
            with open(os.path.join(controllers_test_dir, f"{entity['name']}ControllerTests.kt"), "w") as f:
                f.write(controller_test_content)
            
            # Service tests
            service_test_context = {
                "package": f"{package_name}.services",
                "model_package": f"{package_name}.models",
                "repository_package": f"{package_name}.repositories",
                "entity_name": entity["name"],
                "entity_var": entity["name"][0].lower() + entity["name"][1:],
                "use_dtos": "generate-dtos" in config.get("features", [])
            }
            
            service_test_content = self.render_template("spring-boot/kotlin/ServiceTests.kt.j2", service_test_context)
            with open(os.path.join(services_test_dir, f"{entity['name']}ServiceTests.kt"), "w") as f:
                f.write(service_test_content)
            
            # Repository tests
            repository_test_context = {
                "package": f"{package_name}.repositories",
                "model_package": f"{package_name}.models",
                "entity_name": entity["name"],
                "entity_var": entity["name"][0].lower() + entity["name"][1:]
            }
            
            repository_test_content = self.render_template("spring-boot/kotlin/RepositoryTests.kt.j2", repository_test_context)
            with open(os.path.join(repositories_test_dir, f"{entity['name']}RepositoryTests.kt"), "w") as f:
                f.write(repository_test_content)
    
    def _get_imports_for_kotlin_entity(self, fields: List[Dict[str, Any]]) -> List[str]:
        """Get the required imports for a Kotlin entity based on its field types.
        
        Args:
            fields: List of field definitions
            
        Returns:
            List[str]: List of import statements
        """
        imports = set(["jakarta.persistence.*"])
        
        for field in fields:
            field_type = field.get("type", "")
            
            # Remove nullable indicator for import checking
            if field_type.endswith("?"):
                field_type = field_type[:-1]
            
            if field_type in ["LocalDate", "LocalDateTime", "LocalTime"]:
                imports.add(f"java.time.{field_type}")
            elif field_type in ["Date", "Timestamp"]:
                imports.add(f"java.sql.{field_type}")
            elif field_type.startswith("List<") or field_type.startswith("Set<") or field_type.startswith("Map<"):
                collection_type = field_type.split("<")[0]
                imports.add(f"java.util.{collection_type}")
                
                # Check for non-primitive types in generics
                inner_types = re.findall(r"<([^,>]+)(?:,\s*([^>]+))?>", field_type)
                if inner_types:
                    for inner_type_group in inner_types:
                        for inner_type in inner_type_group:
                            if inner_type and inner_type not in ["String", "Int", "Long", "Double", "Boolean", "Float", "Short", "Byte"]:
                                # This is a simplification; in a real app we'd need better type resolution
                                if not inner_type.startswith("java.") and not inner_type.startswith("kotlin."):
                                    imports.add(inner_type)
        
        return sorted(list(imports))
    
    def _get_imports_for_kotlin_dto(self, fields: List[Dict[str, Any]]) -> List[str]:
        """Get the required imports for a Kotlin DTO based on its field types.
        
        Args:
            fields: List of field definitions
            
        Returns:
            List[str]: List of import statements
        """
        imports = set()
        
        for field in fields:
            field_type = field.get("type", "")
            
            # Remove nullable indicator for import checking
            if field_type.endswith("?"):
                field_type = field_type[:-1]
            
            if field_type in ["LocalDate", "LocalDateTime", "LocalTime"]:
                imports.add(f"java.time.{field_type}")
            elif field_type in ["Date", "Timestamp"]:
                imports.add(f"java.sql.{field_type}")
            elif field_type.startswith("List<") or field_type.startswith("Set<") or field_type.startswith("Map<"):
                collection_type = field_type.split("<")[0]
                imports.add(f"java.util.{collection_type}")
        
        return sorted(list(imports))
