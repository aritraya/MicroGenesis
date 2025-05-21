"""Session state management for MicroGenesis UI."""

import streamlit as st
from datetime import datetime

def initialize_session_state():
    """Initialize all session state variables needed for the UI."""
    # Step navigation
    if 'step' not in st.session_state:
        st.session_state.step = 1
        
    # Project configuration
    if 'projectName' not in st.session_state:
        st.session_state.projectName = "MyMicroservice"
    if 'basePackageName' not in st.session_state:
        st.session_state.basePackageName = "com.example"
        
    # Selections dictionary
    if 'selections' not in st.session_state:
        st.session_state.selections = {
            'language': None,
            'languageVersion': None,
            'framework': None,
            'frameworkVersion': None,
            'buildTool': None,
            'gradleDsl': None,
            'pipeline': None,
            'database': None,
            'serviceType': None,
            'features': [],
            'swagger': None,
            'ddl': None
        }
        
    # File uploads
    if 'swaggerFile' not in st.session_state:
        st.session_state.swaggerFile = None
    if 'ddlFile' not in st.session_state:
        st.session_state.ddlFile = None
        
    # Entities management
    if 'entities' not in st.session_state:
        st.session_state.entities = []
    if 'relationships' not in st.session_state:
        st.session_state.relationships = []
        
    # Download state
    if 'show_download' not in st.session_state:
        st.session_state.show_download = False
    if 'generated_zip' not in st.session_state:
        st.session_state.generated_zip = None
        
    # Project generation history
    if 'project_history' not in st.session_state:
        st.session_state.project_history = []
        

def save_project_to_history():
    """Save the current project configuration to history."""
    project_info = {
        "name": st.session_state.projectName,
        "package": st.session_state.basePackageName,
        "language": st.session_state.selections['language']['name'] if st.session_state.selections['language'] else None,
        "framework": st.session_state.selections['framework']['name'] if st.session_state.selections['framework'] else None,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entity_count": len(st.session_state.entities)
    }
    
    # Add to history
    st.session_state.project_history.append(project_info)
    
    # Limit history to last 10 items
    if len(st.session_state.project_history) > 10:
        st.session_state.project_history = st.session_state.project_history[-10:]
