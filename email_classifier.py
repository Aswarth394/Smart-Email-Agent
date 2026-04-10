import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Step 1: Configuration & Security
load_dotenv()
# You will need to get an API Key from Google AI Studio (I will show you how next)
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

def classify_emails():
    # Step 2: Load our cleaned data from Day 3
    if not os.path.exists('data/emails.json'):
        print("Error: data/emails.json not found!")
        return
    
    with open('data/emails.json', 'r', encoding='utf-8') as f:
        emails = json.load(f)

    classified_results = []

    print("AI is now analyzing your emails...")

    for email in emails:
        # Step 3: Prompt Engineering (The Instructions for the Brain)
        # We give the AI a very strict 'Identity' and 'Format'
        prompt = f"""
        You are an elite Email Classifier. 
        Categorize the following email into exactly ONE of these labels: 
        [Transaction, Promotion, Personal, Social, Alert, Update].

        Subject: {email['subject']}
        Body: {email['body'][:500]} 

        Return ONLY the label name. No explanation.
        """
        
        # Step 4: Execution (The API Call)
        response = model.generate_content(prompt)
        category = response.text.strip()

        # Step 5: Append the new 'Category' to our data
        email['category'] = category
        classified_results.append(email)
        print(f"Subject: {email['subject'][:30]}... -> CATEGORY: {category}")

    # Step 6: Save the new 'Intelligent' dataset
    with open('data/classified_emails.json', 'w', encoding='utf-8') as f:
        json.dump(classified_results, f, indent=4)

    print("\nSUCCESS: All emails classified and saved!")

if __name__ == '__main__':
    classify_emails()