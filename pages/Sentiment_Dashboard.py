import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from utils.session import init_session
from theme import dark_theme
from utils.sidebar import dashboard_sidebar
from utils.rag_panel import rag_panel
from utils.session import load_chat
load_chat()
init_session()
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

st.title(f"Sentiment Analysis — {persona}")
st.write("Sentiment distribution and customer emotion tracking.")

# ---------------- FIND SENTIMENT COLUMN ----------------
sentiment_col = None

for col in df.columns:
    if "sentiment" in col.lower():
        sentiment_col = col
        break

if sentiment_col is None:
    st.warning("No sentiment column detected in dataset.")
    rag_panel()
    st.stop()

# ---------------- KPI CARDS ----------------
col1, col2, col3 = st.columns(3)

positive = (df[sentiment_col].str.lower() == "positive").sum()
negative = (df[sentiment_col].str.lower() == "negative").sum()
neutral = (df[sentiment_col].str.lower() == "neutral").sum()

col1.metric("Positive", positive)
col2.metric("Neutral", neutral)
col3.metric("Negative", negative)

st.divider()

# ---------------- DONUT CHART ----------------
sentiment_counts = df[sentiment_col].value_counts().reset_index()
sentiment_counts.columns = ["Sentiment", "Count"]

fig = px.pie(
    sentiment_counts,
    names="Sentiment",
    values="Count",
    hole=0.6,
    title="Sentiment Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- TREND OVER TIME ----------------
date_col = None
for col in df.columns:
    if "date" in col.lower():
        date_col = col
        break

if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    trend = df.groupby([date_col, sentiment_col]).size().reset_index(name="count")

    fig2 = px.line(
        trend,
        x=date_col,
        y="count",
        color=sentiment_col,
        title="Sentiment Trend Over Time"
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------------- HEATMAP ----------------
numeric_cols = df.select_dtypes(include="number").columns

if len(numeric_cols) > 1:
    corr = df[numeric_cols].corr()

    fig3 = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Heatmap",
        color_continuous_scale="RdBu"
    )

    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ---------------- RAG CHAT ----------------
try:
    rag_panel()
except Exception as e:
    st.error(f"Chat failed: {e}")

