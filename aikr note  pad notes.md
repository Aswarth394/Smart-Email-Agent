# credentials.json (your Visitor Keycard)
The Difference: credentials.json is your permanent ID [like a passport]. token.json is your temporary session [like a boarding pass].
Automation: Once we create token.json, you won't have to log in through the browser every time you run your AI agent.
FORMAT CODE (clean structure)   --- Shift + Alt + F 
 python.exe -m pip install --upgrade pip  
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process




Reasoning (Brain): * ML Layer: Uses BERT to categorize the email.

Search Layer: Uses BFS (Breadth-First Search) to look for other emails in the same conversation thread to understand the history.

Rule-Based Layer: Checks for urgent keywords to assign a priority score.