#!/usr/bin/env python3
"""
Send email from .md template file
Reads email configuration from .md file and sends it directly
"""

import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from pathlib import Path
import re
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def parse_email_template(template_path):
    """Parse .md template file to extract email configuration"""

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract To email
        to_match = re.search(r'\*\*To:\*\*\s*(.+?)(?:\n|$)', content)
        to_email = to_match.group(1).strip() if to_match else None

        # Extract Subject
        subject_match = re.search(r'\*\*Subject:\*\*\s*(.+?)(?:\n|$)', content)
        subject = subject_match.group(1).strip() if subject_match else None

        # Extract message body (everything after "## Message Body")
        body_match = re.search(r'## Message Body\s*\n(.*?)(?=## Status|$)', content, re.DOTALL)
        body = body_match.group(1).strip() if body_match else None

        if not to_email or not subject or not body:
            print("Error: Missing required fields in template")
            print(f"  To: {to_email}")
            print(f"  Subject: {subject}")
            print(f"  Body: {'Present' if body else 'Missing'}")
            return None

        return {
            'to': to_email,
            'subject': subject,
            'body': body
        }

    except Exception as e:
        print(f"Error parsing template: {e}")
        return None

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

def send_email_from_template(template_path):
    """Send email using .md template file"""

    try:
        # Parse template
        email_config = parse_email_template(template_path)
        if not email_config:
            return False

        print(f"\nParsed email template:")
        print(f"  To: {email_config['to']}")
        print(f"  Subject: {email_config['subject']}")

        # Get Gmail service
        service = get_gmail_service()
        if not service:
            return False

        # Create message
        message = MIMEText(email_config['body'], 'plain', 'utf-8')
        message['to'] = email_config['to']
        message['subject'] = email_config['subject']

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = {'raw': raw_message}

        # Send email
        result = service.users().messages().send(userId='me', body=send_message).execute()

        print("\n" + "="*60)
        print("SUCCESS - Email Sent from Template!")
        print("="*60)
        print(f"To: {email_config['to']}")
        print(f"Subject: {email_config['subject']}")
        print(f"Message ID: {result['id']}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Template: {template_path}")
        print("="*60 + "\n")

        return True

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python send_from_template.py <template_path>")
        print("\nExample:")
        print("  python send_from_template.py email_templates/meeting_reminder_template.md")
        sys.exit(1)

    template_path = sys.argv[1]
    send_email_from_template(template_path)
