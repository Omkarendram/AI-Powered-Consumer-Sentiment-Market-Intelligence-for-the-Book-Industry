"""
Sentiment Dashboard - Granular Sentiment Analysis & Model Confidence Monitoring.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data import load_book_data
from book_market_intelligence.analytics.sentiment import sentiment_analyzer
from book_market_intelligence.ui.theme import apply_theme
from book_market_intelligence.ui.components import (
    require_authentication,
    render_sidebar,
    kpi_card
)
from book_market_intelligence.ui.rag_widget import render_rag_widget

# 1. Page Configuration MUST be first
st.set_page_config(
    page_title="Sentiment Analysis - Book Market AI",
    page_icon="📈",
    layout="wide"
)

# 2. Authentication & Theme
persona = require_authentication()
apply_theme()
render_sidebar("Sentiment Analysis")
render_rag_widget()

st.title("📈 Sentiment Analysis & Model Metrics")
st.caption(f"Active User Persona: **{persona}** &bull; Granular emotion distributions, confidence scoring, and trend trajectories.")

df = load_book_data()

# ---------------- Live Inference Playground ----------------
with st.expander("🧪 Real-Time Sentiment Prediction Playground", expanded=False):
    st.write("Test the inference pipeline on arbitrary reader review or feedback text:")
    sample_input = st.text_area("Input reader text:", "The physical book arrived on time, but the binding quality was quite flimsy and pages tore easily.")
    if st.button("Predict Sentiment"):
        with st.spinner("Analyzing text..."):
            pred_sent, pred_conf = sentiment_analyzer.analyze(sample_input)

        badge_color = "#10b981" if pred_sent == "positive" else ("#f43f5e" if pred_sent == "negative" else "#64748b")
        st.markdown(f"""
        <div style="background: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid {badge_color}; margin-top: 10px;">
            <b>Predicted Sentiment:</b> <span style="color: {badge_color}; font-weight: bold; text-transform: uppercase;">{pred_sent}</span><br>
            <b>Model Confidence:</b> <code>{pred_conf:.2f}</code> / 1.00
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ---------------- KPI Row ----------------
total = len(df)
pos_count = (df["sentiment"].str.lower() == "positive").sum()
neg_count = (df["sentiment"].str.lower() == "negative").sum()
neu_count = (df["sentiment"].str.lower() == "neutral").sum()

pos_pct = (pos_count / total * 100) if total > 0 else 0
neg_pct = (neg_count / total * 100) if total > 0 else 0
neu_pct = (neu_count / total * 100) if total > 0 else 0
avg_conf = df["confidence"].mean() if "confidence" in df.columns else 0.78

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Positive Feedback", f"{pos_count:,}", f"{pos_pct:.1f}% of total", badge="Advocacy", badge_color="#10b981")
with c2:
    kpi_card("Neutral Inquiries", f"{neu_count:,}", f"{neu_pct:.1f}% of total", badge="Neutral", badge_color="#64748b")
with c3:
    kpi_card("Negative Friction", f"{neg_count:,}", f"{neg_pct:.1f}% of total", badge="Churn Risk", badge_color="#f43f5e")
with c4:
    kpi_card("Average Confidence", f"{avg_conf:.2f}", "Across 2,000+ predictions", badge="High Quality", badge_color="#38bdf8")

st.divider()

# ---------------- Charts ----------------
col_pie, col_conf = st.columns([1, 1])

with col_pie:
    sentiment_counts = df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    fig_donut = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Count",
        title="Overall Sentiment Distribution",
        hole=0.6,
        color="Sentiment",
        color_discrete_map={
            "Positive": "#10b981",
            "Neutral": "#64748b",
            "Negative": "#f43f5e"
        }
    )
    fig_donut.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with col_conf:
    if "confidence" in df.columns:
        fig_hist = px.histogram(
            df,
            x="confidence",
            color="sentiment",
            nbins=20,
            title="Model Confidence Score Distribution",
            color_discrete_map={
                "Positive": "#10b981",
                "Neutral": "#64748b",
                "Negative": "#f43f5e"
            }
        )
        fig_hist.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Confidence Score (0.0 to 1.0)",
            yaxis_title="Record Count"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

# ---------------- Trend Over Time ----------------
if "date" in df.columns:
    st.subheader("📅 Sentiment Volume Trajectory Over Time")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    trend_df = df.groupby([pd.Grouper(key="date", freq="W"), "sentiment"]).size().reset_index(name="count")

    fig_line = px.line(
        trend_df,
        x="date",
        y="count",
        color="sentiment",
        title="Weekly Sentiment Velocity",
        color_discrete_map={
            "Positive": "#10b981",
            "Neutral": "#64748b",
            "Negative": "#f43f5e"
        },
        markers=True
    )
    fig_line.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Timeline",
        yaxis_title="Weekly Record Volume"
    )
    st.plotly_chart(fig_line, use_container_width=True)
