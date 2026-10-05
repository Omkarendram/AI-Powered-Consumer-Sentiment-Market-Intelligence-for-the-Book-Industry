"""
Backward compatibility layer for dispatching email alerts.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.ui.components import send_alert_notification


def send_alert(message: str):
    """Sends incident alert notification with safe fallback."""
    success, detail = send_alert_notification(message)
    return success
