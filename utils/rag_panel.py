"""
Backward compatibility layer for RAG sidebar chat panel.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.ui.rag_widget import render_rag_widget


def rag_panel():
    """Renders interactive AI chat widget."""
    render_rag_widget()
