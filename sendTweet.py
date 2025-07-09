import openai
import os
import requests
from datetime import datetime, timezone
from openai import OpenAI
from email.utils import formataddr
import urllib.parse

# Config
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
RESEND_API_KEY = os.environ["RESEND_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
SENDER_EMAIL = os.environ["SENDER_EMAIL"]  # example: darktweetbot@yourdomain.com
BASE_URL = os.environ["BASE_URL"]  # example: https://darktweetbot.vercel.app

# 1. Fetch active subscribers
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}
res = requests.get(
    f"{SUPABASE_URL}/rest/v1/subscribers?is_subscribed=eq.true&select=email",
    headers=headers
)
users = res.json()

if not users:
    print("No active users found.")
    exit(0)

# 2. Generate 3 tweets

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a dark humor writer who writes short, sarcastic, witty tweets under 140 characters in Indian context. Don't add hashtags or wrap in quotes."},
        {"role": "user", "content": "Write 3 dark humor tweets, each starting with '1.', '2.', and '3.'."}
    ]
)
content = response.choices[0].message.content.strip()

tweets = [
    line.split('.', 1)[1].strip()
    for line in content.splitlines()
    if line.strip().startswith(('1.', '2.', '3.'))
]

# 3. Build email HTML
body_blocks = ""
for tweet in tweets:
    encoded = urllib.parse.quote(tweet)
    tweet_button = f"""
        <tr>
            <td style="padding: 25px 40px 10px;">
                <p style="font-size: 20px; line-height: 1.6; color: #dcdcdc; margin: 0;">{tweet}</p>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 10px 40px;">
                <a href="https://twitter.com/intent/tweet?text={encoded}" target="_blank" style="background-color: #1da1f2; color: #fff; padding: 10px 24px; font-size: 14px; border-radius: 6px; text-decoration: none; font-weight: 600;">
                    Tweet This
                </a>
            </td>
        </tr>
        <tr><td style="height: 1px; background-color: #222; margin: 20px 0;"></td></tr>
    """
    body_blocks += tweet_button

utc_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')

# Email wrapper
html_body = f"""
<html><body style="background-color: #000000; font-family: Helvetica, sans-serif;">
  <table style="max-width: 640px; margin: auto; background-color: #111111; color: #ffffff; border-radius: 12px;">
    <tr><td style="padding: 40px; text-align: center; font-size: 28px; font-weight: bold; letter-spacing: 0.5px; color: #fff;">
      DarkTweetBot™ Drop
    </td></tr>
    {body_blocks}
    <tr>
      <td style="padding: 20px 40px; text-align: center; font-size: 12px; color: #666;">
        Dispatched: {utc_time} UTC &mdash; <a href="https://resend.com" style="color:#888;">Resend</a> + <a href="https://openai.com" style="color:#888;">OpenAI</a><br>
        <i>Because your humor deserves a black suit too.</i>
      </td>
    </tr>
  </table>
</body></html>
"""

# 4. Send email via Resend
for user in users:
    email = user['email']
    unsubscribe_link = f"{BASE_URL}/unsubscribe.html?email={urllib.parse.quote(email)}"
    full_body = html_body.replace("</body></html>", f"<p style='text-align:center;padding:20px;'><a href='{unsubscribe_link}' style='color:#777;'>Unsubscribe</a></p></body></html>")

    payload = {
        "from": formataddr(("DarkTweetBot", SENDER_EMAIL)),
        "to": [email],
        "subject": "Your DarkTweetBot™ Drop",
        "html": full_body
    }

    r = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    print(f"Sent to {email}: {r.status_code}")
