import os
import json
import base64
from bs4 import BeautifulSoup
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def fetch_and_clean_emails():
    # --- STEP 1 & 2: Same Authentication as before ---
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        print("Error: No token found. Run gmail_auth.py first!")
        return

    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', maxResults=15).execute()
    messages = results.get('messages', [])

    if not messages:
        return

    final_data = []

    for msg in messages:
        content = service.users().messages().get(userId='me', id=msg['id']).execute()
        
        # --- STEP 3: Headers (Same as before) ---
        headers = content['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
        sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown")

        # --- STEP 4: The Deep Logic Body Extraction ---
        body_text = "No readable text" # The Fallback
        
        # Look for the 'parts' list (where Gmail hides the actual text)
        if 'parts' in content['payload']:
            for part in content['payload']['parts']:
                # We specifically want the plain text or HTML parts
                if part['mimeType'] in ['text/plain', 'text/html']:
                    raw_scramble = part['body'].get('data', '')
                    if raw_scramble:
                        # 1. Decode the Base64 scramble into raw HTML string
                        decoded_html = base64.urlsafe_b64decode(raw_scramble).decode('utf-8')
                        
                        # 2. Use BeautifulSoup to strip away all <div> and <br> tags
                        soup = BeautifulSoup(decoded_html, 'html.parser')
                        body_text = soup.get_text(separator=' ', strip=True)
                        break # Stop looking once we find the first readable part
                        
        # If 'parts' doesn't exist, try grabbing it from the main body directly
        elif 'data' in content['payload']['body']:
            raw_scramble = content['payload']['body']['data']
            decoded_html = base64.urlsafe_b64decode(raw_scramble).decode('utf-8')
            soup = BeautifulSoup(decoded_html, 'html.parser')
            body_text = soup.get_text(separator=' ', strip=True)

        email_entry = {
            "id": msg['id'],
            "sender": sender,
            "subject": subject,
            "body": body_text 
        }
        final_data.append(email_entry)
        print(f"Cleaned & Fetched: {subject}")

    with open('data/emails.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4)

    print("\nSUCCESS: 15 Cleaned emails saved to data/emails.json")

if __name__ == '__main__':
    fetch_and_clean_emails()