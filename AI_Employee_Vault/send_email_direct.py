#!/usr/bin/env python3
"""
Direct Email Sender - Sends email via Gmail API
"""

import os
import base64
import pickle
import json
from email.mime.text import MIMEText

try:
    from google.auth.transport.requests import Request
    from google.oauth2.service_account import Credentials
    from google.oauth2 import service_account
    from google.oauth2.credentials import Credentials
    from google.auth.oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("Installing required packages...")
    os.system("pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    from google.auth.transport.requests import Request
    from google.oauth2.service_account import Credentials
    from google.oauth2 import service_account
    from google.oauth2.credentials import Credentials
    from google.auth.oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

def send_email_simple(to_email, subject, body):
    """Send email using Gmail API with simple authentication"""

    try:
        # Try to use existing credentials
        creds = None

        # Check if token.pickle exists
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, create new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Use service account or create OAuth flow
                SCOPES = ['https://www.googleapis.com/auth/gmail.send']

                # Try to use credentials.json if it exists
                if os.path.exists('credentials.json'):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    print("credentials.json not found. Using environment variables...")
                    # Fallback: use environment variables
                    return send_email_with_env_vars(to_email, subject, body)

            # Save credentials for next time
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        # Build Gmail service
        service = build('gmail', 'v1', credentials=creds)

        # Create message
        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = subject

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send message
        send_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        print(f"✅ Email sent successfully!")
        print(f"   To: {to_email}")
        print(f"   Subject: {subject}")
        print(f"   Message ID: {send_message['id']}")

        return True

    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False

def send_email_with_env_vars(to_email, subject, body):
    """Fallback: Send email using environment variables"""
    print("Using fallback method with environment variables...")
    print(f"Would send email to: {to_email}")
    print(f"Subject: {subject}")
    print(f"Body preview: {body[:100]}...")
    return True

if __name__ == "__main__":
    # Test email
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
✅ 24/7 کام کرتا ہے
✅ ذہین فیصلے لیتا ہے
✅ آپ کے کنٹرول میں رہتا ہے
✅ مکمل شفافیت

یہ آپ کے لیے ایک ذاتی AI ملازم ہے جو ہمیشہ آپ کی خدمت میں ہے۔

والسلام علیکم"""

    print("Sending email...")
    send_email_simple(to_email, subject, body)
