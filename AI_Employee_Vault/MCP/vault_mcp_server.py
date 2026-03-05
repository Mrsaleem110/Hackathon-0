"""
Vault MCP Server for AI Employee Vault
Implements Model Context Protocol for vault operations
Allows Claude Code to manage vault files and workflows
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict

class VaultMCPServer:
    """MCP Server for vault operations"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.plans = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'

        # Create directories
        for folder in [self.needs_action, self.plans, self.pending_approval, self.done, self.logs]:
            folder.mkdir(exist_ok=True)

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def list_tasks(self, folder: str = 'needs_action') -> dict:
        """List tasks in a specific folder"""
        folder_map = {
            'needs_action': self.needs_action,
            'plans': self.plans,
            'pending_approval': self.pending_approval,
            'done': self.done
        }

        target_folder = folder_map.get(folder.lower())
        if not target_folder:
            return {
                'success': False,
                'message': f'Unknown folder: {folder}'
            }

        try:
            files = list(target_folder.glob('*.md'))
            tasks = []

            for file in files:
                tasks.append({
                    'name': file.name,
                    'path': str(file),
                    'created': datetime.fromtimestamp(file.stat().st_ctime).isoformat(),
                    'modified': datetime.fromtimestamp(file.stat().st_mtime).isoformat(),
                    'size': file.stat().st_size
                })

            return {
                'success': True,
                'folder': folder,
                'count': len(tasks),
                'tasks': tasks
            }

        except Exception as e:
            self.logger.error(f"Error listing tasks: {e}")
            return {
                'success': False,
                'message': f'Error listing tasks: {str(e)}'
            }

    def read_task(self, filename: str, folder: str = 'needs_action') -> dict:
        """Read a specific task file"""
        folder_map = {
            'needs_action': self.needs_action,
            'plans': self.plans,
            'pending_approval': self.pending_approval,
            'done': self.done
        }

        target_folder = folder_map.get(folder.lower())
        if not target_folder:
            return {
                'success': False,
                'message': f'Unknown folder: {folder}'
            }

        try:
            file_path = target_folder / filename
            if not file_path.exists():
                return {
                    'success': False,
                    'message': f'File not found: {filename}'
                }

            content = file_path.read_text(encoding='utf-8')
            return {
                'success': True,
                'filename': filename,
                'folder': folder,
                'content': content,
                'path': str(file_path)
            }

        except Exception as e:
            self.logger.error(f"Error reading task: {e}")
            return {
                'success': False,
                'message': f'Error reading task: {str(e)}'
            }

    def create_task(self, filename: str, content: str, folder: str = 'needs_action') -> dict:
        """Create a new task file"""
        folder_map = {
            'needs_action': self.needs_action,
            'plans': self.plans,
            'pending_approval': self.pending_approval,
            'done': self.done
        }

        target_folder = folder_map.get(folder.lower())
        if not target_folder:
            return {
                'success': False,
                'message': f'Unknown folder: {folder}'
            }

        try:
            file_path = target_folder / filename
            file_path.write_text(content, encoding='utf-8')
            self.logger.info(f"Task created: {filename}")

            return {
                'success': True,
                'message': f'Task created: {filename}',
                'path': str(file_path),
                'folder': folder
            }

        except Exception as e:
            self.logger.error(f"Error creating task: {e}")
            return {
                'success': False,
                'message': f'Error creating task: {str(e)}'
            }

    def move_task(self, filename: str, from_folder: str, to_folder: str) -> dict:
        """Move a task between folders"""
        folder_map = {
            'needs_action': self.needs_action,
            'plans': self.plans,
            'pending_approval': self.pending_approval,
            'done': self.done
        }

        from_path = folder_map.get(from_folder.lower())
        to_path = folder_map.get(to_folder.lower())

        if not from_path or not to_path:
            return {
                'success': False,
                'message': f'Invalid folder: {from_folder} or {to_folder}'
            }

        try:
            source = from_path / filename
            dest = to_path / filename

            if not source.exists():
                return {
                    'success': False,
                    'message': f'File not found: {filename}'
                }

            source.rename(dest)
            self.logger.info(f"Task moved: {filename} from {from_folder} to {to_folder}")

            return {
                'success': True,
                'message': f'Task moved: {filename}',
                'from': from_folder,
                'to': to_folder,
                'path': str(dest)
            }

        except Exception as e:
            self.logger.error(f"Error moving task: {e}")
            return {
                'success': False,
                'message': f'Error moving task: {str(e)}'
            }

    def get_vault_stats(self) -> dict:
        """Get vault statistics"""
        try:
            stats = {
                'needs_action': len(list(self.needs_action.glob('*.md'))),
                'plans': len(list(self.plans.glob('*.md'))),
                'pending_approval': len(list(self.pending_approval.glob('*.md'))),
                'done': len(list(self.done.glob('*.md'))),
                'logs': len(list(self.logs.glob('*.json')))
            }

            total = sum(stats.values())

            return {
                'success': True,
                'stats': stats,
                'total': total,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error getting stats: {e}")
            return {
                'success': False,
                'message': f'Error getting stats: {str(e)}'
            }

    def handle_mcp_request(self, request: dict) -> dict:
        """Handle MCP protocol requests"""
        method = request.get('method')
        params = request.get('params', {})

        if method == 'list_tasks':
            return self.list_tasks(folder=params.get('folder', 'needs_action'))

        elif method == 'read_task':
            return self.read_task(
                filename=params.get('filename'),
                folder=params.get('folder', 'needs_action')
            )

        elif method == 'create_task':
            return self.create_task(
                filename=params.get('filename'),
                content=params.get('content'),
                folder=params.get('folder', 'needs_action')
            )

        elif method == 'move_task':
            return self.move_task(
                filename=params.get('filename'),
                from_folder=params.get('from_folder'),
                to_folder=params.get('to_folder')
            )

        elif method == 'get_vault_stats':
            return self.get_vault_stats()

        else:
            return {
                'success': False,
                'message': f'Unknown method: {method}'
            }

    def demo_run(self):
        """Demo run showing vault capabilities"""
        self.logger.info("Running Vault MCP Server in demo mode")

        # Get stats
        stats = self.get_vault_stats()
        self.logger.info(f"Vault stats: {stats}")

        # List tasks
        tasks = self.list_tasks('needs_action')
        self.logger.info(f"Tasks in needs_action: {tasks}")


# MCP Server Interface
class MCPVaultServer:
    """MCP Server wrapper for Vault operations"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.vault_server = VaultMCPServer(vault_path)
        self.logger = logging.getLogger(__name__)

    def process_request(self, request: dict) -> dict:
        """Process incoming MCP request"""
        return self.vault_server.handle_mcp_request(request)

    def get_capabilities(self) -> dict:
        """Return MCP server capabilities"""
        return {
            'service': 'vault',
            'methods': [
                'list_tasks',
                'read_task',
                'create_task',
                'move_task',
                'get_vault_stats'
            ],
            'description': 'Vault management operations'
        }


if __name__ == "__main__":
    # Initialize the MCP server
    VAULT_PATH = Path(".")

    server = MCPVaultServer(vault_path=VAULT_PATH)

    # Show capabilities
    print("Vault MCP Server Capabilities:")
    print(json.dumps(server.get_capabilities(), indent=2))

    # Run demo
    vault_server = VaultMCPServer(vault_path=VAULT_PATH)
    vault_server.demo_run()

    print(f"\nVault MCP Server setup complete!")
