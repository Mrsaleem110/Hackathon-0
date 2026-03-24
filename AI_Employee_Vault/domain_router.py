"""
Domain Router - Route tasks to personal or business domain
"""

import logging
from typing import Dict, List, Optional
from pathlib import Path
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DomainRouter:
    """Route tasks to personal or business domain"""

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize domain router

        Args:
            config_file: Path to domain configuration file
        """
        self.config = self._load_config(config_file)
        self.personal_domains = self.config.get('domains', {}).get('personal', {}).get('email_domains', [])
        self.business_domains = self.config.get('domains', {}).get('business', {}).get('email_domains', [])

    def _load_config(self, config_file: Optional[str]) -> Dict:
        """Load domain configuration"""
        if config_file and Path(config_file).exists():
            try:
                with open(config_file, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                return self._default_config()
        return self._default_config()

    def _default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'domains': {
                'personal': {
                    'email_domains': ['gmail.com', 'yahoo.com', 'outlook.com'],
                    'approval_threshold': 30,
                    'auto_approve': False,
                    'channels': ['gmail', 'whatsapp'],
                },
                'business': {
                    'email_domains': ['company.com', 'business.com'],
                    'approval_threshold': 70,
                    'auto_approve': True,
                    'channels': ['gmail', 'linkedin', 'odoo'],
                }
            }
        }

    def detect_domain(self, email: str) -> str:
        """
        Detect if email is personal or business

        Args:
            email: Email address

        Returns:
            'personal' or 'business'
        """
        if not email:
            return 'unknown'

        domain = email.split('@')[-1].lower()

        if domain in self.personal_domains:
            return 'personal'
        elif domain in self.business_domains:
            return 'business'
        else:
            # Default to business if unknown
            logger.warning(f"Unknown domain: {domain}, defaulting to business")
            return 'business'

    def route_task(self, task: Dict) -> str:
        """
        Route task to appropriate domain

        Args:
            task: Task dictionary with 'email' or 'from_email' field

        Returns:
            Domain identifier ('personal' or 'business')
        """
        email = task.get('email') or task.get('from_email') or task.get('sender', '')
        domain = self.detect_domain(email)
        logger.info(f"Routing task to {domain} domain (email: {email})")
        return domain

    def get_domain_config(self, domain: str) -> Dict:
        """
        Get configuration for domain

        Args:
            domain: Domain identifier ('personal' or 'business')

        Returns:
            Domain-specific configuration
        """
        return self.config.get('domains', {}).get(domain, {})

    def get_approval_threshold(self, domain: str) -> int:
        """Get approval threshold for domain"""
        config = self.get_domain_config(domain)
        return config.get('approval_threshold', 50)

    def should_auto_approve(self, domain: str) -> bool:
        """Check if domain should auto-approve"""
        config = self.get_domain_config(domain)
        return config.get('auto_approve', False)

    def get_channels(self, domain: str) -> List[str]:
        """Get active channels for domain"""
        config = self.get_domain_config(domain)
        return config.get('channels', [])

    def get_vault_path(self, domain: str) -> Path:
        """Get vault path for domain"""
        if domain == 'personal':
            return Path('Personal')
        elif domain == 'business':
            return Path('Business')
        else:
            return Path('Shared')

    def get_inbox_path(self, domain: str) -> Path:
        """Get inbox path for domain"""
        return self.get_vault_path(domain) / 'Inbox'

    def get_needs_action_path(self, domain: str) -> Path:
        """Get needs_action path for domain"""
        return self.get_vault_path(domain) / 'Needs_Action'

    def get_pending_approval_path(self, domain: str) -> Path:
        """Get pending_approval path for domain"""
        return self.get_vault_path(domain) / 'Pending_Approval'

    def get_done_path(self, domain: str) -> Path:
        """Get done path for domain"""
        return self.get_vault_path(domain) / 'Done'

    def get_logs_path(self, domain: str) -> Path:
        """Get logs path for domain"""
        return self.get_vault_path(domain) / 'Logs'

    def create_domain_structure(self, base_path: Path = Path('.')):
        """Create vault structure for all domains"""
        for domain in ['personal', 'business']:
            vault_path = base_path / self.get_vault_path(domain)
            vault_path.mkdir(exist_ok=True)

            # Create subdirectories
            (vault_path / 'Inbox').mkdir(exist_ok=True)
            (vault_path / 'Needs_Action').mkdir(exist_ok=True)
            (vault_path / 'Pending_Approval').mkdir(exist_ok=True)
            (vault_path / 'Pending_Approval' / 'Approved').mkdir(exist_ok=True)
            (vault_path / 'Pending_Approval' / 'Rejected').mkdir(exist_ok=True)
            (vault_path / 'Done').mkdir(exist_ok=True)
            (vault_path / 'Logs').mkdir(exist_ok=True)

            logger.info(f"Created {domain} domain structure at {vault_path}")

    def get_all_domains(self) -> List[str]:
        """Get all configured domains"""
        return list(self.config.get('domains', {}).keys())
