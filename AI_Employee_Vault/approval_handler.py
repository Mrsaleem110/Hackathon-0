"""
Approval Handler for AI Employee Vault
Manages human-in-the-loop approval workflow for sensitive actions
Monitors Pending_Approval folder and executes approved actions
"""

import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
import json
from enum import Enum


class ApprovalStatus(Enum):
    """Approval status enum"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ApprovalHandler:
    """Manages approval workflow for sensitive actions"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.pending_approval / 'Approved'
        self.rejected = self.pending_approval / 'Rejected'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'

        # Create directories
        self.pending_approval.mkdir(exist_ok=True)
        self.approved.mkdir(exist_ok=True)
        self.rejected.mkdir(exist_ok=True)
        self.done.mkdir(exist_ok=True)
        self.logs.mkdir(exist_ok=True)

        # Set up logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def create_approval_request(self, action_type: str, details: dict, expires_in_hours: int = 24) -> Path:
        """Create an approval request file"""
        filename = f"{action_type}_{details.get('id', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = self.pending_approval / filename

        expiry = datetime.now() + timedelta(hours=expires_in_hours)

        content = f"""---
type: approval_request
action_type: {action_type}
created: {datetime.now().isoformat()}
expires: {expiry.isoformat()}
status: pending
---

# Approval Request: {action_type.upper()}

## Action Details
"""

        # Add details based on action type
        if action_type == 'email_send':
            content += f"""
- **To**: {details.get('to', 'Unknown')}
- **Subject**: {details.get('subject', 'No Subject')}
- **Body Preview**: {details.get('body', '')[:200]}...
- **CC**: {details.get('cc', 'None')}
- **BCC**: {details.get('bcc', 'None')}
"""

        elif action_type == 'payment':
            content += f"""
- **Amount**: ${details.get('amount', '0.00')}
- **Recipient**: {details.get('recipient', 'Unknown')}
- **Account**: {details.get('account', 'Unknown')}
- **Reference**: {details.get('reference', 'None')}
- **Reason**: {details.get('reason', 'None')}
"""

        elif action_type == 'linkedin_post':
            content += f"""
- **Title**: {details.get('title', 'No Title')}
- **Content Preview**: {details.get('content', '')[:200]}...
- **Hashtags**: {', '.join(details.get('hashtags', []))}
"""

        elif action_type == 'contact_new':
            content += f"""
- **Contact Name**: {details.get('name', 'Unknown')}
- **Email**: {details.get('email', 'Unknown')}
- **Message**: {details.get('message', '')[:200]}...
"""

        content += f"""

## To Approve
1. Review the details above
2. Move this file to `/Pending_Approval/Approved/` folder
3. AI Employee will execute the action

## To Reject
1. Move this file to `/Pending_Approval/Rejected/` folder
2. Add rejection reason in comments below

## Rejection Reason (if applicable)
[Add reason here if rejecting]

---
**Expires**: {expiry.isoformat()}
**Created**: {datetime.now().isoformat()}
"""

        try:
            filepath.write_text(content, encoding='utf-8')
            self.logger.info(f"Created approval request: {filepath}")
            self.log_approval_action('request_created', action_type, details.get('id', 'unknown'), 'pending')
        except Exception as e:
            self.logger.error(f"Error creating approval request: {e}")

        return filepath

    def check_approved_actions(self) -> list:
        """Check Approved folder for approved actions"""
        approved_actions = []

        for file in self.approved.glob('*.md'):
            try:
                content = file.read_text(encoding='utf-8')
                action_type = self._extract_action_type(content)

                approved_actions.append({
                    'file': file,
                    'filename': file.name,
                    'action_type': action_type,
                    'content': content
                })
            except Exception as e:
                self.logger.error(f"Error reading approved action: {e}")

        return approved_actions

    def check_rejected_actions(self) -> list:
        """Check Rejected folder for rejected actions"""
        rejected_actions = []

        for file in self.rejected.glob('*.md'):
            try:
                content = file.read_text(encoding='utf-8')
                action_type = self._extract_action_type(content)

                rejected_actions.append({
                    'file': file,
                    'filename': file.name,
                    'action_type': action_type,
                    'content': content
                })
            except Exception as e:
                self.logger.error(f"Error reading rejected action: {e}")

        return rejected_actions

    def check_expired_approvals(self) -> list:
        """Check for expired approval requests"""
        expired_actions = []

        for file in self.pending_approval.glob('*.md'):
            try:
                content = file.read_text(encoding='utf-8')
                expires_line = [line for line in content.split('\n') if 'expires:' in line.lower()]

                if expires_line:
                    expires_str = expires_line[0].split(':', 1)[1].strip()
                    expires = datetime.fromisoformat(expires_str)

                    if datetime.now() > expires:
                        expired_actions.append({
                            'file': file,
                            'filename': file.name,
                            'expires': expires
                        })
            except Exception as e:
                self.logger.debug(f"Error checking expiry: {e}")

        return expired_actions

    def _extract_action_type(self, content: str) -> str:
        """Extract action type from approval request content"""
        for line in content.split('\n'):
            if 'action_type:' in line.lower():
                return line.split(':', 1)[1].strip()
        return 'unknown'

    def process_approved_actions(self):
        """Process all approved actions"""
        approved_actions = self.check_approved_actions()

        if not approved_actions:
            self.logger.info("No approved actions to process")
            return

        self.logger.info(f"Found {len(approved_actions)} approved actions")

        for action in approved_actions:
            try:
                self.logger.info(f"Processing approved action: {action['filename']}")

                # Log approval
                self.log_approval_action(
                    'action_approved',
                    action['action_type'],
                    action['filename'],
                    'approved'
                )

                # Move to Done
                done_file = self.done / action['filename']
                action['file'].rename(done_file)

                self.logger.info(f"Moved to Done: {done_file}")

            except Exception as e:
                self.logger.error(f"Error processing approved action: {e}")

    def process_rejected_actions(self):
        """Process all rejected actions"""
        rejected_actions = self.check_rejected_actions()

        if not rejected_actions:
            self.logger.info("No rejected actions to process")
            return

        self.logger.info(f"Found {len(rejected_actions)} rejected actions")

        for action in rejected_actions:
            try:
                self.logger.info(f"Processing rejected action: {action['filename']}")

                # Log rejection
                self.log_approval_action(
                    'action_rejected',
                    action['action_type'],
                    action['filename'],
                    'rejected'
                )

                # Move to Done (with rejection marker)
                done_file = self.done / f"REJECTED_{action['filename']}"
                action['file'].rename(done_file)

                self.logger.info(f"Moved to Done (rejected): {done_file}")

            except Exception as e:
                self.logger.error(f"Error processing rejected action: {e}")

    def handle_expired_approvals(self):
        """Handle expired approval requests"""
        expired_actions = self.check_expired_approvals()

        if not expired_actions:
            self.logger.info("No expired approvals")
            return

        self.logger.info(f"Found {len(expired_actions)} expired approvals")

        for action in expired_actions:
            try:
                self.logger.warning(f"Approval expired: {action['filename']}")

                # Move to Done with expiry marker
                done_file = self.done / f"EXPIRED_{action['filename']}"
                action['file'].rename(done_file)

                # Log expiry
                self.log_approval_action(
                    'approval_expired',
                    'unknown',
                    action['filename'],
                    'expired'
                )

            except Exception as e:
                self.logger.error(f"Error handling expired approval: {e}")

    def log_approval_action(self, action: str, action_type: str, action_id: str, status: str):
        """Log approval action to audit trail"""
        log_file = self.logs / f"{datetime.now().strftime('%Y-%m-%d')}.json"

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'action_type': action_type,
            'action_id': action_id,
            'status': status,
            'component': 'approval_handler'
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

    def demo_run(self):
        """Demo run that creates sample approval requests"""
        self.logger.info("Running Approval Handler in demo mode")

        sample_approvals = [
            {
                'action_type': 'email_send',
                'details': {
                    'id': 'client_a_invoice',
                    'to': 'client@example.com',
                    'subject': 'Invoice #1234 - Payment Due',
                    'body': 'Dear Client,\n\nPlease find attached your invoice for January 2026.',
                    'cc': None,
                    'bcc': None
                }
            },
            {
                'action_type': 'payment',
                'details': {
                    'id': 'payment_vendor_001',
                    'amount': '500.00',
                    'recipient': 'Vendor A',
                    'account': 'XXXX1234',
                    'reference': 'Invoice #5678',
                    'reason': 'Monthly software subscription'
                }
            },
            {
                'action_type': 'linkedin_post',
                'details': {
                    'id': 'linkedin_post_001',
                    'title': 'Q1 2026 Business Update',
                    'content': 'Excited to share our progress this quarter. We\'ve achieved 45% growth.',
                    'hashtags': ['#business', '#growth', '#2026']
                }
            }
        ]

        for approval in sample_approvals:
            self.create_approval_request(
                approval['action_type'],
                approval['details']
            )

        self.logger.info(f"Created {len(sample_approvals)} demo approval requests")


if __name__ == "__main__":
    # Initialize the approval handler
    VAULT_PATH = Path(".")

    handler = ApprovalHandler(vault_path=VAULT_PATH)

    # For demo purposes, create sample approval requests
    handler.demo_run()

    print(f"\nApproval Handler setup complete!")
    print(f"Approval requests created in: {handler.pending_approval}")
    print(f"\nTo process approvals:")
    print(f"  handler.process_approved_actions()")
    print(f"  handler.process_rejected_actions()")
    print(f"  handler.handle_expired_approvals()")
