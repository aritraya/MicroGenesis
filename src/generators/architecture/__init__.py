"""Architecture service type implementations for MicroGenesis.

This module provides the specialized code structure and organization
patterns for each supported service architecture type.
"""

from typing import Dict, Any, List
import os

class ServiceArchitecture:
    """Base class for service architecture implementations."""
    
    @staticmethod
    def get_architecture(service_type: str):
        """Factory method to get the appropriate architecture implementation."""
        architectures = {
            "domain-driven": DomainDrivenArchitecture(),
            "entity-driven": EntityDrivenArchitecture(),
            "technical-layered": TechnicalLayeredArchitecture(),
            "data-driven": DataDrivenArchitecture(),
            "function-oriented": FunctionOrientedArchitecture()
        }
        return architectures.get(service_type, DomainDrivenArchitecture())
    
    def create_directory_structure(self, src_main_code_dir: str, config: Dict[str, Any]) -> None:
        """Create the directory structure for this architecture."""
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_package_structure(self) -> Dict[str, Any]:
        """Get the package structure for this architecture."""
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_template_context_additions(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Get additional template context values specific to this architecture."""
        return {"architecture_type": self.__class__.__name__.replace("Architecture", "")}


class DomainDrivenArchitecture(ServiceArchitecture):
    """Domain-Driven Design architecture implementation."""
    
    def create_directory_structure(self, src_main_code_dir: str, config: Dict[str, Any]) -> None:
        """Create the directory structure for Domain-Driven Design architecture."""
        # Core domain directories
        domain_dir = os.path.join(src_main_code_dir, "domain")
        os.makedirs(domain_dir, exist_ok=True)
        
        # Domain model, value objects, aggregates
        os.makedirs(os.path.join(domain_dir, "model"), exist_ok=True)
        os.makedirs(os.path.join(domain_dir, "valueobject"), exist_ok=True)
        os.makedirs(os.path.join(domain_dir, "event"), exist_ok=True)
        
        # Domain services and repositories
        os.makedirs(os.path.join(domain_dir, "service"), exist_ok=True)
        os.makedirs(os.path.join(domain_dir, "repository"), exist_ok=True)
        
        # Application layer
        application_dir = os.path.join(src_main_code_dir, "application")
        os.makedirs(application_dir, exist_ok=True)
        os.makedirs(os.path.join(application_dir, "service"), exist_ok=True)
        os.makedirs(os.path.join(application_dir, "dto"), exist_ok=True)
        os.makedirs(os.path.join(application_dir, "mapper"), exist_ok=True)
        
        # Infrastructure layer
        infra_dir = os.path.join(src_main_code_dir, "infrastructure")
        os.makedirs(infra_dir, exist_ok=True)
        os.makedirs(os.path.join(infra_dir, "persistence"), exist_ok=True)
        os.makedirs(os.path.join(infra_dir, "config"), exist_ok=True)
        os.makedirs(os.path.join(infra_dir, "messaging"), exist_ok=True)
        
        # Interface layer (API)
        interface_dir = os.path.join(src_main_code_dir, "interfaces")
        os.makedirs(interface_dir, exist_ok=True)
        os.makedirs(os.path.join(interface_dir, "rest"), exist_ok=True)
        os.makedirs(os.path.join(interface_dir, "graphql"), exist_ok=True)
    
    def get_package_structure(self) -> Dict[str, Any]:
        """Get the package structure for Domain-Driven Design architecture."""
        return {
            "domain": {
                "description": "Core domain model and business logic",
                "subpackages": {
                    "model": "Domain entities and aggregates",
                    "valueobject": "Immutable value objects",
                    "event": "Domain events",
                    "service": "Domain services",
                    "repository": "Repository interfaces"
                }
            },
            "application": {
                "description": "Application services and use cases",
                "subpackages": {
                    "service": "Application services orchestrating domain operations",
                    "dto": "Data transfer objects",
                    "mapper": "Object mappers between domains and DTOs"
                }
            },
            "infrastructure": {
                "description": "Technical implementations and external integrations",
                "subpackages": {
                    "persistence": "Database implementations of repositories",
                    "config": "Framework and application configuration",
                    "messaging": "Message queue integrations"
                }
            },
            "interfaces": {
                "description": "API and UI interfaces",
                "subpackages": {
                    "rest": "REST API controllers",
                    "graphql": "GraphQL resolvers and schema"
                }
            }
        }
    
    def get_template_context_additions(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Get additional template context for DDD."""
        additions = super().get_template_context_additions(config)
        additions.update({
            "has_domain_events": True,
            "has_value_objects": True,
            "has_aggregates": True,
            "bounded_context": config.get("project_name", "").capitalize()
        })
        return additions


class EntityDrivenArchitecture(ServiceArchitecture):
    """Entity-Driven architecture implementation."""
    
    def create_directory_structure(self, src_main_code_dir: str, config: Dict[str, Any]) -> None:
        """Create the directory structure for Entity-Driven architecture."""
        # Entity directories
        os.makedirs(os.path.join(src_main_code_dir, "entity"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "dto"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "repository"), exist_ok=True)
        
        # Service layer
        os.makedirs(os.path.join(src_main_code_dir, "service"), exist_ok=True)
        
        # API layer
        os.makedirs(os.path.join(src_main_code_dir, "controller"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "api"), exist_ok=True)
        
        # Config and utility
        os.makedirs(os.path.join(src_main_code_dir, "config"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "util"), exist_ok=True)
    
    def get_package_structure(self) -> Dict[str, Any]:
        """Get the package structure for Entity-Driven architecture."""
        return {
            "entity": "JPA/database entities",
            "dto": "Data transfer objects",
            "repository": "Data access repositories",
            "service": "Business logic services",
            "controller": "REST controllers",
            "api": "API models and interfaces",
            "config": "Application configuration",
            "util": "Utility classes"
        }
    
    def get_template_context_additions(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Get additional template context for Entity-Driven architecture."""
        additions = super().get_template_context_additions(config)
        additions.update({
            "uses_jpa": True,
            "entity_focused": True
        })
        return additions


class TechnicalLayeredArchitecture(ServiceArchitecture):
    """Technical/Layered architecture implementation."""
    
    def create_directory_structure(self, src_main_code_dir: str, config: Dict[str, Any]) -> None:
        """Create the directory structure for Technical/Layered architecture."""
        # Standard layered approach
        os.makedirs(os.path.join(src_main_code_dir, "controller"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "service"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "repository"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "model"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "dto"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "config"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "exception"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "util"), exist_ok=True)
    
    def get_package_structure(self) -> Dict[str, Any]:
        """Get the package structure for Technical/Layered architecture."""
        return {
            "controller": "REST API controllers",
            "service": "Business logic services",
            "repository": "Data access layer",
            "model": "Domain models and entities",
            "dto": "Data transfer objects",
            "config": "Application configuration",
            "exception": "Custom exceptions and error handling",
            "util": "Utility classes"
        }
    
    def get_template_context_additions(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Get additional template context for Layered architecture."""
        additions = super().get_template_context_additions(config)
        additions.update({
            "strict_layers": True,
            "technical_focus": True
        })
        return additions


class DataDrivenArchitecture(ServiceArchitecture):
    """Data-Driven architecture implementation."""
    
    def create_directory_structure(self, src_main_code_dir: str, config: Dict[str, Any]) -> None:
        """Create the directory structure for Data-Driven architecture."""
        # Data processing focus
        os.makedirs(os.path.join(src_main_code_dir, "data"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "data", "entity"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "data", "repository"), exist_ok=True)
        
        # Processing layers
        os.makedirs(os.path.join(src_main_code_dir, "process"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "transform"), exist_ok=True)
        
        # API interfaces
        os.makedirs(os.path.join(src_main_code_dir, "api"), exist_ok=True)
        
        # Configuration and utilities
        os.makedirs(os.path.join(src_main_code_dir, "config"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "util"), exist_ok=True)
    
    def get_package_structure(self) -> Dict[str, Any]:
        """Get the package structure for Data-Driven architecture."""
        return {
            "data": {
                "description": "Data models and storage",
                "subpackages": {
                    "entity": "Data entities",
                    "repository": "Data repositories and DAOs"
                }
            },
            "process": "Data processing services",
            "transform": "Data transformation and mapping",
            "api": "API interfaces and controllers",
            "config": "Application and data source configuration",
            "util": "Utility classes and helpers"
        }
    
    def get_template_context_additions(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Get additional template context for Data-Driven architecture."""
        additions = super().get_template_context_additions(config)
        additions.update({
            "data_processing_focus": True,
            "data_pipeline": True
        })
        return additions


class FunctionOrientedArchitecture(ServiceArchitecture):
    """Function-Oriented architecture implementation."""
    
    def create_directory_structure(self, src_main_code_dir: str, config: Dict[str, Any]) -> None:
        """Create the directory structure for Function-Oriented architecture."""
        # Function modules
        os.makedirs(os.path.join(src_main_code_dir, "function"), exist_ok=True)
        
        # Common modules
        os.makedirs(os.path.join(src_main_code_dir, "common"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "common", "model"), exist_ok=True)
        os.makedirs(os.path.join(src_main_code_dir, "common", "util"), exist_ok=True)
        
        # API handlers
        os.makedirs(os.path.join(src_main_code_dir, "handler"), exist_ok=True)
        
        # Configuration
        os.makedirs(os.path.join(src_main_code_dir, "config"), exist_ok=True)
    
    def get_package_structure(self) -> Dict[str, Any]:
        """Get the package structure for Function-Oriented architecture."""
        return {
            "function": "Functional units with specific business capabilities",
            "common": {
                "description": "Shared components",
                "subpackages": {
                    "model": "Shared data models",
                    "util": "Utility functions and helpers"
                }
            },
            "handler": "API handlers and endpoints",
            "config": "Configuration and setup"
        }
    
    def get_template_context_additions(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Get additional template context for Function-Oriented architecture."""
        additions = super().get_template_context_additions(config)
        additions.update({
            "functional_approach": True,
            "stateless_design": True
        })
        return additions
