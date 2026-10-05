"""
Integrated interactive RAG Chatbot widget for Streamlit dashboards.
"""

import streamlit as st
from book_market_intelligence.rag.engine import rag_engine


def render_rag_widget() -> None:
    """Renders the AI Market Intelligence Assistant chat widget in the sidebar."""
    with st.sidebar:
        st.markdown("---")
        with st.expander("💬 AI Market Analyst Assistant", expanded=False):
            st.caption("Ask questions across customer reviews and get data-backed answers.")

            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            # Display previous chat messages
            chat_container = st.container()
            with chat_container:
                for role, text in st.session_state.chat_history[-6:]:
                    if role == "user":
                        st.markdown(f"**🧑 You:** {text}")
                    else:
                        st.markdown(f"**🤖 AI:** {text}")

            user_query = st.text_input("Ask a market question:", key="rag_sidebar_query_input", placeholder="e.g. Why are deliveries delayed?")

            col_send, col_clear = st.columns([2, 1])
            if col_send.button("Send", key="rag_send_btn", use_container_width=True) and user_query.strip():
                with st.spinner("Analyzing feedback corpus..."):
                    result = rag_engine.query(user_query)

                st.session_state.chat_history.append(("user", user_query))
                st.session_state.chat_history.append(("ai", result.answer))
                st.rerun()

            if col_clear.button("Clear", key="rag_clear_btn", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
