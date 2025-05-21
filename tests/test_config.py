"""Test module for the config class."""

import os
import unittest
import tempfile
import json
import yaml
from src.core.config import Config

# Add this line for debugging
print("Starting test_config.py tests...")


class TestConfig(unittest.TestCase):
    """Test cases for the Config class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test config files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.json_config_path = os.path.join(self.temp_dir.name, "test_config.json")
        self.yaml_config_path = os.path.join(self.temp_dir.name, "test_config.yaml")
        
        # Set up environment variables for testing overrides
        os.environ["MICROGENESIS_LOGGING__LEVEL"] = "DEBUG"
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
        # Clean up environment variables
        if "MICROGENESIS_LOGGING__LEVEL" in os.environ:
            del os.environ["MICROGENESIS_LOGGING__LEVEL"]
    
    def test_default_config(self):
        """Test default configuration values."""
        config = Config(config_path=self.json_config_path)
        self.assertEqual(config.get("application.name"), "MicroGenesis")
        self.assertEqual(config.get("logging.level"), "DEBUG")  # From environment variable
        self.assertIn("spring-boot", config.get("generators.frameworks"))
    
    def test_nested_set_get_config(self):
        """Test setting and getting nested configuration values."""
        config = Config(config_path=self.json_config_path)
        
        # Test get with default
        self.assertEqual(config.get("non_existent.path", "default"), "default")
        
        # Test nested set and get
        config.set("database.settings.url", "jdbc:mysql://localhost:3306/testdb")
        self.assertEqual(config.get("database.settings.url"), "jdbc:mysql://localhost:3306/testdb")
        
        # Test dictionary-style access
        config["custom"] = {"key1": "value1", "key2": "value2"}
        self.assertEqual(config["custom"]["key1"], "value1")
    
    def test_json_save_load_config(self):
        """Test saving and loading JSON configuration."""
        # Create and save config
        config1 = Config(config_path=self.json_config_path)
        config1.set("test_save.nested.value", "test_value")
        config1.save()
        
        # Verify file exists with correct content
        self.assertTrue(os.path.exists(self.json_config_path))
        with open(self.json_config_path, "r") as f:
            saved_data = json.load(f)
            self.assertEqual(saved_data["test_save"]["nested"]["value"], "test_value")
        
        # Load into a new config object and verify
        config2 = Config(config_path=self.json_config_path)
        self.assertEqual(config2.get("test_save.nested.value"), "test_value")
    
    def test_yaml_save_load_config(self):
        """Test saving and loading YAML configuration."""
        # Create and save config
        config1 = Config(config_path=self.yaml_config_path)
        config1.set("test_save.nested.value", "yaml_value")
        config1.save()
        
        # Verify file exists with correct content
        self.assertTrue(os.path.exists(self.yaml_config_path))
        with open(self.yaml_config_path, "r") as f:
            saved_data = yaml.safe_load(f)
            self.assertEqual(saved_data["test_save"]["nested"]["value"], "yaml_value")
        
        # Load into a new config object and verify
        config2 = Config(config_path=self.yaml_config_path)
        self.assertEqual(config2.get("test_save.nested.value"), "yaml_value")
    
    def test_deep_update(self):
        """Test deep update of configuration dictionaries."""
        config = Config(config_path=self.json_config_path)
        
        # Original value
        original_frameworks = config.get("generators.frameworks")
        
        # Set up test config with partial override
        test_config = {
            "generators": {
                "frameworks": ["quarkus", "helidon"]
            }
        }
        
        # Write test config to file
        with open(self.json_config_path, "w") as f:
            json.dump(test_config, f)
        
        # Load the config
        config.load()
        
        # Verify override happened
        self.assertEqual(config.get("generators.frameworks"), ["quarkus", "helidon"])
        
        # But other settings should remain
        self.assertIsNotNone(config.get("generators.languages"))
    
    def test_environment_override(self):
        """Test environment variable overrides."""
        config = Config(config_path=self.json_config_path)
        
        # This should be overridden by the environment variable set in setUp
        self.assertEqual(config.get("logging.level"), "DEBUG")
        
        # Set a new environment variable and reload
        os.environ["MICROGENESIS_APPLICATION__NAME"] = "EnvTestApp"
        config.load()  # This should apply the new environment variable
        
        # Verify the override
        self.assertEqual(config.get("application.name"), "EnvTestApp")
        
        # Clean up
        del os.environ["MICROGENESIS_APPLICATION__NAME"]
    
    def test_as_dict(self):
        """Test getting the complete config as a dictionary."""
        config = Config(config_path=self.json_config_path)
        config_dict = config.as_dict()
        
        # Verify it's a copy, not the original
        config_dict["test_key"] = "test_value"
        self.assertFalse("test_key" in config.config_data)
        
        # Verify it contains all the expected sections
        self.assertIn("application", config_dict)
        self.assertIn("logging", config_dict)
        self.assertIn("generators", config_dict)


if __name__ == "__main__":
    unittest.main()
