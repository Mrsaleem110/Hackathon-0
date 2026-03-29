#!/usr/bin/env python3
"""
Cloud Agent - Runs 24/7 on cloud VM
Monitors email and social media, creates drafts, writes to Pending_Approval
Does NOT access: WhatsApp sessions, banking credentials, payment tokens
Syncs vault via git, writes signals to Updates/
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from vault_coordinator import VaultCoordinator
from dashboard_manager import DashboardManager
from git_sync_manager import GitSyncManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CloudAgent:
    """Cloud agent for 24/7 monitoring and drafting"""

    def __init__(self, vault_path: str = ".", check_interval: int = 60):
        """
        Initialize cloud agent

        Args:
            vault_path: Path to vault directory
            check_interval: Seconds between checks
        """
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        self.agent_name = "cloud"

        # Initialize components
        self.coordinator = VaultCoordinator(vault_path)
        self.dashboard = DashboardManager(vault_path)
        self.git_sync = GitSyncManager(vault_path)

        # Directories
        self.needs_action_email = self.vault_path / "Needs_Action" / "email"
        self.needs_action_social = self.vault_path / "Needs_Action" / "social"
        self.in_progress = self.vault_path / "In_Progress" / self.agent_name
        self.pending_approval_email = self.vault_path / "Pending_Approval" / "email"
        self.pending_approval_social = self.vault_path / "Pending_Approval" / "social"
        self.updates = self.vault_path / "Updates"

        # Create directories
        for directory in [
            self.needs_action_email,
            self.needs_action_social,
            self.in_progress,
            self.pending_approval_email,
            self.pending_approval_social,
            self.updates,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

        logger.info("Cloud Agent initialized")

    def run_continuous(self, duration: Optional[int] = None):
        """
        Run cloud agent continuously

        Args:
            duration: Optional duration in seconds (None = infinite)
        """
        start_time = time.time()
        iteration = 0

        try:
            logger.info(f"Cloud Agent starting (check interval: {self.check_interval}s)")
            self.dashboard.update_status("Cloud Agent", "OPERATIONAL")

            while True:
                iteration += 1
                logger.info(f"--- Cloud Agent Iteration {iteration} ---")

                try:
                    # 1. Sync vault (pull latest changes)
                    logger.info("Syncing vault...")
                    success, msg = self.git_sync.pull_vault(self.agent_name)
                    if success:
                        logger.info(f"Vault synced: {msg}")
                    else:
                        logger.warning(f"Vault sync failed: {msg}")

                    # 2. Process email tasks
                    logger.info("Processing email tasks...")
                    self._process_email_tasks()

                    # 3. Process social media tasks
                    logger.info("Processing social media tasks...")
                    self._process_social_tasks()

                    # 4. Write health signal
                    self._write_health_signal()

                    # 5. Push vault changes
                    logger.info("Pushing vault changes...")
                    success, msg = self.git_sync.push_vault(
                        self.agent_name,
                        f"Cloud Agent sync - iteration {iteration}"
                    )
                    if success:
                        logger.info(f"Vault pushed: {msg}")
                    else:
                        logger.warning(f"Vault push failed: {msg}")

                except Exception as e:
                    logger.error(f"Error in iteration {iteration}: {e}")
                    self.dashboard.write_signal(
                        self.agent_name,
                        "alert",
                        {"level": "ERROR", "message": f"Iteration error: {str(e)}"}
                    )

                # Check duration
                if duration and (time.time() - start_time) > duration:
                    logger.info(f"Cloud Agent stopping after {duration}s")
                    break

                # Sleep before next iteration
                logger.info(f"Sleeping for {self.check_interval}s...")
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            logger.info("Cloud Agent stopped by user")
        except Exception as e:
            logger.error(f"Cloud Agent fatal error: {e}")
            self.dashboard.update_status("Cloud Agent", "DOWN")
        finally:
            logger.info("Cloud Agent shutdown")

    def _process_email_tasks(self):
        """Process email tasks from Needs_Action/email/"""
        try:
            # Get all email tasks
            email_tasks = list(self.needs_action_email.glob("*.md"))
            if not email_tasks:
                logger.info("No email tasks to process")
                return

            logger.info(f"Found {len(email_tasks)} email tasks")

            for task_file in email_tasks:
                task_name = task_file.name
                logger.info(f"Processing email task: {task_name}")

                # Claim task
                if not self.coordinator.claim_task("email", task_name, self.agent_name):
                    logger.warning(f"Failed to claim task: {task_name}")
                    continue

                # Read task content
                with open(task_file, "r") as f:
                    content = f.read()

                # Generate draft reply
                draft = self._generate_email_draft(content)

                # Move to approval with draft
                if self.coordinator.move_to_approval(
                    self.agent_name,
                    task_name,
                    "email",
                    draft
                ):
                    logger.info(f"Email draft created: {task_name}")
                    self.dashboard.add_activity(
                        "Email Draft",
                        f"Created draft for {task_name}"
                    )
                else:
                    logger.error(f"Failed to move task to approval: {task_name}")
                    self.coordinator.release_task(self.agent_name, task_name, "email")

        except Exception as e:
            logger.error(f"Error processing email tasks: {e}")

    def _process_social_tasks(self):
        """Process social media tasks from Needs_Action/social/"""
        try:
            # Get all social tasks
            social_tasks = list(self.needs_action_social.glob("*.md"))
            if not social_tasks:
                logger.info("No social media tasks to process")
                return

            logger.info(f"Found {len(social_tasks)} social media tasks")

            for task_file in social_tasks:
                task_name = task_file.name
                logger.info(f"Processing social task: {task_name}")

                # Claim task
                if not self.coordinator.claim_task("social", task_name, self.agent_name):
                    logger.warning(f"Failed to claim task: {task_name}")
                    continue

                # Read task content
                with open(task_file, "r") as f:
                    content = f.read()

                # Generate draft post
                draft = self._generate_social_draft(content)

                # Move to approval with draft
                if self.coordinator.move_to_approval(
                    self.agent_name,
                    task_name,
                    "social",
                    draft
                ):
                    logger.info(f"Social draft created: {task_name}")
                    self.dashboard.add_activity(
                        "Social Draft",
                        f"Created draft for {task_name}"
                    )
                else:
                    logger.error(f"Failed to move task to approval: {task_name}")
                    self.coordinator.release_task(self.agent_name, task_name, "social")

        except Exception as e:
            logger.error(f"Error processing social tasks: {e}")

    def _generate_email_draft(self, task_content: str) -> str:
        """
        Generate email draft reply

        Args:
            task_content: Original email task content

        Returns:
            Draft reply text
        """
        # Extract sender from task
        sender = "Unknown"
        for line in task_content.split("\n"):
            if line.startswith("from:"):
                sender = line.split(":", 1)[1].strip()
                break

        # Simple draft template (in production, use Claude API)
        draft = f"""Subject: Re: [Original Subject]

Dear {sender},

Thank you for your email. I appreciate you reaching out.

[Draft response - awaiting local approval]

Best regards,
AI Employee"""

        return draft

    def _generate_social_draft(self, task_content: str) -> str:
        """
        Generate social media draft post

        Args:
            task_content: Original social task content

        Returns:
            Draft post text
        """
        # Simple draft template (in production, use Claude API)
        draft = """[Social Media Draft Post]

This is a draft post awaiting local approval.

Key points:
- Point 1
- Point 2
- Point 3

#hashtags #draft

[Awaiting local approval before posting]"""

        return draft

    def _write_health_signal(self):
        """Write health signal to Updates/"""
        try:
            health_signal = {
                "component": "Cloud Agent",
                "status": "HEALTHY",
                "timestamp": datetime.utcnow().isoformat(),
                "tasks_processed": len(list(self.in_progress.glob("*.md"))),
            }

            self.dashboard.write_signal(
                self.agent_name,
                "status",
                health_signal
            )

            logger.info("Health signal written")
        except Exception as e:
            logger.error(f"Failed to write health signal: {e}")

    def get_status(self) -> Dict:
        """Get cloud agent status"""
        try:
            claimed_tasks = self.coordinator.get_claimed_tasks(self.agent_name)
            pending_approvals_email = self.coordinator.get_pending_approvals("email")
            pending_approvals_social = self.coordinator.get_pending_approvals("social")

            return {
                "agent": self.agent_name,
                "status": "OPERATIONAL",
                "timestamp": datetime.utcnow().isoformat(),
                "claimed_tasks": len(claimed_tasks),
                "pending_approvals_email": len(pending_approvals_email),
                "pending_approvals_social": len(pending_approvals_social),
                "total_pending": len(pending_approvals_email) + len(pending_approvals_social),
            }
        except Exception as e:
            logger.error(f"Failed to get status: {e}")
            return {"agent": self.agent_name, "status": "ERROR", "error": str(e)}


def main():
    """Demo of cloud agent"""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    agent = CloudAgent(check_interval=5)

    print("Cloud Agent Demo\n")

    # 1. Show initial status
    print("1. Initial status:")
    status = agent.get_status()
    print(f"   Claimed tasks: {status['claimed_tasks']}")
    print(f"   Pending approvals (email): {status['pending_approvals_email']}")
    print(f"   Pending approvals (social): {status['pending_approvals_social']}\n")

    # 2. Create test email task
    print("2. Creating test email task...")
    test_email = """---
type: email
from: test@example.com
received: 2026-03-29T14:00:00Z
priority: high
status: pending
---

## Test Email
This is a test email from test@example.com requesting information about our services.
"""
    test_email_file = agent.needs_action_email / "TEST_email_inquiry.md"
    with open(test_email_file, "w") as f:
        f.write(test_email)
    print(f"   Created: {test_email_file}\n")

    # 3. Create test social task
    print("3. Creating test social task...")
    test_social = """---
type: social
platform: linkedin
received: 2026-03-29T14:00:00Z
priority: normal
status: pending
---

## Social Post
This is a test social media post about AI automation.
"""
    test_social_file = agent.needs_action_social / "TEST_social_automation.md"
    with open(test_social_file, "w") as f:
        f.write(test_social)
    print(f"   Created: {test_social_file}\n")

    # 4. Run one iteration
    print("4. Running one iteration...")
    try:
        # Sync vault
        success, msg = agent.git_sync.pull_vault(agent.agent_name)
        print(f"   Pull: {msg}")

        # Process tasks
        agent._process_email_tasks()
        agent._process_social_tasks()

        # Write health signal
        agent._write_health_signal()

        # Push vault
        success, msg = agent.git_sync.push_vault(agent.agent_name, "Demo: Cloud Agent test")
        print(f"   Push: {msg}\n")

    except Exception as e:
        print(f"   Error: {e}\n")

    # 5. Show final status
    print("5. Final status:")
    status = agent.get_status()
    print(f"   Claimed tasks: {status['claimed_tasks']}")
    print(f"   Pending approvals (email): {status['pending_approvals_email']}")
    print(f"   Pending approvals (social): {status['pending_approvals_social']}")
    print(f"   Total pending: {status['total_pending']}\n")

    print("[OK] Cloud Agent demo completed!")


if __name__ == "__main__":
    main()
