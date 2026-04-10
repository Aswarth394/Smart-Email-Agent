# agent.py
import json
import os
from bfs_thread import analyze_thread_bfs # Your Search Algorithm
from summarizer import summarize_email, generate_reply # Your LLM logic

class EmailAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        # In a real system, the thread_map comes from the Gmail API
        self.thread_memory = {} 

    def process_new_email(self, email_data, thread_map):
        """
        The Agent's reasoning loop.
        """
        print(f"\n[AGENT] Perceiving new input: {email_data['subject']}")
        
        # 1. SEARCH: Use BFS to get conversation history
        # This is the mandatory search algorithm requirement.
        history = analyze_thread_bfs(email_data['id'], thread_map)
        
        # 2. REASON: Decide the category and priority
        category = email_data.get('category', 'Personal')
        
        # 3. ACTION: Generate intelligence [cite: 19]
        summary = summarize_email(email_data['subject'], email_data['body'])
        
        if category.lower() != "spam":
            reply = generate_reply(email_data['subject'], summary, category)
        else:
            reply = "No action taken (Spam)."
            
        return {
            "summary": summary,
            "draft": reply,
            "thread_depth": len(history)
        }

# --- Test the Agent Logic ---
if __name__ == "__main__":
    # Mock data for the "Lively" demonstration [cite: 9]
    sample_email = {
        "id": "Email_A",
        "subject": "Project Viva Update",
        "body": "Please find the updated schedule attached.",
        "category": "Work"
    }
    
    # The same map your BFS just solved!
    mock_map = {'Email_A': ['Email_B'], 'Email_B': []}
    
    print("🤖 AI Agent is now thinking...")
    my_agent = EmailAgent(api_key="YOUR_KEY")
    result = my_agent.process_new_email(sample_email, mock_map)
    
    print(f"\n[AGENT DECISION]:\nSummary: {result['summary']}\nDraft: {result['draft']}")