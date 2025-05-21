"""Test module for GraphQL Java Generator."""

import unittest
import os
import tempfile
import shutil
from unittest.mock import patch

from src.generators.graphql.java import GraphQLJavaGenerator


class TestGraphQLJavaGenerator(unittest.TestCase):
    """Test cases for GraphQL Java Generator."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = GraphQLJavaGenerator()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    @patch('microgenesis.generators.base.BaseGenerator.render_template')
    def test_generate_build_config_maven(self, mock_render):
        """Test Maven build config generation."""
        # Mock the template rendering
        mock_render.return_value = "mock_content"
        
        # Test data
        project_dir = self.temp_dir
        config = {
            "project_name": "test-app",
            "base_package": "com.example",
            "project_version": "1.0.0",
            "framework": {"name": "graphql", "version": "20.0"},
            "language": {"name": "java", "version": "17"},
            "description": "Test GraphQL Application",
            "database": {"name": "h2"},
            "features": ["logging", "swagger"],
            "build_system": {"name": "maven"}
        }
        
        # Call the method
        self.generator._generate_build_config(project_dir, config)
        
        # Assertions
        mock_render.assert_called_with("graphql/pom.xml.j2", {
            "project": "test-app",
            "group_id": "com.example",
            "artifact_id": "test-app",
            "version": "1.0.0",
            "graphql_version": "20.0",
            "java_version": "17",
            "description": "Test GraphQL Application",
            "database": {"name": "h2"},
            "features": ["logging", "swagger"]
        })
        
        # Verify file was created
        self.assertTrue(os.path.exists(os.path.join(project_dir, "pom.xml")))
    
    @patch('microgenesis.generators.base.BaseGenerator.render_template')
    def test_generate_application_class(self, mock_render):
        """Test application class generation."""
        # Mock the template rendering
        mock_render.return_value = "mock_content"
        
        # Test data
        package_path = os.path.join(self.temp_dir, "src", "main", "java", "com", "example")
        os.makedirs(package_path, exist_ok=True)
        package_name = "com.example"
        config = {
            "project_name": "test-app"
        }
        
        # Call the method
        self.generator._generate_application_class(package_path, package_name, config)
        
        # Assertions
        mock_render.assert_called_with("graphql/java/Application.java.j2", {
            "package": "com.example",
            "app_name": "test-app"
        })
        
        # Verify file was created
        self.assertTrue(os.path.exists(os.path.join(package_path, "Application.java")))
    
    @patch('microgenesis.generators.base.BaseGenerator.render_template')
    def test_generate_graphql_schema(self, mock_render):
        """Test GraphQL schema generation."""
        # Mock the template rendering
        mock_render.return_value = "mock_content"
        
        # Test data
        resources_dir = os.path.join(self.temp_dir, "src", "main", "resources")
        os.makedirs(resources_dir, exist_ok=True)
        config = {
            "entities": [
                {
                    "name": "Product",
                    "fields": [
                        {"name": "id", "type": "String", "annotations": ["@Id"]},
                        {"name": "name", "type": "String", "annotations": []},
                        {"name": "price", "type": "Double", "annotations": []}
                    ]
                }
            ]
        }
        
        # Call the method
        self.generator._generate_graphql_schema(resources_dir, config)
        
        # Assertions
        mock_render.assert_called_with("graphql/resources/schema.graphqls.j2", {"entities": config["entities"]})
        
        # Verify file was created
        schema_file = os.path.join(resources_dir, "graphql", "schema.graphqls")
        self.assertTrue(os.path.exists(schema_file))
    
    @patch('microgenesis.generators.base.BaseGenerator.render_template')
    def test_generate_model_classes(self, mock_render):
        """Test model class generation."""
        # Mock the template rendering
        mock_render.return_value = "mock_content"
        
        # Test data
        models_dir = os.path.join(self.temp_dir, "src", "main", "java", "com", "example", "models")
        os.makedirs(models_dir, exist_ok=True)
        package_name = "com.example"
        config = {
            "entities": [
                {
                    "name": "Product",
                    "fields": [
                        {"name": "id", "type": "String", "annotations": ["@Id"]},
                        {"name": "name", "type": "String", "annotations": []},
                        {"name": "price", "type": "Double", "annotations": []}
                    ]
                }
            ]
        }
        
        # Call the method
        self.generator._generate_model_classes(models_dir, package_name, config)
        
        # Assertions
        mock_render.assert_called_with("graphql/java/Model.java.j2", {
            "package": "com.example.models",
            "entity_name": "Product",
            "fields": config["entities"][0]["fields"],
            "imports": self.generator._get_imports_for_entity(config["entities"][0])
        })
        
        # Verify file was created
        self.assertTrue(os.path.exists(os.path.join(models_dir, "Product.java")))
    
    def test_get_imports_for_entity(self):
        """Test import generation for entity."""
        # Test data
        entity = {
            "name": "ComplexEntity",
            "fields": [
                {"name": "id", "type": "String", "annotations": ["@Id"]},
                {"name": "createdAt", "type": "LocalDateTime", "annotations": []},
                {"name": "items", "type": "List<Item>", "annotations": []},
                {"name": "status", "type": "Status", "package": "com.example.models.enums"}
            ]
        }
        
        # Call the method
        imports = self.generator._get_imports_for_entity(entity)
        
        # Assertions
        self.assertIn("jakarta.persistence.Id", imports)
        self.assertIn("java.time.LocalDateTime", imports)
        self.assertIn("java.util.List", imports)


if __name__ == "__main__":
    unittest.main()
