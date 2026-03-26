"""
Send Email using Gmail API
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from pathlib import Path
import base64
from email.mime.text import MIMEText

def send_email():
    # Authenticate
    token_path = Path('token.json')
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    if not token_path.exists():
        print('Token not found. Need to authenticate first.')
        return

    try:
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        service = build('gmail', 'v1', credentials=creds)

        # Email details
        to_email = "muhammad.saleem@example.com" # You can update the real email later
        subject = "Invitation to discuss AI meetup"
        body = """Hi Muhammad Saleem,

I hope this email finds you well.

I would like to invite you for a meetup to discuss AI and its potential impact. It would be great to connect and share ideas.

Please let me know your availability for a meeting.

Best regards,
Agentic Sphere Team"""

        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        print(f"Sending email to: {to_email}")
        print(f"Subject: {subject}")
        print("Body:")
        print(body)
        print("-" * 40)

        # Send email
        message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        print(f"Email sent successfully! Message ID: {message['id']}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_email()