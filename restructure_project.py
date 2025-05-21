"""
Script to restructure MicroGenesis project - moving from src/microgenesis to src
and updating imports accordingly.
"""

import os
import re
import shutil
from pathlib import Path


def update_file_imports(file_path):
    """Update import statements in a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace import statements based on module
    updated_content = content
    
    # Update core modules
    updated_content = re.sub(
        r'from microgenesis\.logging', 
        'from core.logging', 
        updated_content
    )
    updated_content = re.sub(
        r'from microgenesis\.config', 
        'from core.config', 
        updated_content
    )
    updated_content = re.sub(
        r'from microgenesis\.scaffolding', 
        'from core.scaffolding', 
        updated_content
    )
    updated_content = re.sub(
        r'from microgenesis\.((?!generators|templates).+)', 
        r'from core.\1', 
        updated_content
    )
    
    # Update generator imports
    updated_content = re.sub(
        r'from microgenesis\.generators', 
        'from generators', 
        updated_content
    )
    updated_content = re.sub(
        r'import microgenesis\.generators', 
        'import generators', 
        updated_content
    )
    
    # Handle direct microgenesis imports for __version__
    updated_content = re.sub(
        r'from microgenesis import __version__',
        'from __init__ import __version__',
        updated_content
    )
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)


def update_imports(directory):
    """Update import statements in all Python files in directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                update_file_imports(file_path)


def copy_core_files():
    """Copy core files from src/microgenesis to src/core."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    src_files = {
        os.path.join(root_dir, 'src/microgenesis/__init__.py'): os.path.join(root_dir, 'src/__init__.py'),
        os.path.join(root_dir, 'src/microgenesis/config.py'): os.path.join(root_dir, 'src/core/config.py'),
        os.path.join(root_dir, 'src/microgenesis/logging.py'): os.path.join(root_dir, 'src/core/logging.py'),
        os.path.join(root_dir, 'src/microgenesis/main.py'): os.path.join(root_dir, 'src/core/main.py'),
        os.path.join(root_dir, 'src/microgenesis/scaffolding.py'): os.path.join(root_dir, 'src/core/scaffolding.py'),
    }
    
    for src, dest in src_files.items():
        if os.path.exists(src):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            
            # Copy the file
            shutil.copy2(src, dest)
            
            # Update imports
            update_file_imports(dest)
        else:
            print(f"Warning: Source file {src} does not exist")


def copy_generator_files():
    """Copy generator files from src/microgenesis/generators to src/generators."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(root_dir, 'src/microgenesis/generators')
    dest_dir = os.path.join(root_dir, 'src/generators')
    
    # Create the destination directory
    os.makedirs(dest_dir, exist_ok=True)
    
    # Copy the contents recursively
    if os.path.exists(source_dir):
        for item in os.listdir(source_dir):
            source_item = os.path.join(source_dir, item)
            dest_item = os.path.join(dest_dir, item)
            
            if os.path.isdir(source_item):
                shutil.copytree(source_item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy2(source_item, dest_item)
    else:
        print(f"Warning: Source directory {source_dir} does not exist")
    
    # Update imports in all Python files
    update_imports(dest_dir)


def copy_templates():
    """Copy templates from src/microgenesis/templates to src/templates."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(root_dir, 'src/microgenesis/templates')
    
    # We'll organize templates by framework and language after copying
    if os.path.exists(source_dir):
        # Identify template types and copy to appropriate locations
        for item in os.listdir(source_dir):
            source_item = os.path.join(source_dir, item)
            
            if not os.path.isdir(source_item):
                # Handle top-level template files
                if item.endswith('.j2'):
                    if any(ci_term in item.lower() for ci_term in ['jenkins', 'github', 'azure', 'gitlab']):                        # CI/CD templates
                        dest_item = os.path.join(root_dir, 'src/templates/common/ci-cd', item)
                    elif any(doc_term in item.lower() for doc_term in ['readme', 'getting']):
                        # Documentation templates
                        dest_item = os.path.join(root_dir, 'src/templates/common/docs', item)
                    else:
                        # Other common templates
                        dest_item = os.path.join(root_dir, 'src/templates/common', item)
                    
                    # Copy the file
                    os.makedirs(os.path.dirname(dest_item), exist_ok=True)
                    shutil.copy2(source_item, dest_item)
            else:
                # Handle directories (frameworks)
                framework = item  # e.g., spring-boot, micronaut, graphql
                framework_source = os.path.join(source_dir, framework)
                
                for lang_or_resource in os.listdir(framework_source):
                    source_path = os.path.join(framework_source, lang_or_resource)
                    
                    if lang_or_resource == 'resources':                        # Handle resource files
                        dest_path = os.path.join(root_dir, 'src/templates/frameworks', framework, 'resources')
                        os.makedirs(dest_path, exist_ok=True)
                        
                        # Copy resource files
                        if os.path.isdir(source_path):
                            for res_file in os.listdir(source_path):
                                src_file = os.path.join(source_path, res_file)
                                dst_file = os.path.join(dest_path, res_file)
                                shutil.copy2(src_file, dst_file)
                    
                    elif lang_or_resource in ['java', 'kotlin']:
                        # Handle language-specific templates
                        lang = lang_or_resource
                        lang_source = os.path.join(framework_source, lang)
                        
                        if os.path.isdir(lang_source):
                            for template_file in os.listdir(lang_source):
                                src_file = os.path.join(lang_source, template_file)
                                
                                # Determine component type based on filename
                                component_type = 'entity'  # default
                                if 'controller' in template_file.lower():
                                    component_type = 'controller'
                                elif 'service' in template_file.lower():
                                    component_type = 'service'
                                elif 'repository' in template_file.lower():
                                    component_type = 'repository'
                                elif 'dto' in template_file.lower():
                                    component_type = 'dto'
                                elif 'config' in template_file.lower() or 'application' in template_file.lower():
                                    component_type = 'config'
                                elif 'test' in template_file.lower():
                                    component_type = 'test'
                                elif 'mapper' in template_file.lower():
                                    component_type = 'mapper'
                                  # Create destination path
                                dest_path = os.path.join(
                                    root_dir,
                                    'src/templates/frameworks', 
                                    framework, 
                                    lang, 
                                    component_type
                                )
                                os.makedirs(dest_path, exist_ok=True)
                                
                                # Copy file
                                dst_file = os.path.join(dest_path, template_file)
                                shutil.copy2(src_file, dst_file)
                    
                    elif os.path.isfile(source_path) and source_path.endswith('.j2'):                        # Handle build system files (pom.xml, build.gradle, etc.)
                        filename = os.path.basename(source_path)
                        if 'pom.xml' in filename:
                            dest_path = os.path.join(root_dir, 'src/templates/build-systems/maven')
                        elif 'gradle.kts' in filename:
                            dest_path = os.path.join(root_dir, 'src/templates/build-systems/gradle/kotlin')
                        elif 'gradle' in filename:
                            dest_path = os.path.join(root_dir, 'src/templates/build-systems/gradle/groovy')
                        else:
                            # Other framework-specific files
                            dest_path = os.path.join(root_dir, f'src/templates/frameworks/{framework}')
                        
                        os.makedirs(dest_path, exist_ok=True)
                        dst_file = os.path.join(dest_path, filename)
                        shutil.copy2(source_path, dst_file)
    else:
        print(f"Warning: Templates directory {source_dir} does not exist")


def create_init_files():
    """Create necessary __init__.py files."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    init_dirs = [
        os.path.join(root_dir, 'src'),
        os.path.join(root_dir, 'src/core'),
        os.path.join(root_dir, 'src/generators'),
        os.path.join(root_dir, 'src/utils'),
    ]
    
    for directory in init_dirs:
        init_file = os.path.join(directory, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write('"""Package initialization."""\n')


def update_setup_py():
    """Update setup.py to reflect new package structure."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    setup_py = os.path.join(root_dir, 'setup.py')
    if os.path.exists(setup_py):
        with open(setup_py, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Update entry point
        updated_content = re.sub(
            r'microgenesis=microgenesis\.main:main',
            'microgenesis=core.main:main',
            content
        )
        
        with open(setup_py, 'w', encoding='utf-8') as file:
            file.write(updated_content)
    else:
        print(f"Warning: {setup_py} does not exist")


def update_project_files():
    """Update pyproject.toml and MANIFEST.in files to reflect the new structure."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Update pyproject.toml if it exists
    pyproject_path = os.path.join(root_dir, 'pyproject.toml')
    if os.path.exists(pyproject_path):
        with open(pyproject_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Update any references to microgenesis
        updated_content = re.sub(
            r'src/microgenesis',
            'src',
            content
        )
        
        with open(pyproject_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print("Updated pyproject.toml")
    
    # Update MANIFEST.in if it exists
    manifest_path = os.path.join(root_dir, 'MANIFEST.in')
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Update any references to templates or other paths
        updated_content = re.sub(
            r'src/microgenesis/templates',
            'src/templates',
            content
        )
        
        with open(manifest_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print("Updated MANIFEST.in")


def verify_restructuring():
    """Verify that the restructuring was completed successfully."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    verification_points = [
        # Core modules
        (os.path.join(root_dir, 'src/core/__init__.py'), "Core module init file"),
        (os.path.join(root_dir, 'src/core/config.py'), "Configuration module"),
        (os.path.join(root_dir, 'src/core/logging.py'), "Logging module"),
        (os.path.join(root_dir, 'src/core/main.py'), "Main entry point"),
        (os.path.join(root_dir, 'src/core/scaffolding.py'), "Scaffolding engine"),
        
        # Generators
        (os.path.join(root_dir, 'src/generators/__init__.py'), "Generators init file"),
        (os.path.join(root_dir, 'src/generators/base/__init__.py'), "Base generator"),
        
        # Template directories
        (os.path.join(root_dir, 'src/templates/build-systems/maven'), "Maven build system templates"),
        (os.path.join(root_dir, 'src/templates/build-systems/gradle/groovy'), "Gradle Groovy build system templates"),
        (os.path.join(root_dir, 'src/templates/build-systems/gradle/kotlin'), "Gradle Kotlin build system templates"),
        (os.path.join(root_dir, 'src/templates/common/ci-cd'), "CI/CD templates"),
        (os.path.join(root_dir, 'src/templates/common/docs'), "Documentation templates"),
        (os.path.join(root_dir, 'src/templates/frameworks/spring-boot/java'), "Spring Boot Java templates"),
        (os.path.join(root_dir, 'src/templates/frameworks/spring-boot/kotlin'), "Spring Boot Kotlin templates"),
        (os.path.join(root_dir, 'src/templates/frameworks/micronaut/java'), "Micronaut Java templates"),
        (os.path.join(root_dir, 'src/templates/frameworks/graphql/java'), "GraphQL Java templates"),
    ]
    
    print("\nVerifying restructuring...")
    all_valid = True
    
    for path, description in verification_points:
        if os.path.exists(path):
            print(f"✓ {description} found at {path}")
        else:
            print(f"✗ Missing: {description} at {path}")
            all_valid = False
      # Check for entry point updates in setup.py
    setup_py = os.path.join(root_dir, 'setup.py')
    if os.path.exists(setup_py):
        with open(setup_py, 'r', encoding='utf-8') as file:
            content = file.read()
        if 'microgenesis=core.main:main' in content:
            print("✓ Entry point updated in setup.py")
        else:
            print("✗ Entry point not updated in setup.py")
            all_valid = False
    
    return all_valid


def create_backup():
    """Create a backup of the src/microgenesis directory before restructuring."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(root_dir, 'src/microgenesis')
    backup_dir = os.path.join(root_dir, 'backup_microgenesis')
    
    if os.path.exists(source_dir):
        print(f"Creating backup of source directory at {backup_dir}...")
        
        # Remove existing backup if it exists
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        
        # Create backup
        shutil.copytree(source_dir, backup_dir)
        print("Backup created successfully!")
    else:
        print("No source directory found to backup.")
    
    return os.path.exists(backup_dir)


def main():
    """Main function to restructure the project."""
    print("\n========== MicroGenesis Project Restructuring ==========\n")
    
    # Create backup
    print("0. Creating backup of source files...")
    if not create_backup():
        print("Backup failed. Aborting restructuring.")
        return
    
    # Copy core files
    print("1. Copying core files...")
    copy_core_files()
    
    # Copy generator files
    print("\n2. Copying generator files...")
    copy_generator_files()
    
    # Copy templates
    print("\n3. Copying templates...")
    copy_templates()
    
    # Create __init__.py files
    print("\n4. Creating __init__.py files...")
    create_init_files()
    
    # Update setup.py
    print("\n5. Updating setup.py...")
    update_setup_py()
      # Update project files
    print("\n6. Updating project files (pyproject.toml, MANIFEST.in)...")
    update_project_files()
    
    # Verify restructuring
    print("\n========== Verification ==========")
    if verify_restructuring():
        print("\n✅ Project restructuring completed successfully!")
        print("\nNext steps:")
        print("1. Run tests to ensure everything works as expected")
        print("2. Update documentation to reflect the new structure")
        print("3. Remove the old src/microgenesis directory if everything works")
    else:
        print("\n⚠️ Project restructuring completed with errors.")
        print("Please fix the issues noted above and run the script again.")


if __name__ == "__main__":
    main()
