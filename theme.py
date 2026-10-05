"""
Backward compatibility layer for theme functions.
Delegates to book_market_intelligence.ui.theme.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.ui.theme import apply_theme, get_theme_css


def dark_theme():
    """Applies the enterprise dark theme."""
    apply_theme()


def hide_streamlit_sidebar():
    """Hides the default sidebar navigation while preserving toggle."""
    try:
        import streamlit as st
        st.markdown("""
        <style>
        [data-testid="stSidebarNav"] { display: none !important; }
        </style>
        """, unsafe_allow_html=True)
    except Exception:
        pass
