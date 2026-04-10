# app.py (Advanced Two-Pane Layout)
import streamlit as st
import json
import os

# 1. Page Config for a wider layout
st.set_page_config(page_title="Smart Email Agent", page_icon="📧", layout="wide")

st.title("📧 Smart AI Email Agent")
st.markdown("**Built by Aswarth | B.Tech Artificial Intelligence & Data Science**")
st.markdown("---")

@st.cache_data
def load_data():
    file_path = 'data/emails_actionable.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

emails = load_data()

if not emails:
    st.error("No data found in emails_actionable.json!")
else:
    # --- The Two-Pane Architecture ---
    # col1 is the left menu (30% width), col2 is the main view (70% width)
    col1, col2 = st.columns([1, 2.5])
    
    # Session State to track which email is actively selected
    if 'selected_email_index' not in st.session_state:
        st.session_state.selected_email_index = 0

    # LEFT PANE: The Inbox List
    with col1:
        st.subheader("Inbox")
        for i, email in enumerate(emails):
            # Create a button for each email
            btn_label = f"[{email.get('category', 'N/A')}] {email.get('sender', 'Unknown').split('<')[0]}"
            if st.button(btn_label, key=f"btn_{i}", use_container_width=True):
                st.session_state.selected_email_index = i

    # RIGHT PANE: The Email Details
    with col2:
        # Get the currently selected email
        active_email = emails[st.session_state.selected_email_index]
        
        st.subheader(active_email.get('subject', 'No Subject'))
        st.caption(f"From: {active_email.get('sender', 'Unknown')}")
        st.markdown("---")
        
        # Display the AI features
        st.markdown("### ✨ AI Summary")
        st.info(active_email.get('summary', 'No summary available.'))
        
        st.markdown("### ✍️ Draft Reply")
        cat = active_email.get('category', '').lower()
        if cat in ['spam', 'promotions']:
            st.warning(active_email.get('draft_reply', 'No reply needed.'))
        else:
            st.success(active_email.get('draft_reply', 'No reply generated.'))