"""MongoDB configuration utility for database generation."""

import os
from typing import Dict, List, Any, Optional

from microgenesis.logging import get_logger

logger = get_logger()


class MongoDBConfig:
    """MongoDB configuration helper for scaffolding generators."""
    
    @staticmethod
    def get_maven_dependencies(framework: str) -> List[Dict[str, str]]:
        """Get the Maven dependencies for MongoDB based on the framework.
        
        Args:
            framework: Name of the framework (spring-boot, micronaut, etc.)
            
        Returns:
            List[Dict[str, str]]: List of Maven dependency dictionaries
        """
        if framework == "spring-boot":
            return [
                {
                    "groupId": "org.springframework.boot",
                    "artifactId": "spring-boot-starter-data-mongodb",
                    "version": "${spring-boot.version}"
                },
                {
                    "groupId": "de.flapdoodle.embed",
                    "artifactId": "de.flapdoodle.embed.mongo",
                    "version": "4.11.1",
                    "scope": "test"
                }
            ]
        elif framework == "micronaut":
            return [
                {
                    "groupId": "io.micronaut.data",
                    "artifactId": "micronaut-data-mongodb",
                    "version": "${micronaut.data.version}"
                },
                {
                    "groupId": "io.micronaut.mongodb",
                    "artifactId": "micronaut-mongo-reactive",
                    "version": "${micronaut.mongodb.version}"
                },
                {
                    "groupId": "de.flapdoodle.embed",
                    "artifactId": "de.flapdoodle.embed.mongo",
                    "version": "4.11.1",
                    "scope": "test"
                }
            ]
        elif framework == "graphql":
            return [
                {
                    "groupId": "org.springframework.boot",
                    "artifactId": "spring-boot-starter-data-mongodb",
                    "version": "${spring-boot.version}"
                },
                {
                    "groupId": "de.flapdoodle.embed",
                    "artifactId": "de.flapdoodle.embed.mongo",
                    "version": "4.11.1",
                    "scope": "test"
                }
            ]
        else:
            logger.warning(f"Unsupported framework for MongoDB dependencies: {framework}")
            return []
    
    @staticmethod
    def get_gradle_dependencies(framework: str, kotlin: bool = False) -> List[str]:
        """Get the Gradle dependencies for MongoDB based on the framework.
        
        Args:
            framework: Name of the framework (spring-boot, micronaut, etc.)
            kotlin: Whether Kotlin DSL is being used
            
        Returns:
            List[str]: List of Gradle dependency strings
        """
        if framework == "spring-boot":
            if kotlin:
                return [
                    'implementation("org.springframework.boot:spring-boot-starter-data-mongodb")',
                    'testImplementation("de.flapdoodle.embed:de.flapdoodle.embed.mongo:4.11.1")'
                ]
            else:
                return [
                    'implementation "org.springframework.boot:spring-boot-starter-data-mongodb"',
                    'testImplementation "de.flapdoodle.embed:de.flapdoodle.embed.mongo:4.11.1"'
                ]
        elif framework == "micronaut":
            if kotlin:
                return [
                    'implementation("io.micronaut.data:micronaut-data-mongodb")',
                    'implementation("io.micronaut.mongodb:micronaut-mongo-reactive")',
                    'testImplementation("de.flapdoodle.embed:de.flapdoodle.embed.mongo:4.11.1")'
                ]
            else:
                return [
                    'implementation "io.micronaut.data:micronaut-data-mongodb"',
                    'implementation "io.micronaut.mongodb:micronaut-mongo-reactive"',
                    'testImplementation "de.flapdoodle.embed:de.flapdoodle.embed.mongo:4.11.1"'
                ]
        elif framework == "graphql":
            if kotlin:
                return [
                    'implementation("org.springframework.boot:spring-boot-starter-data-mongodb")',
                    'testImplementation("de.flapdoodle.embed:de.flapdoodle.embed.mongo:4.11.1")'
                ]
            else:
                return [
                    'implementation "org.springframework.boot:spring-boot-starter-data-mongodb"',
                    'testImplementation "de.flapdoodle.embed:de.flapdoodle.embed.mongo:4.11.1"'
                ]
        else:
            logger.warning(f"Unsupported framework for MongoDB dependencies: {framework}")
            return []
    
    @staticmethod
    def get_properties_config(framework: str) -> Dict[str, str]:
        """Get the properties configuration for MongoDB based on the framework.
        
        Args:
            framework: Name of the framework (spring-boot, micronaut, etc.)
            
        Returns:
            Dict[str, str]: Dictionary of property key-value pairs
        """
        if framework == "spring-boot":
            return {
                "spring.data.mongodb.uri": "mongodb://localhost:27017/mydatabase",
                "spring.data.mongodb.auto-index-creation": "true"
            }
        elif framework == "micronaut":
            return {
                "mongodb.uri": "mongodb://localhost:27017/mydatabase"
            }
        elif framework == "graphql":
            return {
                "spring.data.mongodb.uri": "mongodb://localhost:27017/mydatabase",
                "spring.data.mongodb.auto-index-creation": "true"
            }
        else:
            logger.warning(f"Unsupported framework for MongoDB properties: {framework}")
            return {}
    
    @staticmethod
    def get_yaml_config(framework: str) -> Dict[str, Any]:
        """Get the YAML configuration for MongoDB based on the framework.
        
        Args:
            framework: Name of the framework (spring-boot, micronaut, etc.)
            
        Returns:
            Dict[str, Any]: Dictionary of YAML configuration
        """
        if framework == "spring-boot":
            return {
                "spring": {
                    "data": {
                        "mongodb": {
                            "uri": "mongodb://localhost:27017/mydatabase",
                            "auto-index-creation": True
                        }
                    }
                }
            }
        elif framework == "micronaut":
            return {
                "mongodb": {
                    "uri": "mongodb://localhost:27017/mydatabase"
                }
            }
        elif framework == "graphql":
            return {
                "spring": {
                    "data": {
                        "mongodb": {
                            "uri": "mongodb://localhost:27017/mydatabase",
                            "auto-index-creation": True
                        }
                    }
                }
            }
        else:
            logger.warning(f"Unsupported framework for MongoDB YAML config: {framework}")
            return {}
    
    @staticmethod
    def get_entity_annotations(framework: str, language: str) -> Dict[str, List[str]]:
        """Get the annotations needed for MongoDB entities based on framework and language.
        
        Args:
            framework: Name of the framework (spring-boot, micronaut, etc.)
            language: Programming language (java, kotlin)
            
        Returns:
            Dict[str, List[str]]: Dictionary mapping annotation types to lists of imports
        """
        if framework == "spring-boot":
            if language == "java":
                return {
                    "class": ["@Document(collection = \"{{entity_name_plural}}\")"],
                    "id": ["@Id"],
                    "imports": [
                        "org.springframework.data.annotation.Id",
                        "org.springframework.data.mongodb.core.mapping.Document"
                    ]
                }
            elif language == "kotlin":
                return {
                    "class": ["@Document(collection = \"{{entity_name_plural}}\")"],
                    "id": ["@Id"],
                    "imports": [
                        "org.springframework.data.annotation.Id",
                        "org.springframework.data.mongodb.core.mapping.Document"
                    ]
                }
        elif framework == "micronaut":
            if language == "java":
                return {
                    "class": ["@MappedEntity(\"{{entity_name_plural}}\")"],
                    "id": ["@Id"],
                    "imports": [
                        "io.micronaut.data.annotation.Id",
                        "io.micronaut.data.annotation.MappedEntity"
                    ]
                }
            elif language == "kotlin":
                return {
                    "class": ["@MappedEntity(\"{{entity_name_plural}}\")"],
                    "id": ["@Id"],
                    "imports": [
                        "io.micronaut.data.annotation.Id",
                        "io.micronaut.data.annotation.MappedEntity"
                    ]
                }
        elif framework == "graphql":
            if language == "java":
                return {
                    "class": ["@Document(collection = \"{{entity_name_plural}}\")"],
                    "id": ["@Id"],
                    "imports": [
                        "org.springframework.data.annotation.Id",
                        "org.springframework.data.mongodb.core.mapping.Document"
                    ]
                }
            elif language == "kotlin":
                return {
                    "class": ["@Document(collection = \"{{entity_name_plural}}\")"],
                    "id": ["@Id"],
                    "imports": [
                        "org.springframework.data.annotation.Id",
                        "org.springframework.data.mongodb.core.mapping.Document"
                    ]
                }
        
        logger.warning(f"Unsupported framework/language for MongoDB annotations: {framework}/{language}")
        return {"class": [], "id": [], "imports": []}
    
    @staticmethod
    def get_repository_interface(framework: str, language: str) -> Dict[str, str]:
        """Get the repository interface details for MongoDB based on framework and language.
        
        Args:
            framework: Name of the framework (spring-boot, micronaut, etc.)
            language: Programming language (java, kotlin)
            
        Returns:
            Dict[str, str]: Dictionary with repository information
        """
        if framework == "spring-boot":
            if language == "java":
                return {
                    "extends": "MongoRepository<{{entity_name}}, {{id_type}}>",
                    "import": "org.springframework.data.mongodb.repository.MongoRepository"
                }
            elif language == "kotlin":
                return {
                    "extends": "MongoRepository<{{entity_name}}, {{id_type}}>",
                    "import": "org.springframework.data.mongodb.repository.MongoRepository"
                }
        elif framework == "micronaut":
            if language == "java":
                return {
                    "extends": "MongoRepository<{{entity_name}}, {{id_type}}>",
                    "import": "io.micronaut.data.mongodb.annotation.MongoRepository"
                }
            elif language == "kotlin":
                return {
                    "extends": "MongoRepository<{{entity_name}}, {{id_type}}>",
                    "import": "io.micronaut.data.mongodb.annotation.MongoRepository"
                }
        elif framework == "graphql":
            if language == "java":
                return {
                    "extends": "MongoRepository<{{entity_name}}, {{id_type}}>",
                    "import": "org.springframework.data.mongodb.repository.MongoRepository"
                }
            elif language == "kotlin":
                return {
                    "extends": "MongoRepository<{{entity_name}}, {{id_type}}>",
                    "import": "org.springframework.data.mongodb.repository.MongoRepository"
                }
        
        logger.warning(f"Unsupported framework/language for MongoDB repository: {framework}/{language}")
        return {"extends": "", "import": ""}
