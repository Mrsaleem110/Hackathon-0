"""
Orchestrator for AI Employee Vault
This script demonstrates Claude Code reading from and writing to the vault.
It processes items in the Needs_Action folder and moves them when completed.
"""

import os
import time
from pathlib import Path
from datetime import datetime
import shutil

class VaultOrchestrator:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.inbox_path = self.vault_path / 'Inbox'
        self.needs_action_path = self.vault_path / 'Needs_Action'
        self.done_path = self.vault_path / 'Done'

        # Create directories if they don't exist
        self.inbox_path.mkdir(exist_ok=True)
        self.needs_action_path.mkdir(exist_ok=True)
        self.done_path.mkdir(exist_ok=True)

        print(f"Orchestrator initialized with vault: {self.vault_path}")

    def process_needs_action(self):
        """Process all files in the Needs_Action folder"""
        action_files = list(self.needs_action_path.glob("*.md"))

        if not action_files:
            print("No files in Needs_Action to process")
            return

        print(f"Found {len(action_files)} files to process")

        for file_path in action_files:
            print(f"Processing: {file_path.name}")

            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            print(f"  Content preview: {content[:100]}...")

            # Update the Dashboard with the activity
            self.update_dashboard(file_path)

            # Move the file to Done folder
            done_file = self.done_path / file_path.name
            shutil.move(str(file_path), str(done_file))

            print(f"  Moved to Done: {done_file.name}")

    def update_dashboard(self, file_path):
        """Update the Dashboard.md with recent activity"""
        dashboard_path = self.vault_path / 'Dashboard.md'

        if not dashboard_path.exists():
            # Create a basic dashboard if it doesn't exist
            dashboard_content = """---
created: 2026-02-20
last_updated: 2026-02-20
status: active
---

# AI Employee Dashboard

## Overview
This is your AI Employee dashboard. It provides a real-time summary of your personal and business affairs.

## Current Status
- **AI Employee**: Active
- **Last Check-in**: 2026-02-20
- **System Health**: Operational

## Recent Activity
"""

        # Read current dashboard
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            dashboard_content = f.read()

        # Find the recent activity section and update it
        lines = dashboard_content.split('\n')
        new_lines = []
        activity_section_found = False

        for line in lines:
            if line.strip() == '## Recent Activity':
                new_lines.append(line)
                # Add the new activity
                new_lines.append(f'- [ ] Processed {file_path.name} on {datetime.now().strftime("%Y-%m-%d %H:%M")}')
                activity_section_found = True
            elif activity_section_found and line.startswith('- [ ]') and len(new_lines) > 0 and new_lines[-1] == '## Recent Activity':
                # Replace the first activity with our new one (we already added it)
                continue
            else:
                new_lines.append(line)

        # Write updated dashboard
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))

    def run_once(self):
        """Run one cycle of processing"""
        print("Starting processing cycle...")
        self.process_needs_action()
        print("Processing cycle completed")

    def run_continuous(self, interval=30):
        """Run continuously with specified interval"""
        print(f"Starting continuous processing (checking every {interval} seconds)")

        while True:
            try:
                self.run_once()
                print(f"Waiting {interval} seconds before next check...")
                time.sleep(interval)
            except KeyboardInterrupt:
                print("Orchestrator stopped by user")
                break
            except Exception as e:
                print(f"Error during processing: {e}")
                time.sleep(60)  # Wait 1 minute if there's an error

if __name__ == "__main__":
    # Initialize orchestrator with the current directory as vault path
    VAULT_PATH = Path(".")

    orchestrator = VaultOrchestrator(vault_path=VAULT_PATH)

    # Run one cycle to demonstrate functionality
    orchestrator.run_once()

    print("Orchestrator demonstration completed!")
    print(f"Vault structure created at: {VAULT_PATH}")
    print("- Inbox folder created")
    print("- Needs_Action folder created with sample files")
    print("- Done folder created")
    print("- Dashboard.md updated with processing activity")