from gmail_auth import authenticate_gmail
import base64
from bs4 import BeautifulSoup
import email.utils 

def clean_html(raw_html):
    if not raw_html: return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator="\n").strip()

def get_full_body(payload):
    body_data = ""
    if 'data' in payload.get('body', {}):
        data = payload['body']['data']
        body_data = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    elif 'parts' in payload:
        for part in payload['parts']:
            mime_type = part.get('mimeType', '')
            if mime_type == 'text/plain':
                data = part['body'].get('data', '')
                body_data = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                break 
            elif mime_type == 'text/html':
                data = part['body'].get('data', '')
                body_data = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            elif 'parts' in part:
                body_data = get_full_body(part)
                if body_data: break
    return clean_html(body_data)

def fetch_unread_emails(limit=30, processed_ids=None): 
    if processed_ids is None:
        processed_ids = set()
        
    service = authenticate_gmail()
    
    results = service.users().messages().list(
        userId='me', 
        includeSpamTrash=True, 
        maxResults=limit
    ).execute()
    
    messages = results.get('messages', [])
    
    for msg in messages:
        # THE FIX: If it's in memory, instantly skip. Do NOT print anything!
        if msg['id'] in processed_ids:
            continue 
            
        try:
            txt = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            
            payload = txt['payload']
            headers = payload['headers']
            
            subject = "No Subject"
            sender = "Unknown Sender"
            raw_date = "Unknown Date"
            
            for h in headers:
                if h['name'].lower() == 'subject': subject = h['value']
                if h['name'].lower() == 'from': sender = h['value']
                if h['name'].lower() == 'date': raw_date = h['value'] 

            try:
                parsed_date = email.utils.parsedate_to_datetime(raw_date)
                clean_date = parsed_date.strftime("%b %d, %Y - %I:%M %p") 
                sort_time = parsed_date.timestamp() 
            except:
                clean_date = raw_date
                sort_time = 0.0
                
            #  We only print this if the ID was NOT in memory.
            print(f" New Email: {subject[:30]}...")
            
            yield {
                'id': msg['id'],
                'threadId': msg['threadId'],
                'subject': subject,
                'sender': sender,
                'received_date': clean_date, 
                'sort_time': sort_time,      
                'body': get_full_body(payload) 
            }

        except Exception as e:
            continue