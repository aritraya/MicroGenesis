"""Test case for the GraphQL Kotlin generator."""

import unittest
import os
import shutil
import tempfile
from pathlib import Path
import json

from src.generators.graphql.kotlin import GraphQLKotlinGenerator
from src.core.logging import get_logger

logger = get_logger()


class TestGraphQLKotlinGenerator(unittest.TestCase):
    """Test cases for GraphQL Kotlin generator."""
    
    def setUp(self):
        """Set up the test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = GraphQLKotlinGenerator()
        self.base_config = {
            "project_name": "graphql-test",
            "base_package": "com.example.graphqltest",
            "description": "GraphQL Test Project",
            "framework": {
                "name": "graphql",
                "version": "6.0.0"
            },
            "language": {
                "name": "kotlin",
                "version": "1.6.10"
            },
            "build_system": {
                "name": "gradle"
            },
            "database": {
                "name": "postgresql",
                "username": "postgres",
                "password": "postgres"
            },
            "features": ["logging", "swagger"],
            "service_type": "domain-driven"
        }
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_generator_creates_gradle_build_file(self):
        """Test that the generator creates a Gradle build file."""
        project_dir = os.path.join(self.temp_dir, "gradle-project")
        os.makedirs(project_dir, exist_ok=True)
        
        self.generator._generate_gradle_config(project_dir, self.base_config)
        
        self.assertTrue(os.path.exists(os.path.join(project_dir, "build.gradle.kts")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "settings.gradle.kts")))
    
    def test_generator_creates_maven_build_file(self):
        """Test that the generator creates a Maven build file."""
        project_dir = os.path.join(self.temp_dir, "maven-project")
        os.makedirs(project_dir, exist_ok=True)
        
        config = self.base_config.copy()
        config["build_system"] = {"name": "maven"}
        
        self.generator._generate_maven_config(project_dir, config)
        
        self.assertTrue(os.path.exists(os.path.join(project_dir, "pom.xml")))
    
    def test_generator_creates_application_class(self):
        """Test that the generator creates an application class."""
        project_dir = os.path.join(self.temp_dir, "app-project")
        os.makedirs(project_dir, exist_ok=True)
        
        src_main_kotlin = os.path.join(project_dir, "src", "main", "kotlin", "com", "example", "graphqltest")
        os.makedirs(src_main_kotlin, exist_ok=True)
        
        # Mock architecture implementation to avoid complex directory creation
        from unittest.mock import patch, MagicMock
        
        # Create a mock architecture that doesn't create directories or add context
        mock_architecture = MagicMock()
        mock_architecture.create_directory_structure.return_value = None
        mock_architecture.get_package_structure.return_value = {}
        mock_architecture.get_template_context_additions.return_value = {}
        
        with patch('src.generators.architecture.ServiceArchitecture.get_architecture', return_value=mock_architecture):
            # Generate the application class
            self.generator._generate_source_code(project_dir, self.base_config)
        
        app_class_path = os.path.join(src_main_kotlin, "GraphqlTestApplication.kt")
        self.assertTrue(os.path.exists(app_class_path))

    def test_different_architecture_types(self):
        """Test that different architecture types create different structures."""
        # This is more of an integration test, testing with actual architecture types
        
        # Create a project with DDD architecture
        ddd_project_dir = os.path.join(self.temp_dir, "ddd-project")
        os.makedirs(ddd_project_dir, exist_ok=True)
        ddd_config = self.base_config.copy()
        ddd_config["service_type"] = "domain-driven"
        
        # Create a project with entity-driven architecture
        entity_project_dir = os.path.join(self.temp_dir, "entity-project")
        os.makedirs(entity_project_dir, exist_ok=True)
        entity_config = self.base_config.copy()
        entity_config["service_type"] = "entity-driven"
        
        # We can't easily test the full generation since it attempts to render templates
        # So we'll just test the directory structure creation
        from src.generators.architecture import ServiceArchitecture
        
        # DDD architecture
        ddd_arch = ServiceArchitecture.get_architecture("domain-driven")
        ddd_src_dir = os.path.join(ddd_project_dir, "src", "main", "kotlin", "com", "example", "graphqltest")
        os.makedirs(ddd_src_dir, exist_ok=True)
        ddd_arch.create_directory_structure(ddd_src_dir, ddd_config)
        
        # Entity architecture
        entity_arch = ServiceArchitecture.get_architecture("entity-driven")
        entity_src_dir = os.path.join(entity_project_dir, "src", "main", "kotlin", "com", "example", "graphqltest")
        os.makedirs(entity_src_dir, exist_ok=True)
        entity_arch.create_directory_structure(entity_src_dir, entity_config)
        
        # Check for DDD-specific directories
        self.assertTrue(os.path.exists(os.path.join(ddd_src_dir, "domain", "model")))
        self.assertTrue(os.path.exists(os.path.join(ddd_src_dir, "domain", "valueobject")))
        self.assertTrue(os.path.exists(os.path.join(ddd_src_dir, "application", "service")))
        
        # Check for entity-driven specific directories
        self.assertTrue(os.path.exists(os.path.join(entity_src_dir, "entity")))
        self.assertTrue(os.path.exists(os.path.join(entity_src_dir, "service")))
        self.assertTrue(os.path.exists(os.path.join(entity_src_dir, "controller")))
        
        # Verify that DDD has directories that entity-driven doesn't
        self.assertTrue(os.path.exists(os.path.join(ddd_src_dir, "domain", "valueobject")))
        self.assertFalse(os.path.exists(os.path.join(entity_src_dir, "domain")))
        
        # Verify that entity-driven has directories that DDD doesn't have directly
        self.assertTrue(os.path.exists(os.path.join(entity_src_dir, "entity")))
        self.assertFalse(os.path.exists(os.path.join(ddd_src_dir, "entity")))
        

if __name__ == "__main__":
    unittest.main()
