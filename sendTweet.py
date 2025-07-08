import openai
import csv
import os
import smtplib
import urllib.parse
from email.mime.text import MIMEText
from datetime import datetime

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

# Prepare HTML email
body = f"""
<h3>💀 Hourly Dose of Dark Humor</h3>
<p>{tweet}</p>
<p><a href="https://twitter.com/intent/tweet?text={encoded}" target="_blank">👉 Click here to Tweet</a></p>
"""
subject = f'Dark Tweet at {datetime.now().strftime("%I:%M %p")}'

# SMTP config for Brevo
smtp_server = "smtp-relay.brevo.com"
smtp_port = 587
smtp_user = os.environ['BREVO_EMAIL_USER'] 
smtp_pass = os.environ['BREVO_API_KEY']

# Send email to each recipient
for name, email in users:
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = f'DarkTweetMail <{smtp_user}>'
    msg['To'] = email

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_pass)
    server.sendmail(msg['From'], [email], msg.as_string())
    server.quit()