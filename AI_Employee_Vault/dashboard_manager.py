#!/usr/bin/env python3
"""
Dashboard Manager - Implements single-writer pattern for Dashboard.md
Local agent only writes to Dashboard.md
Cloud agent writes signals to Updates/ folder
Local agent periodically merges Updates/ into Dashboard.md
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DashboardManager:
    """Manages Dashboard.md with single-writer pattern"""

    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path)
        self.dashboard_file = self.vault_path / "Dashboard.md"
        self.updates_dir = self.vault_path / "Updates"
        self.logs_dir = self.vault_path / "Logs"

        # Create directories if they don't exist
        self.updates_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Initialize dashboard if it doesn't exist
        if not self.dashboard_file.exists():
            self._initialize_dashboard()

    def _initialize_dashboard(self):
        """Initialize Dashboard.md with header"""
        content = """# AI Employee Vault - Dashboard

**Last Updated**: {timestamp}
**Status**: OPERATIONAL

## System Status
- Cloud Agent: INITIALIZING
- Local Agent: INITIALIZING
- Vault Sync: INITIALIZING

## Recent Activity
(No activity yet)

## Cloud Signals
(No signals yet)

## Metrics
- Tasks Completed: 0
- Tasks Pending: 0
- Tasks In Progress: 0
- Approval Rate: 0%

---

*This dashboard is managed by the Dashboard Manager. Local agent only.*
""".format(timestamp=datetime.utcnow().isoformat())

        with open(self.dashboard_file, "w") as f:
            f.write(content)

        logger.info("Dashboard initialized")

    def write_signal(self, agent: str, signal_type: str, content: Dict) -> bool:
        """
        Write a signal from cloud agent to Updates/ folder
        Local agent will merge these into Dashboard.md

        Args:
            agent: Agent writing the signal (should be 'cloud')
            signal_type: Type of signal (status, metric, alert, etc.)
            content: Signal content as dict

        Returns:
            True if successfully written
        """
        if agent != "cloud":
            logger.warning(f"Only cloud agent can write signals, got: {agent}")
            return False

        timestamp = datetime.utcnow().isoformat()
        filename = f"signal_{signal_type}_{timestamp.replace(':', '-')}.json"
        signal_file = self.updates_dir / filename

        try:
            signal_data = {
                "timestamp": timestamp,
                "agent": agent,
                "type": signal_type,
                "content": content,
            }

            with open(signal_file, "w") as f:
                json.dump(signal_data, f, indent=2)

            logger.info(f"Signal written: {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to write signal: {e}")
            return False

    def merge_signals(self) -> bool:
        """
        Merge all signals from Updates/ into Dashboard.md
        Only Local agent should call this

        Returns:
            True if successfully merged
        """
        try:
            # Read current dashboard
            with open(self.dashboard_file, "r") as f:
                dashboard_content = f.read()

            # Collect all signals
            signals = []
            signal_files = sorted(self.updates_dir.glob("signal_*.json"))

            for signal_file in signal_files:
                try:
                    with open(signal_file, "r") as f:
                        signal = json.load(f)
                    signals.append(signal)
                except Exception as e:
                    logger.error(f"Failed to read signal: {signal_file}: {e}")

            if not signals:
                logger.info("No signals to merge")
                return True

            # Process signals
            status_updates = []
            metric_updates = []
            alerts = []
            activity_log = []

            for signal in signals:
                signal_type = signal.get("type", "unknown")
                content = signal.get("content", {})
                timestamp = signal.get("timestamp", "")

                if signal_type == "status":
                    status_updates.append(
                        f"- {content.get('component', 'Unknown')}: {content.get('status', 'UNKNOWN')} ({timestamp})"
                    )
                elif signal_type == "metric":
                    metric_updates.append(
                        f"- {content.get('name', 'Unknown')}: {content.get('value', 'N/A')}"
                    )
                elif signal_type == "alert":
                    alerts.append(
                        f"- **{content.get('level', 'INFO')}**: {content.get('message', 'No message')} ({timestamp})"
                    )
                elif signal_type == "activity":
                    activity_log.append(
                        f"- {content.get('action', 'Unknown')}: {content.get('description', '')} ({timestamp})"
                    )

            # Update dashboard sections
            updated_content = dashboard_content

            # Update Last Updated timestamp
            updated_content = updated_content.replace(
                f"**Last Updated**: {self._extract_timestamp(dashboard_content)}",
                f"**Last Updated**: {datetime.utcnow().isoformat()}",
            )

            # Update Recent Activity
            if activity_log:
                activity_section = "## Recent Activity\n" + "\n".join(activity_log[-10:])
                updated_content = self._replace_section(
                    updated_content, "## Recent Activity", activity_section
                )

            # Update Cloud Signals
            if status_updates or metric_updates or alerts:
                signals_section = "## Cloud Signals\n"
                if status_updates:
                    signals_section += "\n### Status Updates\n" + "\n".join(
                        status_updates
                    )
                if metric_updates:
                    signals_section += "\n\n### Metrics\n" + "\n".join(metric_updates)
                if alerts:
                    signals_section += "\n\n### Alerts\n" + "\n".join(alerts)

                updated_content = self._replace_section(
                    updated_content, "## Cloud Signals", signals_section
                )

            # Write updated dashboard
            with open(self.dashboard_file, "w") as f:
                f.write(updated_content)

            logger.info(f"Merged {len(signals)} signals into dashboard")

            # Archive processed signals
            for signal_file in signal_files:
                archive_dir = self.updates_dir / "archived"
                archive_dir.mkdir(exist_ok=True)
                signal_file.rename(archive_dir / signal_file.name)

            return True
        except Exception as e:
            logger.error(f"Failed to merge signals: {e}")
            return False

    def update_status(self, component: str, status: str) -> bool:
        """
        Update component status in dashboard (Local only)

        Args:
            component: Component name (Cloud Agent, Local Agent, Vault Sync, etc.)
            status: Status (OPERATIONAL, DEGRADED, DOWN, etc.)

        Returns:
            True if successfully updated
        """
        try:
            with open(self.dashboard_file, "r") as f:
                content = f.read()

            # Find and update status line
            status_line = f"- {component}: {status}"

            # If component exists, replace it
            lines = content.split("\n")
            updated_lines = []
            found = False

            for line in lines:
                if line.startswith(f"- {component}:"):
                    updated_lines.append(status_line)
                    found = True
                else:
                    updated_lines.append(line)

            # If not found, add it
            if not found:
                # Find System Status section and add after it
                for i, line in enumerate(updated_lines):
                    if line == "## System Status":
                        updated_lines.insert(i + 1, status_line)
                        break

            updated_content = "\n".join(updated_lines)

            # Update timestamp
            updated_content = updated_content.replace(
                f"**Last Updated**: {self._extract_timestamp(content)}",
                f"**Last Updated**: {datetime.utcnow().isoformat()}",
            )

            with open(self.dashboard_file, "w") as f:
                f.write(updated_content)

            logger.info(f"Updated status: {component} = {status}")
            return True
        except Exception as e:
            logger.error(f"Failed to update status: {e}")
            return False

    def add_activity(self, action: str, description: str) -> bool:
        """
        Add activity to dashboard (Local only)

        Args:
            action: Action name
            description: Action description

        Returns:
            True if successfully added
        """
        try:
            with open(self.dashboard_file, "r") as f:
                content = f.read()

            activity_entry = f"- {action}: {description} ({datetime.utcnow().isoformat()})"

            # Find Recent Activity section and add entry
            lines = content.split("\n")
            updated_lines = []

            for i, line in enumerate(lines):
                updated_lines.append(line)
                if line == "## Recent Activity":
                    # Add new activity after section header
                    if i + 1 < len(lines) and lines[i + 1].startswith("(No activity"):
                        updated_lines[i + 1] = activity_entry
                    else:
                        updated_lines.insert(i + 1, activity_entry)
                    break

            updated_content = "\n".join(updated_lines)

            # Update timestamp
            updated_content = updated_content.replace(
                f"**Last Updated**: {self._extract_timestamp(content)}",
                f"**Last Updated**: {datetime.utcnow().isoformat()}",
            )

            with open(self.dashboard_file, "w") as f:
                f.write(updated_content)

            logger.info(f"Added activity: {action}")
            return True
        except Exception as e:
            logger.error(f"Failed to add activity: {e}")
            return False

    def get_dashboard_content(self) -> str:
        """Get current dashboard content"""
        try:
            with open(self.dashboard_file, "r") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read dashboard: {e}")
            return ""

    def _extract_timestamp(self, content: str) -> str:
        """Extract timestamp from dashboard content"""
        for line in content.split("\n"):
            if "**Last Updated**:" in line:
                return line.split("**Last Updated**: ")[1].strip()
        return ""

    def _replace_section(self, content: str, section_header: str, new_section: str) -> str:
        """Replace a section in the dashboard"""
        lines = content.split("\n")
        updated_lines = []
        in_section = False
        section_start = -1

        for i, line in enumerate(lines):
            if line == section_header:
                in_section = True
                section_start = i
                updated_lines.append(new_section)
            elif in_section and line.startswith("##"):
                # Found next section, stop replacing
                in_section = False
                updated_lines.append(line)
            elif not in_section:
                updated_lines.append(line)

        return "\n".join(updated_lines)


def main():
    """Demo of dashboard manager"""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    manager = DashboardManager()

    print("Dashboard Manager Demo\n")

    # 1. Update status
    print("1. Updating component status...")
    manager.update_status("Cloud Agent", "OPERATIONAL")
    manager.update_status("Local Agent", "OPERATIONAL")
    manager.update_status("Vault Sync", "OPERATIONAL")
    print("[OK] Status updated\n")

    # 2. Add activity
    print("2. Adding activity...")
    manager.add_activity("Email Received", "From: test@example.com")
    manager.add_activity("Task Claimed", "Cloud agent claimed email task")
    manager.add_activity("Draft Created", "Email reply drafted")
    print("[OK] Activity added\n")

    # 3. Write signals from cloud
    print("3. Writing signals from cloud agent...")
    manager.write_signal("cloud", "status", {"component": "Gmail Watcher", "status": "HEALTHY"})
    manager.write_signal("cloud", "metric", {"name": "Emails Processed", "value": 5})
    manager.write_signal("cloud", "alert", {"level": "INFO", "message": "Vault sync completed"})
    print("[OK] Signals written\n")

    # 4. Merge signals
    print("4. Merging signals into dashboard...")
    manager.merge_signals()
    print("[OK] Signals merged\n")

    # 5. Display dashboard
    print("5. Current dashboard content:\n")
    print(manager.get_dashboard_content())


if __name__ == "__main__":
    main()
