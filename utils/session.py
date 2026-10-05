"""
Backward compatibility layer for Streamlit session management.
Delegates to book_market_intelligence.ui.components.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.ui.components import init_session_state
from book_market_intelligence.ui.rag_widget import render_rag_widget


def load_chat():
    """Renders the AI chat widget in sidebar."""
    render_rag_widget()


def init_session():
    """Initializes user session state."""
    init_session_state()
