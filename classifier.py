# classifier.py

def rule_based_classify(email_subject, email_body):
    # Step 1: Normalization
    # We combine the text and make it all lowercase so 'Urgent' and 'urgent' match perfectly.
    text = (email_subject + " " + email_body).lower()

    # Step 2: The Knowledge Base (Our keyword lists)
    urgent_keywords = ['urgent', 'deadline', 'immediately', 'asap']
    work_keywords = ['meeting', 'project', 'assignment', 'report', 'submit']
    spam_keywords = ['offer', 'discount', 'free', 'win', 'limited time']

    # Step 3: The Routing Logic (Checking for matches)
    # Priority 1: Check for Urgent words first
    for word in urgent_keywords:
        if word in text:
            return "Urgent"
            
    # Priority 2: Check for Work words
    for word in work_keywords:
        if word in text:
            return "Work"
            
    # Priority 3: Check for Spam words
    for word in spam_keywords:
        if word in text:
            return "Spam"

    # Step 4: The Fallback
    # If the email contains none of our keywords, we label it Personal.
    return "Personal"

# --- Testing the Engine ---
if __name__ == '__main__':
    # Let's test it with a fake email
    test_subject = "Assignment 3 submission"
    test_body = "Please remember to submit your project report by tomorrow."
    
    result = rule_based_classify(test_subject, test_body)
    print(f"Rule-Based Engine Output: {result}")