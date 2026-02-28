"""
Action Executor for AI Employee Vault
Executes approved actions: sends emails, posts to LinkedIn, replies to WhatsApp
"""

import logging
from pathlib import Path
from datetime import datetime
import json
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from MCP.email_mcp_server import EmailMCPServer
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False
    logger.warning("Email MCP Server not available")

try:
    from Watchers.linkedin_poster import LinkedInPoster
    LINKEDIN_AVAILABLE = True
except ImportError:
    LINKEDIN_AVAILABLE = False
    logger.warning("LinkedIn Poster not available")

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not available")


class ActionExecutor:
    """Execute approved actions from the vault"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.pending_approval / 'Approved'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'

        # Create directories
        self.approved.mkdir(exist_ok=True)
        self.done.mkdir(exist_ok=True)
        self.logs.mkdir(exist_ok=True)

        # Initialize services
        if EMAIL_AVAILABLE:
            self.email_server = EmailMCPServer(vault_path=str(self.vault_path))
        else:
            self.email_server = None

        if LINKEDIN_AVAILABLE:
            self.linkedin_poster = LinkedInPoster(vault_path=str(self.vault_path))
        else:
            self.linkedin_poster = None

        logger.info("Action Executor initialized")

    def execute_approved_actions(self):
        """Execute all approved actions"""
        approved_files = list(self.approved.glob('*.md'))

        if not approved_files:
            logger.info("No approved actions to execute")
            return

        logger.info(f"Found {len(approved_files)} approved actions to execute")

        for file_path in approved_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                action_type = self._extract_action_type(content)

                logger.info(f"Executing {action_type}: {file_path.name}")

                if action_type == 'email_send':
                    self._execute_email(file_path, content)
                elif action_type == 'linkedin_post':
                    self._execute_linkedin_post(file_path, content)
                elif action_type == 'whatsapp_reply':
                    self._execute_whatsapp_reply(file_path, content)
                else:
                    logger.warning(f"Unknown action type: {action_type}")
                    self._move_to_done(file_path, 'UNKNOWN_')

            except Exception as e:
                logger.error(f"Error executing action {file_path.name}: {e}")
                self._move_to_done(file_path, 'ERROR_')

    def _execute_email(self, file_path: Path, content: str):
        """Execute email send action"""
        if not self.email_server or not self.email_server.service:
            logger.warning("Email service not available - moving to done without sending")
            self._move_to_done(file_path, 'DEMO_')
            return

        try:
            # Extract email details
            to = self._extract_field(content, 'to:')
            subject = self._extract_field(content, 'subject:')
            body = self._extract_body(content)

            if not to or not subject:
                logger.error("Missing email details (to/subject)")
                self._move_to_done(file_path, 'FAILED_')
                return

            # Send email
            result = self.email_server.send_email(to, subject, body)

            if result.get('success'):
                logger.info(f"Email sent successfully to {to}")
                self._move_to_done(file_path, 'EXECUTED_')
            else:
                logger.error(f"Failed to send email: {result.get('message')}")
                self._move_to_done(file_path, 'FAILED_')

        except Exception as e:
            logger.error(f"Error executing email: {e}")
            self._move_to_done(file_path, 'ERROR_')

    def _execute_linkedin_post(self, file_path: Path, content: str):
        """Execute LinkedIn post action"""
        if not self.linkedin_poster:
            logger.warning("LinkedIn poster not available - moving to done without posting")
            self._move_to_done(file_path, 'DEMO_')
            return

        try:
            # Extract post details
            title = self._extract_field(content, 'title:')
            post_content = self._extract_body(content)

            if not title and not post_content:
                logger.error("Missing post content")
                self._move_to_done(file_path, 'FAILED_')
                return

            # Post to LinkedIn
            full_content = f"{title}\n\n{post_content}" if title else post_content
            success = self.linkedin_poster.post_to_linkedin(full_content)

            if success:
                logger.info("LinkedIn post published successfully")
                self._move_to_done(file_path, 'EXECUTED_')
            else:
                logger.warning("LinkedIn post failed - moving to done")
                self._move_to_done(file_path, 'DEMO_')

        except Exception as e:
            logger.error(f"Error executing LinkedIn post: {e}")
            self._move_to_done(file_path, 'ERROR_')

    def _execute_whatsapp_reply(self, file_path: Path, content: str):
        """Execute WhatsApp reply action"""
        if not PLAYWRIGHT_AVAILABLE:
            logger.warning("Playwright not available - moving to done without replying")
            self._move_to_done(file_path, 'DEMO_')
            return

        try:
            # Extract WhatsApp details
            chat_name = self._extract_field(content, 'chat:')
            message = self._extract_body(content)

            if not chat_name or not message:
                logger.error("Missing WhatsApp details (chat/message)")
                self._move_to_done(file_path, 'FAILED_')
                return

            # Send WhatsApp message
            session_path = self.vault_path / '.whatsapp_session'
            success = self._send_whatsapp_message(chat_name, message, str(session_path))

            if success:
                logger.info(f"WhatsApp message sent to {chat_name}")
                self._move_to_done(file_path, 'EXECUTED_')
            else:
                logger.warning("WhatsApp message failed - moving to done")
                self._move_to_done(file_path, 'DEMO_')

        except Exception as e:
            logger.error(f"Error executing WhatsApp reply: {e}")
            self._move_to_done(file_path, 'ERROR_')

    def _send_whatsapp_message(self, chat_name: str, message: str, session_path: str) -> bool:
        """Send message via WhatsApp Web"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    session_path,
                    headless=True,
                    viewport={'width': 1280, 'height': 720}
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                try:
                    page.goto('https://web.whatsapp.com', timeout=10000)
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=5000)

                    # Search for chat
                    search_box = page.query_selector('[data-testid="search-input"]')
                    if search_box:
                        search_box.fill(chat_name)
                        page.wait_for_timeout(1000)

                        # Click on first result
                        chat_item = page.query_selector('[data-testid="chat-list-item"]')
                        if chat_item:
                            chat_item.click()
                            page.wait_for_timeout(1000)

                            # Type message
                            message_input = page.query_selector('[data-testid="message-input"]')
                            if message_input:
                                message_input.fill(message)

                                # Send message
                                send_button = page.query_selector('[data-testid="send-button"]')
                                if send_button:
                                    send_button.click()
                                    page.wait_for_timeout(1000)
                                    logger.info(f"WhatsApp message sent to {chat_name}")
                                    return True

                except Exception as e:
                    logger.error(f"Error sending WhatsApp message: {e}")
                    return False
                finally:
                    browser.close()

        except Exception as e:
            logger.error(f"Error in WhatsApp send: {e}")
            return False

    def _extract_action_type(self, content: str) -> str:
        """Extract action type from file content"""
        for line in content.split('\n'):
            if 'action_type:' in line.lower():
                value = line.split(':', 1)[1].strip().lower()
                # Handle different action type formats
                if 'email' in value:
                    return 'email_send'
                elif 'linkedin' in value:
                    return 'linkedin_post'
                elif 'whatsapp' in value:
                    return 'whatsapp_reply'
                return value
        return 'unknown'

    def _extract_field(self, content: str, field_name: str) -> str:
        """Extract field value from markdown content"""
        for line in content.split('\n'):
            if field_name in line.lower():
                value = line.split(':', 1)[1].strip()
                # Remove quotes if present
                value = value.strip('"\'')
                return value

        # Fallback: search for field in different formats
        if 'chat' in field_name.lower():
            # Look for chat name in content
            for line in content.split('\n'):
                if '**chat**' in line.lower() or 'chat:' in line.lower():
                    return line.split(':', 1)[1].strip().strip('*').strip('"\'')

        return ''

    def _extract_body(self, content: str) -> str:
        """Extract body/message content from markdown"""
        lines = content.split('\n')
        in_body = False
        body_lines = []

        for line in lines:
            if line.startswith('## ') and ('body' in line.lower() or 'content' in line.lower() or 'message' in line.lower()):
                in_body = True
                continue
            elif line.startswith('## '):
                in_body = False
            elif in_body and line.strip():
                body_lines.append(line)

        return '\n'.join(body_lines).strip()

    def _move_to_done(self, file_path: Path, prefix: str = ''):
        """Move executed file to Done folder"""
        try:
            done_file = self.done / f"{prefix}{file_path.name}"
            file_path.rename(done_file)
            logger.info(f"Moved to Done: {done_file.name}")
            self._log_execution(file_path.name, prefix.rstrip('_'), 'success')
        except Exception as e:
            logger.error(f"Error moving file to Done: {e}")

    def _log_execution(self, filename: str, status: str, result: str):
        """Log action execution"""
        log_file = self.logs / f"{datetime.now().strftime('%Y-%m-%d')}.json"

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': 'action_executed',
            'item': filename,
            'status': status,
            'result': result,
            'component': 'action_executor'
        }

        try:
            if log_file.exists():
                logs = json.loads(log_file.read_text())
            else:
                logs = []

            logs.append(log_entry)
            log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')
        except Exception as e:
            logger.error(f"Error logging execution: {e}")


if __name__ == "__main__":
    VAULT_PATH = Path(".")
    executor = ActionExecutor(vault_path=str(VAULT_PATH))
    executor.execute_approved_actions()
    logger.info("Action Executor completed")
