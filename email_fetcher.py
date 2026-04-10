# email_fetcher.py
from gmail_auth import authenticate_gmail

def fetch_unread_emails(limit=5):
    """
    Connects to Gmail and fetches 'unread' messages.
    """
    service = authenticate_gmail()
    
    # Search for unread messages
    results = service.users().messages().list(userId='me', q='is:unread', maxResults=limit).execute()
    messages = results.get('messages', [])
    
    email_list = []
    for msg in messages:
        # Get full email details
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        
        # Extract metadata
        payload = txt['payload']
        headers = payload['headers']
        subject = [h['value'] for h in headers if h['name'] == 'Subject'][0]
     
        sender = [h['value'] for h in headers if h['name'] == 'From'][0]
        
        email_list.append({
            'id': msg['id'],
            'threadId': msg['threadId'],
            'subject': subject,
            'sender': sender,
            'body': txt['snippet'] 
        })
        
    return email_list











""" 

import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Line 1: Permission level must match our token exactly
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def fetch_emails():
    # Line 2: Load the 'token.json' we created in Day 1
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        print("Error: No token found. Run gmail_auth.py first!")
        return

    # Line 3: Build the 'service'. This is the virtual "Hand" that reaches into Gmail.
    # 'gmail' is the API name, 'v1' is the version.
    service = build('gmail', 'v1', credentials=creds)

    # Line 4: Ask Gmail for a list of the 15 most recent messages
    results = service.users().messages().list(userId='me', maxResults=15).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No emails found.")
        return

    final_data = []

    # Line 5: Loop through each message ID found
    for msg in messages:
        # Line 6: Fetch the FULL content of this specific email using its ID
        content = service.users().messages().get(userId='me', id=msg['id']).execute()
        
        # Line 7: Extract the 'Headers' (where Subject and Sender live)
        headers = content['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
        sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown")

        # Line 8: Store the details in a Dictionary
        email_entry = {
            "id": msg['id'],
            "sender": sender,
            "subject": subject,
            "body": "Raw content fetched" # We will clean this in the next step
        }
        final_data.append(email_entry)
        print(f"Fetched: {sender}")
        print(f"----fetcehd :{subject}")

    # Line 9: Save the final list into a data folder
    os.makedirs('data', exist_ok=True)
    with open('data/emails.json', 'w') as f:
        json.dump(final_data, f, indent=4)

    print("\nSUCCESS: 15 emails saved to data/emails.json")

if __name__ == '__main__':
    fetch_emails()
    
    """