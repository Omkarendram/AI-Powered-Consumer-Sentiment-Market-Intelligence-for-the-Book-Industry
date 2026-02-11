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
    path = Path("data/processed/book_feedback.csv")

    if not path.exists():
        st.error(f"Dataset not found: {path}")
        st.stop()

    return pd.read_csv(path)

df = load_data()

st.title(f"Market Insights — {persona}")
st.write("Market trends and emerging patterns based on feedback data.")

# ---------------- KPI CARDS ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Reviews", len(df))

# detect numeric column automatically
numeric_cols = df.select_dtypes(include="number").columns

if len(numeric_cols) > 0:
    col2.metric("Avg Score", round(df[numeric_cols[0]].mean(), 2))
else:
    col2.metric("Avg Score", "N/A")

col3.metric("Columns", len(df.columns))

st.divider()

# ---------------- AUTO CHARTS ----------------

st.subheader("Data Distribution")

# pick first numeric column
if len(numeric_cols) > 0:
    fig = px.histogram(
        df,
        x=numeric_cols[0],
        title=f"Distribution of {numeric_cols[0]}",
        color_discrete_sequence=["#6366F1"]
    )
    st.plotly_chart(fig, use_container_width=True)

# pick first categorical column
cat_cols = df.select_dtypes(include="object").columns

if len(cat_cols) > 0:
    top = df[cat_cols[0]].value_counts().head(10).reset_index()
    top.columns = ["Category", "Count"]

    fig2 = px.bar(
        top,
        x="Category",
        y="Count",
        title=f"Top {cat_cols[0]} Categories",
        color="Count"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- HEATMAP ----------------
if len(numeric_cols) > 1:
    corr = df[numeric_cols].corr()

    fig3 = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Heatmap",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ---------------- RAG CHAT ----------------
try:
    rag_panel()
except Exception as e:
    st.error(f"Chat failed: {e}")

