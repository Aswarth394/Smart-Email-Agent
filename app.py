import streamlit as st
import json
import os
from agent import EmailAgent 

AGENT = EmailAgent(api_key="YOUR_API_KEY") 

st.set_page_config(page_title="Smart AI Email Agent", layout="wide")
st.title("Smart AI Email Agent")

DATA_FILE = "data/dashboard_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, dict): return []
                return data
        except: pass
    return []

if st.sidebar.button(" Refresh Inbox"):
    st.rerun()

# Load all fetched emails
raw_emails = load_data()

# NEW LOGIC: Sort the entire dataset chronologically (Newest -> Oldest)
emails = sorted(raw_emails, key=lambda x: x.get('sort_time', 0.0), reverse=True)

work_emails = [e for e in emails if e.get("category") == "Work"]
personal_emails = [e for e in emails if e.get("category") == "Personal"]
spam_emails = [e for e in emails if e.get("category") not in ["Work", "Personal"]]

st.sidebar.metric(label="Total Unread Processed", value=len(emails))

tab_work, tab_personal, tab_spam = st.tabs([
    f"💼 Work ({len(work_emails)})", 
    f"🏠 Personal ({len(personal_emails)})", 
    f"🚫 Spam ({len(spam_emails)})"
])

def display_email_box(email):
    word_count = len(email.get('body', '').split())
    read_time_mins = max(1, word_count // 200) 
    
    # NEW LOGIC: Extract the clean date
    display_date = email.get("received_date", "Unknown Date")
    
    # NEW LOGIC: Add the date into the UI Expander header
    with st.expander(f"📩 {email['subject']} (From: {email['sender']}) | 📅 {display_date} | ⏱️ ~{read_time_mins} min read"):
        
        st.markdown("**Original Message:**")
        st.write(email['body'])
        st.divider()
        
        sum_key = f"sum_{email['id']}"
        draft_key = f"draft_{email['id']}"
        
        if sum_key not in st.session_state: st.session_state[sum_key] = None
        if draft_key not in st.session_state: st.session_state[draft_key] = None

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✨ Summarize", key=f"btn_sum_{email['id']}"):
                with st.spinner("Analyzing..."):
                    st.session_state[sum_key] = AGENT.process_new_email(email, {})['summary']
            if st.session_state[sum_key]: st.info(st.session_state[sum_key])
                
        with col2:
            if st.button("✍️ Draft Reply", key=f"btn_draft_{email['id']}"):
                with st.spinner("Writing Draft..."):
                    st.session_state[draft_key] = AGENT.process_new_email(email, {})['draft']
            if st.session_state[draft_key]: st.success(st.session_state[draft_key])

with tab_work:
    for e in work_emails: display_email_box(e)
with tab_personal:
    for e in personal_emails: display_email_box(e)
with tab_spam:
    for e in spam_emails: display_email_box(e)