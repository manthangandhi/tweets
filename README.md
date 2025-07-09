# Dark Humor Tweet Mailer

This project generates and emails a set of witty, dark humor tweets (with an Indian context) to all active subscribers. Tweets are generated using OpenAI's GPT-4o-mini model and delivered via the Resend email API. Subscriber data is fetched from a Supabase database.

---

## What It Does
- Fetches a list of active subscribers from a Supabase table.
- Uses OpenAI to generate three short, dark humor tweets (under 140 characters, no hashtags, Indian context).
- Builds a visually appealing HTML email containing the tweets, each with a "Tweet This" button for easy sharing.
- Sends the email to each subscriber using the Resend email API.
- Includes an unsubscribe link for each recipient.

---

## Requirements
- OpenAI API key (for tweet generation)
- Supabase project and service key (for subscriber management)
- Resend API key (for email delivery)
- Sender email address and base URL for unsubscribe links

All configuration is handled via environment variables:
- `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `RESEND_API_KEY`, `OPENAI_API_KEY`, `SENDER_EMAIL`, `BASE_URL`

---

## File Overview
- `sendTweet.py` - Main script for generating and sending tweets
- `docs/` - Contains static HTML files (e.g., unsubscribe page)

---

## Notes
- This project is for educational/demonstration purposes and uses paid services (OpenAI, Resend, Supabase).
- Make sure your Supabase and Resend accounts are properly configured for production use.
- Each email includes an unsubscribe link for compliance and user convenience.

---

## License
MIT
