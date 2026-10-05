"""
Book Market Intelligence Platform - Streamlit Main Entrypoint.
"""

import sys
from pathlib import Path

# Ensure src/ is on python path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import streamlit as st
from book_market_intelligence.ui.components import init_session_state
from book_market_intelligence.ui.theme import apply_theme

# 1. Page Configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="AI Book Market Intelligence",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Session & Theme Initialization
init_session_state()
apply_theme()

# Landing page hero
st.markdown("""
<div style="text-align: center; max-width: 900px; margin: 40px auto 20px auto;">
    <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">📚</div>
    <h1 style="font-size: 3rem; font-weight: 800; margin-bottom: 1rem; background: linear-gradient(135deg, #6366f1, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        AI-Powered Book Market Intelligence
    </h1>
    <p style="font-size: 1.25rem; color: #94a3b8; line-height: 1.6;">
        Transforming multi-channel reader sentiment, reviews, and community feedback
        into predictive business decisions, topic intelligence, and executive actions.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

# Feature highlights cards
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="metric-card" style="min-height: 220px;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
        <div style="font-size: 1.15rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem;">Aspect-Based Sentiment</div>
        <p style="font-size: 0.9rem; color: #94a3b8;">
            Granular sentiment analysis across delivery quality, storytelling, pricing models, and platform reliability.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-card" style="min-height: 220px;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧠</div>
        <div style="font-size: 1.15rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem;">Market Intelligence RAG</div>
        <p style="font-size: 0.9rem; color: #94a3b8;">
            Query thousands of consumer reviews using semantic retrieval and LLaMA-powered executive synthesis.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card" style="min-height: 220px;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🚨</div>
        <div style="font-size: 1.15rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem;">Automated Risk Alerts</div>
        <p style="font-size: 0.9rem; color: #94a3b8;">
            Proactive early warning system detecting negative sentiment spikes and alerting lead stakeholders.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# Action Buttons
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🔐 Access Portal (Login)", use_container_width=True):
            st.switch_page("pages/Login.py")
    with btn_col2:
        if st.button("✨ Create Account", use_container_width=True):
            st.switch_page("pages/Signup.py")

st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #1e293b; color: #64748b; font-size: 0.85rem;">
    Enterprise AI Platform &bull; v2.0.0 &bull; Built for Store Managers, Regional Leaders, and Executives
</div>
""", unsafe_allow_html=True)
