"""
Backward compatibility layer for sidebar rendering.
Delegates to book_market_intelligence.ui.components.render_sidebar.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.ui.components import render_sidebar


def dashboard_sidebar():
    """Renders the dashboard sidebar."""
    render_sidebar()
