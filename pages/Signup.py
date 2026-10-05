"""
Signup Page - Enterprise User Registration.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import streamlit as st
from book_market_intelligence.auth.service import auth_service, VALID_PERSONAS
from book_market_intelligence.ui.theme import apply_theme
from book_market_intelligence.ui.components import init_session_state

st.set_page_config(
    page_title="Create Account - Book Market Intelligence",
    page_icon="✨",
    layout="centered"
)

init_session_state()
apply_theme()

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h2 style="font-size: 2.2rem; font-weight: 700;">✨ Create Account</h2>
    <p style="color: #94a3b8;">Register for role-based market intelligence access.</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    username = st.text_input("Choose Username", placeholder="e.g. manager_dan")
    password = st.text_input("Choose Password", type="password", placeholder="Minimum 4 characters")
    persona = st.selectbox("Select Your Organization Persona", VALID_PERSONAS)

    st.write("")
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Complete Registration", use_container_width=True):
            if not username or not password:
                st.error("Please fill out all fields.")
            elif len(password) < 4:
                st.error("Password must be at least 4 characters long.")
            else:
                success = auth_service.register_user(username, password, persona)
                if success:
                    st.success("Account successfully created with salted encryption! Please sign in.")
                    st.switch_page("pages/Login.py")
                else:
                    st.error("Registration failed. Username may already exist or is invalid.")

    with col2:
        if st.button("Back to Login", use_container_width=True):
            st.switch_page("pages/Login.py")
