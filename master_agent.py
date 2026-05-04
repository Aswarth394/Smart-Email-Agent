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
    os.makedirs("data", exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(list(memory_set), f)

def save_for_ui(email):
    os.makedirs("data", exist_ok=True)
    dashboard_data = []
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                dashboard_data = json.load(f)
                if isinstance(dashboard_data, dict): dashboard_data = []
        except: pass

    new_entry = {
        "id": email["id"],
        "subject": email["subject"],
        "sender": email["sender"],
        "body": email.get("body", "No content available."), 
        "category": email.get("category", "Personal"),
        "received_date": email.get("received_date", "Unknown Date"), 
        "sort_time": email.get("sort_time", 0.0), 
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Put the newest email at the very top
    dashboard_data.insert(0, new_entry)
    
    # FIFO Queue constraint. Keeps only 100, deleting the oldest.
    dashboard_data = dashboard_data[:100] 

    with open(DATA_FILE, "w") as f:
        json.dump(dashboard_data, f, indent=4)

def run_lively_agent():
    print(" AI Agent is ONLINE. Fetching strictly the latest 100 emails...")
    processed_emails = load_memory()

    while True:
        try:
            email_stream = fetch_unread_emails(limit=30, processed_ids=processed_emails)
            has_new_emails = False

            for email in email_stream:
                has_new_emails = True
                print(f" Classifying New Email: {email['subject'][:40]}")

                email['category'] = classify_email(email['subject']+""+email['body'])
               ## print(email['subject']+""+email['body'])
                save_for_ui(email)

                processed_emails.add(email['id'])
                save_memory(processed_emails)

            if not has_new_emails:
                print(f" {time.strftime('%H:%M:%S')} - No new emails. Inbox is up to date. Waiting...")

        except Exception as e:
            print(f" Network Wait: {e}")
            time.sleep(2)
            continue

        time.sleep(10)
        

if __name__ == "__main__":
    run_lively_agent()