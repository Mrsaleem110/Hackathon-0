#!/usr/bin/env python3
"""
Vault Consistency Checker - Detects and reports vault inconsistencies
Identifies orphaned tasks, stale tasks, sync conflicts, and other issues
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VaultConsistencyChecker:
    """Checks vault for consistency issues"""

    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / "Needs_Action"
        self.in_progress = self.vault_path / "In_Progress"
        self.pending_approval = self.vault_path / "Pending_Approval"
        self.approved = self.vault_path / "Approved"
        self.done = self.vault_path / "Done"
        self.logs_dir = self.vault_path / "Logs"

        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def check_all(self) -> Dict:
        """
        Run all consistency checks

        Returns:
            Dictionary with all check results
        """
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "is_consistent": True,
            "issues": [],
            "warnings": [],
            "stats": {},
        }

        # Run all checks
        logger.info("Running vault consistency checks...")

        # 1. Check for orphaned tasks
        orphaned = self.check_orphaned_tasks()
        if orphaned:
            report["issues"].extend(orphaned)
            report["is_consistent"] = False

        # 2. Check for stale tasks
        stale = self.check_stale_tasks()
        if stale:
            report["warnings"].extend(stale)

        # 3. Check for sync conflicts
        conflicts = self.check_sync_conflicts()
        if conflicts:
            report["issues"].extend(conflicts)
            report["is_consistent"] = False

        # 4. Check for duplicate tasks
        duplicates = self.check_duplicate_tasks()
        if duplicates:
            report["warnings"].extend(duplicates)

        # 5. Check directory structure
        structure_issues = self.check_directory_structure()
        if structure_issues:
            report["warnings"].extend(structure_issues)

        # 6. Collect statistics
        report["stats"] = self.collect_statistics()

        # Log report
        self._log_report(report)

        return report

    def check_orphaned_tasks(self) -> List[str]:
        """
        Check for orphaned tasks (in multiple states simultaneously)

        Returns:
            List of issue descriptions
        """
        issues = []

        try:
            # Check each domain
            for domain in ["email", "social", "whatsapp", "payments"]:
                needs_action_dir = self.needs_action / domain
                if not needs_action_dir.exists():
                    continue

                for task_file in needs_action_dir.glob("*.md"):
                    task_name = task_file.name

                    # Check if also in In_Progress
                    for agent in ["cloud", "local"]:
                        if (self.in_progress / agent / task_name).exists():
                            issue = f"ORPHANED: {task_name} in both Needs_Action/{domain} and In_Progress/{agent}"
                            issues.append(issue)
                            logger.warning(issue)

                    # Check if also in Pending_Approval
                    if (self.pending_approval / domain / task_name).exists():
                        issue = f"ORPHANED: {task_name} in both Needs_Action/{domain} and Pending_Approval/{domain}"
                        issues.append(issue)
                        logger.warning(issue)

            # Check In_Progress for multiple agents
            for task_file in self.in_progress.glob("*/*.md"):
                task_name = task_file.name
                agents_with_task = []

                for agent in ["cloud", "local"]:
                    if (self.in_progress / agent / task_name).exists():
                        agents_with_task.append(agent)

                if len(agents_with_task) > 1:
                    issue = f"ORPHANED: {task_name} claimed by multiple agents: {agents_with_task}"
                    issues.append(issue)
                    logger.warning(issue)

        except Exception as e:
            logger.error(f"Error checking orphaned tasks: {e}")

        return issues

    def check_stale_tasks(self, stale_hours: int = 24) -> List[str]:
        """
        Check for stale tasks (not updated in specified hours)

        Args:
            stale_hours: Hours before task is considered stale

        Returns:
            List of warning descriptions
        """
        warnings = []
        stale_threshold = datetime.utcnow() - timedelta(hours=stale_hours)

        try:
            # Check In_Progress tasks
            for task_file in self.in_progress.glob("*/*.md"):
                try:
                    stat = task_file.stat()
                    mtime = datetime.fromtimestamp(stat.st_mtime)

                    if mtime < stale_threshold:
                        warning = f"STALE: {task_file.name} in In_Progress for {stale_hours}+ hours"
                        warnings.append(warning)
                        logger.warning(warning)
                except Exception as e:
                    logger.error(f"Error checking file {task_file}: {e}")

            # Check Pending_Approval tasks
            for task_file in self.pending_approval.glob("*/*.md"):
                try:
                    stat = task_file.stat()
                    mtime = datetime.fromtimestamp(stat.st_mtime)

                    if mtime < stale_threshold:
                        warning = f"STALE: {task_file.name} in Pending_Approval for {stale_hours}+ hours"
                        warnings.append(warning)
                        logger.warning(warning)
                except Exception as e:
                    logger.error(f"Error checking file {task_file}: {e}")

        except Exception as e:
            logger.error(f"Error checking stale tasks: {e}")

        return warnings

    def check_sync_conflicts(self) -> List[str]:
        """
        Check for git merge conflicts

        Returns:
            List of issue descriptions
        """
        issues = []

        try:
            # Look for conflict markers in markdown files
            for md_file in self.vault_path.glob("**/*.md"):
                try:
                    with open(md_file, "r") as f:
                        content = f.read()

                    if "<<<<<<< HEAD" in content or "=======" in content or ">>>>>>>" in content:
                        issue = f"CONFLICT: Merge conflict markers found in {md_file.relative_to(self.vault_path)}"
                        issues.append(issue)
                        logger.warning(issue)
                except Exception as e:
                    logger.error(f"Error checking file {md_file}: {e}")

        except Exception as e:
            logger.error(f"Error checking sync conflicts: {e}")

        return issues

    def check_duplicate_tasks(self) -> List[str]:
        """
        Check for duplicate tasks (same task in multiple places)

        Returns:
            List of warning descriptions
        """
        warnings = []
        task_locations = {}

        try:
            # Collect all task files
            for task_file in self.vault_path.glob("**/*.md"):
                if task_file.name.startswith("."):
                    continue

                task_name = task_file.name
                if task_name not in task_locations:
                    task_locations[task_name] = []

                task_locations[task_name].append(str(task_file.relative_to(self.vault_path)))

            # Find duplicates
            for task_name, locations in task_locations.items():
                if len(locations) > 1:
                    # Exclude expected duplicates (e.g., COMPLETED_ prefix)
                    if not task_name.startswith("COMPLETED_"):
                        warning = f"DUPLICATE: {task_name} found in {len(locations)} locations"
                        warnings.append(warning)
                        logger.warning(warning)

        except Exception as e:
            logger.error(f"Error checking duplicate tasks: {e}")

        return warnings

    def check_directory_structure(self) -> List[str]:
        """
        Check for missing required directories

        Returns:
            List of warning descriptions
        """
        warnings = []
        required_dirs = [
            "Needs_Action/email",
            "Needs_Action/social",
            "Needs_Action/whatsapp",
            "Needs_Action/payments",
            "Plans/email",
            "Plans/social",
            "Plans/whatsapp",
            "Plans/payments",
            "In_Progress/cloud",
            "In_Progress/local",
            "Pending_Approval/email",
            "Pending_Approval/social",
            "Pending_Approval/payments",
            "Approved",
            "Done",
            "Updates",
        ]

        try:
            for dir_path in required_dirs:
                full_path = self.vault_path / dir_path
                if not full_path.exists():
                    warning = f"MISSING: Required directory {dir_path} not found"
                    warnings.append(warning)
                    logger.warning(warning)

        except Exception as e:
            logger.error(f"Error checking directory structure: {e}")

        return warnings

    def collect_statistics(self) -> Dict:
        """
        Collect vault statistics

        Returns:
            Dictionary with statistics
        """
        stats = {
            "total_tasks": 0,
            "needs_action": {},
            "in_progress": {},
            "pending_approval": {},
            "approved": 0,
            "done": 0,
        }

        try:
            # Count Needs_Action tasks
            for domain in ["email", "social", "whatsapp", "payments"]:
                domain_dir = self.needs_action / domain
                if domain_dir.exists():
                    count = len(list(domain_dir.glob("*.md")))
                    stats["needs_action"][domain] = count
                    stats["total_tasks"] += count

            # Count In_Progress tasks
            for agent in ["cloud", "local"]:
                agent_dir = self.in_progress / agent
                if agent_dir.exists():
                    count = len(list(agent_dir.glob("*.md")))
                    stats["in_progress"][agent] = count
                    stats["total_tasks"] += count

            # Count Pending_Approval tasks
            for domain in ["email", "social", "payments"]:
                domain_dir = self.pending_approval / domain
                if domain_dir.exists():
                    count = len(list(domain_dir.glob("*.md")))
                    stats["pending_approval"][domain] = count
                    stats["total_tasks"] += count

            # Count Approved tasks
            if self.approved.exists():
                stats["approved"] = len(list(self.approved.glob("*.md")))
                stats["total_tasks"] += stats["approved"]

            # Count Done tasks
            if self.done.exists():
                stats["done"] = len(list(self.done.glob("*.md")))

        except Exception as e:
            logger.error(f"Error collecting statistics: {e}")

        return stats

    def _log_report(self, report: Dict):
        """Log consistency report"""
        try:
            today = datetime.utcnow().strftime("%Y-%m-%d")
            log_file = self.logs_dir / f"consistency_{today}.json"

            logs = []
            if log_file.exists():
                with open(log_file, "r") as f:
                    logs = json.load(f)

            logs.append(report)

            with open(log_file, "w") as f:
                json.dump(logs, f, indent=2)

            logger.info(f"Consistency report logged to {log_file}")
        except Exception as e:
            logger.error(f"Failed to log consistency report: {e}")

    def generate_report(self) -> str:
        """
        Generate human-readable consistency report

        Returns:
            Formatted report string
        """
        report = self.check_all()

        output = []
        output.append("=" * 70)
        output.append("VAULT CONSISTENCY REPORT")
        output.append("=" * 70)
        output.append(f"Timestamp: {report['timestamp']}")
        output.append(f"Status: {'CONSISTENT' if report['is_consistent'] else 'INCONSISTENT'}")
        output.append("")

        if report["issues"]:
            output.append("ISSUES (Critical):")
            for issue in report["issues"]:
                output.append(f"  - {issue}")
            output.append("")

        if report["warnings"]:
            output.append("WARNINGS:")
            for warning in report["warnings"]:
                output.append(f"  - {warning}")
            output.append("")

        output.append("STATISTICS:")
        stats = report["stats"]
        output.append(f"  Total Tasks: {stats['total_tasks']}")
        output.append(f"  Needs Action: {sum(stats['needs_action'].values())}")
        for domain, count in stats["needs_action"].items():
            output.append(f"    - {domain}: {count}")
        output.append(f"  In Progress: {sum(stats['in_progress'].values())}")
        for agent, count in stats["in_progress"].items():
            output.append(f"    - {agent}: {count}")
        output.append(f"  Pending Approval: {sum(stats['pending_approval'].values())}")
        for domain, count in stats["pending_approval"].items():
            output.append(f"    - {domain}: {count}")
        output.append(f"  Approved: {stats['approved']}")
        output.append(f"  Done: {stats['done']}")
        output.append("")
        output.append("=" * 70)

        return "\n".join(output)


def main():
    """Demo of vault consistency checker"""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    checker = VaultConsistencyChecker()

    print("Vault Consistency Checker Demo\n")

    # Run all checks
    print("Running consistency checks...\n")
    report = checker.check_all()

    # Display report
    print(checker.generate_report())

    # Show detailed results
    print("\nDetailed Results:")
    print(f"  Issues: {len(report['issues'])}")
    print(f"  Warnings: {len(report['warnings'])}")
    print(f"  Total Tasks: {report['stats']['total_tasks']}")

    print("\n[OK] Vault consistency checker demo completed!")


if __name__ == "__main__":
    main()
