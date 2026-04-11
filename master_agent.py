# master_agent.py
import time
import json
import os
from email_fetcher import fetch_unread_emails  
from classifier_bert import classify_email     

DATA_FILE = "data/dashboard_data.json"
MEMORY_FILE = "data/seen_emails.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return set(json.load(f))
        except: pass
    return set()

def save_memory(memory_set):
    with open(MEMORY_FILE, "w") as f:
        json.dump(list(memory_set), f)

def save_for_ui(email):
    os.makedirs("data", exist_ok=True)
    dashboard_data = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                dashboard_data = json.load(f)
        except: pass

    # We now save the ORIGINAL body text for the UI
    new_entry = {
        "id": email["id"],
        "subject": email["subject"],
        "sender": email["sender"],
        "body": email.get("body", "No content available."), 
        "category": email.get("category", "Personal"),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    dashboard_data.insert(0, new_entry)
    dashboard_data = dashboard_data[:20] # Keep latest 20

    with open(DATA_FILE, "w") as f:
        json.dump(dashboard_data, f, indent=4)

def run_lively_agent():
    print("🚀 AI Agent is ONLINE. Fetching and Classifying only...")
    processed_emails = load_memory() 
    
    while True:
        try:
            new_emails = fetch_unread_emails(limit=5)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)
            continue
            
        for email in new_emails:
            if email['id'] in processed_emails:
                continue 
                
            print(f"🔍 Storing New Email: {email['subject']}")
            
            # Categorize it (Spam, Work, Personal)
            email['category'] = classify_email(email['body'])
            
            # Save raw data to UI
            save_for_ui(email)
            
            processed_emails.add(email['id'])
            save_memory(processed_emails)

        time.sleep(30)

if __name__ == "__main__":
    run_lively_agent()