"""
Market Insights Dashboard - Thematic Topics & Aspect-Based Market Intelligence.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import streamlit as st
import plotly.express as px
import pandas as pd
from book_market_intelligence.config.settings import settings
from book_market_intelligence.ui.theme import apply_theme
from book_market_intelligence.ui.components import (
    require_authentication,
    render_sidebar,
    kpi_card
)
from book_market_intelligence.ui.rag_widget import render_rag_widget
from book_market_intelligence.analytics.metrics import get_topic_breakdown, get_top_aspects

# 1. Page Configuration MUST be first
st.set_page_config(
    page_title="Market Insights - Book Market AI",
    page_icon="💡",
    layout="wide"
)

# 2. Authentication & Theme
persona = require_authentication()
apply_theme()
render_sidebar("Market Insights")
render_rag_widget()

st.title("💡 Market & Thematic Insights")
st.caption("Aspect extraction, customer driver analysis, and emerging industry themes.")


# Load enriched topic & aspect dataset
@st.cache_data
def load_market_data():
    for p in [settings.processed_topics_path, settings.processed_feedback_path]:
        if p.exists():
            return pd.read_csv(p)
    return pd.DataFrame()


df = load_market_data()

if df.empty:
    st.warning("⚠️ No enriched topic data found. Please run the preprocessing & topic pipeline.")
    st.stop()

# Ensure required columns exist
if "topic" not in df.columns:
    df["topic"] = "general_reading"
if "aspect" not in df.columns:
    df["aspect"] = "general"
if "sentiment" not in df.columns:
    df["sentiment"] = "Neutral"

# ---------------- KPI Row ----------------
top_topic = df["topic"].value_counts().index[0] if not df.empty else "N/A"
neg_df = df[df["sentiment"].str.lower() == "negative"]
pos_df = df[df["sentiment"].str.lower() == "positive"]

top_complaint = (
    neg_df["aspect"].value_counts().index[0]
    if not neg_df.empty and len(neg_df["aspect"].dropna()) > 0
    else "N/A"
)
top_praise = (
    pos_df["aspect"].value_counts().index[0]
    if not pos_df.empty and len(pos_df["aspect"].dropna()) > 0
    else "N/A"
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card("Dominant Topic", top_topic.replace("_", " ").title(), "Highest volume discussion", badge="Theme", badge_color="#818cf8")

with c2:
    kpi_card("Top Complaint Aspect", top_complaint.title(), "Most critical reader friction point", badge="Friction", badge_color="#f43f5e")

with c3:
    kpi_card("Top Praise Aspect", top_praise.title(), "Primary satisfaction driver", badge="Strength", badge_color="#10b981")

with c4:
    kpi_card("Active Channels", f"{df['source'].nunique() if 'source' in df.columns else 1} Sources", "YouTube, News & Retailers", badge="Aggregated", badge_color="#38bdf8")

st.divider()

# ---------------- Topic Sentiment Composition ----------------
st.subheader("📌 Thematic Distribution & Sentiment Composition")

topic_sentiment = df.groupby(["topic", "sentiment"]).size().reset_index(name="count")

fig_topic = px.bar(
    topic_sentiment,
    x="topic",
    y="count",
    color="sentiment",
    title="Feedback Volume by Topic Segment",
    color_discrete_map={
        "Positive": "#10b981",
        "Neutral": "#64748b",
        "Negative": "#f43f5e",
        "positive": "#10b981",
        "neutral": "#64748b",
        "negative": "#f43f5e"
    },
    barmode="stack"
)
fig_topic.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Thematic Topic",
    yaxis_title="Record Count",
    margin=dict(t=50, b=20, l=20, r=20)
)
st.plotly_chart(fig_topic, use_container_width=True)

st.divider()

# ---------------- Aspects Drilldown ----------------
col_aspects_neg, col_aspects_pos = st.columns(2)

with col_aspects_neg:
    st.subheader("⚠️ Top 10 Consumer Pain Points")
    top_neg_aspects = get_top_aspects(df, sentiment_filter="negative", top_n=10)
    if not top_neg_aspects.empty:
        fig_neg = px.bar(
            top_neg_aspects,
            x="count",
            y="aspect",
            orientation="h",
            color="count",
            color_continuous_scale="Reds",
            title="Most Frequent Negative Aspects"
        )
        fig_neg.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_neg, use_container_width=True)
    else:
        st.info("No negative aspect records found.")

with col_aspects_pos:
    st.subheader("✨ Top 10 Consumer Praise Drivers")
    top_pos_aspects = get_top_aspects(df, sentiment_filter="positive", top_n=10)
    if not top_pos_aspects.empty:
        fig_pos = px.bar(
            top_pos_aspects,
            x="count",
            y="aspect",
            orientation="h",
            color="count",
            color_continuous_scale="Greens",
            title="Most Frequent Positive Aspects"
        )
        fig_pos.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_pos, use_container_width=True)
    else:
        st.info("No positive aspect records found.")

st.divider()

# ---------------- Interactive Feedback Explorer ----------------
st.subheader("🔍 Explore Raw Consumer Comments by Topic")

selected_topic_filter = st.selectbox(
    "Filter by Topic Category:",
    ["All Topics"] + sorted(df["topic"].unique().tolist())
)

explorer_df = df if selected_topic_filter == "All Topics" else df[df["topic"] == selected_topic_filter]

search_term = st.text_input("Filter by Keyword in Feedback Text:", "")
if search_term.strip():
    explorer_df = explorer_df[explorer_df["clean_text"].astype(str).str.contains(search_term, case=False, na=False)]

display_cols = [c for c in ["clean_text", "sentiment", "topic", "aspect", "source", "confidence"] if c in explorer_df.columns]
st.dataframe(
    explorer_df[display_cols].head(50),
    use_container_width=True,
    hide_index=True
)
st.caption(f"Showing {min(50, len(explorer_df))} of {len(explorer_df)} matching feedback items.")
