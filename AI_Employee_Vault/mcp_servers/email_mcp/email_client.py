"""Email Client - Gmail API wrapper for Email MCP Server"""

import os
import logging
from typing import Dict, List, Any, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.api_python_client import discovery
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


class EmailClient:
    """Gmail API client for email operations"""

    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json'):
        """Initialize Gmail client"""
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None

        # Load existing token
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)

        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    logger.warning(f"Credentials file not found: {self.credentials_file}")
                    return False

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())

        self.service = discovery.build('gmail', 'v1', credentials=creds)
        logger.info("Gmail authentication successful")
        return True

    def send_email(self, to: str, subject: str, body: str, attachments: Optional[List[str]] = None) -> Dict[str, Any]:
        """Send email via Gmail"""
        try:
            message = MIMEMultipart()
            message['to'] = to
            message['subject'] = subject
            message.attach(MIMEText(body, 'html'))

            # Add attachments if provided
            if attachments:
                for attachment_path in attachments:
                    if os.path.exists(attachment_path):
                        self._attach_file(message, attachment_path)

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_message = {'raw': raw_message}

            result = self.service.users().messages().send(userId='me', body=send_message).execute()
            logger.info(f"Email sent to {to}: {result['id']}")
            return {'success': True, 'message_id': result['id']}

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return {'success': False, 'error': str(e)}

    def get_emails(self, folder: str = 'INBOX', limit: int = 10, query: str = '') -> Dict[str, Any]:
        """Get emails from folder"""
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=limit
            ).execute()

            messages = results.get('messages', [])
            emails = []

            for msg in messages:
                email_data = self.get_email_details(msg['id'])
                emails.append(email_data)

            logger.info(f"Retrieved {len(emails)} emails from {folder}")
            return {'success': True, 'emails': emails, 'count': len(emails)}

        except Exception as e:
            logger.error(f"Failed to get emails: {e}")
            return {'success': False, 'error': str(e)}

    def get_email_details(self, message_id: str) -> Dict[str, Any]:
        """Get details of a specific email"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()

            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')

            body = ''
            if 'parts' in message['payload']:
                for part in message['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data', '')
                        if data:
                            body = base64.urlsafe_b64decode(data).decode('utf-8')
                        break
            else:
                data = message['payload']['body'].get('data', '')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')

            return {
                'id': message_id,
                'subject': subject,
                'from': sender,
                'date': date,
                'body': body[:500],  # First 500 chars
                'snippet': message.get('snippet', '')
            }

        except Exception as e:
            logger.error(f"Failed to get email details: {e}")
            return {'id': message_id, 'error': str(e)}

    def mark_as_read(self, message_id: str) -> Dict[str, Any]:
        """Mark email as read"""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()

            logger.info(f"Marked email {message_id} as read")
            return {'success': True, 'message_id': message_id}

        except Exception as e:
            logger.error(f"Failed to mark email as read: {e}")
            return {'success': False, 'error': str(e)}

    def create_draft(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Create email draft"""
        try:
            message = MIMEText(body, 'html')
            message['to'] = to
            message['subject'] = subject

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            draft_message = {'message': {'raw': raw_message}}

            result = self.service.users().drafts().create(userId='me', body=draft_message).execute()
            logger.info(f"Draft created: {result['id']}")
            return {'success': True, 'draft_id': result['id']}

        except Exception as e:
            logger.error(f"Failed to create draft: {e}")
            return {'success': False, 'error': str(e)}

    def get_email_stats(self) -> Dict[str, Any]:
        """Get email statistics"""
        try:
            unread = self.service.users().messages().list(
                userId='me',
                q='is:unread'
            ).execute()

            total = self.service.users().messages().list(
                userId='me'
            ).execute()

            return {
                'success': True,
                'unread_count': len(unread.get('messages', [])),
                'total_count': total.get('resultSizeEstimate', 0)
            }

        except Exception as e:
            logger.error(f"Failed to get email stats: {e}")
            return {'success': False, 'error': str(e)}

    def _attach_file(self, message: MIMEMultipart, file_path: str):
        """Attach file to email"""
        from email.mime.base import MIMEBase
        from email import encoders

        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(file_path)}')
        message.attach(part)
