"""
Gmail Watcher for AI Employee Vault
This script monitors Gmail for new messages and creates action files in the Needs_Action folder.
"""

import time
import logging
import os
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GmailWatcher:
    def __init__(self, vault_path: str, credentials_path: str = None):
        self.vault_path = Path(vault_path)
        self.needs_action_path = self.vault_path / 'Needs_Action'
        self.credentials_path = credentials_path or str(self.vault_path / 'gmail_credentials.json')
        self.processed_ids = set()
        self.service = None
        self.check_interval = 120  # Check every 2 minutes

        # Create Needs_Action directory if it doesn't exist
        self.needs_action_path.mkdir(exist_ok=True)

        # Initialize Gmail service
        self.authenticate_gmail()

    def authenticate_gmail(self):
        """Authenticate with Gmail API"""
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

        creds = None
        # Token file stores the user's access and refresh tokens
        token_path = self.vault_path / 'token.json'

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Failed to refresh credentials: {e}")
                    if os.path.exists(token_path):
                        os.remove(token_path)  # Remove invalid token file
                    creds = None

            if not creds:
                # For this example, we'll skip actual authentication for now
                # In a real implementation, you'd need to set up OAuth credentials
                logger.warning("Gmail credentials not found. This is a demo implementation.")
                return

        if creds:
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail service authenticated successfully")

    def check_for_updates(self):
        """Check for new Gmail messages"""
        if not self.service:
            logger.warning("Gmail service not available, skipping check")
            return []

        try:
            # Query for unread important messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread is:important',
                maxResults=10  # Limit to 10 newest messages
            ).execute()

            messages = results.get('messages', [])
            new_messages = []

            for message in messages:
                msg_id = message['id']
                if msg_id not in self.processed_ids:
                    # Get full message details
                    full_message = self.service.users().messages().get(
                        userId='me',
                        id=msg_id
                    ).execute()

                    new_messages.append({
                        'id': msg_id,
                        'message': full_message
                    })
                    self.processed_ids.add(msg_id)

            logger.info(f"Found {len(new_messages)} new important messages")
            return new_messages

        except Exception as e:
            logger.error(f"Error checking Gmail: {e}")
            return []

    def extract_message_details(self, message):
        """Extract headers and content from Gmail message"""
        headers = {h['name']: h['value'] for h in message['payload']['headers']}

        # Extract snippet (preview text)
        snippet = message.get('snippet', '')

        # Extract subject, sender, etc.
        subject = headers.get('Subject', 'No Subject')
        sender = headers.get('From', 'Unknown Sender')

        return {
            'subject': subject,
            'from': sender,
            'date': headers.get('Date', ''),
            'snippet': snippet,
            'priority': 'high' if any(word in snippet.lower() for word in ['urgent', 'asap', 'help', 'payment', 'invoice']) else 'normal'
        }

    def create_action_file(self, msg_data):
        """Create a markdown file in Needs_Action folder"""
        message_details = self.extract_message_details(msg_data['message'])

        # Create filename based on message ID
        filename = f"GMAIL_{msg_data['id']}.md"
        filepath = self.needs_action_path / filename

        # Create content for the action file
        content = f"""---
type: email
from: "{message_details['from']}"
subject: "{message_details['subject']}"
received: "{datetime.now().isoformat()}"
priority: {message_details['priority']}
status: pending
source: gmail
---

## Email Content
{message_details['snippet']}

## Sender
{message_details['from']}

## Suggested Actions
- [ ] Review full email content
- [ ] Determine appropriate response
- [ ] Respond or escalate as needed
- [ ] Update status when completed

## Metadata
- Date received: {message_details['date']}
- Priority: {message_details['priority']}
"""

        # Write the content to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Created action file: {filepath}")
        return filepath

    def run(self):
        """Main run loop - continuously monitors for new messages"""
        logger.info("Starting Gmail Watcher...")
        logger.info(f"Monitoring vault: {self.vault_path}")

        while True:
            try:
                # Check for new messages
                new_messages = self.check_for_updates()

                # Create action files for new messages
                for msg_data in new_messages:
                    self.create_action_file(msg_data)

                # Wait before next check
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                logger.info("Gmail Watcher stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

    def demo_run(self):
        """Demo run that creates sample action files without actual Gmail access"""
        logger.info("Running in demo mode - creating sample action files")

        # Sample messages to demonstrate functionality
        sample_messages = [
            {
                'id': 'demo_1',
                'subject': 'Urgent: Invoice Payment Required',
                'from': 'accounts@client1.com',
                'snippet': 'Hi, your invoice #1234 is overdue. Please process payment asap.',
                'priority': 'high'
            },
            {
                'id': 'demo_2',
                'subject': 'Meeting Tomorrow',
                'from': 'colleague@company.com',
                'snippet': 'Just confirming our meeting tomorrow at 10am. Looking forward to it.',
                'priority': 'normal'
            }
        ]

        for msg in sample_messages:
            filename = f"GMAIL_{msg['id']}_demo.md"
            filepath = self.needs_action_path / filename

            content = f"""---
type: email
from: "{msg['from']}"
subject: "{msg['subject']}"
received: "{datetime.now().isoformat()}"
priority: {msg['priority']}
status: pending
source: gmail_demo
---

## Email Content
{msg['snippet']}

## Sender
{msg['from']}

## Suggested Actions
- [ ] Review full email content
- [ ] Determine appropriate response
- [ ] Respond or escalate as needed
- [ ] Update status when completed

## Metadata
- Priority: {msg['priority']}
- This is a demo file showing the structure
"""

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Created demo action file: {filepath}")

if __name__ == "__main__":
    # Initialize the watcher with the current directory as vault path
    VAULT_PATH = Path(".")

    watcher = GmailWatcher(vault_path=VAULT_PATH)

    # For demo purposes, create sample files
    watcher.demo_run()

    logger.info("Gmail Watcher setup complete!")
    logger.info(f"Action files created in: {watcher.needs_action_path}")