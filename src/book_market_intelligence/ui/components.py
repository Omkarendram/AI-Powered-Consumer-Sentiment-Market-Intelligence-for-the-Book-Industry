"""
Reusable Streamlit UI components, session guards, and navigation elements.
"""

from typing import Optional, Any, Tuple
import smtplib
from email.mime.text import MIMEText
import streamlit as st
from book_market_intelligence.config.settings import settings
from book_market_intelligence.core.logging import logger


def init_session_state() -> None:
    """Initializes user session state with default security values."""
    defaults = {
        "authenticated": False,
        "username": None,
        "persona": None,
        "chat_history": []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def require_authentication() -> str:
    """
    Enforces authentication guard on protected dashboard pages.
    Redirects unauthenticated visitors to the login page.
    Returns the user's active persona.
    """
    init_session_state()

    if not st.session_state.get("authenticated", False) or not st.session_state.get("username"):
        st.warning("🔒 Authentication required. Redirecting to login...")
        st.switch_page("pages/1_Login.py")
        st.stop()

    return st.session_state.get("persona", "Executive")


def render_sidebar(current_page: str = "Overview") -> None:
    """Renders the custom branded dashboard sidebar with persona badges and navigation."""
    init_session_state()
    username = st.session_state.get("username", "Guest")
    persona = st.session_state.get("persona", "User")

    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 10px 0 20px 0; border-bottom: 1px solid #1e293b; margin-bottom: 15px;">
            <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff;">📚 Book Market AI</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">Market Intelligence Platform</div>
            <div style="margin-top: 10px; display: inline-block; background: #1e293b; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; border-left: 3px solid #6366f1;">
                👤 <b>{username}</b> &nbsp;|&nbsp; <span style="color:#a5b4fc;">{persona}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### 🧭 Navigation")
        st.page_link("pages/3_Overview.py", label="Executive Overview", icon="📊")
        st.page_link("pages/4_Market_Insights.py", label="Market Insights", icon="💡")
        st.page_link("pages/5_Sentiment_Dashboard.py", label="Sentiment Analysis", icon="📈")
        st.page_link("pages/6_Alerts_Reports.py", label="Alerts & Reports", icon="🚨")

        st.divider()

        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.clear()
            st.switch_page("app.py")


def kpi_card(
    title: str,
    value: Any,
    subtitle: Optional[str] = None,
    badge: Optional[str] = None,
    badge_color: str = "#10b981"
) -> None:
    """Renders a styled dark-mode KPI card widget."""
    badge_html = ""
    if badge:
        badge_html = f"""<span class="metric-badge" style="background-color: {badge_color}22; color: {badge_color}; border: 1px solid {badge_color}44;">{badge}</span>"""

    sub_html = ""
    if subtitle:
        sub_html = f"""<div style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">{subtitle}</div>"""

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {sub_html}
        {badge_html}
    </div>
    """, unsafe_allow_html=True)


def send_alert_notification(message: str, subject: str = "🚨 Sentiment Risk Alert") -> Tuple[bool, str]:
    """
    Dispatches an email alert with graceful fallback to system logging
    if SMTP credentials are not configured.
    """
    sender = settings.ALERT_EMAIL
    password = settings.ALERT_PASSWORD
    receiver = settings.ALERT_RECEIVER

    if not sender or not password or not receiver:
        logger.info(f"Mock Alert Logged (SMTP not configured):\nSubject: {subject}\nMessage: {message}")
        return True, "Alert logged to system audit trail (SMTP credentials not configured in .env)."

    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver

        with smtplib.SMTP_SSL(settings.ALERT_SMTP_SERVER, settings.ALERT_SMTP_PORT, timeout=10) as server:
            server.login(sender, password)
            server.send_message(msg)

        logger.info(f"Alert successfully sent to {receiver}")
        return True, f"Alert dispatched successfully to {receiver}."
    except Exception as e:
        logger.error(f"Failed to dispatch alert: {e}")
        return False, f"Email delivery failed: {str(e)}"
