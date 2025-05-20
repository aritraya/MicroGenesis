"""Unit tests for MongoDB configuration."""

import unittest
from microgenesis.generators.database.mongodb import MongoDBConfig


class TestMongoDBConfig(unittest.TestCase):
    """Test cases for MongoDB configuration."""
    
    def test_maven_dependencies(self):
        """Test MongoDB Maven dependencies for different frameworks."""
        # Spring Boot
        spring_deps = MongoDBConfig.get_maven_dependencies("spring-boot")
        self.assertTrue(any("spring-boot-starter-data-mongodb" in str(dep) for dep in spring_deps))
        self.assertTrue(any("de.flapdoodle.embed.mongo" in str(dep) for dep in spring_deps))
        
        # Micronaut
        micronaut_deps = MongoDBConfig.get_maven_dependencies("micronaut")
        self.assertTrue(any("micronaut-data-mongodb" in str(dep) for dep in micronaut_deps))
        
        # GraphQL
        graphql_deps = MongoDBConfig.get_maven_dependencies("graphql")
        self.assertTrue(any("spring-boot-starter-data-mongodb" in str(dep) for dep in graphql_deps))
        
        # Unsupported framework
        unsupported_deps = MongoDBConfig.get_maven_dependencies("unsupported")
        self.assertEqual(len(unsupported_deps), 0)
    
    def test_gradle_dependencies(self):
        """Test MongoDB Gradle dependencies for different frameworks."""
        # Spring Boot with Groovy DSL
        spring_deps_groovy = MongoDBConfig.get_gradle_dependencies("spring-boot", False)
        self.assertTrue(any("spring-boot-starter-data-mongodb" in dep for dep in spring_deps_groovy))
        self.assertEqual(len(spring_deps_groovy), 2)
        
        # Spring Boot with Kotlin DSL
        spring_deps_kotlin = MongoDBConfig.get_gradle_dependencies("spring-boot", True)
        self.assertTrue(any("spring-boot-starter-data-mongodb" in dep for dep in spring_deps_kotlin))
        
        # Micronaut with Groovy DSL
        micronaut_deps = MongoDBConfig.get_gradle_dependencies("micronaut", False)
        self.assertTrue(any("micronaut-data-mongodb" in dep for dep in micronaut_deps))
        self.assertTrue(any("micronaut-mongo-reactive" in dep for dep in micronaut_deps))
        
        # Unsupported framework
        unsupported_deps = MongoDBConfig.get_gradle_dependencies("unsupported")
        self.assertEqual(len(unsupported_deps), 0)
    
    def test_properties_config(self):
        """Test MongoDB properties configuration."""
        # Spring Boot properties
        spring_props = MongoDBConfig.get_properties_config("spring-boot")
        self.assertIn("spring.data.mongodb.uri", spring_props)
        self.assertIn("spring.data.mongodb.auto-index-creation", spring_props)
        
        # Micronaut properties
        micronaut_props = MongoDBConfig.get_properties_config("micronaut")
        self.assertIn("mongodb.uri", micronaut_props)
        
        # Unsupported framework
        unsupported_props = MongoDBConfig.get_properties_config("unsupported")
        self.assertEqual(len(unsupported_props), 0)
    
    def test_yaml_config(self):
        """Test MongoDB YAML configuration."""
        # Spring Boot YAML
        spring_yaml = MongoDBConfig.get_yaml_config("spring-boot")
        self.assertIn("spring", spring_yaml)
        self.assertIn("data", spring_yaml["spring"])
        self.assertIn("mongodb", spring_yaml["spring"]["data"])
        
        # Micronaut YAML
        micronaut_yaml = MongoDBConfig.get_yaml_config("micronaut")
        self.assertIn("mongodb", micronaut_yaml)
        self.assertIn("uri", micronaut_yaml["mongodb"])
        
        # Unsupported framework
        unsupported_yaml = MongoDBConfig.get_yaml_config("unsupported")
        self.assertEqual(len(unsupported_yaml), 0)
    
    def test_entity_annotations(self):
        """Test MongoDB entity annotations."""
        # Spring Boot Java
        spring_java = MongoDBConfig.get_entity_annotations("spring-boot", "java")
        self.assertIn("class", spring_java)
        self.assertIn("id", spring_java)
        self.assertIn("Document", str(spring_java["class"]))
        self.assertIn("Id", str(spring_java["id"]))
        
        # Micronaut Kotlin
        micronaut_kotlin = MongoDBConfig.get_entity_annotations("micronaut", "kotlin")
        self.assertIn("class", micronaut_kotlin)
        self.assertIn("MappedEntity", str(micronaut_kotlin["class"]))
        
        # Unsupported framework/language
        unsupported = MongoDBConfig.get_entity_annotations("unsupported", "unsupported")
        self.assertEqual(len(unsupported["class"]), 0)
    
    def test_repository_interface(self):
        """Test MongoDB repository interface."""
        # Spring Boot Java
        spring_java_repo = MongoDBConfig.get_repository_interface("spring-boot", "java")
        self.assertIn("extends", spring_java_repo)
        self.assertIn("MongoRepository", spring_java_repo["extends"])
        
        # Micronaut Kotlin
        micronaut_kotlin_repo = MongoDBConfig.get_repository_interface("micronaut", "kotlin")
        self.assertIn("extends", micronaut_kotlin_repo)
        self.assertIn("import", micronaut_kotlin_repo)
        
        # Unsupported framework/language
        unsupported_repo = MongoDBConfig.get_repository_interface("unsupported", "unsupported")
        self.assertEqual(len(unsupported_repo["extends"]), 0)


if __name__ == "__main__":
    unittest.main()
