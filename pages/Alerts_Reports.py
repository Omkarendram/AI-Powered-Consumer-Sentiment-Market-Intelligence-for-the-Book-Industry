import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from theme import dark_theme
from utils.sidebar import dashboard_sidebar
from utils.rag_panel import rag_panel
from utils.session import load_chat
load_chat()

# ---------------- THEME + SIDEBAR ----------------
dark_theme()
dashboard_sidebar()

st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none !important;}
button[aria-label="Menu"] {display: none !important;}
header {visibility: hidden !important;}
</style>
""", unsafe_allow_html=True)

persona = st.session_state.get("persona", "User")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    path = Path("data/processed/sentiment_analysis_results_batch.csv")

    if not path.exists():
        st.error(f"Dataset not found: {path}")
        st.stop()

    return pd.read_csv(path)

df = load_data()

st.title(f"Alerts & Reports — {persona}")
st.write("AI-powered risk detection and automated reporting.")

# ---------------- DETECT COLUMNS ----------------
sentiment_col = None
product_col = None
date_col = None

for col in df.columns:
    if "sentiment" in col.lower():
        sentiment_col = col
    if "product" in col.lower() or "title" in col.lower():
        product_col = col
    if "date" in col.lower():
        date_col = col

if sentiment_col is None:
    st.warning("No sentiment column found.")
    rag_panel()
    st.stop()

# ---------------- ALERT METRICS ----------------
negative_count = (df[sentiment_col].str.lower() == "negative").sum()
total = len(df)
risk_ratio = negative_count / total if total > 0 else 0

col1, col2 = st.columns(2)

col1.metric("Negative Reviews", negative_count)
col2.metric("Risk Ratio", f"{risk_ratio:.2%}")

st.divider()

# ---------------- ALERT CARD ----------------
if risk_ratio > 0.30:
    st.error("🚨 ALERT: High negative sentiment detected!")
elif risk_ratio > 0.15:
    st.warning("⚠ Warning: Negative sentiment rising.")
else:
    st.success("✅ Sentiment stable.")

st.divider()

# ---------------- TOP RISK PRODUCTS ----------------
if product_col:
    risk_products = (
        df[df[sentiment_col].str.lower() == "negative"]
        .groupby(product_col)
        .size()
        .reset_index(name="Negative Reviews")
        .sort_values("Negative Reviews", ascending=False)
        .head(10)
    )

    fig = px.bar(
        risk_products,
        x="Negative Reviews",
        y=product_col,
        orientation="h",
        title="Top Risk Products"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- TREND ALERT ----------------
if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    trend = (
        df[df[sentiment_col].str.lower() == "negative"]
        .groupby(date_col)
        .size()
        .reset_index(name="Negative Trend")
    )

    fig2 = px.line(
        trend,
        x=date_col,
        y="Negative Trend",
        title="Negative Sentiment Trend"
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------------- DOWNLOAD REPORT ----------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Full Report",
    csv,
    "alerts_report.csv",
    "text/csv"
)

st.divider()

# ---------------- RAG CHAT ----------------
try:
    rag_panel()
except Exception as e:
    st.error(f"Chat failed: {e}")

