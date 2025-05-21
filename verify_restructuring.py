#!/usr/bin/env python
"""Verify the restructuring of the MicroGenesis project."""

import os
import sys
from pathlib import Path


def check_path_exists(path, description):
    """Check if path exists and print status."""
    exists = os.path.exists(path)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {path}")
    return exists


def verify_core_modules():
    """Verify core modules are in the correct place."""
    print("\nVerifying Core Modules:")
    
    core_files = [
        ("src/__init__.py", "Root package initialization"),
        ("src/core/__init__.py", "Core module initialization"),
        ("src/core/config.py", "Configuration module"),
        ("src/core/logging.py", "Logging module"),
        ("src/core/main.py", "Main entry point"),
        ("src/core/scaffolding.py", "Scaffolding engine"),
    ]
    
    success = True
    for path, desc in core_files:
        if not check_path_exists(path, desc):
            success = False
    
    return success


def verify_generators():
    """Verify generator modules are in the correct place."""
    print("\nVerifying Generator Modules:")
    
    generator_paths = [
        ("src/generators/__init__.py", "Generators package initialization"),
        ("src/generators/base/__init__.py", "Base generator module"),
        ("src/generators/schema/ddl_parser.py", "DDL parser module"),
        ("src/generators/spring_boot/java/__init__.py", "Spring Boot Java generator"),
        ("src/generators/spring_boot/kotlin/__init__.py", "Spring Boot Kotlin generator"),
        ("src/generators/micronaut/java/__init__.py", "Micronaut Java generator"),
        ("src/generators/micronaut/kotlin/__init__.py", "Micronaut Kotlin generator"),
        ("src/generators/graphql/java/__init__.py", "GraphQL Java generator"),
    ]
    
    success = True
    for path, desc in generator_paths:
        if not check_path_exists(path, desc):
            success = False
    
    return success


def verify_templates():
    """Verify templates are organized correctly."""
    print("\nVerifying Template Structure:")
    
    template_paths = [
        ("src/templates/build-systems/maven", "Maven build templates"),
        ("src/templates/build-systems/gradle/groovy", "Gradle Groovy build templates"),
        ("src/templates/build-systems/gradle/kotlin", "Gradle Kotlin build templates"),
        ("src/templates/common/ci-cd", "CI/CD templates"),
        ("src/templates/common/docs", "Documentation templates"),
        ("src/templates/frameworks/spring-boot/java/entity", "Spring Boot Java entity templates"),
        ("src/templates/frameworks/spring-boot/java/controller", "Spring Boot Java controller templates"),
        ("src/templates/frameworks/spring-boot/kotlin/entity", "Spring Boot Kotlin entity templates"),
        ("src/templates/frameworks/micronaut/java/entity", "Micronaut Java entity templates"),
        ("src/templates/frameworks/graphql/java/entity", "GraphQL Java entity templates"),
    ]
    
    success = True
    for path, desc in template_paths:
        if not check_path_exists(path, desc):
            success = False
    
    return success


def verify_imports():
    """Verify that import statements have been updated correctly."""
    print("\nVerifying Import Statements:")
    
    # Check a sample of files for correct imports
    core_main = "src/core/main.py"
    if os.path.exists(core_main):
        with open(core_main, 'r') as f:
            content = f.read()
            if "from core." in content and "from microgenesis." not in content:
                print(f"✓ Import statements in {core_main} updated correctly")
            else:
                print(f"✗ Import statements in {core_main} not updated correctly")
                return False
    else:
        print(f"✗ Could not check imports - {core_main} does not exist")
        return False
    
    return True


def verify_setup_py():
    """Verify setup.py has been updated correctly."""
    print("\nVerifying setup.py:")
    
    setup_py = "setup.py"
    if os.path.exists(setup_py):
        with open(setup_py, 'r') as f:
            content = f.read()
            if "microgenesis=core.main:main" in content:
                print("✓ Entry point updated correctly in setup.py")
            else:
                print("✗ Entry point not updated correctly in setup.py")
                return False
    else:
        print("✗ setup.py file not found")
        return False
    
    return True


def main():
    """Main verification function."""
    print("\n=== MicroGenesis Project Restructuring Verification ===\n")
    
    # Run all verification checks
    core_success = verify_core_modules()
    generator_success = verify_generators()
    template_success = verify_templates()
    import_success = verify_imports()
    setup_success = verify_setup_py()
    
    # Overall result
    all_success = all([core_success, generator_success, template_success, import_success, setup_success])
    
    print("\n=== Verification Summary ===")
    print(f"Core modules: {'✓' if core_success else '✗'}")
    print(f"Generator modules: {'✓' if generator_success else '✗'}")
    print(f"Template structure: {'✓' if template_success else '✗'}")
    print(f"Import statements: {'✓' if import_success else '✗'}")
    print(f"setup.py: {'✓' if setup_success else '✗'}")
    
    if all_success:
        print("\n✅ Project restructuring verified successfully!")
        print("\nNext steps:")
        print("1. Run comprehensive tests to ensure functionality")
        print("2. Remove the old src/microgenesis directory")
        print("3. Update documentation to reflect the new structure")
        return 0
    else:
        print("\n⚠️ Verification found issues. Please fix them before proceeding.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
