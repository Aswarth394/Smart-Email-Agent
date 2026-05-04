import json
import os
from bfs_thread import analyze_thread_bfs  
from summarizer import summarize_email, generate_reply  

class EmailAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        # this would store full email data
        self.thread_memory = {}

    def process_new_email(self, email_data, thread_map):
       
        print(f"\n[AGENT] Perceiving new input: {email_data['subject']}")

        # Use BFS to get conversation history
        history = analyze_thread_bfs(email_data['id'], thread_map)
        category = email_data.get('category', 'Personal')

        context = ""
        for email_id in history:
        
            if email_id == email_data['id']:
                context += f"Subject: {email_data['subject']}\n"
                context += f"Body: {email_data['body']}\n\n"
                
        summary = summarize_email("Thread Summary", context)

        if category.lower() != "spam":
            reply = generate_reply(email_data['subject'], summary, category)
        else:
            reply = "No action taken (Spam)."

        return {
            "summary": summary,
            "draft": reply,
            "thread_depth": len(history)
        }


# Test the Agent Logic 
if __name__ == "__main__":
    sample_email = {
        "id": "Email_A",
        "subject": "Project Viva Update",
        "body": "Please find the updated schedule attached.",
        "category": "Work"
    }

    mock_map = {
        'Email_A': ['Email_B'],
        'Email_B': []
    }

    print(" AI Agent is now thinking...")
    my_agent = EmailAgent(api_key="YOUR_KEY")
    result = my_agent.process_new_email(sample_email, mock_map)

    print(f"\n[AGENT DECISION]:\nSummary: {result['summary']}\nDraft: {result['draft']}")