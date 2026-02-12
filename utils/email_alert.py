import smtplib
from email.mime.text import MIMEText
import streamlit as st

def send_alert(message: str):

    sender = st.secrets["ALERT_EMAIL"]
    password = st.secrets["ALERT_PASSWORD"]
    receiver = st.secrets["ALERT_RECEIVER"]

    msg = MIMEText(message)
    msg["Subject"] = "🚨 Sentiment Alert"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
