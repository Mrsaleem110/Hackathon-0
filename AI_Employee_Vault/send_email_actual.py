#!/usr/bin/env python3
"""
Send actual meeting reminder email using Gmail OAuth credentials from .env
"""

import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
import json
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """Get Gmail service using OAuth flow"""

    creds = None
    token_path = Path('gmail_token_meeting.json')

    # Try to load existing token
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

            # Refresh if expired
            if creds.expired and creds.refresh_token:
                print("Refreshing expired token...")
                creds.refresh(Request())
                with open(token_path, 'w') as f:
                    f.write(creds.to_json())
                print("Token refreshed!")
                return creds

            if creds.valid:
                return creds
        except Exception as e:
            print(f"Token error: {e}")
            creds = None

    # Create credentials.json from .env
    client_id = os.getenv('GMAIL_CLIENT_ID')
    client_secret = os.getenv('GMAIL_CLIENT_SECRET')
    redirect_uri = os.getenv('GMAIL_REDIRECT_URI', 'http://localhost:8080/callback')

    if not client_id or not client_secret:
        print("Error: GMAIL_CLIENT_ID or GMAIL_CLIENT_SECRET not set in .env")
        return None

    # Create temporary credentials file
    credentials_data = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": [redirect_uri],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }

    creds_file = Path('temp_credentials.json')
    with open(creds_file, 'w') as f:
        json.dump(credentials_data, f)

    try:
        # Run OAuth flow
        print("\nOpening browser for Gmail authentication...")
        print("Please login and grant permissions to send emails.\n")

        flow = InstalledAppFlow.from_client_secrets_file(
            str(creds_file),
            SCOPES
        )
        creds = flow.run_local_server(port=8080)

        # Save token
        with open(token_path, 'w') as f:
            f.write(creds.to_json())

        print("Authentication successful! Token saved.")

        # Clean up temp file
        creds_file.unlink()

        return creds

    except Exception as e:
        print(f"Authentication error: {e}")
        if creds_file.exists():
            creds_file.unlink()
        return None

def send_meeting_reminder():
    """Send meeting reminder email"""

    try:
        # Get Gmail service
        service_module = __import__('googleapiclient.discovery', fromlist=['build'])
        build = service_module.build

        creds = get_gmail_service()
        if not creds:
            print("Failed to authenticate with Gmail")
            return False

        service = build('gmail', 'v1', credentials=creds)

        # Create message
        message_text = """السلام علیکم

یہ آپ کو یاد دلانے کے لیے ہے کہ آپ کے پاس آج رات 11:00 بجے ایک میٹنگ ہے۔

📅 میٹنگ کی تفصیلات:
⏰ وقت: آج رات 11:00 PM
📍 براہ کرم وقت پر موجود رہیں

---

Hello,

This is a reminder that you have a meeting scheduled for today at 11:00 PM.

📅 Meeting Details:
⏰ Time: Today at 11:00 PM
📍 Please be on time

والسلام علیکم"""

        message = MIMEText(message_text, 'plain', 'utf-8')
        message['to'] = 'sm6928234@gmail.com'
        message['subject'] = 'Meeting Reminder - 11:00 PM Today'

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = {'raw': raw_message}

        # Send email
        result = service.users().messages().send(userId='me', body=send_message).execute()

        print("\n" + "="*60)
        print("SUCCESS - Email Sent!")
        print("="*60)
        print(f"To: sm6928234@gmail.com")
        print(f"Subject: Meeting Reminder - 11:00 PM Today")
        print(f"Message ID: {result['id']}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")

        return True

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    send_meeting_reminder()
