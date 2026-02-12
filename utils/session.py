import streamlit as st
from utils.rag_panel import rag_panel

def load_chat():
    rag_panel()

def init_session():
    defaults = {
        "persona": "",   # must be filled at signup
        "user": None,
        "auth": False,
        "role": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
