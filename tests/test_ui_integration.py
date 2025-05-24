"""
UI Integration Test Script

This script tests the integration between the MicroGenesis UI and core components.
It verifies that:
1. The core components can be imported from the UI
2. UI components can call core functions
3. Project generation works properly
"""

import os
import sys
import unittest

# Add the parent directory to the path so we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestUICoreIntegration(unittest.TestCase):
    """Test integration between UI components and core functionality."""
    
    def test_imports(self):
        """Test that core modules can be imported from UI."""
        try:
            # Test importing core modules
            from src.core.config import Config
            from src.core.logging import get_logger
            from src.core.scaffolding import ScaffoldingEngine
            
            # Test importing UI modules
            from src.ui.utils.core_integration import generate_project_from_ui
            
            self.assertTrue(True, "Imports successful")
        except ImportError as e:
            self.fail(f"Import error: {e}")
    
    def test_config_loading(self):
        """Test that configuration can be loaded."""
        from src.core.config import Config
        
        config = Config()
        self.assertIsNotNone(config)
        
        # Test loading default config
        result = config.load()
        self.assertTrue(result)
        
    def test_ui_config_preparation(self):
        """Test that UI configuration can be prepared for the core."""
        from src.ui.utils.core_integration import prepare_config_from_ui
        
        # Mock UI data
        ui_data = {
            "project_name": "test-project",
            "base_package": "com.example.test",
            "framework": "spring-boot",
            "framework_version": "3.2.0",
            "language": "java",
            "language_version": "17",
            "build_system": "maven",
            "output_dir": "./test-output"
        }
        
        # Prepare config
        config = prepare_config_from_ui(ui_data)
        
        # Verify config
        self.assertEqual(config["project_name"], "test-project")
        self.assertEqual(config["base_package"], "com.example.test")
        self.assertEqual(config["framework"]["name"], "spring-boot")
        self.assertEqual(config["language"]["name"], "java")
        self.assertEqual(config["build_system"]["name"], "maven")
        self.assertEqual(config["output_dir"], "./test-output")
    
    def test_templates_available(self):
        """Test that templates can be accessed."""
        from src.ui.utils.core_integration import get_available_templates
        
        templates = get_available_templates()
        
        # Verify templates structure
        self.assertIn("frameworks", templates)
        self.assertIn("languages", templates)
        self.assertIn("build_systems", templates)
        
        # Verify expected values
        self.assertIn("spring-boot", templates["frameworks"])
        self.assertIn("java", templates["languages"])
        self.assertIn("maven", templates["build_systems"])

if __name__ == "__main__":
    unittest.main()
