"""Test module for the config class."""

import os
import unittest
import tempfile
import json
from microgenesis.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for the Config class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test config files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, "test_config.json")
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
    
    def test_default_config(self):
        """Test default configuration values."""
        config = Config(config_path=self.config_path)
        self.assertEqual(config.get("name"), "MicroGenesis")
        self.assertEqual(config.get("debug"), False)
        self.assertEqual(config.get("log_level"), "INFO")
    
    def test_set_get_config(self):
        """Test setting and getting configuration values."""
        config = Config(config_path=self.config_path)
        
        # Test get with default
        self.assertEqual(config.get("non_existent", "default"), "default")
        
        # Test set and get
        config.set("test_key", "test_value")
        self.assertEqual(config.get("test_key"), "test_value")
        
        # Test dictionary-style access
        config["dict_key"] = "dict_value"
        self.assertEqual(config["dict_key"], "dict_value")
    
    def test_save_load_config(self):
        """Test saving and loading configuration."""
        # Create and save config
        config1 = Config(config_path=self.config_path)
        config1.set("test_save", "test_value")
        config1.save()
        
        # Verify file exists with correct content
        self.assertTrue(os.path.exists(self.config_path))
        with open(self.config_path, "r") as f:
            saved_data = json.load(f)
            self.assertEqual(saved_data["test_save"], "test_value")
        
        # Load into a new config object and verify
        config2 = Config(config_path=self.config_path)
        self.assertEqual(config2.get("test_save"), "test_value")


if __name__ == "__main__":
    unittest.main()
