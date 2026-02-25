"""
LinkedIn Watcher for AI Employee Vault
Monitors LinkedIn for business opportunities and engagement
Creates action files for sales leads and important interactions
"""

import time
import logging
from pathlib import Path
from datetime import datetime
from base_watcher import BaseWatcher

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logging.warning("Playwright not installed. Install with: pip install playwright")


class LinkedInWatcher(BaseWatcher):
    """Monitor LinkedIn for business opportunities"""

    def __init__(self, vault_path: str, session_path: str = None):
        super().__init__(vault_path, check_interval=300)  # Check every 5 minutes
        self.session_path = Path(session_path) if session_path else Path(vault_path) / '.linkedin_session'
        self.session_path.mkdir(exist_ok=True)

        # Keywords to watch for
        self.keywords = ['opportunity', 'partnership', 'collaboration', 'project', 'interested', 'proposal']
        self.processed_messages = set()

        if not PLAYWRIGHT_AVAILABLE:
            self.logger.warning("Playwright not available - running in demo mode only")

    def check_for_updates(self) -> list:
        """Check LinkedIn for new messages and opportunities"""
        if not PLAYWRIGHT_AVAILABLE:
            return []

        messages = []
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    viewport={'width': 1280, 'height': 720}
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                try:
                    page.goto('https://www.linkedin.com/messaging/', timeout=10000)
                    page.wait_for_selector('[data-testid="message-list"]', timeout=5000)

                    # Get all message threads
                    message_threads = page.query_selector_all('[data-testid="message-thread-item"]')

                    for thread in message_threads:
                        try:
                            sender = thread.query_selector('[data-testid="message-sender-name"]')
                            preview = thread.query_selector('[data-testid="message-preview"]')

                            if sender and preview:
                                sender_name = sender.inner_text()
                                preview_text = preview.inner_text().lower()

                                # Check for keywords
                                if any(kw in preview_text for kw in self.keywords):
                                    msg_id = f"linkedin_{sender_name.replace(' ', '_')}"

                                    if msg_id not in self.processed_messages:
                                        messages.append({
                                            'sender': sender_name,
                                            'preview': preview_text,
                                            'msg_id': msg_id,
                                            'timestamp': datetime.now().isoformat()
                                        })
                                        self.processed_messages.add(msg_id)
                        except Exception as e:
                            self.logger.debug(f"Error processing message thread: {e}")
                            continue

                    self.logger.info(f"Found {len(messages)} LinkedIn opportunities")

                except Exception as e:
                    self.logger.error(f"Error navigating LinkedIn: {e}")
                finally:
                    browser.close()

        except Exception as e:
            self.logger.error(f"Error in LinkedIn check: {e}")

        return messages

    def create_action_file(self, message) -> Path:
        """Create markdown file for LinkedIn opportunity"""
        filename = f"LINKEDIN_{message['msg_id']}.md"
        filepath = self.needs_action / filename

        content = f"""---
type: linkedin_opportunity
from: "{message['sender']}"
received: "{message['timestamp']}"
priority: high
status: pending
source: linkedin
---

## Message Preview
{message['preview']}

## Sender
{message['sender']}

## Suggested Actions
- [ ] Read full message on LinkedIn
- [ ] Evaluate opportunity fit
- [ ] Draft response or proposal
- [ ] Schedule follow-up meeting if interested
- [ ] Update status when completed

## Metadata
- Received: {message['timestamp']}
- Priority: high (business opportunity)
- Source: LinkedIn Messaging
"""

        try:
            filepath.write_text(content, encoding='utf-8')
            self.logger.info(f"Created action file: {filepath}")
        except Exception as e:
            self.logger.error(f"Error creating action file: {e}")

        return filepath

    def demo_run(self):
        """Demo run that creates sample LinkedIn action files"""
        self.logger.info("Running LinkedIn Watcher in demo mode")

        sample_messages = [
            {
                'sender': 'John Smith',
                'preview': 'interested in partnership opportunity for your services',
                'msg_id': 'john_smith_partnership',
                'timestamp': datetime.now().isoformat()
            },
            {
                'sender': 'Sarah Johnson',
                'preview': 'collaboration proposal - would love to discuss project',
                'msg_id': 'sarah_johnson_collab',
                'timestamp': datetime.now().isoformat()
            },
            {
                'sender': 'Tech Startup Inc',
                'preview': 'opportunity to work on exciting new project',
                'msg_id': 'tech_startup_project',
                'timestamp': datetime.now().isoformat()
            }
        ]

        for msg in sample_messages:
            self.create_action_file(msg)

        self.logger.info(f"Created {len(sample_messages)} demo LinkedIn action files")


if __name__ == "__main__":
    # Initialize the watcher
    VAULT_PATH = Path(".")

    watcher = LinkedInWatcher(vault_path=VAULT_PATH)

    # For demo purposes, create sample files
    watcher.demo_run()

    print(f"\nLinkedIn Watcher setup complete!")
    print(f"Action files created in: {watcher.needs_action}")
    print(f"\nTo run in production mode (requires LinkedIn login):")
    print(f"  watcher.run()")
