# email_fetcher.py
from gmail_auth import authenticate_gmail
import base64 # Required to decode the hidden email text

def get_full_body(payload):
    """
    Recursively searches the Gmail payload to extract the full plain text body.
    """
    # 1. If the email is simple text
    if 'data' in payload.get('body', {}):
        data = payload['body']['data']
        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    
    # 2. If the email has multiple parts (like attachments or HTML)
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            elif 'parts' in part: # Search deeper if needed
                return get_full_body(part)
    
    return ""

def fetch_unread_emails(limit=5):
    """
    Connects to Gmail and fetches 'unread' messages with their FULL body.
    """
    service = authenticate_gmail()
    results = service.users().messages().list(userId='me', q='is:unread', maxResults=limit).execute()
    messages = results.get('messages', [])
    
    email_list = []
    for msg in messages:
        # We must request the 'full' format to get the payload
        txt = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        
        payload = txt['payload']
        headers = payload['headers']
        
        subject = "No Subject"
        sender = "Unknown Sender"
        for h in headers:
            if h['name'].lower() == 'subject': subject = h['value']
            if h['name'].lower() == 'from': sender = h['value']
        
        # THE FIX: Extract the full decoded body instead of just the snippet
        full_body = get_full_body(payload)
        
        # Fallback to the snippet if the email is completely empty
        if not full_body.strip():
            full_body = txt.get('snippet', '')
            
        email_list.append({
            'id': msg['id'],
            'threadId': msg['threadId'],
            'subject': subject,
            'sender': sender,
            'body': full_body 
        })
        
    return email_list