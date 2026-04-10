# classifier_bert.py
from transformers import pipeline

# Load the BERT model for AI Logic requirement
print("Loading BERT Model into Memory...")
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

def classify_email(text):
    """
    Uses BERT to categorize email content.
    """
    if not text or len(text) < 5:
        return "Personal"
    
    # BERT has a 512 token limit
    result = classifier(text[:512])[0]
    
    # Basic mapping for demonstration
    if result['label'] == 'POSITIVE':
        return "Work"
    return "Personal"


"""
import json
from transformers import pipeline

# We keep this here. We will use it for Priority Scoring next week!
def rule_based_classify(email_subject, email_body):
    text = (email_subject + " " + email_body).lower()
    urgent_keywords = ['urgent', 'deadline', 'immediately', 'asap']
    work_keywords = ['meeting', 'project', 'assignment', 'report', 'submit']
    spam_keywords = ['offer', 'discount', 'free', 'win', 'limited time']

    for word in urgent_keywords:
        if word in text: return "Urgent"
    for word in work_keywords:
        if word in text: return "Work"
    for word in spam_keywords:
        if word in text: return "Spam"
    return "Personal"

# --- THE ML UPGRADE ---
print("Loading BERT Model into Memory... (This takes a few seconds)")
# We use zero-shot classification with distilbert to satisfy the ML requirement
bert_classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
candidate_labels = ["Urgent", "Work", "Personal", "Finance", "Spam"]

def bert_classify(email_subject, email_body):
    # We slice the body to 200 characters to prevent memory crashes
    text = email_subject + " " + email_body[:200]
    result = bert_classifier(text, candidate_labels)
    # Return the label with the highest probability score
    return result['labels'][0]

def process_all_emails():
    print("Reading emails.json...")
    with open('data/emails.json', 'r', encoding='utf-8') as f:
        emails = json.load(f)

    print(f"Loaded {len(emails)} emails. Starting BERT Classification...")

    for email in emails:
        # We pass the real subject and body into our new BERT Brain
        subject = email.get('subject', 'No Subject')
        body = email.get('body', 'No readable text')
        
        category = bert_classify(subject, body)
        email['category'] = category
        
        print(f"Subject: {subject[:30]}... -> CATEGORY: {category}")

    # Save to a new file so we don't destroy our raw data
    with open('data/emails_classified.json', 'w', encoding='utf-8') as f:
        json.dump(emails, f, indent=4)
    
    print("\nSUCCESS: All emails classified and saved to data/emails_classified.json!")

# --- Execution Entry Point ---
if __name__ == '__main__':
    process_all_emails()
    
"""