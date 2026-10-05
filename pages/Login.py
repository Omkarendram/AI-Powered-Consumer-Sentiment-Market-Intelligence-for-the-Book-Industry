"""
Login Page - Enterprise Authentication.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import streamlit as st
from book_market_intelligence.auth.service import auth_service
from book_market_intelligence.ui.theme import apply_theme
from book_market_intelligence.ui.components import init_session_state

# Page Config MUST be first
st.set_page_config(
    page_title="Login - Book Market Intelligence",
    page_icon="🔒",
    layout="centered"
)

init_session_state()
apply_theme()

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h2 style="font-size: 2.2rem; font-weight: 700;">🔐 Executive Portal Login</h2>
    <p style="color: #94a3b8;">Enter your credentials to access role-specific market intelligence.</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    username = st.text_input("Username", placeholder="e.g. om1")
    password = st.text_input("Password", type="password", placeholder="••••")

    st.write("")
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Sign In", use_container_width=True):
            if not username or not password:
                st.error("Please enter both username and password.")
            else:
                user = auth_service.authenticate_user(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.username = user.username
                    st.session_state.persona = user.persona
                    st.success(f"Welcome back, {user.username}! Access level: {user.persona}")
                    st.switch_page("pages/Overview.py")
                else:
                    st.error("Invalid credentials. Please verify your username and password.")

    with col2:
        if st.button("Create Account", use_container_width=True):
            st.switch_page("pages/Signup.py")

st.markdown("---")
st.markdown("""
<div style="background: #1e293b; padding: 12px 18px; border-radius: 8px; font-size: 0.85rem; border-left: 4px solid #6366f1;">
    <b>💡 Demo Credentials:</b><br>
    &bull; <code>om1</code> / <code>2004</code> &mdash; Store Manager<br>
    &bull; <code>om2</code> / <code>2004</code> &mdash; Regional Manager<br>
    &bull; <code>om3</code> / <code>2004</code> &mdash; Executive
</div>
""", unsafe_allow_html=True)
