#!/usr/bin/env python3
"""
Send 4pm meeting reminder email
"""

import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from pathlib import Path
from datetime import datetime
import json

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """Get Gmail service using saved token"""

    try:
        token_path = Path('gmail_token_meeting.json')

        if not token_path.exists():
            print("Error: Gmail token not found")
            return None

        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

        # Refresh if expired
        if creds.expired and creds.refresh_token:
            print("Refreshing token...")
            creds.refresh(Request())
            with open(token_path, 'w') as f:
                f.write(creds.to_json())

        from googleapiclient.discovery import build
        service = build('gmail', 'v1', credentials=creds)
        return service

    except Exception as e:
        print(f"Error getting Gmail service: {e}")
        return None

def send_4pm_meeting_reminder():
    """Send 4pm meeting reminder email"""

    try:
        # Get Gmail service
        service = get_gmail_service()
        if not service:
            return False

        to_email = 'sm6928234@gmail.com'
        subject = 'Meeting Reminder - 4:00 PM Today'

        body = """السلام علیکم

یہ آپ کو یاد دلانے کے لیے ہے کہ آپ کے پاس آج 4:00 بجے ایک میٹنگ ہے۔

📅 میٹنگ کی تفصیلات:
⏰ وقت: آج 4:00 PM
📍 براہ کرم وقت پر موجود رہیں

---

Hello,

This is a reminder that you have a meeting scheduled for today at 4:00 PM.

📅 Meeting Details:
⏰ Time: Today at 4:00 PM
📍 Please be on time

والسلام علیکم"""

        # Create message
        message = MIMEText(body, 'plain', 'utf-8')
        message['to'] = to_email
        message['subject'] = subject

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = {'raw': raw_message}

        # Send email
        result = service.users().messages().send(userId='me', body=send_message).execute()

        print("\n" + "="*60)
        print("SUCCESS - 4PM Meeting Reminder Sent!")
        print("="*60)
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Message ID: {result['id']}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")

        # Log the email
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'to': to_email,
            'subject': subject,
            'type': 'meeting_reminder_4pm',
            'status': 'sent',
            'message_id': result['id']
        }

        log_file = Path('Logs/emails_sent_log.json')
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
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    send_4pm_meeting_reminder()
