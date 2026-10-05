"""
Overview Dashboard - High-level Executive & Managerial Market Intelligence.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data import load_book_data
from book_market_intelligence.ui.theme import apply_theme
from book_market_intelligence.ui.components import (
    require_authentication,
    render_sidebar,
    kpi_card
)
from book_market_intelligence.ui.rag_widget import render_rag_widget
from book_market_intelligence.analytics.metrics import calculate_kpis

# 1. Page Configuration MUST be first
st.set_page_config(
    page_title="Executive Overview - Book Market AI",
    page_icon="📊",
    layout="wide"
)

# 2. Authentication Guard & Theme
persona = require_authentication()
apply_theme()
render_sidebar("Overview")
render_rag_widget()

# 3. Load & Filter Data
df = load_book_data()

# ---------------- Header & Persona Controls ----------------
col_header, col_filter = st.columns([3, 2])

with col_header:
    st.title("📊 Executive Overview Dashboard")
    st.caption(f"Role Scope: **{persona}** &bull; Real-time consumer sentiment & operational signals")

with col_filter:
    if persona == "Store Manager":
        available_stores = sorted(df["store"].dropna().unique().tolist())
        selected_store = st.selectbox("🏬 Target Store:", available_stores, index=0)
        filtered_df = df[df["store"] == selected_store]
    elif persona == "Regional Manager":
        available_regions = sorted(df["region"].dropna().unique().tolist())
        selected_region = st.selectbox("🌐 Target Region:", available_regions, index=0)
        filtered_df = df[df["region"] == selected_region]
    else:  # Executive
        selected_regions = st.multiselect("Filter Regions:", sorted(df["region"].dropna().unique().tolist()), default=[])
        if selected_regions:
            filtered_df = df[df["region"].isin(selected_regions)]
        else:
            filtered_df = df

if filtered_df.empty:
    st.info("No records match the current filter selection.")
    filtered_df = df

# ---------------- KPI Metrics ----------------
kpis = calculate_kpis(filtered_df)

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        title="Total Consumer Signals",
        value=f"{kpis['total_feedback']:,}",
        subtitle="Across YouTube, News & Reviews",
        badge="Multi-Channel",
        badge_color="#6366f1"
    )

with c2:
    kpi_card(
        title="Positive Sentiment Rate",
        value=f"{kpis['positive_rate']:.1f}%",
        subtitle=f"{kpis['positive_count']} positive endorsements",
        badge="Healthy",
        badge_color="#10b981"
    )

with c3:
    risk_color = "#f43f5e" if kpis["risk_ratio"] >= 0.25 else "#f59e0b"
    kpi_card(
        title="Negative Risk Ratio",
        value=f"{kpis['negative_rate']:.1f}%",
        subtitle=f"{kpis['negative_count']} critical complaints",
        badge=kpis["risk_level"],
        badge_color=risk_color
    )

with c4:
    kpi_card(
        title="Model Confidence",
        value=f"{kpis['average_confidence']:.2f}",
        subtitle="Zero-shot LLM alignment score",
        badge="Calibrated",
        badge_color="#38bdf8"
    )

st.write("")
st.divider()

# ---------------- Interactive Visualizations ----------------
chart_col1, chart_col2 = st.columns(2)

# Color mapping matching modern dark mode palette
COLOR_MAP = {
    "Positive": "#10b981",
    "Neutral": "#64748b",
    "Negative": "#f43f5e"
}

with chart_col1:
    sentiment_counts = filtered_df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    fig_pie = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Count",
        title="Sentiment Proportions",
        hole=0.55,
        color="Sentiment",
        color_discrete_map=COLOR_MAP
    )
    fig_pie.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    fig_bar = px.bar(
        sentiment_counts,
        x="Sentiment",
        y="Count",
        title="Volume Breakdown by Sentiment",
        color="Sentiment",
        color_discrete_map=COLOR_MAP,
        text="Count"
    )
    fig_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

col_heat, col_cat = st.columns([1, 1])

with col_heat:
    if "region" in filtered_df.columns:
        heat = filtered_df.pivot_table(
            index="region",
            columns="sentiment",
            aggfunc="size",
            fill_value=0
        )
        fig_heat = px.imshow(
            heat,
            text_auto=True,
            title="Regional Sentiment Heatmap",
            color_continuous_scale="Viridis"
        )
        fig_heat.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=50, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_heat, use_container_width=True)

with col_cat:
    if "category" in filtered_df.columns:
        category_counts = filtered_df["category"].value_counts().head(8).reset_index()
        category_counts.columns = ["Category", "Volume"]

        fig_cat = px.bar(
            category_counts,
            x="Volume",
            y="Category",
            orientation="h",
            title="Top Product Categories by Feedback Volume",
            color="Volume",
            color_continuous_scale="Purples"
        )
        fig_cat.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=50, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_cat, use_container_width=True)
