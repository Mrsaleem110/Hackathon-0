"""
Skill Loader - Load and register all skills
"""

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from __init__ import get_registry, Skill


class SkillLoader:
    """Load and register skills"""

    @staticmethod
    def load_all_skills():
        """Load all skills from skills directory"""
        registry = get_registry()
        skills_dir = Path(__file__).parent

        # Import skill modules
        try:
            from email_skills import SendEmailSkill, GetEmailsSkill, ReplyEmailSkill
            from social_skills import PostTwitterSkill, PostInstagramSkill, PostFacebookSkill, GetSocialMetricsSkill
            from accounting_skills import CreateInvoiceSkill, RecordExpenseSkill, GetFinancialSummarySkill, GetSalesPipelineSkill

            # Register email skills
            registry.register_skill(SendEmailSkill())
            registry.register_skill(GetEmailsSkill())
            registry.register_skill(ReplyEmailSkill())

            # Register social skills
            registry.register_skill(PostTwitterSkill())
            registry.register_skill(PostInstagramSkill())
            registry.register_skill(PostFacebookSkill())
            registry.register_skill(GetSocialMetricsSkill())

            # Register accounting skills
            registry.register_skill(CreateInvoiceSkill())
            registry.register_skill(RecordExpenseSkill())
            registry.register_skill(GetFinancialSummarySkill())
            registry.register_skill(GetSalesPipelineSkill())

            logger.info(f"Loaded {len(registry.skills)} skills")

        except Exception as e:
            logger.error(f"Failed to load skills: {e}")

    @staticmethod
    def get_skill_manifest() -> Dict[str, Any]:
        """Get manifest for Claude Code"""
        registry = get_registry()
        return registry.get_skill_manifest()

    @staticmethod
    def list_skills_by_group(group: str = None) -> Dict[str, Any]:
        """List skills by group"""
        registry = get_registry()
        if group:
            skills = registry.list_skills(group)
            return {
                'group': group,
                'skills': skills,
                'count': len(skills),
            }
        else:
            return {
                'groups': registry.skill_groups,
                'total_skills': len(registry.skills),
            }
