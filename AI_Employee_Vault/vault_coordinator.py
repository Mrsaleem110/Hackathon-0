#!/usr/bin/env python3
"""
Vault Coordinator - Implements claim-by-move pattern for multi-agent coordination
Prevents double-work by ensuring only one agent can claim a task
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VaultCoordinator:
    """Manages task claiming and state transitions in the vault"""

    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / "Needs_Action"
        self.in_progress = self.vault_path / "In_Progress"
        self.pending_approval = self.vault_path / "Pending_Approval"
        self.approved = self.vault_path / "Approved"
        self.done = self.vault_path / "Done"
        self.updates = self.vault_path / "Updates"
        self.logs = self.vault_path / "Logs"

        # Create directories if they don't exist
        for directory in [
            self.needs_action,
            self.in_progress,
            self.pending_approval,
            self.approved,
            self.done,
            self.updates,
            self.logs,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

    def claim_task(self, domain: str, task_file: str, agent: str) -> bool:
        """
        Claim a task using atomic move (claim-by-move pattern)

        Args:
            domain: Task domain (email, social, whatsapp, payments)
            task_file: Task filename
            agent: Agent claiming the task (cloud or local)

        Returns:
            True if successfully claimed, False if already claimed
        """
        source = self.needs_action / domain / task_file
        dest = self.in_progress / agent / task_file

        if not source.exists():
            logger.warning(f"Task not found: {source}")
            return False

        # Ensure destination directory exists
        dest.parent.mkdir(parents=True, exist_ok=True)

        # Check if already claimed by another agent
        for other_agent in ["cloud", "local"]:
            if other_agent != agent:
                if (self.in_progress / other_agent / task_file).exists():
                    logger.warning(
                        f"Task already claimed by {other_agent}: {task_file}"
                    )
                    return False

        try:
            # Atomic move (claim-by-move)
            shutil.move(str(source), str(dest))
            logger.info(f"Task claimed by {agent}: {task_file}")

            # Log the claim
            self._log_action(
                action="claim",
                domain=domain,
                task=task_file,
                agent=agent,
                status="success",
            )
            return True
        except Exception as e:
            logger.error(f"Failed to claim task: {e}")
            self._log_action(
                action="claim",
                domain=domain,
                task=task_file,
                agent=agent,
                status="failed",
                error=str(e),
            )
            return False

    def release_task(self, agent: str, task_file: str, domain: str) -> bool:
        """
        Release a task back to Needs_Action (if rejected or failed)

        Args:
            agent: Agent releasing the task
            task_file: Task filename
            domain: Task domain

        Returns:
            True if successfully released
        """
        source = self.in_progress / agent / task_file
        dest = self.needs_action / domain / task_file

        if not source.exists():
            logger.warning(f"Task not found in In_Progress: {source}")
            return False

        try:
            shutil.move(str(source), str(dest))
            logger.info(f"Task released by {agent}: {task_file}")
            self._log_action(
                action="release",
                domain=domain,
                task=task_file,
                agent=agent,
                status="success",
            )
            return True
        except Exception as e:
            logger.error(f"Failed to release task: {e}")
            return False

    def move_to_approval(
        self, agent: str, task_file: str, domain: str, draft_content: str = None
    ) -> bool:
        """
        Move task from In_Progress to Pending_Approval

        Args:
            agent: Agent moving the task
            task_file: Task filename
            domain: Task domain
            draft_content: Optional draft content to include

        Returns:
            True if successfully moved
        """
        source = self.in_progress / agent / task_file
        dest = self.pending_approval / domain / task_file

        if not source.exists():
            logger.warning(f"Task not found: {source}")
            return False

        try:
            # Read source file
            with open(source, "r") as f:
                content = f.read()

            # Add draft content if provided
            if draft_content:
                content += f"\n\n## Draft\n{draft_content}"

            # Write to destination
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "w") as f:
                f.write(content)

            # Remove source
            source.unlink()

            logger.info(f"Task moved to approval: {task_file}")
            self._log_action(
                action="move_to_approval",
                domain=domain,
                task=task_file,
                agent=agent,
                status="success",
            )
            return True
        except Exception as e:
            logger.error(f"Failed to move task to approval: {e}")
            return False

    def approve_task(self, task_file: str, domain: str) -> bool:
        """
        Approve a task (move from Pending_Approval to Approved)

        Args:
            task_file: Task filename
            domain: Task domain

        Returns:
            True if successfully approved
        """
        source = self.pending_approval / domain / task_file
        dest = self.approved / task_file

        if not source.exists():
            logger.warning(f"Task not found in Pending_Approval: {source}")
            return False

        try:
            # Add approval metadata
            with open(source, "r") as f:
                content = f.read()

            # Add approval timestamp
            approval_line = f"\napproved_at: {datetime.utcnow().isoformat()}\n"
            content += approval_line

            # Write to destination
            self.approved.mkdir(parents=True, exist_ok=True)
            with open(dest, "w") as f:
                f.write(content)

            # Remove source
            source.unlink()

            logger.info(f"Task approved: {task_file}")
            self._log_action(
                action="approve",
                domain=domain,
                task=task_file,
                status="success",
            )
            return True
        except Exception as e:
            logger.error(f"Failed to approve task: {e}")
            return False

    def reject_task(self, task_file: str, domain: str, reason: str = "") -> bool:
        """
        Reject a task (move back to Needs_Action with feedback)

        Args:
            task_file: Task filename
            domain: Task domain
            reason: Rejection reason

        Returns:
            True if successfully rejected
        """
        source = self.pending_approval / domain / task_file
        dest = self.needs_action / domain / task_file

        if not source.exists():
            logger.warning(f"Task not found in Pending_Approval: {source}")
            return False

        try:
            # Read source and add rejection feedback
            with open(source, "r") as f:
                content = f.read()

            if reason:
                content += f"\n\n## Rejection Feedback\n{reason}\nrejected_at: {datetime.utcnow().isoformat()}\n"

            # Write to destination
            self.needs_action.mkdir(parents=True, exist_ok=True)
            with open(dest, "w") as f:
                f.write(content)

            # Remove source
            source.unlink()

            logger.info(f"Task rejected: {task_file}")
            self._log_action(
                action="reject",
                domain=domain,
                task=task_file,
                status="success",
                reason=reason,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to reject task: {e}")
            return False

    def complete_task(self, task_file: str, domain: str, result: str = "") -> bool:
        """
        Complete a task (move to Done)

        Args:
            task_file: Task filename
            domain: Task domain
            result: Execution result/output

        Returns:
            True if successfully completed
        """
        source = self.approved / task_file
        dest = self.done / f"COMPLETED_{task_file}"

        if not source.exists():
            logger.warning(f"Task not found in Approved: {source}")
            return False

        try:
            # Read source and add completion metadata
            with open(source, "r") as f:
                content = f.read()

            if result:
                content += f"\n\n## Execution Result\n{result}\n"

            content += f"\ncompleted_at: {datetime.utcnow().isoformat()}\n"

            # Write to destination
            self.done.mkdir(parents=True, exist_ok=True)
            with open(dest, "w") as f:
                f.write(content)

            # Remove source
            source.unlink()

            logger.info(f"Task completed: {task_file}")
            self._log_action(
                action="complete",
                domain=domain,
                task=task_file,
                status="success",
            )
            return True
        except Exception as e:
            logger.error(f"Failed to complete task: {e}")
            return False

    def get_claimed_tasks(self, agent: str) -> List[str]:
        """Get all tasks claimed by an agent"""
        agent_dir = self.in_progress / agent
        if not agent_dir.exists():
            return []
        return [f.name for f in agent_dir.glob("*.md")]

    def get_pending_approvals(self, domain: str) -> List[str]:
        """Get all tasks pending approval in a domain"""
        domain_dir = self.pending_approval / domain
        if not domain_dir.exists():
            return []
        return [f.name for f in domain_dir.glob("*.md")]

    def get_approved_tasks(self) -> List[str]:
        """Get all approved tasks ready for execution"""
        if not self.approved.exists():
            return []
        return [f.name for f in self.approved.glob("*.md")]

    def detect_orphaned_tasks(self) -> Dict[str, List[str]]:
        """Detect tasks claimed by multiple agents (should not happen)"""
        orphaned = {}

        # Check each task in Needs_Action
        for domain_dir in self.needs_action.glob("*"):
            if not domain_dir.is_dir():
                continue

            for task_file in domain_dir.glob("*.md"):
                # Check if also in In_Progress
                for agent in ["cloud", "local"]:
                    if (self.in_progress / agent / task_file.name).exists():
                        key = f"in_needs_and_in_progress_{agent}"
                        if key not in orphaned:
                            orphaned[key] = []
                        orphaned[key].append(task_file.name)

        return orphaned

    def _log_action(
        self,
        action: str,
        domain: str = "",
        task: str = "",
        agent: str = "",
        status: str = "",
        error: str = "",
        reason: str = "",
    ):
        """Log coordinator action to audit trail"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "domain": domain,
            "task": task,
            "agent": agent,
            "status": status,
        }

        if error:
            log_entry["error"] = error
        if reason:
            log_entry["reason"] = reason

        # Append to daily log
        today = datetime.utcnow().strftime("%Y-%m-%d")
        log_file = self.logs / f"coordinator_{today}.json"

        try:
            if log_file.exists():
                with open(log_file, "r") as f:
                    logs = json.load(f)
            else:
                logs = []

            logs.append(log_entry)

            with open(log_file, "w") as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to log action: {e}")


def main():
    """Demo of vault coordinator"""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    coordinator = VaultCoordinator()

    # Create a test task
    test_domain = "email"
    test_task = "TEST_email_demo.md"
    test_content = """---
type: email
from: test@example.com
received: 2026-03-28T20:00:00Z
priority: high
status: pending
---

## Test Email
This is a test email for the vault coordinator demo.
"""

    # Create test task in Needs_Action
    test_file = coordinator.needs_action / test_domain / test_task
    test_file.parent.mkdir(parents=True, exist_ok=True)
    with open(test_file, "w") as f:
        f.write(test_content)

    print(f"Created test task: {test_file}")

    # Test claim-by-move
    print("\n1. Testing claim-by-move...")
    if coordinator.claim_task(test_domain, test_task, "cloud"):
        print("[OK] Cloud agent claimed task")
    else:
        print("[FAIL] Failed to claim task")

    # Verify task is in In_Progress
    claimed = coordinator.get_claimed_tasks("cloud")
    print(f"Cloud claimed tasks: {claimed}")

    # Test move to approval
    print("\n2. Testing move to approval...")
    draft = "This is a draft reply to the test email."
    if coordinator.move_to_approval("cloud", test_task, test_domain, draft):
        print("[OK] Task moved to approval")
    else:
        print("[FAIL] Failed to move to approval")

    # Verify task is in Pending_Approval
    pending = coordinator.get_pending_approvals(test_domain)
    print(f"Pending approvals in {test_domain}: {pending}")

    # Test approve
    print("\n3. Testing approve...")
    if coordinator.approve_task(test_task, test_domain):
        print("[OK] Task approved")
    else:
        print("[FAIL] Failed to approve task")

    # Verify task is in Approved
    approved = coordinator.get_approved_tasks()
    print(f"Approved tasks: {approved}")

    # Test complete
    print("\n4. Testing complete...")
    result = "Email sent successfully to test@example.com"
    if coordinator.complete_task(test_task, test_domain, result):
        print("[OK] Task completed")
    else:
        print("[FAIL] Failed to complete task")

    # Verify task is in Done
    done_files = list(coordinator.done.glob("*.md"))
    print(f"Done tasks: {[f.name for f in done_files]}")

    print("\n[OK] Vault coordinator demo completed successfully!")


if __name__ == "__main__":
    main()
