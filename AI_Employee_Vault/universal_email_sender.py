#!/usr/bin/env python3
"""
Universal Email Sender - Send email to anyone on any topic
Usage: python universal_email_sender.py
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
            print("Error: Gmail token not found. Run send_email_actual.py first to authenticate.")
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

def send_email(to_email, subject, body):
    """Send email to anyone on any topic"""

    try:
        # Get Gmail service
        service = get_gmail_service()
        if not service:
            return False

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
        print("SUCCESS - Email Sent!")
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

def interactive_email_sender():
    """Interactive mode - ask user for email details"""

    print("\n" + "="*60)
    print("UNIVERSAL EMAIL SENDER")
    print("="*60)

    # Get recipient email
    to_email = input("\nKis ko email send karna hai? (Email address): ").strip()
    if not to_email:
        print("Error: Email address required")
        return False

    # Get subject
    subject = input("Subject kya hona chahiye?: ").strip()
    if not subject:
        print("Error: Subject required")
        return False

    # Get message body
    print("\nMessage likho (Enter ke baad Ctrl+D ya Ctrl+Z dabao jab khatam ho):")
    print("(Ya ek line likho aur Enter dabao):")

    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    body = '\n'.join(lines).strip()
    if not body:
        print("Error: Message body required")
        return False

    # Confirm before sending
    print("\n" + "-"*60)
    print("Email Details:")
    print(f"  To: {to_email}")
    print(f"  Subject: {subject}")
    print(f"  Message:\n{body}")
    print("-"*60)

    confirm = input("\nKya email send karna hai? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y', 'haan', 'ha']:
        print("Email cancelled.")
        return False

    # Send email
    return send_email(to_email, subject, body)

def send_email_direct(to_email, subject, body):
    """Send email directly without interactive mode"""

    return send_email(to_email, subject, body)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == '--help':
            print("Usage:")
            print("  Interactive mode: python universal_email_sender.py")
            print("  Direct mode: python universal_email_sender.py <to_email> <subject> <body>")
            print("\nExample:")
            print("  python universal_email_sender.py ali@example.com 'Meeting' 'Salam Ali, meeting kal 3pm par hai'")
        elif len(sys.argv) >= 4:
            to_email = sys.argv[1]
            subject = sys.argv[2]
            body = ' '.join(sys.argv[3:])
            send_email_direct(to_email, subject, body)
        else:
            print("Error: Invalid arguments")
            print("Run with --help for usage information")
    else:
        # Interactive mode
        interactive_email_sender()
