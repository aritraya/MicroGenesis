"""Helper functions for MicroGenesis UI."""

import io
import os
import zipfile
import streamlit as st
from datetime import datetime


def update_selection(key, value):
    """Update a selection in the session state.
    
    Args:
        key: The key to update
        value: The value to set
    """
    st.session_state.selections[key] = value


def generate_zip():
    """Generate a ZIP file of the project.
    
    Returns:
        bytes: The ZIP file contents
    """
    if not hasattr(st.session_state, 'generated_path') or not os.path.exists(st.session_state.generated_path):
        return create_simple_zip()
    
    # Create a ZIP file of the actual generated project
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(st.session_state.generated_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(st.session_state.generated_path))
                zipf.write(file_path, arcname)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def create_simple_zip():
    """Create a simple ZIP file with README for when actual project isn't available.
    
    Returns:
        bytes: The ZIP file contents
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zf:
        # Add README with project info
        readme_content = (
            f"Project: {st.session_state.projectName}\n"
            f"Package: {st.session_state.basePackageName}\n\n"
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Language: {st.session_state.selections['language']['name'] if st.session_state.selections['language'] else 'Not selected'}\n"
            f"Language Version: {st.session_state.selections['languageVersion']['name'] if st.session_state.selections['languageVersion'] else 'Not selected'}\n"
            f"Framework: {st.session_state.selections['framework']['name'] if st.session_state.selections['framework'] else 'Not selected'}\n"
            f"Framework Version: {st.session_state.selections['frameworkVersion']['name'] if st.session_state.selections['frameworkVersion'] else 'Not selected'}\n"
            f"Build Tool: {st.session_state.selections['buildTool']['name'] if st.session_state.selections['buildTool'] else 'Not selected'}\n"
            f"Service Type: {st.session_state.selections['serviceType']['name'] if st.session_state.selections['serviceType'] else 'Not selected'}\n"
            f"Database: {st.session_state.selections['database']['name'] if st.session_state.selections['database'] else 'Not selected'}\n"
            f"Pipeline: {st.session_state.selections['pipeline']['name'] if st.session_state.selections['pipeline'] else 'Not selected'}\n"
            f"Features: {', '.join(f['name'] for f in st.session_state.selections['features'])}\n\n"
            f"Entities: {len(st.session_state.entities)}\n"
            f"Relationships: {len(st.session_state.relationships)}\n"
        )
        zf.writestr(f"{st.session_state.projectName}/README.txt", readme_content)
        
        # Add DDL if provided
        if st.session_state.selections['ddl']:
            zf.writestr(f"{st.session_state.projectName}/schema.sql", st.session_state.selections['ddl'])
        
        # Add Swagger if provided
        if st.session_state.selections['swagger']:
            ext = "yaml" if st.session_state.swaggerFile and st.session_state.swaggerFile.name.lower().endswith(("yaml", "yml")) else "json"
            zf.writestr(f"{st.session_state.projectName}/swagger.{ext}", st.session_state.selections['swagger'])
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def render_step_indicator():
    """Render the step indicator in the UI."""
    steps = [
        {"num": 1, "name": "Project Configuration"},
        {"num": 2, "name": "Entity Configuration"},
        {"num": 3, "name": "API Configuration"},
        {"num": 4, "name": "Generate Project"},
    ]
    
    html = '<div class="step-indicator">'
    
    for i, step in enumerate(steps):
        status = ""
        if st.session_state.step == step["num"]:
            status = "active"
        elif st.session_state.step > step["num"]:
            status = "completed"
            
        html += f'<div class="step {status}"><div>Step {step["num"]}</div><div>{step["name"]}</div></div>'
        
        if i < len(steps) - 1:
            html += '<div class="step-divider"></div>'
            
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)
    
    st.markdown("---")
