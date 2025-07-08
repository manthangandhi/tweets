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
body = body = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>DarkTweetBot™</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0; padding:0; background-color:#0f0f0f; font-family:'Helvetica Neue','Segoe UI',sans-serif; color:#e4e4e4;">

  <table width="100%" cellpadding="0" cellspacing="0" style="padding: 60px 0; background-color: #0f0f0f;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background-color:#181818; border-radius:10px; box-shadow: 0 0 20px rgba(0,0,0,0.4); overflow:hidden;">

          <!-- BRAND HEADER (minimalistic) -->
          <tr>
            <td style="padding: 24px 40px 10px; text-align: right;">
              <span style="font-size: 12px; color: #555; letter-spacing: 1px;">DarkTweetBot™</span>
            </td>
          </tr>

          <!-- TWEET BODY -->
          <tr>
            <td style="padding: 30px 40px 10px;">
              <p style="font-size: 20px; line-height: 1.6; color: #dcdcdc; margin: 0;">
                {tweet}
              </p>
            </td>
          </tr>

          <!-- CTA BUTTON -->
          <tr>
            <td align="center" style="padding: 30px 40px;">
              <a href="https://twitter.com/intent/tweet?text={encoded}" target="_blank" style="background-color: #1da1f2; color: #fff; padding: 12px 28px; font-size: 15px; border-radius: 6px; text-decoration: none; font-weight: 600; letter-spacing: 0.5px;">
                Tweet This
              </a>
            </td>
          </tr>

          <!-- FOOTER -->
          <tr>
            <td style="background-color: #111111; padding: 20px 40px; text-align: center; font-size: 12px; color: #666;">
              <div style="margin-bottom: 6px;">{datetime.now().strftime("%I:%M %p")} — powered by <a href="https://resend.com" style="color:#888; text-decoration:none;">Resend</a> + <a href="https://openai.com" style="color:#888; text-decoration:none;">OpenAI</a></div>
              <div style="color:#444; font-style: italic;">Because your humor deserves a black suit too.</div>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>

</body>
</html>
"""
subject = f'Dark Tweet at {datetime.now().strftime("%I:%M %p")}'

# Resend config
resend_api_key = os.environ["RESEND_API_KEY"]
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