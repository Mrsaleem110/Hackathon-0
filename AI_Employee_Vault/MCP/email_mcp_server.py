"""
Email MCP Server for AI Employee Vault
Implements Model Context Protocol for sending emails via Gmail API
Allows Claude Code to send emails through MCP interface
"""

import json
import logging
from pathlib import Path
from datetime import datetime
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False
    logging.warning("Google API client not installed. Install with: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")


class EmailMCPServer:
    """MCP Server for email operations"""

    def __init__(self, vault_path: str, credentials_path: str = None):
        self.vault_path = Path(vault_path)
        self.credentials_path = credentials_path or str(self.vault_path / 'gmail_credentials.json')
        self.logs = self.vault_path / 'Logs'
        self.logs.mkdir(exist_ok=True)

        self.service = None
        self.logger = logging.getLogger(__name__)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        if GMAIL_AVAILABLE:
            self.authenticate_gmail()

    def authenticate_gmail(self):
        """Authenticate with Gmail API"""
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']

        creds = None
        token_path = self.vault_path / 'token.json'

        try:
            if token_path.exists():
                creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    self.logger.warning("Gmail credentials not found. Demo mode only.")
                    return

            if creds:
                self.service = build('gmail', 'v1', credentials=creds)
                self.logger.info("Gmail service authenticated successfully")

        except Exception as e:
            self.logger.error(f"Authentication error: {e}")

    def send_email(self, to: str, subject: str, body: str, cc: str = None, bcc: str = None) -> dict:
        """Send email via Gmail API"""
        if not self.service:
            self.logger.warning("Gmail service not available - demo mode")
            return {
                'success': False,
                'message': 'Gmail service not available',
                'mode': 'demo'
            }

        try:
            message = MIMEMultipart()
            message['to'] = to
            message['subject'] = subject

            if cc:
                message['cc'] = cc
            if bcc:
                message['bcc'] = bcc

            message.attach(MIMEText(body, 'plain'))

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            send_message = {
                'raw': raw_message
            }

            result = self.service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()

            self.logger.info(f"Email sent successfully to {to}")
            self.log_email_action('send', to, subject, 'success')

            return {
                'success': True,
                'message': f'Email sent to {to}',
                'message_id': result.get('id')
            }

        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            self.log_email_action('send', to, subject, 'failed')

            return {
                'success': False,
                'message': f'Error sending email: {str(e)}'
            }

    def draft_email(self, to: str, subject: str, body: str) -> dict:
        """Create a draft email (doesn't send)"""
        if not self.service:
            self.logger.warning("Gmail service not available - demo mode")
            return {
                'success': False,
                'message': 'Gmail service not available',
                'mode': 'demo'
            }

        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            draft_message = {
                'message': {
                    'raw': raw_message
                }
            }

            result = self.service.users().drafts().create(
                userId='me',
                body=draft_message
            ).execute()

            self.logger.info(f"Draft created for {to}")
            self.log_email_action('draft', to, subject, 'success')

            return {
                'success': True,
                'message': f'Draft created for {to}',
                'draft_id': result.get('id')
            }

        except Exception as e:
            self.logger.error(f"Error creating draft: {e}")
            return {
                'success': False,
                'message': f'Error creating draft: {str(e)}'
            }

    def log_email_action(self, action: str, to: str, subject: str, status: str):
        """Log email action to audit trail"""
        log_file = self.logs / f"{datetime.now().strftime('%Y-%m-%d')}.json"

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'to': to,
            'subject': subject,
            'status': status,
            'component': 'email_mcp'
        }

        try:
            if log_file.exists():
                logs = json.loads(log_file.read_text())
            else:
                logs = []

            logs.append(log_entry)
            log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Error logging action: {e}")

    def handle_mcp_request(self, request: dict) -> dict:
        """Handle MCP protocol requests"""
        method = request.get('method')
        params = request.get('params', {})

        if method == 'send_email':
            return self.send_email(
                to=params.get('to'),
                subject=params.get('subject'),
                body=params.get('body'),
                cc=params.get('cc'),
                bcc=params.get('bcc')
            )

        elif method == 'draft_email':
            return self.draft_email(
                to=params.get('to'),
                subject=params.get('subject'),
                body=params.get('body')
            )

        else:
            return {
                'success': False,
                'message': f'Unknown method: {method}'
            }

    def demo_run(self):
        """Demo run showing email capabilities"""
        self.logger.info("Running Email MCP Server in demo mode")

        demo_requests = [
            {
                'method': 'draft_email',
                'params': {
                    'to': 'client@example.com',
                    'subject': 'Invoice #1234 - Payment Due',
                    'body': 'Dear Client,\n\nPlease find attached your invoice for January 2026.\n\nBest regards,\nAI Employee'
                }
            },
            {
                'method': 'draft_email',
                'params': {
                    'to': 'team@company.com',
                    'subject': 'Weekly Status Update',
                    'body': 'Team,\n\nHere\'s this week\'s progress update...\n\nBest regards,\nAI Employee'
                }
            }
        ]

        for request in demo_requests:
            result = self.handle_mcp_request(request)
            self.logger.info(f"Demo request result: {result}")

        self.logger.info(f"Processed {len(demo_requests)} demo email requests")


# MCP Server Interface
class MCPServer:
    """MCP Server wrapper for Claude Code integration"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.email_server = EmailMCPServer(vault_path)
        self.logger = logging.getLogger(__name__)

    def process_request(self, request: dict) -> dict:
        """Process incoming MCP request"""
        service = request.get('service')

        if service == 'email':
            return self.email_server.handle_mcp_request(request)

        else:
            return {
                'success': False,
                'message': f'Unknown service: {service}'
            }

    def get_capabilities(self) -> dict:
        """Return MCP server capabilities"""
        return {
            'services': {
                'email': {
                    'methods': [
                        'send_email',
                        'draft_email'
                    ],
                    'description': 'Email operations via Gmail API'
                }
            }
        }


if __name__ == "__main__":
    # Initialize the MCP server
    VAULT_PATH = Path(".")

    server = MCPServer(vault_path=VAULT_PATH)

    # Show capabilities
    print("Email MCP Server Capabilities:")
    print(json.dumps(server.get_capabilities(), indent=2))

    # Run demo
    email_server = EmailMCPServer(vault_path=VAULT_PATH)
    email_server.demo_run()

    print(f"\nEmail MCP Server setup complete!")
    print(f"Logs created in: {email_server.logs}")
