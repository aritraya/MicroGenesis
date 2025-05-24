"""Architecture service type implementations for MicroGenesis.

This module provides the specialized code structure and organization
patterns for each supported service architecture type.
"""

from typing import Dict, Any, List
import os

class ServiceArchitecture:
    """Base class for service architecture implementations."""
    
    def get_package_structure(self) -> Dict[str, List[str]]:
        """Get the package structure for this architecture.
        
        Returns:
            Dict[str, List[str]]: Package structure definition
        """
        return {
            "root": [],
            "model": ["entity", "dto"],
            "service": ["impl"],
            "repository": [],
            "controller": [],
            "config": []
        }
    
    def get_template_context_additions(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Get additional template context for this architecture.
        
        Args:
            config: Project configuration dictionary
        
        Returns:
            Dict[str, Any]: Additional context for templates
        """
        return {}

class SimplifiedArchitecture(ServiceArchitecture):
    """Simple monolithic architecture with basic layering."""
    
    def get_package_structure(self) -> Dict[str, List[str]]:
        return {
            "root": [],
            "model": [],
            "service": ["impl"],
            "controller": [],
            "repository": []
        }

class DomainDrivenArchitecture(ServiceArchitecture):
    """Domain-Driven Design (DDD) architecture."""
    
    def get_package_structure(self) -> Dict[str, List[str]]:
        return {
            "root": [],
            "domain": [
                "model",
                "repository",
                "service",
                "event"
            ],
            "application": [
                "service",
                "dto",
                "mapper"
            ],
            "infrastructure": [
                "persistence",
                "messaging",
                "security"
            ],
            "interfaces": [
                "rest",
                "websocket",
                "scheduler"
            ]
        }
    
    def get_template_context_additions(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "has_events": True,
            "has_messaging": True
        }

class TechnicalLayeredArchitecture(ServiceArchitecture):
    """Technical layering architecture."""
    
    def get_package_structure(self) -> Dict[str, List[str]]:
        return {
            "root": [],
            "presentation": [
                "controller",
                "dto",
                "mapper"
            ],
            "business": [
                "service",
                "model"
            ],
            "persistence": [
                "repository",
                "entity"
            ],
            "common": [
                "config",
                "util"
            ]
        }

class DataDrivenArchitecture(ServiceArchitecture):
    """Data-centric architecture."""
    
    def get_package_structure(self) -> Dict[str, List[str]]:
        return {
            "root": [],
            "model": [
                "entity",
                "dto"
            ],
            "repository": [],
            "service": [
                "crud",
                "query",
                "transaction"
            ],
            "api": [
                "rest",
                "graphql"
            ]
        }

class FunctionOrientedArchitecture(ServiceArchitecture):
    """Function-oriented architecture."""
    
    def get_package_structure(self) -> Dict[str, List[str]]:
        return {
            "root": [],
            "function": [
                "handler",
                "model",
                "util"
            ],
            "shared": [
                "model",
                "service",
                "repository"
            ]
        }

class EntityDrivenArchitecture(ServiceArchitecture):
    """Entity-driven architecture."""
    
    def get_package_structure(self) -> Dict[str, List[str]]:
        return {
            "root": [],
            "entity": [],
            "repository": [],
            "service": ["impl"],
            "controller": [],
            "mapper": []
        }
