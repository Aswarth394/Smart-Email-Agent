# Smart AI Email Agent

## 1. Project Description

This project is an AI-based Email Management System that helps automate the process of handling emails. Traditional email systems require users to manually read, filter, and reply to emails, which is time-consuming.

The Smart AI Email Agent improves this by automatically performing the following tasks:

* Fetches unread emails from Gmail using the Gmail API
* Extracts important information such as subject, sender, and body
* Classifies emails into three categories: Work, Personal, and Spam
* Generates a short summary of each email
* Creates a reply draft automatically using an AI model
* Displays all processed emails in a dashboard

The system uses Machine Learning (learning from data patterns), Natural Language Processing (understanding human language), and an AI Agent (decision-making system) to improve productivity.


## 2. Installation Steps

Step 1: Clone the repository

```bash
git clone https://github.com/Aswarth394/Smart-Email-Agent
cd smart-ai-email-agent
```

Step 2: Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

Step 4: Setup API credentials

1. Download credentials.json from Google Cloud Console (Gmail API enabled)
2. Place it in the project root folder

Step 5: Setup environment variables

Create a file named `.env` and add:

GROQ_API_KEY=your_groq_api_key_here

3. How to Run the Project

Step 1: Start the backend agent

```bash
python master_agent.py
```

This process:

* Fetches emails continuously
* Classifies them
* Stores results in JSON files

Step 2: Start the dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser at:
http://localhost:8501



## 4. Example Input / Output

Example Input:

Subject: Invitation to birthday party

From: Mounish Vadagam ([mounish.v24@iiits.in](mailto:mounish.v24@iiits.in))

Date: May 04, 2026 - 08:04 AM

Body:
Hey Aswarth, how are you? Tomorrow is my birthday and there is cake cutting at today midnight. You have to come, no excuses there. Bye



Example Output:

Category:
Personal

Summary:
The sender is inviting you to attend a birthday celebration with cake cutting at midnight.

Reply Draft:

Hi Mounish,

Thank you for the invitation. I will come for the cake cutting at midnight. Looking forward to celebrating with you.

Best regards,
Aswarth


