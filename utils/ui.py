"""
Backward compatibility layer for UI cards and components.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.ui.components import kpi_card as enterprise_kpi_card


def kpi_card(title, value, color="#6C63FF"):
    """Renders styled KPI card."""
    enterprise_kpi_card(title=title, value=value, badge_color=color)
