# app.py
import streamlit as st
import json
import os
from agent import EmailAgent # We bring the Brain to the Frontend now

# Initialize the LLM Agent here so it can generate on-demand
AGENT = EmailAgent(api_key="YOUR_API_KEY") 

st.set_page_config(page_title="Smart AI Email Agent", layout="wide")
st.title("📧 Smart AI Email Agent")

DATA_FILE = "data/dashboard_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

st.sidebar.button("🔄 Refresh Inbox", on_click=st.rerun)
emails = load_data()

# The specific folders you requested
tab_work, tab_personal, tab_spam = st.tabs(["💼 Work", "🏠 Personal", "🚫 Spam"])

def display_email_box(email):
    with st.expander(f"📩 {email['subject']} (From: {email['sender']})"):
        
        # 1. Show Original Message First
        st.markdown("**Original Message:**")
        st.write(email['body'])
        st.divider()
        
        # Setup Session State Memory for Buttons
        sum_key = f"sum_{email['id']}"
        draft_key = f"draft_{email['id']}"
        
        if sum_key not in st.session_state:
            st.session_state[sum_key] = None
        if draft_key not in st.session_state:
            st.session_state[draft_key] = None

        # 2. The Interactive Buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✨ Summarize", key=f"btn_sum_{email['id']}"):
                with st.spinner("Analyzing..."):
                    # Call your agent's logic here on demand!
                    st.session_state[sum_key] = AGENT.process_new_email(email, {})['summary']
                    
            if st.session_state[sum_key]:
                st.info(st.session_state[sum_key])
                
        with col2:
            if st.button("✍️ Draft Reply", key=f"btn_draft_{email['id']}"):
                with st.spinner("Writing Draft..."):
                    # Call your agent's logic here on demand!
                    st.session_state[draft_key] = AGENT.process_new_email(email, {})['draft']
                    
            if st.session_state[draft_key]:
                st.success(st.session_state[draft_key])

# Filter into folders based on BERT output
with tab_work:
    for e in [e for e in emails if e.get("category") == "Work"]: display_email_box(e)

with tab_personal:
    for e in [e for e in emails if e.get("category") == "Personal"]: display_email_box(e)

with tab_spam:
    for e in [e for e in emails if e.get("category") not in ["Work", "Personal"]]: display_email_box(e)