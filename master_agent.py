# master_agent.py
import time
import json
import os
from email_fetcher import fetch_unread_emails  
from agent import EmailAgent                  
from classifier_bert import classify_email     

AGENT = EmailAgent(api_key="YOUR_API_KEY")

# This is the file Streamlit will read from
DATA_FILE = "data/dashboard_data.json"

def save_for_ui(email, results):
    """
    Saves the Agent's decisions to a JSON file so Streamlit can display them.
    """
    # Create the 'data' folder if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Load existing data so we don't delete older emails
    dashboard_data = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                dashboard_data = json.load(f)
        except json.JSONDecodeError:
            dashboard_data = []

    # Create the data package for the UI
    new_entry = {
        "id": email["id"],
        "subject": email["subject"],
        "sender": email["sender"],
        "category": email.get("category", "Personal"),
        "summary": results.get("summary", "No summary available."),
        "draft": results.get("draft", "No draft required."),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Add the new email to the top of the list
    dashboard_data.insert(0, new_entry)
    
    # Keep only the latest 20 emails to keep the dashboard fast
    dashboard_data = dashboard_data[:20]

    # Save it to the hard drive for Streamlit to read
    with open(DATA_FILE, "w") as f:
        json.dump(dashboard_data, f, indent=4)

def run_lively_agent():
    print("🚀 AI Agent is ONLINE. Monitoring Gmail...")
    
    # THE MEMORY: Stops the infinite loop
    processed_emails = set() 
    
    while True:
        try:
            new_emails = fetch_unread_emails(limit=3)
        except Exception as e:
            print(f"Error fetching: {e}")
            time.sleep(10)
            continue
        
        if not new_emails:
            print("📭 Inbox clean. Checking in 30s...")
            time.sleep(30)
            continue
            
        for email in new_emails:
            # 1. Check Memory: Skip if already processed
            if email['id'] in processed_emails:
                continue 
                
            print(f"🔍 New Email: {email['subject']}")
            
            # 2. REASON: ML Classification
            email['category'] = classify_email(email['body'])
            
            # 3. SEARCH: Bounded BFS 
            results = AGENT.process_new_email(email, email.get('threadMap', {}))
            
            print(f"✅ Action Taken: {email['category']} processed.")
            
            # 4. ACTION: Send to Streamlit Dashboard
            save_for_ui(email, results)
            
            # 5. Update Memory
            processed_emails.add(email['id'])

        time.sleep(30)

if __name__ == "__main__":
    run_lively_agent()