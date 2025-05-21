"""Configuration management module for MicroGenesis scaffolding tool."""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Union

from src.core.logging import get_logger

logger = get_logger()


class Config:
    """Handle application configuration with enhanced features.
    
    This class provides comprehensive configuration management for MicroGenesis,
    supporting both JSON and YAML formats, environment variable overrides,
    and hierarchical configuration settings.
    """
    
    DEFAULT_CONFIG = {
        "application": {
            "name": "MicroGenesis",
            "version": "1.0.0",
            "description": "Application Scaffolding Generator"
        },
        "logging": {
            "level": "INFO",
            "file": None
        },
        "templates": {
            "base_path": None,
            "custom_paths": []
        },
        "generators": {
            "frameworks": ["spring-boot", "micronaut", "graphql"],
            "languages": ["java", "kotlin"],
            "build_systems": ["maven", "gradle"],
            "databases": ["mysql", "postgresql", "h2", "mongodb", "none"],
            "pipelines": ["github-actions", "jenkins", "azure-devops", "gitlab-ci"]
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration with optional config path.
        
        Args:
            config_path: Path to configuration file (JSON or YAML)
        """
        self.config_data = self.DEFAULT_CONFIG.copy()
        self.config_path = config_path or self._default_config_path()
        self.load()
    
    def _default_config_path(self) -> str:
        """Get the default configuration path.
        
        Returns:
            str: Path to default configuration file
        """
        config_dir = os.environ.get(
            "MICROGENESIS_CONFIG_DIR", 
            str(Path.home() / ".microgenesis")
        )
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "config.json")
    
    def load(self) -> bool:
        """Load configuration from file.
        
        Returns:
            bool: True if configuration was loaded successfully, False otherwise
        """
        if not os.path.exists(self.config_path):
            logger.warning(f"Configuration file not found: {self.config_path}")
            return False
        
        try:
            file_extension = os.path.splitext(self.config_path)[1].lower()
            
            with open(self.config_path, "r") as f:
                if file_extension == ".json":
                    loaded_config = json.load(f)
                elif file_extension in [".yaml", ".yml"]:
                    loaded_config = yaml.safe_load(f)
                else:
                    loaded_config = json.load(f)  # Default to JSON
                
                # Deep merge configuration
                self._deep_update(self.config_data, loaded_config)
                
            # Apply environment variable overrides
            self._apply_env_overrides()
            
            logger.info(f"Configuration loaded from {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return False
    
    def save(self) -> bool:
        """Save configuration to file.
        
        Returns:
            bool: True if configuration was saved successfully, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            file_extension = os.path.splitext(self.config_path)[1].lower()
            
            with open(self.config_path, "w") as f:
                if file_extension == ".json":
                    json.dump(self.config_data, f, indent=2)
                elif file_extension in [".yaml", ".yml"]:
                    yaml.dump(self.config_data, f, default_flow_style=False)
                else:
                    json.dump(self.config_data, f, indent=2)  # Default to JSON
            
            logger.info(f"Configuration saved to {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation for nested keys.
        
        Args:
            key_path: Dot-separated path to configuration value (e.g., "logging.level")
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default if not found
        """
        keys = key_path.split(".")
        value = self.config_data
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
                
        return value
    
    def set(self, key_path: str, value: Any) -> None:
        """Set a configuration value using dot notation for nested keys.
        
        Args:
            key_path: Dot-separated path to configuration value (e.g., "logging.level")
            value: Value to set
        """
        keys = key_path.split(".")
        config = self.config_data
        
        # Navigate to the innermost dictionary
        for key in keys[:-1]:
            if key not in config or not isinstance(config[key], dict):
                config[key] = {}
            config = config[key]
            
        # Set the value
        config[keys[-1]] = value
    
    def _deep_update(self, target: Dict, source: Dict) -> None:
        """Recursively update a dictionary with another dictionary.
        
        Args:
            target: Target dictionary to update
            source: Source dictionary with new values
        """
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
    
    def _apply_env_overrides(self) -> None:
        """Apply overrides from environment variables.
        
        Environment variables prefixed with MICROGENESIS_ will override
        configuration values. Nested keys are separated by double underscores.
        Example: MICROGENESIS_LOGGING__LEVEL=DEBUG would override logging.level
        """
        for env_var, env_value in os.environ.items():
            if env_var.startswith("MICROGENESIS_"):
                # Convert MICROGENESIS_SECTION__KEY to section.key
                key_path = env_var[len("MICROGENESIS_"):].lower().replace("__", ".")
                self.set(key_path, env_value)
    
    def as_dict(self) -> Dict[str, Any]:
        """Get a copy of the entire configuration as a dictionary.
        
        Returns:
            Dict[str, Any]: Copy of the configuration dictionary
        """
        return self.config_data.copy()
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-like access to config.
        
        Args:
            key: Configuration key
            
        Returns:
            Configuration value
        """
        return self.config_data[key]
        
    def __setitem__(self, key: str, value: Any) -> None:
        """Allow dictionary-like setting of config.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config_data[key] = value
