#!/usr/bin/env python3
"""
Send meeting reminder email with automatic re-authentication if needed
"""

import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
import json
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def refresh_or_reauth():
    """Refresh token or re-authenticate if needed"""

    token_path = Path('token.json')
    credentials_path = Path('gmail_credentials.json')

    creds = None

    # Try to load existing token
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

            # Try to refresh if expired
            if creds.expired and creds.refresh_token:
                print("Token expired, refreshing...")
                creds.refresh(Request())

                # Save refreshed token
                with open(token_path, 'w') as f:
                    f.write(creds.to_json())
                print("Token refreshed successfully!")
                return creds
        except Exception as e:
            print(f"Token refresh failed: {e}")
            creds = None

    # If no valid token, do full re-authentication
    if not creds and credentials_path.exists():
        print("Performing full re-authentication...")
        flow = InstalledAppFlow.from_client_secrets_file(
            str(credentials_path),
            SCOPES
        )
        creds = flow.run_local_server(port=0)

        # Save new token
        with open(token_path, 'w') as f:
            f.write(creds.to_json())
        print("Re-authentication successful!")
        return creds

    return None

def send_meeting_reminder():
    """Send meeting reminder email"""

    try:
        # Get valid credentials
        creds = refresh_or_reauth()
        if not creds:
            print("Error: Could not authenticate with Gmail")
            return False

        from googleapiclient.discovery import build
        service = build('gmail', 'v1', credentials=creds)

        # Create message
        message = MIMEText("""السلام علیکم

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

والسلام علیکم""", 'plain', 'utf-8')

        message['to'] = 'sm6928234@gmail.com'
        message['subject'] = 'Meeting Reminder - 11:00 PM Today'

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = {'raw': raw_message}

        # Send email
        result = service.users().messages().send(userId='me', body=send_message).execute()

        print("\n" + "="*60)
        print("SUCCESS - Meeting Reminder Sent!")
        print("="*60)
        print(f"To: sm6928234@gmail.com")
        print(f"Subject: Meeting Reminder - 11:00 PM Today")
        print(f"Message ID: {result['id']}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")

        # Log the action
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': 'SEND_EMAIL',
            'recipient': 'sm6928234@gmail.com',
            'subject': 'Meeting Reminder - 11:00 PM Today',
            'type': 'meeting_reminder',
            'status': 'sent',
            'message_id': result['id']
        }

        # Append to log
        log_file = Path('Logs/email_sent.json')
        log_file.parent.mkdir(parents=True, exist_ok=True)

        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(log_entry)

        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

        return True

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

if __name__ == "__main__":
    send_meeting_reminder()
