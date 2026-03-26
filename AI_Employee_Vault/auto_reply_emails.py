"""
Auto Reply to Unread Emails
Fetches unread emails and generates appropriate replies
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from pathlib import Path
import base64
from email.mime.text import MIMEText

def get_email_body(message):
    """Extract email body from message"""
    try:
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            data = message['payload']['body'].get('data', '')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8')
    except:
        pass
    return message.get('snippet', '')

def generate_reply(from_email, subject, body_snippet):
    """Generate appropriate reply based on email type"""

    # Skip promotional/newsletter emails
    skip_domains = ['neon.tech', 'fiverr.com', 'pinterest.com', 'canva.com', 'no-reply', 'noreply']
    if any(domain in from_email.lower() for domain in skip_domains):
        return None

    # Google security alert - acknowledge
    if 'google' in from_email.lower() and 'security' in subject.lower():
        return {
            'subject': f'Re: {subject}',
            'body': '''Thank you for the security alert.

I have reviewed the notification and confirmed the activity. My account security is important to me, and I appreciate Google's proactive monitoring.

Best regards'''
        }

    # Default professional reply
    return {
        'subject': f'Re: {subject}',
        'body': f'''Thank you for your email.

I have received your message and will review it carefully. I will get back to you with a detailed response shortly.

If this matter is urgent, please feel free to reach out directly.

Best regards,
Agentic Sphere Team

---
This is an automated acknowledgment sent by Agentic Sphere - Your Personal AI Employee'''
    }

def main():
    # Authenticate
    token_path = Path('token.json')
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

    if not token_path.exists():
        print('Token not found. Need to authenticate first.')
        return

    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    # Fetch unread emails
    results = service.users().messages().list(userId='me', q='is:unread', maxResults=10).execute()
    messages = results.get('messages', [])

    print(f'Found {len(messages)} unread emails')
    print('='*60)

    replied_count = 0
    skipped_count = 0

    for msg in messages:
        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = message['payload']['headers']

        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        message_id = next((h['value'] for h in headers if h['name'] == 'Message-ID'), None)

        print(f'\nProcessing: {subject[:50]}...')
        print(f'From: {from_email}')

        # Generate reply
        reply_data = generate_reply(from_email, subject, message.get('snippet', ''))

        if reply_data:
            try:
                # Create reply message
                reply_message = MIMEText(reply_data['body'])
                reply_message['to'] = from_email
                reply_message['subject'] = reply_data['subject']
                if message_id:
                    reply_message['In-Reply-To'] = message_id
                    reply_message['References'] = message_id

                raw_message = base64.urlsafe_b64encode(reply_message.as_bytes()).decode()

                # Send reply
                service.users().messages().send(
                    userId='me',
                    body={'raw': raw_message, 'threadId': message['threadId']}
                ).execute()

                # Mark as read
                service.users().messages().modify(
                    userId='me',
                    id=msg['id'],
                    body={'removeLabelIds': ['UNREAD']}
                ).execute()

                print(f'  -> Replied and marked as read')
                replied_count += 1

            except Exception as e:
                print(f'  -> Error: {e}')
        else:
            # Just mark as read (promotional emails)
            try:
                service.users().messages().modify(
                    userId='me',
                    id=msg['id'],
                    body={'removeLabelIds': ['UNREAD']}
                ).execute()
                print(f'  -> Skipped (promotional) and marked as read')
                skipped_count += 1
            except Exception as e:
                print(f'  -> Error marking as read: {e}')

    print('\n' + '='*60)
    print(f'Summary:')
    print(f'  Replied: {replied_count}')
    print(f'  Skipped: {skipped_count}')
    print(f'  Total processed: {replied_count + skipped_count}')
    print('='*60)

if __name__ == "__main__":
    main()
