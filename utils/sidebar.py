import streamlit as st

def dashboard_sidebar():

    persona = st.session_state.persona

    # 🚨 Strict protection: persona must exist
    if not persona:
        st.error("Session invalid. Please login again.")
        st.switch_page("pages/Login.py")
        st.stop()

    st.sidebar.title(f"📊 {persona}")

    st.sidebar.page_link("pages/Overview.py", label="Overview")
    st.sidebar.page_link("pages/Market_Insights.py", label="Market Insights")
    st.sidebar.page_link("pages/Sentiment_Dashboard.py", label="Sentiment Analysis")
    st.sidebar.page_link("pages/Alerts_Reports.py", label="Alerts & Reports")

    st.sidebar.divider()

    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.switch_page("app.py")
