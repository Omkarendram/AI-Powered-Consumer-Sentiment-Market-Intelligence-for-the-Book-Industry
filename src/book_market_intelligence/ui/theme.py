"""
Enterprise dark theme and styling tokens for Streamlit dashboards.
"""

def get_theme_css() -> str:
    """Returns CSS styles for dark mode enterprise dashboard."""
    return """
    <style>
    /* Global Base */
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Top Header & Chrome */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Block Container */
    .block-container {
        max-width: 1400px !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    p, span, label {
        color: #cbd5e1;
    }

    /* Cards */
    .metric-card {
        background: linear-gradient(145deg, #131d31, #0f172a);
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #6366f1;
    }

    .metric-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin-bottom: 0.25rem;
    }

    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
    }

    .metric-badge {
        display: inline-block;
        font-size: 0.75rem;
        padding: 0.15rem 0.5rem;
        border-radius: 9999px;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    /* Inputs */
    input, textarea, select {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }

    /* Primary Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.25rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5, #4338ca);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.45);
        transform: translateY(-1px);
    }

    /* Hide standard multi-page sidebar navigation (custom sidebar is used) */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    </style>
    """


def apply_theme():
    """Applies the dark theme CSS to the active Streamlit page."""
    try:
        import streamlit as st
        st.markdown(get_theme_css(), unsafe_allow_html=True)
    except Exception:
        pass
