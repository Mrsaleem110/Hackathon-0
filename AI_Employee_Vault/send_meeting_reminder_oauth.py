#!/usr/bin/env python3
"""
Send meeting reminder email using Gmail API with existing credentials
"""

import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from pathlib import Path
import json

def send_meeting_reminder():
    """Send meeting reminder email"""

    try:
        # Load existing Gmail token
        token_path = Path('gmail_token.json')
        if not token_path.exists():
            print("Error: gmail_token.json not found")
            return False

        creds = Credentials.from_authorized_user_file(str(token_path))

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

        print("✓ Meeting reminder sent successfully!")
        print(f"  To: sm6928234@gmail.com")
        print(f"  Subject: Meeting Reminder - 11:00 PM Today")
        print(f"  Message ID: {result['id']}")

        # Log the action
        log_entry = {
            'action': 'SEND_EMAIL',
            'recipient': 'sm6928234@gmail.com',
            'subject': 'Meeting Reminder - 11:00 PM Today',
            'type': 'meeting_reminder',
            'status': 'sent',
            'message_id': result['id']
        }

        # Append to log
        log_file = Path('Logs/email_sent.json')
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
