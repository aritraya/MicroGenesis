"""Spring Boot generator for Java applications."""

import os
import json
from typing import Dict, List, Any, Optional
import re

from src.generators.base import BaseGenerator
from src.generators.architecture import ServiceArchitecture
from src.core.logging import get_logger


class SpringBootJavaGenerator(BaseGenerator):
    """Generator for Spring Boot Java applications."""
    
    def __init__(self):
        """Initialize the Spring Boot Java generator."""
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
        # Get safe database config
        database_config = self.get_safe_database_config(config)
        
        # Prepare context for template rendering        
        context = {
            "project": config.get("project_name", "app"),
            "group_id": config.get("base_package", "com.example"),
            "artifact_id": config.get("project_name", "app").lower(),
            "version": config.get("project_version", "0.1.0"),
            "framework": config.get("framework", {"name": "spring-boot", "version": "2.7.0"}),
            "java_version": config.get("language", {}).get("version", "11"),
            "description": config.get("description", "Generated Spring Boot application"),
            "database": database_config.get("name", ""),
            "features": config.get("features", []),
        }
          # Render pom.xml template using Spring Boot specific Maven template
        pom_content = self.render_template("build-systems/maven/spring-boot/pom.xml.j2", context)
        with open(os.path.join(project_dir, "pom.xml"), "w") as f:
            f.write(pom_content)
    def _generate_gradle_config(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate Gradle configuration (build.gradle).
        
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
            "framework": config.get("framework", {"name": "spring-boot", "version": "2.7.0"}),
            "java_version": config.get("language", {}).get("version", "11"),
            "description": config.get("description", "Generated Spring Boot application"),
            "database": database_config.get("name", ""),
            "features": config.get("features", []),
            "gradle_version": "8.5"  # Latest stable Gradle version at the time
        }
        
        # Render build.gradle template
        build_gradle_content = self.render_template("build-systems/gradle/groovy/spring-boot/build.gradle.j2", context)
        with open(os.path.join(project_dir, "build.gradle"), "w") as f:
            f.write(build_gradle_content)
        
        # Render settings.gradle template
        settings_gradle_content = self.render_template("build-systems/gradle/groovy/settings.gradle.j2", context)
        with open(os.path.join(project_dir, "settings.gradle"), "w") as f:
            f.write(settings_gradle_content)
          # Add Gradle wrapper
        gradle_wrapper_dir = os.path.join(project_dir, "gradle", "wrapper")
        os.makedirs(gradle_wrapper_dir, exist_ok=True)
        
        gradle_wrapper_props = self.render_template("build-systems/gradle/wrapper/gradle-wrapper.properties.j2", context)
        with open(os.path.join(gradle_wrapper_dir, "gradle-wrapper.properties"), "w") as f:
            f.write(gradle_wrapper_props)
        
        gradlew_content = self.render_template("build-systems/gradle/wrapper/gradlew.j2", {})
        with open(os.path.join(project_dir, "gradlew"), "w") as f:
            f.write(gradlew_content)
        
        gradlew_bat_content = self.render_template("build-systems/gradle/wrapper/gradlew.bat.j2", {})
        with open(os.path.join(project_dir, "gradlew.bat"), "w") as f:
            f.write(gradlew_bat_content)
    
    def _generate_source_code(self, project_dir: str, config: Dict[str, Any]) -> None:
        """Generate source code files.
        
        Args:
            project_dir: Target directory for the generated project
            config: Project configuration dictionary
        """
        # Create source code directory structure
        src_main_java = os.path.join(project_dir, "src", "main", "java")
        src_main_resources = os.path.join(project_dir, "src", "main", "resources")
        
        # Convert base package to directory structure
        package_path = config.get("base_package", "com.example").replace(".", os.sep)
        base_package_dir = os.path.join(src_main_java, package_path)
        
        # Create all required directories
        for path in [
            os.path.join(base_package_dir, "controller"),
            os.path.join(base_package_dir, "service"),
            os.path.join(base_package_dir, "repository"),
            os.path.join(base_package_dir, "model"),
            os.path.join(base_package_dir, "dto"),
            os.path.join(base_package_dir, "config"),
            os.path.join(src_main_resources, "config"),
            os.path.join(src_main_resources, "static"),
            os.path.join(src_main_resources, "templates"),
        ]:
            os.makedirs(path, exist_ok=True)
            
        # Get architecture handler
        architecture = self.get_architecture_handler(config)
        
        # Determine service type
        service_type = config.get("service_type", "simple")
        
        # Prepare context for template rendering
        context = {
            "application_name": f"{config.get('project_name', 'Application')}Application",
            "base_package": config.get("base_package", "com.example"),
            "description": config.get("description", "Generated Spring Boot application"),
            "database": self.get_safe_database_config(config),
            "features": config.get("features", []),
            "service_type": service_type,
            "package_structure": architecture.get_package_structure()
        }
        
        # Add architecture-specific context additions
        context.update(architecture.get_template_context_additions(config))
        
        # Generate application class
        app_class_content = self.render_template("frameworks/spring-boot/java/Application.java.j2", context)
        app_class_path = os.path.join(base_package_dir, f"{context['application_name']}.java")
        with open(app_class_path, "w") as f:
            f.write(app_class_content)
        
        # Generate configuration
        self._generate_application_config(src_main_resources, context, config)
        
        # Generate models, controllers, services, etc. from swagger if provided
        swagger_path = config.get("swagger_file")
        if swagger_path:
            self._generate_from_swagger(base_package_dir, swagger_path, context, config)
        else:
            # Generate sample code
            self._generate_sample_code(base_package_dir, context, config)
    
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
        app_test_content = self.render_template("frameworks/spring-boot/java/test/ApplicationTests.java.j2", context)
        test_file_path = os.path.join(project_dir, "src", "test", "java", base_package_path, f"{context['application_name']}Tests.java")
        os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
        with open(test_file_path, "w") as f:
            f.write(app_test_content)
        
        # Generate test configuration
        test_properties = self.render_template("frameworks/spring-boot/resources/application-test.properties.j2", context)
        with open(os.path.join(src_test_resources, "application-test.properties"), "w") as f:
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
        """
        # Generate application.properties or application.yml
        use_yaml = any(feature == "yaml-config" for feature in config.get("features", []))
        
        if use_yaml:
            app_config = self.render_template("frameworks/spring-boot/resources/application.yml.j2", context)
            with open(os.path.join(resources_dir, "application.yml"), "w") as f:
                f.write(app_config)
        else:
            # Default to YAML if properties template doesn't exist
            app_config = self.render_template("frameworks/spring-boot/resources/application.yml.j2", context)
            with open(os.path.join(resources_dir, "application.yml"), "w") as f:
                f.write(app_config)
          # Generate logback configuration if needed
        if any(feature == "logging" for feature in config.get("features", [])):
            logback_config = self.render_template("frameworks/spring-boot/resources/logback-spring.xml.j2", context)
            with open(os.path.join(resources_dir, "logback-spring.xml"), "w") as f:
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
        
        # Generate models
        self._generate_models(src_dir, api_info, context, config)
        
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
    
    def _generate_models(self, src_dir: str, api_info: Dict[str, Any], context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate model classes from API info.
        
        Args:
            src_dir: Source directory for generated code
            api_info: API information extracted from Swagger
            context: Template rendering context
            config: Project configuration dictionary
        """
        model_dir = os.path.join(src_dir, "model")
        
        for model_name, model_info in api_info.get("models", {}).items():
            if model_info["type"] == "entity":
                # Prepare model context
                model_context = {**context, "model": model_info}
                  # Generate entity class
                entity_content = self.render_template("frameworks/spring-boot/java/entity/Entity.java.j2", model_context)
                with open(os.path.join(model_dir, f"{model_name}.java"), "w") as f:
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
        # Create DTO directory if it doesn't exist
        os.makedirs(dto_dir, exist_ok=True)
        
        for model_name, model_info in api_info.get("models", {}).items():
            if model_info["type"] == "dto" or any(feature == "generate-dtos" for feature in config.get("features", [])):
                # Prepare DTO context
                dto_context = {**context, "dto": model_info}
                # Generate DTO class
                dto_content = self.render_template("frameworks/spring-boot/java/dto/DTO.java.j2", dto_context)
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
        # Create controller directory if it doesn't exist
        os.makedirs(controller_dir, exist_ok=True)
        
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
            controller_content = self.render_template("frameworks/spring-boot/java/controller/Controller.java.j2", controller_context)
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
        impl_dir = os.path.join(service_dir, "impl")
        # Create service and impl directories
        os.makedirs(service_dir, exist_ok=True)
        os.makedirs(impl_dir, exist_ok=True)
        
        service_type = config.get("service_type", "domain-driven")
        
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
            service_content = self.render_template("frameworks/spring-boot/java/service/Service.java.j2", service_context)
            with open(os.path.join(service_dir, f"{service_name}.java"), "w") as f:
                f.write(service_content)
            
            # Generate service implementation
            impl_content = self.render_template("frameworks/spring-boot/java/service/ServiceImpl.java.j2", service_context)
            with open(os.path.join(service_dir, "impl", f"{impl_name}.java"), "w") as f:
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
                repo_content = self.render_template("frameworks/spring-boot/java/repository/Repository.java.j2", repo_context)
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
                      # Generate mapper class
                    mapper_content = self.render_template("frameworks/spring-boot/java/mapper/Mapper.java.j2", mapper_context)
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
            test_content = self.render_template("frameworks/spring-boot/java/test/ControllerTest.java.j2", test_context)
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
            test_content = self.render_template("frameworks/spring-boot/java/test/ServiceTest.java.j2", test_context)
            with open(os.path.join(service_test_dir, f"{test_name}.java"), "w") as f:
                f.write(test_content)
    def _generate_sample_code(self, src_dir: str, context: Dict[str, Any], config: Dict[str, Any]) -> None:
        """Generate sample code when no Swagger file is provided.
        
        Args:
            src_dir: Source directory for generated code
            context: Template rendering context
            config: Project configuration dictionary
        """
        # Create sample model
        model_dir = os.path.join(src_dir, "model")
        sample_model = self.render_template("frameworks/spring-boot/java/entity/SampleEntity.java.j2", context)
        with open(os.path.join(model_dir, "SampleEntity.java"), "w") as f:
            f.write(sample_model)
          # Create sample DTO
        dto_dir = os.path.join(src_dir, "dto")
        sample_dto = self.render_template("frameworks/spring-boot/java/dto/SampleDTO.java.j2", context)
        with open(os.path.join(dto_dir, "SampleDTO.java"), "w") as f:
            f.write(sample_dto)
        
        # Create sample controller
        controller_dir = os.path.join(src_dir, "controller")
        sample_controller = self.render_template("frameworks/spring-boot/java/controller/SampleController.java.j2", context)
        with open(os.path.join(controller_dir, "SampleController.java"), "w") as f:
            f.write(sample_controller)
        
        # Create sample service
        service_dir = os.path.join(src_dir, "service")
        impl_dir = os.path.join(service_dir, "impl")
        os.makedirs(impl_dir, exist_ok=True)
        
        sample_service = self.render_template("frameworks/spring-boot/java/service/SampleService.java.j2", context)
        with open(os.path.join(service_dir, "SampleService.java"), "w") as f:
            f.write(sample_service)
        
        sample_service_impl = self.render_template("frameworks/spring-boot/java/service/SampleServiceImpl.java.j2", context)
        with open(os.path.join(impl_dir, "SampleServiceImpl.java"), "w") as f:
            f.write(sample_service_impl)
        
        # Create sample repository
        repo_dir = os.path.join(src_dir, "repository")
        sample_repo = self.render_template("frameworks/spring-boot/java/repository/SampleRepository.java.j2", context)
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
    
    def _to_camel_case(self, text: str, capitalize_first: bool = True) -> str:
        """Convert string to camelCase or PascalCase.
        
        Args:
            text: Text to convert
            capitalize_first: Whether to capitalize the first letter (PascalCase) or not (camelCase)
            
        Returns:
            str: camelCase or PascalCase text
        """
        # Replace non-alphanumeric with spaces and split
        words = re.sub('[^0-9a-zA-Z]+', ' ', text).split()
        
        if not words:
            return ""
          # Handle first word according to capitalize_first parameter
        if capitalize_first:
            result = ''.join(word.capitalize() for word in words)
        else:
            result = words[0].lower() + ''.join(word.capitalize() for word in words[1:])
            
        return result
    
    def _to_snake_case(self, text: str) -> str:
        """Convert string to snake_case.
        
        Args:
            text: Text to convert
            
        Returns:
            str: snake_case text
        """
        # Replace non-alphanumeric with spaces and split
        words = re.sub('[^0-9a-zA-Z]+', ' ', text).split()
        
        # Join with underscore and lowercase
        result = '_'.join(word.lower() for word in words)
        return result
    
    def _to_kebab_case(self, text: str) -> str:
        """Convert string to kebab-case.
        
        Args:
            text: Text to convert
            
        Returns:
            str: kebab-case text
        """
        # Replace non-alphanumeric with spaces and split
        words = re.sub('[^0-9a-zA-Z]+', ' ', text).split()
        
        # Join with hyphen and lowercase
        result = '-'.join(word.lower() for word in words)
        return result
    
    def get_architecture_handler(self, config: Dict[str, Any]) -> ServiceArchitecture:
        """Get the appropriate architecture handler based on configuration.
        
        Args:
            config: Project configuration dictionary
            
        Returns:
            ServiceArchitecture: Handler for the specified architecture
        """
        service_type = config.get("service_type", "simple").lower()
        # Import all architecture handlers
        from src.generators.architecture import (
            SimplifiedArchitecture,
            DomainDrivenArchitecture,
            TechnicalLayeredArchitecture,
            DataDrivenArchitecture,
            FunctionOrientedArchitecture,
            EntityDrivenArchitecture
        )
        
        # Map service types to architecture handlers
        architecture_map = {
            "simple": SimplifiedArchitecture,
            "domain-driven": DomainDrivenArchitecture,
            "technical-layered": TechnicalLayeredArchitecture,
            "data-driven": DataDrivenArchitecture,
            "function-oriented": FunctionOrientedArchitecture,
            "entity-driven": EntityDrivenArchitecture
        }
        
        # Get the appropriate architecture handler class
        architecture_class = architecture_map.get(service_type, SimplifiedArchitecture)
        
        # Return an instance of the architecture handler
        return architecture_class()
    def parse_swagger_file(self, swagger_path: str) -> Dict[str, Any]:
        """Parse Swagger/OpenAPI file and extract API information.
        
        Args:
            swagger_path: Path to the Swagger/OpenAPI definition file
            
        Returns:
            Dict[str, Any]: Extracted API information including models and endpoints
        """
        import yaml
        import os

        _, ext = os.path.splitext(swagger_path)
        
        with open(swagger_path, "r") as f:
            if ext.lower() in ['.yaml', '.yml']:
                swagger_data = yaml.safe_load(f)
            else:
                swagger_data = json.load(f)
        
        api_info = {
            "models": {},
            "endpoints": []
        }
        
        # Parse model definitions (OpenAPI 3.0)
        components = swagger_data.get("components", {})
        schemas = components.get("schemas", {})
        
        for model_name, schema in schemas.items():
            # Determine if the model is an entity or DTO based on schema properties
            is_entity = any(
                prop.get("x-entity", False) 
                for prop in schema.get("properties", {}).values()
            )
            
            api_info["models"][model_name] = {
                "name": model_name,
                "type": "entity" if is_entity else "dto",
                "properties": schema.get("properties", {}),
                "required": schema.get("required", [])
            }
        
        # Parse paths (endpoints)
        paths = swagger_data.get("paths", {})
        for path, methods in paths.items():
            for method, operation in methods.items():
                if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                    continue
                
                # Extract response type from successful response schemas
                responses = operation.get("responses", {})
                success_response = responses.get("200", {}) or responses.get("201", {})
                response_schema = (
                    success_response.get("content", {})
                    .get("application/json", {})
                    .get("schema", {})
                )
                
                response_type = "void"
                if response_schema:
                    if "$ref" in response_schema:
                        ref = response_schema["$ref"].split("/")[-1]
                        response_type = ref
                    elif response_schema.get("type") == "array":
                        if "$ref" in response_schema.get("items", {}):
                            ref = response_schema["items"]["$ref"].split("/")[-1]
                            response_type = f"List<{ref}>"
                        else:
                            response_type = f"List<{response_schema['items'].get('type', 'Object')}>"
                    else:
                        response_type = response_schema.get("type", "void")
                
                # Extract parameters
                parameters = []
                for param in operation.get("parameters", []):
                    param_schema = param.get("schema", {})
                    param_type = "String"  # Default to String if type not specified
                    
                    if "$ref" in param_schema:
                        ref = param_schema["$ref"].split("/")[-1]
                        param_type = ref
                    elif param_schema.get("type") == "array":
                        if "$ref" in param_schema.get("items", {}):
                            ref = param_schema["items"]["$ref"].split("/")[-1]
                            param_type = f"List<{ref}>"
                        else:
                            param_type = f"List<{param_schema['items'].get('type', 'Object')}>"
                    elif "type" in param_schema:
                        type_mapping = {
                            "string": "String",
                            "integer": "Integer",
                            "number": "Double",
                            "boolean": "Boolean",
                            "array": "List",
                            "object": "Object"
                        }
                        param_type = type_mapping.get(param_schema["type"], "String")
                    
                    parameters.append({
                        "name": param["name"],
                        "type": param_type,
                        "in": param["in"],
                        "required": param.get("required", False)
                    })
                
                # Extract request body if present
                if "requestBody" in operation:
                    request_schema = (
                        operation["requestBody"]
                        .get("content", {})
                        .get("application/json", {})
                        .get("schema", {})
                    )
                    
                    if request_schema:
                        if "$ref" in request_schema:
                            ref = request_schema["$ref"].split("/")[-1]
                            parameters.append({
                                "name": self._to_camel_case(ref, False),
                                "type": ref,
                                "in": "body",
                                "required": True
                            })
                
                endpoint = {
                    "path": path,
                    "method": method.upper(),
                    "operationId": operation.get("operationId", ""),
                    "tags": operation.get("tags", ["Default"]),
                    "summary": operation.get("summary", ""),
                    "parameters": parameters,
                    "response": {
                        "type": response_type
                    }
                }
                
                api_info["endpoints"].append(endpoint)
        
        return api_info
