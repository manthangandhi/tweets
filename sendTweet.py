import openai
import csv
import os
import urllib.parse
from email.utils import formataddr
from datetime import datetime
import requests

# Load recipients from users.csv
with open('users.csv', 'r') as f:
    users = list(csv.reader(f))[1:]  # Skip header

# Generate tweet with OpenAI
client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a sarcastic, dark humor writer."},
        {"role": "user", "content": "Write a dark humor tweet under 280 characters."}
    ]
)

tweet = response.choices[0].message.content.strip()
encoded = urllib.parse.quote(tweet)

# Email HTML content
body = f"""
<h3>💀 Hourly Dose of Dark Humor</h3>
<p>{tweet}</p>
<p><a href="https://twitter.com/intent/tweet?text={encoded}" target="_blank">👉 Click here to Tweet</a></p>
"""
subject = f'Dark Tweet at {datetime.now().strftime("%I:%M %p")}'

# Resend config
resend_api_key = os.environ["RESEND_EMAIL_KEY"]
sender = "DarkTweetBot <onboarding@resend.dev>"

# Send email to each user using Resend API
for name, email in users:
    data = {
        "from": sender,
        "to": [email],
        "subject": subject,
        "html": body
    }

    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {resend_api_key}",
            "Content-Type": "application/json"
        },
        json=data,
    )

    print(f"✅ Email sent to {email}: {response.status_code}")