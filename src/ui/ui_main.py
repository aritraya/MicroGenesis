"""Main MicroGenesis UI module using Streamlit."""

import streamlit as st
from src.ui.styles.css import apply_custom_css
from src.ui.state.session_state import initialize_session_state
from src.ui.data.static_data import LANGUAGES, FRAMEWORKS, BUILD_TOOLS, PIPELINES, DATABASES, FEATURES, SERVICE_TYPES
from src.ui.utils.helpers import update_selection, generate_zip, render_step_indicator
from src.ui.components.navigation import render_step_1_ui, render_step_2_ui, render_step_3_ui, render_step_4_ui

# Set page configuration
st.set_page_config(
    page_title="MicroGenesis - Microservice Generator",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
apply_custom_css()

# Initialize session state
initialize_session_state()

# Main UI header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("src/ui/static/images/logo.png", use_container_width="auto")
    st.markdown("<h1 style='text-align: center;'>MicroGenesis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Microservice Project Generator</p>", unsafe_allow_html=True)

# Render step indicator
render_step_indicator()

# Step 1: Project Configuration (Language, Framework, Build Tools)
if st.session_state.step == 1:
    render_step_1_ui(LANGUAGES, FRAMEWORKS, BUILD_TOOLS, PIPELINES, DATABASES, FEATURES, SERVICE_TYPES)

# Step 2: Entity Configuration (DDL Upload or Manual Entity Creation)
elif st.session_state.step == 2:
    render_step_2_ui()

# Step 3: API Configuration (Swagger/OpenAPI Upload)
elif st.session_state.step == 3:
    render_step_3_ui()

# Step 4: Generate and Download
elif st.session_state.step == 4:
    render_step_4_ui(generate_zip)
