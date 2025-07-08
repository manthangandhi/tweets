import openai
import csv
import smtplib
import urllib.parse
from email.mime.text import MIMEText
from datetime import datetime

# Load users
with open('users.csv', 'r') as f:
    lines = list(csv.reader(f))[1:]  # skip header

# Generate tweet
openai.api_key = "YOUR_OPENAI_API_KEY"
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a sarcastic, witty, and dark humor writer."},
        {"role": "user", "content": "Write a dark humor tweet under 280 characters."}
    ]
)
tweet = response['choices'][0]['message']['content'].strip()
encoded = urllib.parse.quote(tweet)

# Compose email
body = f"""
<h3>💀 Hourly Dose of Dark Humor</h3>
<p>{tweet}</p>
<p><a href="https://twitter.com/intent/tweet?text={encoded}" target="_blank">👉 Click here to Tweet</a></p>
"""
subject = f'Dark Tweet at {datetime.now().strftime("%I:%M %p")}'

# Send to all users
for name, email in lines:
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = 'DarkTweetMail <you@yourdomain.com>'
    msg['To'] = email

    server = smtplib.SMTP("smtp.mailgun.org", 587)
    server.starttls()
    server.login("postmaster@yourdomain.com", "MAILGUN_API_KEY")
    server.sendmail(msg['From'], [msg['To']], msg.as_string())
    server.quit()