"""Configuration management module for MicroGenesis."""

import os
import json
from pathlib import Path


class Config:
    """Handle application configuration."""
    
    DEFAULT_CONFIG = {
        "name": "MicroGenesis",
        "debug": False,
        "log_level": "INFO"
    }
    
    def __init__(self, config_path=None):
        """Initialize configuration with optional config path."""
        self.config_data = self.DEFAULT_CONFIG.copy()
        self.config_path = config_path or self._default_config_path()
        self.load()
    
    def _default_config_path(self):
        """Get the default configuration path."""
        config_dir = os.environ.get(
            "MICROGENESIS_CONFIG_DIR", 
            str(Path.home() / ".microgenesis")
        )
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "config.json")
    
    def load(self):
        """Load configuration from file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    loaded_config = json.load(f)
                    self.config_data.update(loaded_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}")
    
    def save(self):
        """Save configuration to file."""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w") as f:
                json.dump(self.config_data, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """Get a configuration value."""
        return self.config_data.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value."""
        self.config_data[key] = value
        
    def __getitem__(self, key):
        """Allow dictionary-like access to config."""
        return self.config_data[key]
        
    def __setitem__(self, key, value):
        """Allow dictionary-like setting of config."""
        self.config_data[key] = value
