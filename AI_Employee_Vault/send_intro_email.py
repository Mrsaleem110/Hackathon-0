#!/usr/bin/env python3
"""
Send introductory email using Gmail API
"""

import base64
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
import google.auth
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def send_email_via_api(to_email, subject, body):
    """Send email using Gmail API"""

    try:
        # Load token
        token_file = Path("token.json")
        if not token_file.exists():
            print("Error: token.json not found!")
            return False

        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

        # Refresh if needed
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Build Gmail service
        service = build('gmail', 'v1', credentials=creds)

        # Create message
        message = MIMEText(body, 'plain', 'utf-8')
        message['to'] = to_email
        message['subject'] = subject

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send
        send_message = {'raw': raw_message}
        result = service.users().messages().send(userId='me', body=send_message).execute()

        print(f"Email sent successfully!")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Message ID: {result['id']}")

        return True

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

if __name__ == "__main__":
    to_email = "sm6928234@gmail.com"
    subject = "Agentic Sphere - Your Personal AI Employee"
    body = """السلام علیکم

میں آپ کو Agentic Sphere کا تعارف کرانا چاہتا ہوں - ایک انقلابی AI نظام جو آپ کے ذاتی اور کاروباری کاموں کو خودکار طریقے سے سنبھالتا ہے۔

Agentic Sphere کیا ہے؟
یہ ایک ذہین AI نظام ہے جو:
- آپ کی emails، WhatsApp، اور LinkedIn کو monitor کرتا ہے
- ذہین منصوبے بناتا ہے
- آپ کی منظوری سے کام انجام دیتا ہے
- ہر کام کا مکمل ریکارڈ رکھتا ہے

فوائل:
✓ 24/7 کام کرتا ہے
✓ ذہین فیصلے لیتا ہے
✓ آپ کے کنٹرول میں رہتا ہے
✓ مکمل شفافیت

یہ آپ کے لیے ایک ذاتی AI ملازم ہے جو ہمیشہ آپ کی خدمت میں ہے۔

والسلام علیکم"""

    print("Sending email via Gmail API...")
    send_email_via_api(to_email, subject, body)
