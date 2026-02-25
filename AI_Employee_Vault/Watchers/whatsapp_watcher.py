"""
WhatsApp Watcher for AI Employee Vault
Monitors WhatsApp Web for urgent messages and creates action files
Uses Playwright for browser automation
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


class WhatsAppWatcher(BaseWatcher):
    """Monitor WhatsApp Web for urgent messages"""

    def __init__(self, vault_path: str, session_path: str = None):
        super().__init__(vault_path, check_interval=30)
        self.session_path = Path(session_path) if session_path else Path(vault_path) / '.whatsapp_session'
        self.session_path.mkdir(exist_ok=True)

        # Keywords to watch for
        self.keywords = ['urgent', 'asap', 'help', 'invoice', 'payment', 'emergency', 'important']
        self.processed_chats = set()

        if not PLAYWRIGHT_AVAILABLE:
            self.logger.warning("Playwright not available - running in demo mode only")

    def check_for_updates(self) -> list:
        """Check WhatsApp Web for new urgent messages"""
        if not PLAYWRIGHT_AVAILABLE:
            return []

        messages = []
        try:
            with sync_playwright() as p:
                # Launch browser with persistent session
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    viewport={'width': 1280, 'height': 720}
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                try:
                    page.goto('https://web.whatsapp.com', timeout=10000)
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=5000)

                    # Get all chat items
                    chat_items = page.query_selector_all('[data-testid="chat-list-item"]')

                    for chat in chat_items:
                        try:
                            # Extract chat info
                            chat_name = chat.query_selector('[data-testid="chat-list-item-title"]')
                            chat_preview = chat.query_selector('[data-testid="chat-list-item-message"]')

                            if chat_name and chat_preview:
                                name = chat_name.inner_text()
                                preview = chat_preview.inner_text().lower()

                                # Check for keywords
                                if any(kw in preview for kw in self.keywords):
                                    chat_id = f"whatsapp_{name.replace(' ', '_')}"

                                    if chat_id not in self.processed_chats:
                                        messages.append({
                                            'name': name,
                                            'preview': preview,
                                            'chat_id': chat_id,
                                            'timestamp': datetime.now().isoformat()
                                        })
                                        self.processed_chats.add(chat_id)
                        except Exception as e:
                            self.logger.debug(f"Error processing chat item: {e}")
                            continue

                    self.logger.info(f"Found {len(messages)} urgent WhatsApp messages")

                except Exception as e:
                    self.logger.error(f"Error navigating WhatsApp Web: {e}")
                finally:
                    browser.close()

        except Exception as e:
            self.logger.error(f"Error in WhatsApp check: {e}")

        return messages

    def create_action_file(self, message) -> Path:
        """Create markdown file for WhatsApp message"""
        filename = f"WHATSAPP_{message['chat_id']}.md"
        filepath = self.needs_action / filename

        content = f"""---
type: whatsapp
from: "{message['name']}"
received: "{message['timestamp']}"
priority: high
status: pending
source: whatsapp
---

## Message Preview
{message['preview']}

## Sender
{message['name']}

## Suggested Actions
- [ ] Read full message in WhatsApp
- [ ] Determine appropriate response
- [ ] Respond or escalate as needed
- [ ] Update status when completed

## Metadata
- Received: {message['timestamp']}
- Priority: high (contains urgent keyword)
- Source: WhatsApp Web
"""

        try:
            filepath.write_text(content, encoding='utf-8')
            self.logger.info(f"Created action file: {filepath}")
        except Exception as e:
            self.logger.error(f"Error creating action file: {e}")

        return filepath

    def demo_run(self):
        """Demo run that creates sample WhatsApp action files"""
        self.logger.info("Running WhatsApp Watcher in demo mode")

        sample_messages = [
            {
                'name': 'Client A',
                'preview': 'urgent: can you send the invoice asap?',
                'chat_id': 'client_a_urgent',
                'timestamp': datetime.now().isoformat()
            },
            {
                'name': 'Team Lead',
                'preview': 'help needed on project alpha - payment issue',
                'chat_id': 'team_lead_help',
                'timestamp': datetime.now().isoformat()
            },
            {
                'name': 'Finance',
                'preview': 'invoice #1234 payment received - important update',
                'chat_id': 'finance_payment',
                'timestamp': datetime.now().isoformat()
            }
        ]

        for msg in sample_messages:
            self.create_action_file(msg)

        self.logger.info(f"Created {len(sample_messages)} demo WhatsApp action files")


if __name__ == "__main__":
    # Initialize the watcher
    VAULT_PATH = Path(".")

    watcher = WhatsAppWatcher(vault_path=VAULT_PATH)

    # For demo purposes, create sample files
    watcher.demo_run()

    print(f"\nWhatsApp Watcher setup complete!")
    print(f"Action files created in: {watcher.needs_action}")
    print(f"\nTo run in production mode (requires WhatsApp Web login):")
    print(f"  watcher.run()")
