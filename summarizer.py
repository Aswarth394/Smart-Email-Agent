# summarizer.py (Real-World Integration with Groq Llama 3)
import os
import json
from dotenv import load_dotenv
from groq import Groq

# Step 1: Securely Load the Vault & Initialize
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    api_key = input("\n[SYSTEM] Paste your exact Groq API Key (gsk_...): ").strip()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    print(f"Connection failed: {e}")

# Step 2: The Summarization Engine
def summarize_email(email_subject, email_body):
    prompt = f"""
    Summarize this email in exactly 2 sentences.
    Focus only on the main action item. Be direct.
    
    Subject: {email_subject}
    Body: {email_body[:800]} 
    """
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Summary Error: {str(e)}"

# Step 3: The Drafting Engine
def generate_reply(email_subject, email_summary, category):
    if category.lower() in ["spam", "promotions"]:
        return "No reply needed."

    prompt = f"""
    You are an AI assistant drafting an email reply for Aswarth.
    The email is categorized as: {category}.
    The summary of the email is: {email_summary}.
    
    Draft a polite, concise, and professional reply. 
    Keep it under 3 sentences. Do not include placeholders like [Your Name]. 
    Sign off as 'Aswarth's AI Assistant'.
    """
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Reply Error: {str(e)}"

# Step 4: The Real-World Batch Processor
def process_real_inbox():
    # 1. Open the output from Week 2
    if not os.path.exists('data/emails_classified.json'):
        print("ERROR: Run Week 2 classifier first!")
        return

    print("Loading real emails from Week 2...")
    with open('data/emails_classified.json', 'r', encoding='utf-8') as f:
        emails = json.load(f)

    print(f"Loaded {len(emails)} emails. Connecting to Groq...\n")
    actionable_emails = []

    # 2. Loop through every real email
    for email in emails:
        subject = email.get('subject', 'No Subject')
        body = email.get('body', 'No Text')
        category = email.get('category', 'Personal')

        print(f"Processing: {subject[:40]}...")

        # 3. Apply the Intelligence
        summary = summarize_email(subject, body)
        draft = generate_reply(subject, summary, category)

        # 4. Attach new intelligence to the email dictionary
        email['summary'] = summary
        email['draft_reply'] = draft
        actionable_emails.append(email)

    # 5. Save the final Week 3 output
    with open('data/emails_actionable.json', 'w', encoding='utf-8') as f:
        json.dump(actionable_emails, f, indent=4)

    print("\nSUCCESS: All 15 real emails summarized and replied to.")
    print("Check 'data/emails_actionable.json' to see the final outputs!")

# --- Execution Entry Point ---
if __name__ == '__main__':
    process_real_inbox()