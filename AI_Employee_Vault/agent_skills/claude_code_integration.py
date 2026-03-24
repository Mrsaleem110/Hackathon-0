"""
Claude Code Integration - Bridge between skills and Claude Code Agent SDK
"""

from typing import Dict, Any, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from __init__ import get_registry
from loader import SkillLoader


class ClaudeCodeBridge:
    """Bridge between skills and Claude Code"""

    def __init__(self):
        """Initialize Claude Code bridge"""
        SkillLoader.load_all_skills()
        self.registry = get_registry()

    def get_available_commands(self) -> Dict[str, Any]:
        """Get available commands for Claude Code"""
        manifest = self.registry.get_skill_manifest()
        return {
            'commands': [
                {
                    'name': f"/{skill['name']}",
                    'description': skill['description'],
                    'group': skill['group'],
                }
                for skill in manifest['skills']
            ],
            'total': manifest['total'],
            'groups': manifest['groups'],
        }

    def execute_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a skill command

        Args:
            command: Command name (with or without /)
            **kwargs: Command parameters

        Returns:
            Execution result
        """
        skill_name = command.lstrip('/')
        skill = self.registry.get_skill(skill_name)

        if not skill:
            return {
                'status': 'error',
                'error': f'Skill not found: {skill_name}',
            }

        try:
            logger.info(f"Executing command: {skill_name}")
            result = skill.execute(**kwargs)
            return result
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
            }

    def get_skill_help(self, skill_name: str) -> Dict[str, Any]:
        """Get help for a skill"""
        skill = self.registry.get_skill(skill_name)
        if not skill:
            return {'error': f'Skill not found: {skill_name}'}
        return skill.get_manifest()

    def list_skills(self, group: str = None) -> Dict[str, Any]:
        """List available skills"""
        if group:
            skills = self.registry.list_skills(group)
            return {
                'group': group,
                'skills': skills,
                'count': len(skills),
            }
        else:
            return {
                'groups': self.registry.skill_groups,
                'total_skills': len(self.registry.skills),
            }

    def get_skill_manifest(self) -> Dict[str, Any]:
        """Get complete skill manifest"""
        return self.registry.get_skill_manifest()

    def execute_workflow(self, workflow: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute a workflow of multiple skills

        Args:
            workflow: List of skill commands to execute

        Returns:
            Workflow execution result
        """
        results = []
        context = {}

        for step in workflow:
            command = step.get('command')
            params = step.get('params', {})

            # Merge context into params
            params.update(context)

            logger.info(f"Executing workflow step: {command}")

            result = self.execute_command(command, **params)
            results.append({
                'command': command,
                'result': result,
            })

            # Update context with result
            if result.get('status') == 'success':
                context.update(result.get('data', {}))
            else:
                # Stop on error
                return {
                    'status': 'failed',
                    'error': result.get('error'),
                    'completed_steps': len(results),
                    'results': results,
                }

        return {
            'status': 'success',
            'completed_steps': len(results),
            'results': results,
            'context': context,
        }

    def get_skill_execution_history(self, skill_name: str) -> List[Dict[str, Any]]:
        """Get execution history for a skill"""
        skill = self.registry.get_skill(skill_name)
        if not skill:
            return []
        return skill.get_execution_history()

    def clear_skill_history(self, skill_name: str) -> Dict[str, Any]:
        """Clear execution history for a skill"""
        skill = self.registry.get_skill(skill_name)
        if not skill:
            return {'error': f'Skill not found: {skill_name}'}
        skill.clear_history()
        return {'status': 'success', 'message': f'History cleared for {skill_name}'}
