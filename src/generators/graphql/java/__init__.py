"""GraphQL generator for Java applications."""

import os
import json
from typing import Dict, List, Any, Optional
import re

from microgenesis.generators.base import BaseGenerator
from microgenesis.logging import get_logger


class GraphQLJavaGenerator(BaseGenerator):
    """Generator for GraphQL Java applications."""
    
    def __init__(self):
        """Initialize the GraphQL Java generator."""
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
            "graphql_version": config.get("framework", {}).get("version", "20.0"),
            "java_version": config.get("language", {}).get("version", "17"),
            "description": config.get("description", "Generated GraphQL Java application"),
            "database": config.get("database", {}).get("name", ""),
            "features": config.get("features", []),
        }
        
        # Render pom.xml template
        pom_content = self.render_template("graphql/pom.xml.j2", context)
        with open(os.path.join(project_dir, "pom.xml"), "w") as f:
            f.write(pom_content)
    
    def _generate_gradle_config(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate Gradle configuration (build.gradle).
        
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
            "graphql_version": config.get("framework", {}).get("version", "20.0"),
            "java_version": config.get("language", {}).get("version", "17"),
            "description": config.get("description", "Generated GraphQL Java application"),
            "database": config.get("database", {}).get("name", ""),
            "features": config.get("features", []),
        }
        
        # Render build.gradle template
        build_gradle_content = self.render_template("graphql/build.gradle.j2", context)
        with open(os.path.join(project_dir, "build.gradle"), "w") as f:
            f.write(build_gradle_content)
        
        # Render settings.gradle template
        settings_gradle_content = self.render_template("graphql/settings.gradle.j2", context)
        with open(os.path.join(project_dir, "settings.gradle"), "w") as f:
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
        src_main_java = os.path.join(project_dir, "src", "main", "java")
        package_path = os.path.join(src_main_java, *package_name.split("."))
        os.makedirs(package_path, exist_ok=True)
        
        # Subdirectories for GraphQL components
        resolvers_dir = os.path.join(package_path, "resolvers")
        types_dir = os.path.join(package_path, "types")
        models_dir = os.path.join(package_path, "models")
        repositories_dir = os.path.join(package_path, "repositories")
        
        for directory in [resolvers_dir, types_dir, models_dir, repositories_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Create resources directory for schema files
        resources_dir = os.path.join(project_dir, "src", "main", "resources")
        os.makedirs(resources_dir, exist_ok=True)
        
        # Generate application class
        self._generate_application_class(package_path, package_name, config)
        
        # Generate GraphQL schema file
        self._generate_graphql_schema(resources_dir, config)
        
        # Generate model classes
        self._generate_model_classes(models_dir, package_name, config)
        
        # Generate type classes
        self._generate_type_classes(types_dir, package_name, config)
        
        # Generate resolver classes
        self._generate_resolver_classes(resolvers_dir, package_name, config)
        
        # Generate repository interfaces
        self._generate_repository_interfaces(repositories_dir, package_name, config)
        
        # Generate configuration classes
        self._generate_config_classes(package_path, package_name, config)
    
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
        
        application_content = self.render_template("graphql/java/Application.java.j2", context)
        with open(os.path.join(package_path, "Application.java"), "w") as f:
            f.write(application_content)
    
    def _generate_graphql_schema(self, resources_dir: str, config: Dict[str, Any]) -> None:
        """Generate the GraphQL schema file.
        
        Args:
            resources_dir: Path to the resources directory
            config: Project configuration dictionary
        """
        # Create GraphQL schema directory
        schema_dir = os.path.join(resources_dir, "graphql")
        os.makedirs(schema_dir, exist_ok=True)
        
        # Generate schema file
        schema_content = self.render_template("graphql/resources/schema.graphqls.j2", {"entities": config.get("entities", [])})
        with open(os.path.join(schema_dir, "schema.graphqls"), "w") as f:
            f.write(schema_content)
        
        # Generate application properties/yml
        use_yaml = "yaml-config" in config.get("features", [])
        
        if use_yaml:
            config_content = self.render_template("graphql/resources/application.yml.j2", {"config": config})
            with open(os.path.join(resources_dir, "application.yml"), "w") as f:
                f.write(config_content)
        else:
            config_content = self.render_template("graphql/resources/application.properties.j2", {"config": config})
            with open(os.path.join(resources_dir, "application.properties"), "w") as f:
                f.write(config_content)
    
    def _generate_model_classes(self, models_dir: str, package_name: str, config: Dict[str, Any]) -> None:
        """Generate model classes based on entities.
        
        Args:
            models_dir: Path to the models directory
            package_name: Package name
            config: Project configuration dictionary
        """
        models_package = f"{package_name}.models"
        entities = config.get("entities", [])
        
        if not entities:
            # Generate sample entity if no entities defined
            context = {
                "package": models_package,
                "entity_name": "Sample",
                "fields": [
                    {"name": "id", "type": "String", "annotations": ["@Id"]},
                    {"name": "name", "type": "String", "annotations": []},
                    {"name": "description", "type": "String", "annotations": []},
                    {"name": "createdAt", "type": "LocalDateTime", "annotations": []}
                ],
                "imports": ["java.time.LocalDateTime"]
            }
            
            model_content = self.render_template("graphql/java/Model.java.j2", context)
            with open(os.path.join(models_dir, "Sample.java"), "w") as f:
                f.write(model_content)
        else:
            # Generate entities from configuration
            for entity in entities:
                context = {
                    "package": models_package,
                    "entity_name": entity["name"],
                    "fields": entity["fields"],
                    "imports": self._get_imports_for_entity(entity)
                }
                
                model_content = self.render_template("graphql/java/Model.java.j2", context)
                with open(os.path.join(models_dir, f"{entity['name']}.java"), "w") as f:
                    f.write(model_content)
    
    def _generate_type_classes(self, types_dir: str, package_name: str, config: Dict[str, Any]) -> None:
        """Generate GraphQL type classes.
        
        Args:
            types_dir: Path to the types directory
            package_name: Package name
            config: Project configuration dictionary
        """
        types_package = f"{package_name}.types"
        models_package = f"{package_name}.models"
        entities = config.get("entities", [])
        
        if not entities:
            # Generate sample type if no entities defined
            context = {
                "package": types_package,
                "model_package": models_package,
                "type_name": "SampleType",
                "entity_name": "Sample"
            }
            
            type_content = self.render_template("graphql/java/Type.java.j2", context)
            with open(os.path.join(types_dir, "SampleType.java"), "w") as f:
                f.write(type_content)
        else:
            # Generate type classes from configuration
            for entity in entities:
                context = {
                    "package": types_package,
                    "model_package": models_package,
                    "type_name": f"{entity['name']}Type",
                    "entity_name": entity["name"]
                }
                
                type_content = self.render_template("graphql/java/Type.java.j2", context)
                with open(os.path.join(types_dir, f"{entity['name']}Type.java"), "w") as f:
                    f.write(type_content)
    
    def _generate_resolver_classes(self, resolvers_dir: str, package_name: str, config: Dict[str, Any]) -> None:
        """Generate GraphQL resolver classes.
        
        Args:
            resolvers_dir: Path to the resolvers directory
            package_name: Package name
            config: Project configuration dictionary
        """
        resolvers_package = f"{package_name}.resolvers"
        models_package = f"{package_name}.models"
        repos_package = f"{package_name}.repositories"
        entities = config.get("entities", [])
        
        # Generate query resolver
        context = {
            "package": resolvers_package,
            "model_package": models_package,
            "repository_package": repos_package,
            "entities": entities if entities else [{"name": "Sample"}]
        }
        
        query_content = self.render_template("graphql/java/QueryResolver.java.j2", context)
        with open(os.path.join(resolvers_dir, "QueryResolver.java"), "w") as f:
            f.write(query_content)
        
        # Generate mutation resolver
        mutation_content = self.render_template("graphql/java/MutationResolver.java.j2", context)
        with open(os.path.join(resolvers_dir, "MutationResolver.java"), "w") as f:
            f.write(mutation_content)
    
    def _generate_repository_interfaces(self, repositories_dir: str, package_name: str, config: Dict[str, Any]) -> None:
        """Generate repository interfaces.
        
        Args:
            repositories_dir: Path to the repositories directory
            package_name: Package name
            config: Project configuration dictionary
        """
        repos_package = f"{package_name}.repositories"
        models_package = f"{package_name}.models"
        entities = config.get("entities", [])
        
        if not entities:
            # Generate sample repository if no entities defined
            context = {
                "package": repos_package,
                "model_package": models_package,
                "entity_name": "Sample",
                "id_type": "String"
            }
            
            repo_content = self.render_template("graphql/java/Repository.java.j2", context)
            with open(os.path.join(repositories_dir, "SampleRepository.java"), "w") as f:
                f.write(repo_content)
        else:
            # Generate repository interfaces from configuration
            for entity in entities:
                id_field = next((f for f in entity.get("fields", []) if f.get("name") == "id"), {"type": "String"})
                
                context = {
                    "package": repos_package,
                    "model_package": models_package,
                    "entity_name": entity["name"],
                    "id_type": id_field.get("type", "String")
                }
                
                repo_content = self.render_template("graphql/java/Repository.java.j2", context)
                with open(os.path.join(repositories_dir, f"{entity['name']}Repository.java"), "w") as f:
                    f.write(repo_content)
    
    def _generate_config_classes(self, package_path: str, package_name: str, config: Dict[str, Any]) -> None:
        """Generate configuration classes.
        
        Args:
            package_path: Path to the package directory
            package_name: Package name
            config: Project configuration dictionary
        """
        # Create config directory
        config_dir = os.path.join(package_path, "config")
        os.makedirs(config_dir, exist_ok=True)
        
        # Generate GraphQL configuration
        context = {
            "package": f"{package_name}.config",
            "base_package": package_name
        }
        
        graphql_config_content = self.render_template("graphql/java/GraphQLConfig.java.j2", context)
        with open(os.path.join(config_dir, "GraphQLConfig.java"), "w") as f:
            f.write(graphql_config_content)
    
    def _generate_tests(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate test files.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        package_name = config.get("base_package", "com.example")
        
        # Prepare test directories
        test_dir = os.path.join(project_dir, "src", "test", "java")
        test_package_path = os.path.join(test_dir, *package_name.split("."))
        os.makedirs(test_package_path, exist_ok=True)
        
        # Generate application tests
        context = {
            "package": package_name,
            "app_name": config.get("project_name", "app"),
        }
        
        test_content = self.render_template("graphql/java/ApplicationTests.java.j2", context)
        with open(os.path.join(test_package_path, "ApplicationTests.java"), "w") as f:
            f.write(test_content)
        
        # Generate resolver tests
        resolvers_test_dir = os.path.join(test_package_path, "resolvers")
        os.makedirs(resolvers_test_dir, exist_ok=True)
        
        entities = config.get("entities", [])
        if not entities:
            entities = [{"name": "Sample"}]
        
        for entity in entities:
            context = {
                "package": f"{package_name}.resolvers",
                "entity_name": entity["name"]
            }
            
            resolver_test_content = self.render_template("graphql/java/ResolverTests.java.j2", context)
            with open(os.path.join(resolvers_test_dir, f"{entity['name']}ResolverTests.java"), "w") as f:
                f.write(resolver_test_content)
    
    def _get_imports_for_entity(self, entity: Dict[str, Any]) -> List[str]:
        """Get the required imports for an entity based on its field types.
        
        Args:
            entity: Entity definition dictionary
            
        Returns:
            List[str]: List of import statements
        """
        imports = set()
        
        for field in entity.get("fields", []):
            field_type = field.get("type", "")
            
            if field_type in ["LocalDate", "LocalDateTime"]:
                imports.add(f"java.time.{field_type}")
            elif field_type in ["Date", "Timestamp"]:
                imports.add(f"java.sql.{field_type}")
            elif field_type.startswith("List<") or field_type.startswith("Set<"):
                imports.add("java.util." + field_type.split("<")[0])
                
                # Add import for the type inside the collection if it's not a primitive
                inner_type = re.search(r"<([^>]+)>", field_type)
                if inner_type and inner_type.group(1) not in ["String", "Integer", "Long", "Double", "Boolean"]:
                    # Assuming it's from the same package
                    imports.add(f"{entity.get('package', '')}.{inner_type.group(1)}")
            
            # Add imports for annotations
            for annotation in field.get("annotations", []):
                if annotation == "@Id":
                    imports.add("jakarta.persistence.Id")
        
        return sorted(list(imports))
