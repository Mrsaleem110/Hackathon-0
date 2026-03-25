"""Vault Client - Obsidian vault wrapper for Vault MCP Server"""

import os
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VaultClient:
    """Obsidian vault client for task management"""

    def __init__(self, vault_path: str = '.'):
        """Initialize vault client"""
        self.vault_path = Path(vault_path)
        self.needs_action_path = self.vault_path / 'Needs_Action'
        self.plans_path = self.vault_path / 'Plans'
        self.pending_approval_path = self.vault_path / 'Pending_Approval'
        self.done_path = self.vault_path / 'Done'

        # Create directories if they don't exist
        for path in [self.needs_action_path, self.plans_path, self.pending_approval_path, self.done_path]:
            path.mkdir(exist_ok=True)

        logger.info(f"Vault client initialized at {self.vault_path}")

    def create_task(self, title: str, description: str, folder: str = 'Needs_Action') -> Dict[str, Any]:
        """Create a new task"""
        try:
            folder_path = self.vault_path / folder
            folder_path.mkdir(exist_ok=True)

            # Create filename from title
            filename = f"{title.replace(' ', '_')}.md"
            file_path = folder_path / filename

            # Create task content
            content = f"""---
title: {title}
created: {datetime.now().isoformat()}
status: pending
---

# {title}

## Description
{description}

## Status
- [ ] Not Started
- [ ] In Progress
- [ ] Completed

## Notes
"""

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Task created: {file_path}")
            return {
                'success': True,
                'task_id': filename,
                'path': str(file_path),
                'title': title
            }

        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            return {'success': False, 'error': str(e)}

    def list_tasks(self, folder: str = 'Needs_Action', status: Optional[str] = None) -> Dict[str, Any]:
        """List tasks in folder"""
        try:
            folder_path = self.vault_path / folder

            if not folder_path.exists():
                return {'success': True, 'tasks': [], 'count': 0}

            tasks = []
            for file_path in folder_path.glob('*.md'):
                task_data = self._parse_task_file(file_path)
                if status is None or task_data.get('status') == status:
                    tasks.append(task_data)

            logger.info(f"Listed {len(tasks)} tasks from {folder}")
            return {'success': True, 'tasks': tasks, 'count': len(tasks)}

        except Exception as e:
            logger.error(f"Failed to list tasks: {e}")
            return {'success': False, 'error': str(e)}

    def update_task(self, task_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update task"""
        try:
            # Find task file
            task_file = None
            for folder in [self.needs_action_path, self.plans_path, self.pending_approval_path, self.done_path]:
                potential_file = folder / task_id
                if potential_file.exists():
                    task_file = potential_file
                    break

            if not task_file:
                return {'success': False, 'error': f'Task not found: {task_id}'}

            # Read current content
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update status if provided
            if 'status' in updates:
                content = content.replace(
                    f"status: {self._extract_status(content)}",
                    f"status: {updates['status']}"
                )

            # Update modified timestamp
            content = content.replace(
                'modified:',
                f'modified: {datetime.now().isoformat()}'
            )

            # Write updated content
            with open(task_file, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Task updated: {task_id}")
            return {'success': True, 'task_id': task_id}

        except Exception as e:
            logger.error(f"Failed to update task: {e}")
            return {'success': False, 'error': str(e)}

    def move_task(self, task_id: str, from_folder: str, to_folder: str) -> Dict[str, Any]:
        """Move task between folders"""
        try:
            from_path = self.vault_path / from_folder / task_id
            to_path = self.vault_path / to_folder / task_id

            if not from_path.exists():
                return {'success': False, 'error': f'Task not found: {from_path}'}

            # Create destination folder if needed
            to_path.parent.mkdir(exist_ok=True)

            # Move file
            from_path.rename(to_path)

            logger.info(f"Task moved: {task_id} from {from_folder} to {to_folder}")
            return {'success': True, 'task_id': task_id, 'new_path': str(to_path)}

        except Exception as e:
            logger.error(f"Failed to move task: {e}")
            return {'success': False, 'error': str(e)}

    def get_vault_stats(self) -> Dict[str, Any]:
        """Get vault statistics"""
        try:
            stats = {
                'needs_action': len(list(self.needs_action_path.glob('*.md'))),
                'plans': len(list(self.plans_path.glob('*.md'))),
                'pending_approval': len(list(self.pending_approval_path.glob('*.md'))),
                'done': len(list(self.done_path.glob('*.md'))),
            }

            stats['total'] = sum(stats.values())

            logger.info(f"Vault stats: {stats}")
            return {'success': True, 'stats': stats}

        except Exception as e:
            logger.error(f"Failed to get vault stats: {e}")
            return {'success': False, 'error': str(e)}

    def _parse_task_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse task file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract frontmatter
            lines = content.split('\n')
            title = file_path.stem
            status = 'pending'

            for line in lines:
                if line.startswith('title:'):
                    title = line.replace('title:', '').strip()
                elif line.startswith('status:'):
                    status = line.replace('status:', '').strip()

            return {
                'id': file_path.name,
                'title': title,
                'status': status,
                'path': str(file_path),
                'created': file_path.stat().st_ctime
            }

        except Exception as e:
            logger.error(f"Failed to parse task file: {e}")
            return {'id': file_path.name, 'error': str(e)}

    def _extract_status(self, content: str) -> str:
        """Extract status from content"""
        for line in content.split('\n'):
            if line.startswith('status:'):
                return line.replace('status:', '').strip()
        return 'pending'
