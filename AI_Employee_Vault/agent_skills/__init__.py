"""
Agent Skills Framework for AI Employee Vault
Integrates with Claude Code Agent SDK
"""

from typing import Dict, Any, Callable, List
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SkillRegistry:
    """Registry for all available skills"""

    def __init__(self):
        self.skills: Dict[str, 'Skill'] = {}
        self.skill_groups: Dict[str, List[str]] = {}

    def register_skill(self, skill: 'Skill'):
        """Register a skill"""
        self.skills[skill.name] = skill
        group = skill.group or 'general'
        if group not in self.skill_groups:
            self.skill_groups[group] = []
        self.skill_groups[group].append(skill.name)
        logger.info(f"Registered skill: {skill.name}")

    def get_skill(self, name: str) -> 'Skill':
        """Get skill by name"""
        return self.skills.get(name)

    def list_skills(self, group: str = None) -> List[str]:
        """List available skills"""
        if group:
            return self.skill_groups.get(group, [])
        return list(self.skills.keys())

    def get_skill_manifest(self) -> Dict:
        """Get manifest of all skills for Claude Code"""
        return {
            'skills': [
                {
                    'name': skill.name,
                    'description': skill.description,
                    'group': skill.group,
                    'parameters': skill.parameters,
                    'version': skill.version,
                }
                for skill in self.skills.values()
            ],
            'total': len(self.skills),
            'groups': list(self.skill_groups.keys()),
        }


# Global registry
_registry = SkillRegistry()


def get_registry() -> SkillRegistry:
    """Get global skill registry"""
    return _registry
