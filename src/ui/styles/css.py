"""Custom CSS styling for MicroGenesis UI."""

import streamlit as st

def apply_custom_css():
    """Apply custom CSS to the Streamlit application."""
    st.markdown("""
    <style>
      .main .block-container {
          padding-top: 1rem;
          padding-bottom: 1rem;
          padding-left: 1rem;
          padding-right: 1rem;
          max-width: 100% !important;
      }
      .stApp {
          min-height: 100vh;
          background: #0e1117;
          color: white;
      }
      .stAlert {
          position: fixed;
          top: 20px;
          right: 20px;
          z-index: 1000;
          width: auto;
          max-width: 400px;
      }
      .stButton>button {
          text-transform: none !important;
          border-radius: 4px;
          font-weight: 500;
      }
      .stButton>button[kind="primary"] {
          background-color: #8ab446;
          color: white !important;
          border-color: #8ab446;
      }
      .stButton>button[kind="primary"]:hover {
          background-color: #7aa336;
          border-color: #7aa336;
      }
      .color-primary {
          color: #8ab446 !important;
      }
      .color-warn {
          color: #FF9900 !important;
      }
      .stFileUploader>div {
          background: #1e2129 !important;
          border: 1px solid #444 !important;
      }
      .step-indicator {
          display: flex;
          justify-content: space-between;
          margin-bottom: 2rem;
          user-select: none;
      }
      .step {
          text-align: center;
          flex-grow: 1;
          padding: 0.5rem;
          position: relative;
          cursor: default;
      }
      .step.active {
          color: #8ab446;
          font-weight: bold;
      }
      .step.completed {
          color: #8ab446;
      }
      .step-divider {
          flex-grow: 1;
          border-top: 2px solid #444;
          margin-top: 1rem;
      }
      .summary-value {
          flex: 2;
          text-align: left;
      }
      .summary-card {
        background-color: #1e2129;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 1.5rem;
        color: white;
      }
      .summary-row {
          display: flex;
          flex-wrap: wrap;
          justify-content: space-between;
          margin-bottom: 1rem;
      }
      .summary-label {
          font-weight: bold;
          color: #8ab446;
          margin-right: 0.5rem;
      }
      label, stTextInput > label {
          color: #ffffff !important;
      }
      .stTabs [data-baseweb="tab-list"] {
          gap: 24px;
      }
      .stTabs [data-baseweb="tab"] {
          height: 50px;
          white-space: pre-wrap;
          background-color: #1e2129;
          border-radius: 4px 4px 0 0;
          gap: 1px;
          padding-left: 16px;
          padding-right: 16px;
      }
      .stTabs [aria-selected="true"] {
          background-color: #8ab446 !important;
          color: white !important;
      }
    </style>
    """, unsafe_allow_html=True)
