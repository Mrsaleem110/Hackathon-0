#!/usr/bin/env python3
"""
Git Sync Manager - Handles vault synchronization between Cloud and Local agents
Implements conflict resolution with Local-wins strategy
Excludes secrets (.env, .session, banking creds) from sync
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GitSyncManager:
    """Manages git-based vault synchronization"""

    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path)
        self.logs_dir = self.vault_path / "Logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Verify git repo exists
        if not (self.vault_path / ".git").exists():
            logger.warning("Not a git repository. Initialize with: git init")

    def pull_vault(self, agent: str = "local") -> Tuple[bool, str]:
        """
        Pull latest vault changes from remote
        Handles conflicts with Local-wins strategy

        Args:
            agent: Agent pulling (cloud or local)

        Returns:
            Tuple of (success, message)
        """
        try:
            # Fetch latest changes
            result = subprocess.run(
                ["git", "fetch", "origin"],
                cwd=self.vault_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                msg = f"Git fetch failed: {result.stderr}"
                logger.error(msg)
                self._log_sync_action(agent, "pull", "failed", msg)
                return False, msg

            # Check for conflicts
            status_result = subprocess.run(
                ["git", "status"],
                cwd=self.vault_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if "both modified" in status_result.stdout or "conflict" in status_result.stdout:
                logger.info(f"Conflicts detected, resolving with {agent}-wins strategy")
                self._resolve_conflicts(agent)

            # Merge changes
            merge_result = subprocess.run(
                ["git", "merge", "origin/main"],
                cwd=self.vault_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if merge_result.returncode != 0:
                # Handle merge conflicts
                if "CONFLICT" in merge_result.stdout:
                    logger.info("Merge conflicts detected, resolving...")
                    self._resolve_conflicts(agent)

                    # Complete merge
                    complete_result = subprocess.run(
                        ["git", "commit", "-m", f"Merge conflicts resolved by {agent}"],
                        cwd=self.vault_path,
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )

                    if complete_result.returncode != 0:
                        msg = f"Failed to complete merge: {complete_result.stderr}"
                        logger.error(msg)
                        self._log_sync_action(agent, "pull", "failed", msg)
                        return False, msg
                else:
                    msg = f"Git merge failed: {merge_result.stderr}"
                    logger.error(msg)
                    self._log_sync_action(agent, "pull", "failed", msg)
                    return False, msg

            msg = "Vault pulled successfully"
            logger.info(msg)
            self._log_sync_action(agent, "pull", "success", msg)
            return True, msg

        except subprocess.TimeoutExpired:
            msg = "Git pull timed out"
            logger.error(msg)
            self._log_sync_action(agent, "pull", "failed", msg)
            return False, msg
        except Exception as e:
            msg = f"Git pull failed: {str(e)}"
            logger.error(msg)
            self._log_sync_action(agent, "pull", "failed", msg)
            return False, msg

    def push_vault(self, agent: str = "local", message: str = "") -> Tuple[bool, str]:
        """
        Push vault changes to remote

        Args:
            agent: Agent pushing (cloud or local)
            message: Commit message

        Returns:
            Tuple of (success, message)
        """
        try:
            # Stage changes (excluding secrets)
            stage_result = subprocess.run(
                ["git", "add", "-A", "--", "Needs_Action/", "Plans/", "In_Progress/",
                 "Pending_Approval/", "Approved/", "Done/", "Updates/", "Dashboard.md"],
                cwd=self.vault_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if stage_result.returncode != 0:
                logger.warning(f"Git add warning: {stage_result.stderr}")

            # Check if there are changes to commit
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.vault_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if not status_result.stdout.strip():
                msg = "No changes to commit"
                logger.info(msg)
                return True, msg

            # Create commit
            if not message:
                message = f"Vault sync by {agent} at {datetime.utcnow().isoformat()}"

            commit_result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.vault_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if commit_result.returncode != 0:
                msg = f"Git commit failed: {commit_result.stderr}"
                logger.error(msg)
                self._log_sync_action(agent, "push", "failed", msg)
                return False, msg

            # Push to remote with retry
            for attempt in range(3):
                push_result = subprocess.run(
                    ["git", "push", "origin", "main"],
                    cwd=self.vault_path,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if push_result.returncode == 0:
                    msg = "Vault pushed successfully"
                    logger.info(msg)
                    self._log_sync_action(agent, "push", "success", msg)
                    return True, msg
                elif "rejected" in push_result.stderr or "non-fast-forward" in push_result.stderr:
                    # Remote has changes, pull and retry
                    logger.info(f"Push rejected, pulling and retrying (attempt {attempt + 1}/3)")
                    self.pull_vault(agent)
                else:
                    msg = f"Git push failed: {push_result.stderr}"
                    logger.error(msg)
                    self._log_sync_action(agent, "push", "failed", msg)
                    return False, msg

            msg = "Git push failed after 3 retries"
            logger.error(msg)
            self._log_sync_action(agent, "push", "failed", msg)
            return False, msg

        except subprocess.TimeoutExpired:
            msg = "Git push timed out"
            logger.error(msg)
            self._log_sync_action(agent, "push", "failed", msg)
            return False, msg
        except Exception as e:
            msg = f"Git push failed: {str(e)}"
            logger.error(msg)
            self._log_sync_action(agent, "push", "failed", msg)
            return False, msg

    def sync_vault(self, agent: str = "local", message: str = "") -> Tuple[bool, str]:
        """
        Full sync: pull, then push

        Args:
            agent: Agent syncing (cloud or local)
            message: Commit message for push

        Returns:
            Tuple of (success, message)
        """
        # Pull first
        pull_success, pull_msg = self.pull_vault(agent)
        if not pull_success:
            return False, f"Pull failed: {pull_msg}"

        # Then push
        push_success, push_msg = self.push_vault(agent, message)
        if not push_success:
            return False, f"Push failed: {push_msg}"

        return True, "Vault synced successfully"

    def _resolve_conflicts(self, agent: str):
        """
        Resolve merge conflicts with agent-wins strategy
        Local wins over Cloud

        Args:
            agent: Agent resolving conflicts
        """
        try:
            if agent == "local":
                # Local wins: use ours
                subprocess.run(
                    ["git", "checkout", "--ours", "."],
                    cwd=self.vault_path,
                    capture_output=True,
                    timeout=30,
                )
            else:
                # Cloud loses: use theirs (remote)
                subprocess.run(
                    ["git", "checkout", "--theirs", "."],
                    cwd=self.vault_path,
                    capture_output=True,
                    timeout=30,
                )

            # Stage resolved files
            subprocess.run(
                ["git", "add", "."],
                cwd=self.vault_path,
                capture_output=True,
                timeout=30,
            )

            logger.info(f"Conflicts resolved with {agent}-wins strategy")
        except Exception as e:
            logger.error(f"Failed to resolve conflicts: {e}")

    def verify_sync(self) -> Tuple[bool, dict]:
        """
        Verify vault sync consistency

        Returns:
            Tuple of (is_consistent, report)
        """
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "is_consistent": True,
            "issues": [],
            "stats": {},
        }

        try:
            # Check git status
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.vault_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if status_result.stdout.strip():
                report["issues"].append("Uncommitted changes detected")
                report["is_consistent"] = False

            # Check for conflicts
            if "UU" in status_result.stdout or "AA" in status_result.stdout:
                report["issues"].append("Merge conflicts detected")
                report["is_consistent"] = False

            # Check remote status
            fetch_result = subprocess.run(
                ["git", "fetch", "origin"],
                cwd=self.vault_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

            log_result = subprocess.run(
                ["git", "log", "--oneline", "-1", "HEAD"],
                cwd=self.vault_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if log_result.stdout:
                report["stats"]["latest_commit"] = log_result.stdout.strip()

            # Count files in each directory
            for domain in ["email", "social", "whatsapp", "payments"]:
                needs_action_dir = self.vault_path / "Needs_Action" / domain
                if needs_action_dir.exists():
                    count = len(list(needs_action_dir.glob("*.md")))
                    report["stats"][f"needs_action_{domain}"] = count

            logger.info(f"Sync verification: {'CONSISTENT' if report['is_consistent'] else 'INCONSISTENT'}")
            return report["is_consistent"], report

        except Exception as e:
            report["issues"].append(f"Verification failed: {str(e)}")
            report["is_consistent"] = False
            logger.error(f"Sync verification failed: {e}")
            return False, report

    def _log_sync_action(self, agent: str, action: str, status: str, message: str):
        """Log sync action to audit trail"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent,
            "action": action,
            "status": status,
            "message": message,
        }

        today = datetime.utcnow().strftime("%Y-%m-%d")
        log_file = self.logs_dir / f"sync_{today}.json"

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
            logger.error(f"Failed to log sync action: {e}")


def main():
    """Demo of git sync manager"""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    manager = GitSyncManager()

    print("Git Sync Manager Demo\n")

    # 1. Verify sync
    print("1. Verifying vault sync...")
    is_consistent, report = manager.verify_sync()
    print(f"[OK] Sync status: {'CONSISTENT' if is_consistent else 'INCONSISTENT'}")
    print(f"    Latest commit: {report['stats'].get('latest_commit', 'N/A')}")
    print(f"    Issues: {len(report['issues'])}\n")

    # 2. Pull vault
    print("2. Pulling vault changes...")
    success, msg = manager.pull_vault("local")
    print(f"[{'OK' if success else 'FAIL'}] {msg}\n")

    # 3. Push vault
    print("3. Pushing vault changes...")
    success, msg = manager.push_vault("local", "Demo: Platinum Tier Phase 1 - Vault Restructuring")
    print(f"[{'OK' if success else 'FAIL'}] {msg}\n")

    # 4. Full sync
    print("4. Full sync (pull + push)...")
    success, msg = manager.sync_vault("local", "Demo: Full vault sync")
    print(f"[{'OK' if success else 'FAIL'}] {msg}\n")

    print("[OK] Git sync manager demo completed!")


if __name__ == "__main__":
    main()
