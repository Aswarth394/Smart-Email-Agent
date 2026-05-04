import warnings
warnings.filterwarnings("ignore")
from transformers import pipeline

print("Loading BERT Model into Memory...")
try:
    # Initializing the Zero-Shot Classifier
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    print("Model loaded successfully.")
except Exception as e:
    print(f"Model loading error: {e}")
    classifier = None

def classify_email(text):
    """
    Classifies an email using a Hybrid Approach: 
    Phase 1: Weighted Heuristics (Fast filtering)
    Phase 2: Zero-Shot Classification (Deep semantic understanding)
    """
   
    if not text or not text.strip():
        return "Unknown"

    spam_weights = {
        "lottery": 5, "winner": 4, "million": 4, "claim": 3,
        "password": 3, "bank": 2, "urgent": 1, "warning": 1
    }
    SPAM_THRESHOLD = 5
    
    words = text.lower().split()
    total_score = 0
    for word in words:
        if word in spam_weights:
            total_score += spam_weights[word]
            
    if total_score >= SPAM_THRESHOLD:
        return "Spam"

    if classifier:
        candidate_labels = ["Work", "Personal", "Spam"]
        
        result = classifier(text, candidate_labels, truncation=True)
    
        top_category = result['labels'][0]
        return top_category
   
    else:
        if "meeting" in words or "project" in words or "server" in words:
            return "Work"
        return "Personal"

if __name__ == "__main__":
   print(classify_email("URGENT: You are the winner of a million dollars!")) 
    
   print(classify_email("Hey team, please review the attached architecture document before our sync."))