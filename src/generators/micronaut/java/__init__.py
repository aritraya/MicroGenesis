"""Micronaut generator for Java applications."""

import os
import json
from typing import Dict, List, Any, Optional
import re

from src.generators.base import BaseGenerator
from src.core.logging import get_logger


class MicronautJavaGenerator(BaseGenerator):
    """Generator for Micronaut Java applications."""
    
    def __init__(self):
        """Initialize the Micronaut Java generator."""
        super().__init__()
        self.logger = get_logger()
    
    def _generate_build_config(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate build configuration files.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        build_system = config.get("build_system", "gradle")
        
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
            "micronaut_version": config.get("framework", {}).get("version", "3.7.0"),
            "java_version": config.get("language", {}).get("version", "17"),
            "description": config.get("description", "Generated Micronaut application"),
            "database": config.get("database", {}).get("name", ""),
            "features": config.get("features", []),
        }
        # Render pom.xml template
        pom_content = self.render_template("build-systems/maven/micronaut/pom.xml.j2", context)
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
            "micronaut_version": config.get("framework", {}).get("version", "3.7.0"),
            "java_version": config.get("language", {}).get("version", "17"),
            "description": config.get("description", "Generated Micronaut application"),
            "database": config.get("database", {}).get("name", ""),
            "features": config.get("features", []),
        }
          # Render build.gradle template
        build_gradle_content = self.render_template("build-systems/gradle/groovy/build.gradle.j2", context)
        with open(os.path.join(project_dir, "build.gradle"), "w") as f:
            f.write(build_gradle_content)
        
        # Render settings.gradle template
        settings_gradle_content = self.render_template("build-systems/gradle/groovy/settings.gradle.j2", context)
        with open(os.path.join(project_dir, "settings.gradle"), "w") as f:
            f.write(settings_gradle_content)
        
        # Add Gradle wrapper
        gradle_wrapper_dir = os.path.join(project_dir, "gradle", "wrapper")
        os.makedirs(gradle_wrapper_dir, exist_ok=True)
        gradle_wrapper_props = self.render_template("build-systems/gradle/gradle-wrapper.properties.j2", context)
        with open(os.path.join(gradle_wrapper_dir, "gradle-wrapper.properties"), "w") as f:
            f.write(gradle_wrapper_props)
        
        gradlew_content = self.render_template("build-systems/gradle/gradlew.j2", {})
        with open(os.path.join(project_dir, "gradlew"), "w") as f:
            f.write(gradlew_content)
        
        gradlew_bat_content = self.render_template("build-systems/gradle/gradlew.bat.j2", {})
        with open(os.path.join(project_dir, "gradlew.bat"), "w") as f:
            f.write(gradlew_bat_content)
    
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
        src_main_java = os.path.join(project_dir, "src", "main", "java", base_package_path)
        os.makedirs(src_main_java, exist_ok=True)
        
        src_main_resources = os.path.join(project_dir, "src", "main", "resources")
        os.makedirs(src_main_resources, exist_ok=True)
        
        # Create standard directories
        for dir_name in ["controller", "service", "repository", "domain", "dto", "config", "exception"]:
            os.makedirs(os.path.join(src_main_java, dir_name), exist_ok=True)
        
        # Context for template rendering
        context = {
            "base_package": base_package,
            "project_name": project_name,
            "application_name": self._to_pascal_case(project_name) + "Application",
            "database": config.get("database", {}),
            "features": config.get("features", []),
            "service_type": config.get("service_type", "domain-driven"),
        }
          # Generate application class
        app_class_content = self.render_template("frameworks/micronaut/java/Application.java.j2", context)
        with open(os.path.join(src_main_java, f"{context['application_name']}.java"), "w") as f:
            f.write(app_class_content)
        
        # Generate configuration
        self._generate_application_config(src_main_resources, context, config)
        
        # Generate models, controllers, services, etc. from swagger if provided
        swagger_path = config.get("swagger_file")
        if swagger_path:
            self._generate_from_swagger(src_main_java, swagger_path, context, config)
        else:
            # Generate sample code
            self._generate_sample_code(src_main_java, context, config)
    
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
        src_test_java = os.path.join(project_dir, "src", "test", "java", base_package_path)
        os.makedirs(src_test_java, exist_ok=True)
        
        src_test_resources = os.path.join(project_dir, "src", "test", "resources")
        os.makedirs(src_test_resources, exist_ok=True)
        
        # Create test directories
        for dir_name in ["controller", "service", "repository"]:
            os.makedirs(os.path.join(src_test_java, dir_name), exist_ok=True)
        
        # Context for template rendering
        context = {
            "base_package": base_package,
            "project_name": project_name,
            "application_name": self._to_pascal_case(project_name) + "Application",
        }
          # Generate application tests
        app_test_content = self.render_template("frameworks/micronaut/java/ApplicationTest.java.j2", context)
        with open(os.path.join(src_test_java, f"{context['application_name']}Test.java"), "w") as f:
            f.write(app_test_content)
        
        # Generate test configuration
        test_properties = self.render_template("frameworks/micronaut/resources/application-test.yml.j2", context)
        with open(os.path.join(src_test_resources, "application-test.yml"), "w") as f:
            f.write(test_properties)
        
        # Generate sample tests
        swagger_path = config.get("swagger_file")
        if swagger_path:
            self._generate_tests_from_swagger(src_test_java, swagger_path, context, config)
    
    def _generate_application_config(self, resources_dir: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate application configuration files.
        
        Args:
            resources_dir: Resources directory path
            context: Template rendering context
            config: Project configuration dictionary
        """        # Micronaut typically uses YAML for configuration
        app_config = self.render_template("frameworks/micronaut/resources/application.yml.j2", context)
        with open(os.path.join(resources_dir, "application.yml"), "w") as f:
            f.write(app_config)
        
        # Generate logback configuration if needed
        if any(feature == "logging" for feature in config.get("features", [])):
            logback_config = self.render_template("frameworks/micronaut/resources/logback.xml.j2", context)
            with open(os.path.join(resources_dir, "logback.xml"), "w") as f:
                f.write(logback_config)
    
    def _generate_from_swagger(self, src_dir: str, swagger_path: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate code from Swagger/OpenAPI definition.
        
        Args:
            src_dir: Source directory for generated code
            swagger_path: Path to the Swagger/OpenAPI definition file
            context: Template rendering context
            config: Project configuration dictionary
        """
        api_info = self.parse_swagger_file(swagger_path)
        if not api_info:
            self.logger.warning("Failed to parse Swagger file or empty API definition")
            return
        
        # Generate domain classes (models)
        self._generate_domain_classes(src_dir, api_info, context, config)
        
        # Generate DTOs
        self._generate_dtos(src_dir, api_info, context, config)
        
        # Generate controllers
        self._generate_controllers(src_dir, api_info, context, config)
        
        # Generate services
        self._generate_services(src_dir, api_info, context, config)
        
        # Generate repositories
        self._generate_repositories(src_dir, api_info, context, config)
        
        # Generate mappers
        self._generate_mappers(src_dir, api_info, context, config)
    
    def _generate_domain_classes(self, src_dir: str, api_info: Dict[str, Any], context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate domain classes from API info.
        
        Args:
            src_dir: Source directory for generated code
            api_info: API information extracted from Swagger
            context: Template rendering context
            config: Project configuration dictionary
        """
        domain_dir = os.path.join(src_dir, "domain")
        
        for model_name, model_info in api_info.get("models", {}).items():
            if model_info["type"] == "entity":
                # Prepare model context
                model_context = {**context, "model": model_info}
                  # Generate entity class
                entity_content = self.render_template("frameworks/micronaut/java/Entity.java.j2", model_context)
                with open(os.path.join(domain_dir, f"{model_name}.java"), "w") as f:
                    f.write(entity_content)
    
    def _generate_dtos(self, src_dir: str, api_info: Dict[str, Any], context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate DTO classes from API info.
        
        Args:
            src_dir: Source directory for generated code
            api_info: API information extracted from Swagger
            context: Template rendering context
            config: Project configuration dictionary
        """
        dto_dir = os.path.join(src_dir, "dto")
        
        for model_name, model_info in api_info.get("models", {}).items():
            if model_info["type"] == "dto" or any(feature == "generate-dtos" for feature in config.get("features", [])):
                # Prepare DTO context
                dto_context = {**context, "dto": model_info}
                  # Generate DTO class
                dto_content = self.render_template("frameworks/micronaut/java/DTO.java.j2", dto_context)
                with open(os.path.join(dto_dir, f"{model_name}.java"), "w") as f:
                    f.write(dto_content)
    
    def _generate_controllers(self, src_dir: str, api_info: Dict[str, Any], context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate controller classes from API info.
        
        Args:
            src_dir: Source directory for generated code
            api_info: API information extracted from Swagger
            context: Template rendering context
            config: Project configuration dictionary
        """
        controller_dir = os.path.join(src_dir, "controller")
        
        # Group endpoints by tag
        endpoints_by_tag = {}
        for endpoint in api_info.get("endpoints", []):
            tags = endpoint.get("tags", ["Default"])
            for tag in tags:
                if tag not in endpoints_by_tag:
                    endpoints_by_tag[tag] = []
                endpoints_by_tag[tag].append(endpoint)
        
        # Generate controller per tag
        for tag, endpoints in endpoints_by_tag.items():
            controller_name = self._to_pascal_case(tag) + "Controller"
            
            # Prepare controller context
            controller_context = {
                **context,
                "controller_name": controller_name,
                "tag": tag,
                "endpoints": endpoints
            }
              # Generate controller class
            controller_content = self.render_template("frameworks/micronaut/java/Controller.java.j2", controller_context)
            with open(os.path.join(controller_dir, f"{controller_name}.java"), "w") as f:
                f.write(controller_content)
    
    def _generate_services(self, src_dir: str, api_info: Dict[str, Any], context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate service classes from API info.
        
        Args:
            src_dir: Source directory for generated code
            api_info: API information extracted from Swagger
            context: Template rendering context
            config: Project configuration dictionary
        """
        service_dir = os.path.join(src_dir, "service")
        service_type = config.get("service_type", "domain-driven")
        
        # Create impl directory
        impl_dir = os.path.join(service_dir, "impl") 
        os.makedirs(impl_dir, exist_ok=True)
        
        # Group endpoints by tag (similar to controllers)
        endpoints_by_tag = {}
        for endpoint in api_info.get("endpoints", []):
            tags = endpoint.get("tags", ["Default"])
            for tag in tags:
                if tag not in endpoints_by_tag:
                    endpoints_by_tag[tag] = []
                endpoints_by_tag[tag].append(endpoint)
        
        # Generate service interfaces and implementations
        for tag, endpoints in endpoints_by_tag.items():
            service_name = self._to_pascal_case(tag) + "Service"
            impl_name = service_name + "Impl"
            
            # Prepare service context
            service_context = {
                **context,
                "service_name": service_name,
                "impl_name": impl_name,
                "tag": tag,
                "endpoints": endpoints,
                "service_type": service_type
            }
              # Generate service interface
            service_content = self.render_template("frameworks/micronaut/java/Service.java.j2", service_context)
            with open(os.path.join(service_dir, f"{service_name}.java"), "w") as f:
                f.write(service_content)
            
            # Generate service implementation
            impl_content = self.render_template("frameworks/micronaut/java/ServiceImpl.java.j2", service_context)
            with open(os.path.join(impl_dir, f"{impl_name}.java"), "w") as f:
                f.write(impl_content)
    
    def _generate_repositories(self, src_dir: str, api_info: Dict[str, Any], context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate repository interfaces from API info.
        
        Args:
            src_dir: Source directory for generated code
            api_info: API information extracted from Swagger
            context: Template rendering context
            config: Project configuration dictionary
        """
        repo_dir = os.path.join(src_dir, "repository")
        
        for model_name, model_info in api_info.get("models", {}).items():
            if model_info["type"] == "entity":
                # Prepare repository context
                repo_context = {
                    **context,
                    "model": model_info,
                    "repository_name": f"{model_name}Repository"
                }
                  # Generate repository interface
                repo_content = self.render_template("frameworks/micronaut/java/Repository.java.j2", repo_context)
                with open(os.path.join(repo_dir, f"{repo_context['repository_name']}.java"), "w") as f:
                    f.write(repo_content)
    
    def _generate_mappers(self, src_dir: str, api_info: Dict[str, Any], context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate mapper classes for entity-DTO conversion.
        
        Args:
            src_dir: Source directory for generated code
            api_info: API information extracted from Swagger
            context: Template rendering context
            config: Project configuration dictionary
        """
        # Create mapper directory
        mapper_dir = os.path.join(src_dir, "mapper")
        os.makedirs(mapper_dir, exist_ok=True)
        
        entities = [name for name, info in api_info.get("models", {}).items() if info["type"] == "entity"]
        dtos = [name for name, info in api_info.get("models", {}).items() if info["type"] == "dto"]
        
        # Match entities with DTOs and generate mappers
        for entity_name in entities:
            # Find matching DTOs (e.g., UserDTO matches User)
            matching_dtos = [dto for dto in dtos if entity_name in dto]
            
            if matching_dtos:
                for dto_name in matching_dtos:
                    # Prepare mapper context
                    mapper_context = {
                        **context,
                        "entity": api_info["models"][entity_name],
                        "dto": api_info["models"].get(dto_name, {}),
                        "mapper_name": f"{entity_name}Mapper",
                        "entity_name": entity_name,
                        "dto_name": dto_name
                    }
                      # Generate mapper class - Micronaut usually uses Mapstruct
                    mapper_content = self.render_template("frameworks/micronaut/java/Mapper.java.j2", mapper_context)
                    with open(os.path.join(mapper_dir, f"{mapper_context['mapper_name']}.java"), "w") as f:
                        f.write(mapper_content)
    
    def _generate_tests_from_swagger(self, test_dir: str, swagger_path: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate tests from Swagger/OpenAPI definition.
        
        Args:
            test_dir: Test directory for generated code
            swagger_path: Path to the Swagger/OpenAPI definition file
            context: Template rendering context
            config: Project configuration dictionary
        """
        api_info = self.parse_swagger_file(swagger_path)
        if not api_info:
            return
        
        # Group endpoints by tag
        endpoints_by_tag = {}
        for endpoint in api_info.get("endpoints", []):
            tags = endpoint.get("tags", ["Default"])
            for tag in tags:
                if tag not in endpoints_by_tag:
                    endpoints_by_tag[tag] = []
                endpoints_by_tag[tag].append(endpoint)
        
        # Generate controller tests
        controller_test_dir = os.path.join(test_dir, "controller")
        for tag, endpoints in endpoints_by_tag.items():
            controller_name = self._to_pascal_case(tag) + "Controller"
            test_name = controller_name + "Test"
            
            # Prepare test context
            test_context = {
                **context,
                "controller_name": controller_name,
                "test_name": test_name,
                "tag": tag,
                "endpoints": endpoints
            }
              # Generate controller test class
            test_content = self.render_template("frameworks/micronaut/java/ControllerTest.java.j2", test_context)
            with open(os.path.join(controller_test_dir, f"{test_name}.java"), "w") as f:
                f.write(test_content)
        
        # Generate service tests
        service_test_dir = os.path.join(test_dir, "service")
        for tag, endpoints in endpoints_by_tag.items():
            service_name = self._to_pascal_case(tag) + "Service"
            test_name = service_name + "Test"
            
            # Prepare test context
            test_context = {
                **context,
                "service_name": service_name,
                "test_name": test_name,
                "tag": tag,
                "endpoints": endpoints
            }
              # Generate service test class
            test_content = self.render_template("frameworks/micronaut/java/ServiceTest.java.j2", test_context)
            with open(os.path.join(service_test_dir, f"{test_name}.java"), "w") as f:
                f.write(test_content)
    
    def _generate_sample_code(self, src_dir: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate sample code when no Swagger file is provided.
        
        Args:
            src_dir: Source directory for generated code
            context: Template rendering context
            config: Project configuration dictionary
        """        # Create sample domain class
        domain_dir = os.path.join(src_dir, "domain")
        sample_entity = self.render_template("frameworks/micronaut/java/SampleEntity.java.j2", context)
        with open(os.path.join(domain_dir, "SampleEntity.java"), "w") as f:
            f.write(sample_entity)
        
        # Create sample DTO
        dto_dir = os.path.join(src_dir, "dto")
        sample_dto = self.render_template("frameworks/micronaut/java/SampleDTO.java.j2", context)
        with open(os.path.join(dto_dir, "SampleDTO.java"), "w") as f:
            f.write(sample_dto)
          # Create sample controller
        controller_dir = os.path.join(src_dir, "controller")
        sample_controller = self.render_template("frameworks/micronaut/java/SampleController.java.j2", context)
        with open(os.path.join(controller_dir, "SampleController.java"), "w") as f:
            f.write(sample_controller)
        
        # Create sample service
        service_dir = os.path.join(src_dir, "service")
        impl_dir = os.path.join(service_dir, "impl")
        os.makedirs(impl_dir, exist_ok=True)
        
        sample_service = self.render_template("frameworks/micronaut/java/SampleService.java.j2", context)
        with open(os.path.join(service_dir, "SampleService.java"), "w") as f:
            f.write(sample_service)
        
        sample_service_impl = self.render_template("frameworks/micronaut/java/SampleServiceImpl.java.j2", context)
        with open(os.path.join(impl_dir, "SampleServiceImpl.java"), "w") as f:
            f.write(sample_service_impl)
        
        # Create sample repository
        repo_dir = os.path.join(src_dir, "repository")
        sample_repo = self.render_template("frameworks/micronaut/java/SampleRepository.java.j2", context)
        with open(os.path.join(repo_dir, "SampleRepository.java"), "w") as f:
            f.write(sample_repo)
    
    def _to_pascal_case(self, text: str) -> str:
        """Convert string to PascalCase.
        
        Args:
            text: Text to convert
            
        Returns:
            str: PascalCase text
        """
        # Replace non-alphanumeric with spaces, split and join with title case
        result = ''.join(word.capitalize() for word in re.sub('[^0-9a-zA-Z]+', ' ', text).split())
        return result
