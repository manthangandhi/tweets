# Dark Humor Tweet Mailer

This project generates dark humor tweets using OpenAI's GPT-3.5-turbo and emails them to a list of users. User emails are read from a CSV file, and emails are sent using Mailgun's SMTP service.

## Features
- Generates a dark humor tweet using OpenAI's GPT-3.5-turbo
- Sends the tweet to all users listed in `users.csv`
- Uses Mailgun SMTP for email delivery

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd tweets
```

### 2. Install Dependencies
```bash
pip install openai
```

### 3. Prepare User List
- Create a `users.csv` file in the project directory.
- The first row should be a header (e.g., `name,email`).
- Each subsequent row should contain a user's name and email address.

Example `users.csv`:
```
name,email
Alice,alice@example.com
Bob,bob@example.com
```

### 4. Configure API Keys and SMTP
- Open `.github/sendTweet.py` and set the following:
  - `openai.api_key = "<YOUR_OPENAI_API_KEY>"`
  - `server.login("postmaster@<YOUR_MAILGUN_DOMAIN>", "<MAILGUN_API_KEY>")`
  - Update the `msg['From']` address as needed.

### 5. Run the Script
```bash
python .github/sendTweet.py
```
- This will generate a tweet and send it to all users in `users.csv`.

---

## File Overview
- `.github/sendTweet.py` - Main script for generating and sending tweets
- `users.csv` - List of users to email (must be created by you)

---

## Notes
- This project requires an OpenAI API key and a Mailgun account (both paid services).
- Make sure your Mailgun account is authorized to send emails to your recipients.
- The script is intended for educational/demonstration purposes.

---

## License
MIT 