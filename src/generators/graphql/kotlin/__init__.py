"""GraphQL Kotlin generator for implementing GraphQL APIs using Kotlin.

This module provides code generation for GraphQL APIs using Kotlin and the GraphQL Kotlin library.
"""

import os
from typing import Dict, List, Any, Optional

from src.generators.base import BaseGenerator
from src.generators.architecture import ServiceArchitecture
from src.core.logging import get_logger


class GraphQLKotlinGenerator(BaseGenerator):
    """Generator for GraphQL Kotlin applications."""
    
    def __init__(self):
        """Initialize the GraphQL Kotlin generator."""
        super().__init__()
        self.logger = get_logger()
    
    def _generate_build_config(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate build configuration files.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        build_system = config.get("build_system", {}).get("name", "gradle")
        
        if build_system == "gradle":
            self._generate_gradle_config(project_dir, config)
        elif build_system == "maven":
            self._generate_maven_config(project_dir, config)
        else:
            self.logger.warning(f"Unsupported build system: {build_system}")
    
    def _generate_gradle_config(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate Gradle configuration for GraphQL Kotlin.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        # Get safe database config
        database_config = self.get_safe_database_config(config)
        
        # Prepare context for template rendering
        context = {
            "project": config.get("project_name", "app"),
            "group_id": config.get("base_package", "com.example"),
            "artifact_id": config.get("project_name", "app").lower(),
            "version": config.get("project_version", "0.1.0"),
            "graphql_kotlin_version": config.get("framework", {}).get("version", "6.0.0"),
            "kotlin_version": config.get("language", {}).get("version", "1.6.10"),
            "description": config.get("description", "Generated GraphQL Kotlin application"),
            "database": database_config.get("name", ""),
            "features": config.get("features", []),
        }
        
        # Render build.gradle.kts template
        build_gradle_content = self.render_template("graphql/kotlin/build.gradle.kts.j2", context)
        with open(os.path.join(project_dir, "build.gradle.kts"), "w") as f:
            f.write(build_gradle_content)
        
        # Render settings.gradle.kts template
        settings_gradle_content = self.render_template("graphql/kotlin/settings.gradle.kts.j2", context)
        with open(os.path.join(project_dir, "settings.gradle.kts"), "w") as f:
            f.write(settings_gradle_content)
        
        # Add Gradle wrapper
        gradle_wrapper_dir = os.path.join(project_dir, "gradle", "wrapper")
        os.makedirs(gradle_wrapper_dir, exist_ok=True)
        
        gradle_wrapper_props = self.render_template("common/gradle-wrapper.properties.j2", context)
        with open(os.path.join(gradle_wrapper_dir, "gradle-wrapper.properties"), "w") as f:
            f.write(gradle_wrapper_props)
        
        gradlew_content = self.render_template("common/gradlew.j2", {})
        with open(os.path.join(project_dir, "gradlew"), "w") as f:
            f.write(gradlew_content)
        
        gradlew_bat_content = self.render_template("common/gradlew.bat.j2", {})
        with open(os.path.join(project_dir, "gradlew.bat"), "w") as f:
            f.write(gradlew_bat_content)
    
    def _generate_maven_config(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate Maven configuration for GraphQL Kotlin.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        # Get safe database config
        database_config = self.get_safe_database_config(config)
        
        # Prepare context for template rendering
        context = {
            "project": config.get("project_name", "app"),
            "group_id": config.get("base_package", "com.example"),
            "artifact_id": config.get("project_name", "app").lower(),
            "version": config.get("project_version", "0.1.0"),
            "graphql_kotlin_version": config.get("framework", {}).get("version", "6.0.0"),
            "kotlin_version": config.get("language", {}).get("version", "1.6.10"),
            "description": config.get("description", "Generated GraphQL Kotlin application"),
            "database": database_config.get("name", ""),
            "features": config.get("features", []),
        }
        
        # Render pom.xml template
        pom_content = self.render_template("graphql/kotlin/pom.xml.j2", context)
        with open(os.path.join(project_dir, "pom.xml"), "w") as f:
            f.write(pom_content)
    
    def _generate_source_code(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate source code files.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        base_package = config.get("base_package", "com.example")
        base_package_path = base_package.replace(".", os.path.sep)
        project_name = config.get("project_name", "app")
        
        # Main source directories
        src_main_kotlin = os.path.join(project_dir, "src", "main", "kotlin", base_package_path)
        os.makedirs(src_main_kotlin, exist_ok=True)
        
        src_main_resources = os.path.join(project_dir, "src", "main", "resources")
        os.makedirs(src_main_resources, exist_ok=True)
        
        # Get the appropriate architecture implementation
        service_type = config.get("service_type", "domain-driven")
        architecture = ServiceArchitecture.get_architecture(service_type)
        
        # Create architecture-specific directory structure
        architecture.create_directory_structure(src_main_kotlin, config)
        
        # Add architecture-specific context
        context = {
            "base_package": base_package,
            "project_name": project_name,
            "application_name": self._to_pascal_case(project_name) + "Application",
            "database": self.get_safe_database_config(config),
            "features": config.get("features", []),
            "service_type": service_type,
            "package_structure": architecture.get_package_structure()
        }
        
        # Add architecture-specific context additions
        context.update(architecture.get_template_context_additions(config))
        
        # Generate application class
        app_class_content = self.render_template("graphql/kotlin/Application.kt.j2", context)
        with open(os.path.join(src_main_kotlin, f"{context['application_name']}.kt"), "w") as f:
            f.write(app_class_content)
        
        # Generate GraphQL schema
        self._generate_graphql_schema(src_main_resources, context, config)
        
        # Generate GraphQL types
        self._generate_graphql_types(src_main_kotlin, context, config)
        
        # Generate resolvers
        self._generate_graphql_resolvers(src_main_kotlin, context, config)
        
        # Generate configuration
        self._generate_application_config(src_main_resources, context, config)
        
        # Generate models, services, etc. from swagger if provided
        swagger_path = config.get("swagger_file")
        if swagger_path:
            self._generate_from_swagger(src_main_kotlin, swagger_path, context, config)
        else:
            # Generate sample code
            self._generate_sample_code(src_main_kotlin, context, config)
    
    def _generate_graphql_schema(self, resources_dir: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate GraphQL schema file.
        
        Args:
            resources_dir: Resources directory
            context: Template rendering context
            config: Project configuration
        """
        graphql_dir = os.path.join(resources_dir, "graphql")
        os.makedirs(graphql_dir, exist_ok=True)
        
        schema_content = self.render_template("graphql/resources/schema.graphqls.j2", context)
        with open(os.path.join(graphql_dir, "schema.graphqls"), "w") as f:
            f.write(schema_content)
    
    def _generate_graphql_types(self, src_main_kotlin: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate GraphQL type definitions.
        
        Args:
            src_main_kotlin: Kotlin source directory
            context: Template rendering context
            config: Project configuration
        """
        service_type = config.get("service_type", "domain-driven")
        base_package = context.get("base_package")
        
        # For DDD architecture, generate types in domain layer
        if service_type == "domain-driven":
            types_dir = os.path.join(src_main_kotlin, "domain", "model")
        else:
            types_dir = os.path.join(src_main_kotlin, "model")
        
        os.makedirs(types_dir, exist_ok=True)
        
        # Generate sample types
        sample_type_content = self.render_template(f"graphql/kotlin/{service_type}/model/SampleType.kt.j2", context)
        with open(os.path.join(types_dir, "SampleType.kt"), "w") as f:
            f.write(sample_type_content)
    
    def _generate_graphql_resolvers(self, src_main_kotlin: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate GraphQL resolvers.
        
        Args:
            src_main_kotlin: Kotlin source directory
            context: Template rendering context
            config: Project configuration
        """
        service_type = config.get("service_type", "domain-driven")
        
        # For DDD architecture, generate resolvers in interfaces layer
        if service_type == "domain-driven":
            resolvers_dir = os.path.join(src_main_kotlin, "interfaces", "graphql")
        else:
            resolvers_dir = os.path.join(src_main_kotlin, "resolver")
        
        os.makedirs(resolvers_dir, exist_ok=True)
        
        # Generate query resolver
        query_resolver_content = self.render_template(f"graphql/kotlin/{service_type}/resolver/QueryResolver.kt.j2", context)
        with open(os.path.join(resolvers_dir, "QueryResolver.kt"), "w") as f:
            f.write(query_resolver_content)
        
        # Generate mutation resolver
        mutation_resolver_content = self.render_template(f"graphql/kotlin/{service_type}/resolver/MutationResolver.kt.j2", context)
        with open(os.path.join(resolvers_dir, "MutationResolver.kt"), "w") as f:
            f.write(mutation_resolver_content)
    
    def _generate_application_config(self, resources_dir: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate application configuration files.
        
        Args:
            resources_dir: Resources directory
            context: Template rendering context
            config: Project configuration
        """
        # Generate application.yml
        app_yml_content = self.render_template("graphql/resources/application.yml.j2", context)
        with open(os.path.join(resources_dir, "application.yml"), "w") as f:
            f.write(app_yml_content)
    
    def _generate_sample_code(self, src_main_kotlin: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate sample code for the application.
        
        Args:
            src_main_kotlin: Kotlin source directory
            context: Template rendering context
            config: Project configuration
        """
        service_type = config.get("service_type", "domain-driven")
        
        # Sample implementations will be created based on the architecture type
        if service_type == "domain-driven":
            # Generate domain entities
            self._generate_domain_entities(src_main_kotlin, context, config)
            
            # Generate application services
            self._generate_application_services(src_main_kotlin, context, config)
            
            # Generate infrastructure components
            self._generate_infrastructure_components(src_main_kotlin, context, config)
        else:
            # Generate standard models and services
            self._generate_standard_models(src_main_kotlin, context, config)
            self._generate_standard_services(src_main_kotlin, context, config)
    
    def _generate_from_swagger(self, src_main_kotlin: str, swagger_path: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate code from Swagger/OpenAPI specification.
        
        Args:
            src_main_kotlin: Kotlin source directory
            swagger_path: Path to Swagger/OpenAPI file
            context: Template rendering context
            config: Project configuration
        """
        api_info = self.parse_swagger_file(swagger_path)
        if not api_info:
            self.logger.warning(f"Could not parse Swagger file: {swagger_path}")
            self._generate_sample_code(src_main_kotlin, context, config)
            return
        
        # Add API info to context
        context.update({"api": api_info})
        
        service_type = config.get("service_type", "domain-driven")
        
        # Generate models from schemas
        if service_type == "domain-driven":
            self._generate_domain_models_from_swagger(src_main_kotlin, context, config)
        else:
            self._generate_models_from_swagger(src_main_kotlin, context, config)
        
        # Generate resolvers from endpoints
        self._generate_resolvers_from_swagger(src_main_kotlin, context, config)
    
    def _generate_tests(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate test files.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        base_package = config.get("base_package", "com.example")
        base_package_path = base_package.replace(".", os.path.sep)
        project_name = config.get("project_name", "app")
        
        # Test source directories
        src_test_kotlin = os.path.join(project_dir, "src", "test", "kotlin", base_package_path)
        os.makedirs(src_test_kotlin, exist_ok=True)
        
        src_test_resources = os.path.join(project_dir, "src", "test", "resources")
        os.makedirs(src_test_resources, exist_ok=True)
        
        # Context for template rendering
        context = {
            "base_package": base_package,
            "project_name": project_name,
            "application_name": self._to_pascal_case(project_name) + "Application",
        }
        
        # Generate application test
        app_test_content = self.render_template("graphql/kotlin/ApplicationTest.kt.j2", context)
        with open(os.path.join(src_test_kotlin, f"{context['application_name']}Test.kt"), "w") as f:
            f.write(app_test_content)
        
        # Generate test schema executor
        schema_test_content = self.render_template("graphql/kotlin/SchemaTest.kt.j2", context)
        with open(os.path.join(src_test_kotlin, "SchemaTest.kt"), "w") as f:
            f.write(schema_test_content)
        
        # Generate test properties
        test_yaml_content = self.render_template("graphql/resources/application-test.yml.j2", context)
        with open(os.path.join(src_test_resources, "application-test.yml"), "w") as f:
            f.write(test_yaml_content)
    
    # Helper methods for generating specific types of code
    
    def _generate_domain_entities(self, src_main_kotlin: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate domain entities for DDD architecture.
        
        Args:
            src_main_kotlin: Kotlin source directory
            context: Template rendering context
            config: Project configuration
        """
        domain_model_dir = os.path.join(src_main_kotlin, "domain", "model")
        os.makedirs(domain_model_dir, exist_ok=True)
        
        # Generate sample entity
        entity_content = self.render_template("graphql/kotlin/domain-driven/model/Entity.kt.j2", context)
        with open(os.path.join(domain_model_dir, "Entity.kt"), "w") as f:
            f.write(entity_content)
        
        # Generate value objects if the architecture has them
        if context.get("has_value_objects"):
            vo_dir = os.path.join(src_main_kotlin, "domain", "valueobject")
            os.makedirs(vo_dir, exist_ok=True)
            
            vo_content = self.render_template("graphql/kotlin/domain-driven/valueobject/ValueObject.kt.j2", context)
            with open(os.path.join(vo_dir, "ValueObject.kt"), "w") as f:
                f.write(vo_content)
        
        # Generate domain events if the architecture has them
        if context.get("has_domain_events"):
            event_dir = os.path.join(src_main_kotlin, "domain", "event")
            os.makedirs(event_dir, exist_ok=True)
            
            event_content = self.render_template("graphql/kotlin/domain-driven/event/DomainEvent.kt.j2", context)
            with open(os.path.join(event_dir, "DomainEvent.kt"), "w") as f:
                f.write(event_content)
    
    def _generate_application_services(self, src_main_kotlin: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate application services for DDD architecture.
        
        Args:
            src_main_kotlin: Kotlin source directory
            context: Template rendering context
            config: Project configuration
        """
        app_service_dir = os.path.join(src_main_kotlin, "application", "service")
        os.makedirs(app_service_dir, exist_ok=True)
        
        dto_dir = os.path.join(src_main_kotlin, "application", "dto")
        os.makedirs(dto_dir, exist_ok=True)
        
        # Generate sample application service
        service_content = self.render_template("graphql/kotlin/domain-driven/application/service/ApplicationService.kt.j2", context)
        with open(os.path.join(app_service_dir, "ApplicationService.kt"), "w") as f:
            f.write(service_content)
        
        # Generate sample DTOs
        dto_content = self.render_template("graphql/kotlin/domain-driven/application/dto/DTOs.kt.j2", context)
        with open(os.path.join(dto_dir, "DTOs.kt"), "w") as f:
            f.write(dto_content)
    
    def _generate_infrastructure_components(self, src_main_kotlin: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate infrastructure components for DDD architecture.
        
        Args:
            src_main_kotlin: Kotlin source directory
            context: Template rendering context
            config: Project configuration
        """
        infra_persistence_dir = os.path.join(src_main_kotlin, "infrastructure", "persistence")
        os.makedirs(infra_persistence_dir, exist_ok=True)
        
        # Generate repository implementation
        repo_impl_content = self.render_template("graphql/kotlin/domain-driven/infrastructure/persistence/RepositoryImpl.kt.j2", context)
        with open(os.path.join(infra_persistence_dir, "RepositoryImpl.kt"), "w") as f:
            f.write(repo_impl_content)
    
    def _generate_standard_models(self, src_main_kotlin: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate standard models for non-DDD architectures.
        
        Args:
            src_main_kotlin: Kotlin source directory
            context: Template rendering context
            config: Project configuration
        """
        model_dir = os.path.join(src_main_kotlin, "model")
        os.makedirs(model_dir, exist_ok=True)
        
        # Generate model class
        model_content = self.render_template("graphql/kotlin/entity-driven/model/Model.kt.j2", context)
        with open(os.path.join(model_dir, "Model.kt"), "w") as f:
            f.write(model_content)
    
    def _generate_standard_services(self, src_main_kotlin: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate standard services for non-DDD architectures.
        
        Args:
            src_main_kotlin: Kotlin source directory
            context: Template rendering context
            config: Project configuration
        """
        service_dir = os.path.join(src_main_kotlin, "service")
        os.makedirs(service_dir, exist_ok=True)
        
        # Generate service class
        service_content = self.render_template("graphql/kotlin/entity-driven/service/Service.kt.j2", context)
        with open(os.path.join(service_dir, "Service.kt"), "w") as f:
            f.write(service_content)
