#!/usr/bin/env python3
"""
Local Agent - Runs on local machine
Monitors approvals, executes actions, handles WhatsApp and banking
Merges cloud signals into Dashboard.md
Does NOT sync secrets (.env, .whatsapp_session, banking creds)
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


class LocalAgent:
    """Local agent for approvals, execution, and sensitive operations"""

    def __init__(self, vault_path: str = ".", check_interval: int = 30):
        """
        Initialize local agent

        Args:
            vault_path: Path to vault directory
            check_interval: Seconds between checks
        """
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        self.agent_name = "local"

        # Initialize components
        self.coordinator = VaultCoordinator(vault_path)
        self.dashboard = DashboardManager(vault_path)
        self.git_sync = GitSyncManager(vault_path)

        # Directories
        self.pending_approval_email = self.vault_path / "Pending_Approval" / "email"
        self.pending_approval_social = self.vault_path / "Pending_Approval" / "social"
        self.pending_approval_payments = self.vault_path / "Pending_Approval" / "payments"
        self.approved = self.vault_path / "Approved"
        self.in_progress = self.vault_path / "In_Progress" / self.agent_name
        self.needs_action_whatsapp = self.vault_path / "Needs_Action" / "whatsapp"
        self.needs_action_payments = self.vault_path / "Needs_Action" / "payments"
        self.updates = self.vault_path / "Updates"
        self.done = self.vault_path / "Done"

        # Create directories
        for directory in [
            self.pending_approval_email,
            self.pending_approval_social,
            self.pending_approval_payments,
            self.approved,
            self.in_progress,
            self.needs_action_whatsapp,
            self.needs_action_payments,
            self.updates,
            self.done,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

        logger.info("Local Agent initialized")

    def run_continuous(self, duration: Optional[int] = None):
        """
        Run local agent continuously

        Args:
            duration: Optional duration in seconds (None = infinite)
        """
        start_time = time.time()
        iteration = 0

        try:
            logger.info(f"Local Agent starting (check interval: {self.check_interval}s)")
            self.dashboard.update_status("Local Agent", "OPERATIONAL")

            while True:
                iteration += 1
                logger.info(f"--- Local Agent Iteration {iteration} ---")

                try:
                    # 1. Sync vault (pull latest changes)
                    logger.info("Syncing vault...")
                    success, msg = self.git_sync.pull_vault(self.agent_name)
                    if success:
                        logger.info(f"Vault synced: {msg}")
                    else:
                        logger.warning(f"Vault sync failed: {msg}")

                    # 2. Merge cloud signals into dashboard
                    logger.info("Merging cloud signals...")
                    self.dashboard.merge_signals()

                    # 3. Monitor approvals
                    logger.info("Monitoring approvals...")
                    self._monitor_approvals()

                    # 4. Process WhatsApp tasks
                    logger.info("Processing WhatsApp tasks...")
                    self._process_whatsapp_tasks()

                    # 5. Process payment tasks
                    logger.info("Processing payment tasks...")
                    self._process_payment_tasks()

                    # 6. Execute approved tasks
                    logger.info("Executing approved tasks...")
                    self._execute_approved_tasks()

                    # 7. Push vault changes
                    logger.info("Pushing vault changes...")
                    success, msg = self.git_sync.push_vault(
                        self.agent_name,
                        f"Local Agent sync - iteration {iteration}"
                    )
                    if success:
                        logger.info(f"Vault pushed: {msg}")
                    else:
                        logger.warning(f"Vault push failed: {msg}")

                except Exception as e:
                    logger.error(f"Error in iteration {iteration}: {e}")

                # Check duration
                if duration and (time.time() - start_time) > duration:
                    logger.info(f"Local Agent stopping after {duration}s")
                    break

                # Sleep before next iteration
                logger.info(f"Sleeping for {self.check_interval}s...")
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            logger.info("Local Agent stopped by user")
        except Exception as e:
            logger.error(f"Local Agent fatal error: {e}")
            self.dashboard.update_status("Local Agent", "DOWN")
        finally:
            logger.info("Local Agent shutdown")

    def _monitor_approvals(self):
        """Monitor and display pending approvals"""
        try:
            email_approvals = self.coordinator.get_pending_approvals("email")
            social_approvals = self.coordinator.get_pending_approvals("social")
            payment_approvals = self.coordinator.get_pending_approvals("payments")

            total = len(email_approvals) + len(social_approvals) + len(payment_approvals)

            if total > 0:
                logger.info(f"Pending approvals: {total}")
                logger.info(f"  Email: {len(email_approvals)}")
                logger.info(f"  Social: {len(social_approvals)}")
                logger.info(f"  Payments: {len(payment_approvals)}")

                # Log to dashboard
                self.dashboard.add_activity(
                    "Approvals Pending",
                    f"{total} items awaiting approval"
                )
            else:
                logger.info("No pending approvals")

        except Exception as e:
            logger.error(f"Error monitoring approvals: {e}")

    def _process_whatsapp_tasks(self):
        """Process WhatsApp tasks (local only - has session)"""
        try:
            whatsapp_tasks = list(self.needs_action_whatsapp.glob("*.md"))
            if not whatsapp_tasks:
                logger.info("No WhatsApp tasks to process")
                return

            logger.info(f"Found {len(whatsapp_tasks)} WhatsApp tasks")

            for task_file in whatsapp_tasks:
                task_name = task_file.name
                logger.info(f"Processing WhatsApp task: {task_name}")

                # Claim task
                if not self.coordinator.claim_task("whatsapp", task_name, self.agent_name):
                    logger.warning(f"Failed to claim task: {task_name}")
                    continue

                # In production: Send WhatsApp message via MCP
                # For now: Just move to approval
                if self.coordinator.move_to_approval(
                    self.agent_name,
                    task_name,
                    "whatsapp",
                    "WhatsApp reply drafted"
                ):
                    logger.info(f"WhatsApp task moved to approval: {task_name}")
                else:
                    logger.error(f"Failed to move task to approval: {task_name}")
                    self.coordinator.release_task(self.agent_name, task_name, "whatsapp")

        except Exception as e:
            logger.error(f"Error processing WhatsApp tasks: {e}")

    def _process_payment_tasks(self):
        """Process payment tasks (local only - has banking creds)"""
        try:
            payment_tasks = list(self.needs_action_payments.glob("*.md"))
            if not payment_tasks:
                logger.info("No payment tasks to process")
                return

            logger.info(f"Found {len(payment_tasks)} payment tasks")

            for task_file in payment_tasks:
                task_name = task_file.name
                logger.info(f"Processing payment task: {task_name}")

                # Claim task
                if not self.coordinator.claim_task("payments", task_name, self.agent_name):
                    logger.warning(f"Failed to claim task: {task_name}")
                    continue

                # In production: Create payment draft via Odoo MCP
                # For now: Just move to approval
                if self.coordinator.move_to_approval(
                    self.agent_name,
                    task_name,
                    "payments",
                    "Payment draft created"
                ):
                    logger.info(f"Payment task moved to approval: {task_name}")
                else:
                    logger.error(f"Failed to move task to approval: {task_name}")
                    self.coordinator.release_task(self.agent_name, task_name, "payments")

        except Exception as e:
            logger.error(f"Error processing payment tasks: {e}")

    def _execute_approved_tasks(self):
        """Execute approved tasks"""
        try:
            approved_tasks = self.coordinator.get_approved_tasks()
            if not approved_tasks:
                logger.info("No approved tasks to execute")
                return

            logger.info(f"Found {len(approved_tasks)} approved tasks to execute")

            for task_name in approved_tasks:
                logger.info(f"Executing approved task: {task_name}")

                try:
                    # In production: Execute via MCP servers
                    # For now: Just move to Done
                    result = f"Executed by local agent at {datetime.utcnow().isoformat()}"

                    if self.coordinator.complete_task(task_name, "unknown", result):
                        logger.info(f"Task completed: {task_name}")
                        self.dashboard.add_activity(
                            "Task Executed",
                            f"Completed: {task_name}"
                        )
                    else:
                        logger.error(f"Failed to complete task: {task_name}")

                except Exception as e:
                    logger.error(f"Error executing task {task_name}: {e}")

        except Exception as e:
            logger.error(f"Error executing approved tasks: {e}")

    def approve_task(self, task_name: str, domain: str) -> bool:
        """
        Approve a task (move from Pending_Approval to Approved)

        Args:
            task_name: Task filename
            domain: Task domain (email, social, payments)

        Returns:
            True if successfully approved
        """
        try:
            if self.coordinator.approve_task(task_name, domain):
                logger.info(f"Task approved: {task_name}")
                self.dashboard.add_activity(
                    "Task Approved",
                    f"Approved: {task_name}"
                )
                return True
            else:
                logger.error(f"Failed to approve task: {task_name}")
                return False
        except Exception as e:
            logger.error(f"Error approving task: {e}")
            return False

    def reject_task(self, task_name: str, domain: str, reason: str = "") -> bool:
        """
        Reject a task (move back to Needs_Action with feedback)

        Args:
            task_name: Task filename
            domain: Task domain
            reason: Rejection reason

        Returns:
            True if successfully rejected
        """
        try:
            if self.coordinator.reject_task(task_name, domain, reason):
                logger.info(f"Task rejected: {task_name}")
                self.dashboard.add_activity(
                    "Task Rejected",
                    f"Rejected: {task_name}"
                )
                return True
            else:
                logger.error(f"Failed to reject task: {task_name}")
                return False
        except Exception as e:
            logger.error(f"Error rejecting task: {e}")
            return False

    def get_status(self) -> Dict:
        """Get local agent status"""
        try:
            pending_email = self.coordinator.get_pending_approvals("email")
            pending_social = self.coordinator.get_pending_approvals("social")
            pending_payments = self.coordinator.get_pending_approvals("payments")
            approved = self.coordinator.get_approved_tasks()

            return {
                "agent": self.agent_name,
                "status": "OPERATIONAL",
                "timestamp": datetime.utcnow().isoformat(),
                "pending_approvals_email": len(pending_email),
                "pending_approvals_social": len(pending_social),
                "pending_approvals_payments": len(pending_payments),
                "approved_tasks": len(approved),
                "total_pending": len(pending_email) + len(pending_social) + len(pending_payments),
            }
        except Exception as e:
            logger.error(f"Failed to get status: {e}")
            return {"agent": self.agent_name, "status": "ERROR", "error": str(e)}


def main():
    """Demo of local agent"""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    agent = LocalAgent(check_interval=5)

    print("Local Agent Demo\n")

    # 1. Show initial status
    print("1. Initial status:")
    status = agent.get_status()
    print(f"   Pending approvals (email): {status['pending_approvals_email']}")
    print(f"   Pending approvals (social): {status['pending_approvals_social']}")
    print(f"   Pending approvals (payments): {status['pending_approvals_payments']}")
    print(f"   Approved tasks: {status['approved_tasks']}\n")

    # 2. Create test WhatsApp task
    print("2. Creating test WhatsApp task...")
    test_whatsapp = """---
type: whatsapp
from: +1234567890
received: 2026-03-29T14:00:00Z
priority: high
status: pending
---

## WhatsApp Message
This is a test WhatsApp message from a client.
"""
    test_whatsapp_file = agent.needs_action_whatsapp / "TEST_whatsapp_client.md"
    with open(test_whatsapp_file, "w") as f:
        f.write(test_whatsapp)
    print(f"   Created: {test_whatsapp_file}\n")

    # 3. Create test payment task
    print("3. Creating test payment task...")
    test_payment = """---
type: payment
amount: 500
currency: USD
received: 2026-03-29T14:00:00Z
priority: high
status: pending
---

## Payment Request
This is a test payment request for invoice #12345.
"""
    test_payment_file = agent.needs_action_payments / "TEST_payment_invoice.md"
    with open(test_payment_file, "w") as f:
        f.write(test_payment)
    print(f"   Created: {test_payment_file}\n")

    # 4. Run one iteration
    print("4. Running one iteration...")
    try:
        # Sync vault
        success, msg = agent.git_sync.pull_vault(agent.agent_name)
        print(f"   Pull: {msg}")

        # Merge signals
        agent.dashboard.merge_signals()

        # Monitor approvals
        agent._monitor_approvals()

        # Process tasks
        agent._process_whatsapp_tasks()
        agent._process_payment_tasks()

        # Push vault
        success, msg = agent.git_sync.push_vault(agent.agent_name, "Demo: Local Agent test")
        print(f"   Push: {msg}\n")

    except Exception as e:
        print(f"   Error: {e}\n")

    # 5. Show final status
    print("5. Final status:")
    status = agent.get_status()
    print(f"   Pending approvals (email): {status['pending_approvals_email']}")
    print(f"   Pending approvals (social): {status['pending_approvals_social']}")
    print(f"   Pending approvals (payments): {status['pending_approvals_payments']}")
    print(f"   Approved tasks: {status['approved_tasks']}")
    print(f"   Total pending: {status['total_pending']}\n")

    print("[OK] Local Agent demo completed!")


if __name__ == "__main__":
    main()
