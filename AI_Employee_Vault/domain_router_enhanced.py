"""Enhanced Domain Router - Personal vs Business separation"""

import os
import logging
from typing import Dict, Any, Optional, Tuple
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Domain(Enum):
    """Domain types"""
    PERSONAL = "personal"
    BUSINESS = "business"
    UNKNOWN = "unknown"


class DomainRouter:
    """Route communications to personal or business handlers"""

    def __init__(self):
        """Initialize domain router"""
        # Personal domain configuration
        self.personal_domain = {
            'gmail': os.getenv('PERSONAL_GMAIL', 'personal@gmail.com'),
            'whatsapp': os.getenv('PERSONAL_WHATSAPP', '+1234567890'),
            'linkedin': os.getenv('PERSONAL_LINKEDIN', 'personal-profile'),
        }

        # Business domain configuration
        self.business_domain = {
            'gmail': os.getenv('BUSINESS_GMAIL', 'business@company.com'),
            'whatsapp': os.getenv('BUSINESS_WHATSAPP', '+0987654321'),
            'linkedin': os.getenv('BUSINESS_LINKEDIN', 'company-profile'),
        }

        logger.info("Domain router initialized")

    def route_email(self, email_address: str) -> Tuple[Domain, Dict[str, Any]]:
        """Route email to personal or business handler"""
        try:
            email_lower = email_address.lower()

            # Check personal domain
            if email_lower == self.personal_domain['gmail'].lower():
                logger.info(f"Email {email_address} routed to PERSONAL")
                return Domain.PERSONAL, {
                    'handler': 'personal_email_handler',
                    'config': self.personal_domain
                }

            # Check business domain
            if email_lower == self.business_domain['gmail'].lower():
                logger.info(f"Email {email_address} routed to BUSINESS")
                return Domain.BUSINESS, {
                    'handler': 'business_email_handler',
                    'config': self.business_domain
                }

            # Check if it's a known business contact
            if 'company.com' in email_lower or 'business' in email_lower:
                logger.info(f"Email {email_address} routed to BUSINESS (domain match)")
                return Domain.BUSINESS, {
                    'handler': 'business_email_handler',
                    'config': self.business_domain
                }

            logger.warning(f"Email {email_address} domain unknown, defaulting to PERSONAL")
            return Domain.PERSONAL, {
                'handler': 'personal_email_handler',
                'config': self.personal_domain
            }

        except Exception as e:
            logger.error(f"Error routing email: {e}")
            return Domain.UNKNOWN, {'error': str(e)}

    def route_whatsapp(self, phone_number: str) -> Tuple[Domain, Dict[str, Any]]:
        """Route WhatsApp to personal or business handler"""
        try:
            phone_normalized = phone_number.replace(' ', '').replace('-', '')

            # Check personal domain
            if phone_normalized == self.personal_domain['whatsapp'].replace('+', ''):
                logger.info(f"WhatsApp {phone_number} routed to PERSONAL")
                return Domain.PERSONAL, {
                    'handler': 'personal_whatsapp_handler',
                    'config': self.personal_domain
                }

            # Check business domain
            if phone_normalized == self.business_domain['whatsapp'].replace('+', ''):
                logger.info(f"WhatsApp {phone_number} routed to BUSINESS")
                return Domain.BUSINESS, {
                    'handler': 'business_whatsapp_handler',
                    'config': self.business_domain
                }

            logger.warning(f"WhatsApp {phone_number} domain unknown, defaulting to PERSONAL")
            return Domain.PERSONAL, {
                'handler': 'personal_whatsapp_handler',
                'config': self.personal_domain
            }

        except Exception as e:
            logger.error(f"Error routing WhatsApp: {e}")
            return Domain.UNKNOWN, {'error': str(e)}

    def route_linkedin(self, profile_url: str) -> Tuple[Domain, Dict[str, Any]]:
        """Route LinkedIn to personal or business handler"""
        try:
            url_lower = profile_url.lower()

            # Check personal domain
            if self.personal_domain['linkedin'].lower() in url_lower:
                logger.info(f"LinkedIn {profile_url} routed to PERSONAL")
                return Domain.PERSONAL, {
                    'handler': 'personal_linkedin_handler',
                    'config': self.personal_domain
                }

            # Check business domain
            if self.business_domain['linkedin'].lower() in url_lower or 'company' in url_lower:
                logger.info(f"LinkedIn {profile_url} routed to BUSINESS")
                return Domain.BUSINESS, {
                    'handler': 'business_linkedin_handler',
                    'config': self.business_domain
                }

            logger.warning(f"LinkedIn {profile_url} domain unknown, defaulting to PERSONAL")
            return Domain.PERSONAL, {
                'handler': 'personal_linkedin_handler',
                'config': self.personal_domain
            }

        except Exception as e:
            logger.error(f"Error routing LinkedIn: {e}")
            return Domain.UNKNOWN, {'error': str(e)}

    def get_domain_config(self, domain: Domain) -> Dict[str, Any]:
        """Get configuration for domain"""
        if domain == Domain.PERSONAL:
            return self.personal_domain
        elif domain == Domain.BUSINESS:
            return self.business_domain
        else:
            return {}

    def set_personal_config(self, gmail: str = None, whatsapp: str = None, linkedin: str = None):
        """Set personal domain configuration"""
        if gmail:
            self.personal_domain['gmail'] = gmail
        if whatsapp:
            self.personal_domain['whatsapp'] = whatsapp
        if linkedin:
            self.personal_domain['linkedin'] = linkedin
        logger.info("Personal domain configuration updated")

    def set_business_config(self, gmail: str = None, whatsapp: str = None, linkedin: str = None):
        """Set business domain configuration"""
        if gmail:
            self.business_domain['gmail'] = gmail
        if whatsapp:
            self.business_domain['whatsapp'] = whatsapp
        if linkedin:
            self.business_domain['linkedin'] = linkedin
        logger.info("Business domain configuration updated")
