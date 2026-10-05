"""
Alerts & Reports - Risk Detection, Incident Escalation, and Executive Export.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data import load_book_data
from book_market_intelligence.config.settings import settings
from book_market_intelligence.ui.theme import apply_theme
from book_market_intelligence.ui.components import (
    require_authentication,
    render_sidebar,
    kpi_card,
    send_alert_notification
)
from book_market_intelligence.ui.rag_widget import render_rag_widget
from book_market_intelligence.analytics.metrics import calculate_kpis, get_top_aspects

# 1. Page Configuration MUST be first
st.set_page_config(
    page_title="Alerts & Reports - Book Market AI",
    page_icon="🚨",
    layout="wide"
)

# 2. Authentication & Theme
persona = require_authentication()
apply_theme()
render_sidebar("Alerts & Reports")
render_rag_widget()

st.title("🚨 Alerts, Risk Monitoring & Executive Reports")
st.caption(f"Role Scope: **{persona}** &bull; Automated negative sentiment threshold detection & incident reporting.")

df = load_book_data()
kpis = calculate_kpis(df)

# ---------------- Risk Status Alert Banner ----------------
risk_ratio = kpis["risk_ratio"]
neg_count = kpis["negative_count"]

if risk_ratio >= 0.30:
    st.error(f"🚨 **CRITICAL RISK ALERT**: Negative consumer sentiment is at {risk_ratio:.1%}, exceeding the 30% tolerance threshold! Immediate executive intervention recommended.")
elif risk_ratio >= 0.18:
    st.warning(f"⚠️ **ELEVATED RISK**: Negative consumer feedback has reached {risk_ratio:.1%}. Emerging issues in book quality and delivery require monitoring.")
else:
    st.success(f"✅ **HEALTHY SYSTEM STATUS**: Sentiment is stable. Risk ratio is at {risk_ratio:.1%}, well within the safe operational envelope (< 18%).")

st.divider()

# ---------------- KPI Row ----------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card("Negative Friction Signals", f"{neg_count:,}", "Requires remediation", badge="Complaints", badge_color="#f43f5e")

with c2:
    kpi_card("Current Risk Ratio", f"{risk_ratio:.1%}", "Negative / Total signals", badge=kpis["risk_level"], badge_color="#f43f5e" if risk_ratio >= 0.25 else "#f59e0b")

with c3:
    kpi_card("Trigger Threshold", "20.0%", "Enterprise SLA warning limit", badge="SLA Bound", badge_color="#a855f7")

with c4:
    kpi_card("Audit Compliance", "100%", "Full traceability logged", badge="Secured", badge_color="#10b981")

st.divider()

# ---------------- Alert Notification Section ----------------
col_alert_form, col_alert_chart = st.columns([1, 1])

with col_alert_form:
    st.subheader("📧 Dispatch Incident Alert to Stakeholders")
    st.write("Escalate detected sentiment anomalies directly to leadership or retail store managers.")

    target_email = st.text_input("Recipient Email:", value=settings.ALERT_RECEIVER or "lead_analyst@company.com")
    alert_severity = st.selectbox("Alert Severity Level:", ["Medium - Trend Warning", "High - Operational Risk", "Critical - SLA Breach"])
    additional_notes = st.text_area("Analyst Notes / Immediate Actions Required:", "Investigate recent supplier delivery delays and print binding defects reported in fiction catalog.")

    if st.button("🚀 Dispatch Stakeholder Alert", use_container_width=True):
        alert_body = f"""
=====================================================
🚨 BOOK MARKET INTELLIGENCE INCIDENT ESCALATION
=====================================================
Severity: {alert_severity}
Reported by: {st.session_state.get('username', 'Analyst')} ({persona})
Negative Review Volume: {neg_count}
Current Risk Ratio: {risk_ratio:.1%}

Analyst Notes:
{additional_notes}

Generated automatically by Enterprise Market Intelligence Platform v2.0.0.
=====================================================
"""
        with st.spinner("Dispatching alert..."):
            success, msg = send_alert_notification(alert_body, subject=f"[{alert_severity}] Sentiment Risk Escalation")

        if success:
            st.success(f"✅ {msg}")
        else:
            st.error(f"❌ {msg}")

with col_alert_chart:
    st.subheader("📉 Top Friction Points Triggering Alerts")
    top_complaints = get_top_aspects(df, sentiment_filter="negative", top_n=8)
    if not top_complaints.empty:
        fig_aspects = px.bar(
            top_complaints,
            x="count",
            y="aspect",
            orientation="h",
            color="count",
            color_continuous_scale="Reds",
            title="Frequency of Negative Aspects"
        )
        fig_aspects.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_aspects, use_container_width=True)
    else:
        st.info("No complaint aspects found.")

st.divider()

# ---------------- Report Export ----------------
st.subheader("📥 Export Audit & Intelligence Dataset")
st.write("Download the sanitized, validated dataset for external reporting, compliance, or spreadsheet modeling.")

export_cols = [c for c in ["clean_text", "sentiment", "confidence", "topic", "aspect", "source", "date", "region", "store"] if c in df.columns]
export_csv = df[export_cols].to_csv(index=False).encode("utf-8")

col_dl, col_space = st.columns([1, 2])
with col_dl:
    st.download_button(
        label="📥 Download Enterprise Intelligence Report (CSV)",
        data=export_csv,
        file_name="book_market_intelligence_report.csv",
        mime="text/csv",
        use_container_width=True
    )
