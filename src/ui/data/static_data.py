"""Static data definitions for MicroGenesis UI."""

# Language definitions
LANGUAGES = [
    {"id": "java", "name": "Java", "versions": [
        {"id": "17", "name": "Java 17", "recommended": True},
        {"id": "11", "name": "Java 11", "recommended": False},
        {"id": "8", "name": "Java 8", "recommended": False}
    ]},
    {"id": "kotlin", "name": "Kotlin", "versions": [
        {"id": "1.9.0", "name": "Kotlin 1.9.0", "recommended": True},
        {"id": "1.8.0", "name": "Kotlin 1.8.0", "recommended": False},
        {"id": "1.7.0", "name": "Kotlin 1.7.0", "recommended": False}
    ]},
]

# Framework definitions
FRAMEWORKS = [
    {"id": "spring-boot", "name": "Spring Boot", "recommended": True,
     "versions": [
         {"id": "3.2.0", "name": "Spring Boot 3.2.0", "recommended": True},
         {"id": "3.1.0", "name": "Spring Boot 3.1.0", "recommended": False},
         {"id": "2.7.0", "name": "Spring Boot 2.7.0", "recommended": False}
     ]},
    {"id": "micronaut", "name": "Micronaut", "recommended": False,
     "versions": [
         {"id": "4.0.0", "name": "Micronaut 4.0.0", "recommended": True},
         {"id": "3.9.1", "name": "Micronaut 3.9.1", "recommended": False},
         {"id": "3.8.0", "name": "Micronaut 3.8.0", "recommended": False}
     ]},
    {"id": "graphql", "name": "GraphQL", "recommended": False,
     "versions": [
         {"id": "20.0", "name": "GraphQL 20.0", "recommended": True},
         {"id": "19.2", "name": "GraphQL 19.2", "recommended": False},
         {"id": "19.0", "name": "GraphQL 19.0", "recommended": False}
     ]},
]

# Build tool definitions
BUILD_TOOLS = [
    {"id": "maven", "name": "Maven"},
    {"id": "gradle", "name": "Gradle", "dsl_options": [
        {"id": "groovy", "name": "Groovy DSL"},
        {"id": "kotlin", "name": "Kotlin DSL"}
    ]}
]

# CI/CD Pipeline definitions
PIPELINES = [
    {"id": "github-actions", "name": "GitHub Actions"},
    {"id": "jenkins", "name": "Jenkins"},
    {"id": "gitlab-ci", "name": "GitLab CI"},
    {"id": "azure-devops", "name": "Azure DevOps"}
]

# Database definitions
DATABASES = [
    {"id": "postgresql", "name": "PostgreSQL"},
    {"id": "mysql", "name": "MySQL"},
    {"id": "h2", "name": "H2"},
    {"id": "mongodb", "name": "MongoDB"},
    {"id": "none", "name": "No Database"}
]

# Additional features
FEATURES = [
    {"id": "swagger", "name": "Swagger/OpenAPI", 
     "description": "REST API documentation with Swagger/OpenAPI"},
    {"id": "logging", "name": "Enhanced Logging", 
     "description": "Advanced logging configuration"},
    {"id": "docker", "name": "Docker Support", 
     "description": "Docker configuration files"},
    {"id": "kubernetes", "name": "Kubernetes", 
     "description": "Kubernetes deployment files"},
    {"id": "aws", "name": "AWS Integration", 
     "description": "AWS cloud integration"},
    {"id": "actuator", "name": "Spring Actuator", 
     "description": "Production-ready monitoring and metrics"},
]

# Service architecture types
SERVICE_TYPES = [
    {"id": "domain-driven", "name": "Domain-Driven Design", 
     "description": "Organized around business domains and logic"},
    {"id": "entity-driven", "name": "Entity-Driven Design", 
     "description": "Centered around data entities and relationships"},
    {"id": "technical-layered", "name": "Technical/Layered", 
     "description": "Traditional layered architecture (controller, service, repository)"},
    {"id": "data-driven", "name": "Data-Driven", 
     "description": "Focused on data processing and transformation"},
    {"id": "function-oriented", "name": "Function-Oriented", 
     "description": "Organized around functional units of work"}
]
