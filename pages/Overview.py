import streamlit as st
import plotly.express as px
import pandas as pd
from utils.session import init_session
from theme import dark_theme
from utils.sidebar import dashboard_sidebar
from utils.rag_panel import rag_panel
from utils.data import load_book_data
from utils.ui import kpi_card
from utils.session import load_chat
load_chat()
init_session()
# -----------------------------
# Setup
# -----------------------------
dark_theme()
dashboard_sidebar()
st.set_page_config(layout="wide")

st.markdown("""
<style>

/* Force full desktop layout */
.block-container {
    max-width: 1600px !important;
    padding-left: 4rem !important;
    padding-right: 4rem !important;
}

/* Prevent Streamlit auto scaling */
html, body, [data-testid="stAppViewContainer"] {
    zoom: 100%;
}

/* Fix chart container stretching */
[data-testid="stVerticalBlock"] {
    gap: 2rem;
}

/* Sidebar width lock */
section[data-testid="stSidebar"] {
    min-width: 300px !important;
    max-width: 300px !important;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
[data-testid="stSidebarNav"] {display:none;}
button[aria-label="Menu"] {display:none;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

persona = st.session_state.get("persona", "User")

# -----------------------------
# Load data
# -----------------------------

df = load_book_data()

# Persona filtering logic
if persona == "Store Manager":
    df = df[df["store"] == df["store"].iloc[0]]

elif persona == "Regional Manager":
    df = df[df["region"] == df["region"].iloc[0]]

# Executive sees all data

# -----------------------------
# Title
# -----------------------------

st.title(f"Overview Dashboard — {persona}")
st.caption("Real-time platform insights")

# -----------------------------
# KPI CARDS
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

total_feedback = len(df)
positive_rate = (df["sentiment"] == "Positive").mean() * 100
negative_rate = (df["sentiment"] == "Negative").mean() * 100
avg_conf = df["confidence"].mean()

with col1:
    kpi_card("Total Feedback", f"{total_feedback:,}")

with col2:
    kpi_card("Positive %", f"{positive_rate:.1f}%")

with col3:
    kpi_card("Negative %", f"{negative_rate:.1f}%")

with col4:
    kpi_card("Avg Confidence", f"{avg_conf:.2f}")

st.divider()

# -----------------------------
# Sentiment Distribution
# -----------------------------

colA, colB = st.columns(2)

sentiment_counts = df["sentiment"].value_counts()

fig_pie = px.pie(
    values=sentiment_counts.values,
    names=sentiment_counts.index,
    title="Sentiment Distribution",
    hole=0.4
)

fig_bar = px.bar(
    sentiment_counts,
    title="Sentiment Volume",
    labels={"index": "Sentiment", "value": "Count"}
)

colA.plotly_chart(fig_pie, use_container_width=True)
colB.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# -----------------------------
# Region Heatmap
# -----------------------------

heat = df.pivot_table(
    index="region",
    columns="sentiment",
    aggfunc="size",
    fill_value=0
)

fig_heat = px.imshow(
    heat,
    text_auto=True,
    title="Regional Sentiment Heatmap"
)

st.plotly_chart(fig_heat, use_container_width=True)

st.divider()

# -----------------------------
# Category Insights
# -----------------------------

category_counts = df["category"].value_counts()

fig_cat = px.bar(
    category_counts,
    title="Top Categories",
    labels={"index": "Category", "value": "Feedback Volume"}
)

st.plotly_chart(fig_cat, use_container_width=True)

# -----------------------------
# Floating AI Chat
# -----------------------------

# try:
#     rag_panel()
# except Exception as e:
#     st.error(f"Chat failed: {e}")

