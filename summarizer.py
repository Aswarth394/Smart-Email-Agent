import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_email(subject, body):

    prompt = f"Summarize this email . Subject: {subject}\n\nEmail Body: {body}"
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.3
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def generate_reply(subject, summary, category):
   
    # Strict First-Person Identity Prompting
    draft_prompt = f"""
    You are Aswarth. You are writing a direct, personal reply to an email.
    
    Email Context:
    - Subject: {subject}
    - Summary of the message: {summary}
    - Category: {category}
    
    Strict Rules for your reply:
    1. Greet the sender professionally.
    2. Write strictly from the first-person perspective ("I"). 
    3. UNDER NO CIRCUMSTANCES should you refer to yourself as an AI, a bot, or an assistant.
    4. Keep the reply brief and directly related to the subject.
    5. Your signature must be exactly this, with nothing added or changed:
    
    Best regards,
    Aswarth
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": draft_prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"