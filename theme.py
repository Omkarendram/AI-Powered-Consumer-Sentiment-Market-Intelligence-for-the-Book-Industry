import streamlit as st

def dark_theme():
    st.markdown("""
    <style>

    .stApp {
        background-color: #0b0f1a;
        color: #f1f5f9;
    }

    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        color: #e5e7eb;
    }

    h1, h2, h3, h4 {
        color: #f8fafc !important;
    }

    p, span, div {
        color: #cbd5f5;
        font-size: 16px;
    }

    input, textarea, select {
    color: #f1f5f9 !important;
    background-color: #111827 !important;
    }

    .stButton>button {
        background-color: #6366f1;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #4f46e5;
    }

    .kpi-card {
        background: #111827;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        color: #f1f5f9;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.4);
    }

    </style>
    """, unsafe_allow_html=True)

    # Stronger global layout fixes: remove Streamlit header from layout and reset top padding/margins
    st.markdown("""
    <style>
    /* Remove any header elements from layout flow (multiple selectors for robustness) */
    header,
    main > header,
    div[data-testid="stAppViewContainer"] header,
    div.block-container > header {
        display: none !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Reset top padding/margins that can create a visual gap */
    .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    html, body {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    /* Aggressively remove any Streamlit header/toolbar placeholders and top spacing */
    div[data-testid="stToolbar"],
    div[data-testid="stHeader"],
    section[data-testid="stHeader"],
    div[data-testid="stAppViewContainer"],
    .reportview-container,
    .main,
    .stApp {
        margin-top: 0 !important;
        padding-top: 0 !important;
        height: auto !important;
    }
    /* ensure no invisible header occupies space */
    header, header * {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 0 !important;
    }
    /* Remove default top margins from headings and the first block child */
    h1, h2, h3, h4, h5 {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    .block-container > *:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def hide_streamlit_sidebar():
    st.markdown("""
    <style>

    /* Hide sidebar content only */
    [data-testid="stSidebarNav"] {
        visibility: hidden;
    }

    /* KEEP toggle button alive */
    [data-testid="collapsedControl"] {
        display: block !important;
    }

    </style>
    """, unsafe_allow_html=True)
