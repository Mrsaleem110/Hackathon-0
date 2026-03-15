"""
Configuration loader for AI Employee Vault
Loads credentials from .env file and environment variables
"""

import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to load .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        logger.info(f"Loaded .env from {env_path}")
    else:
        logger.warning(f".env file not found at {env_path}")
except ImportError:
    logger.warning("python-dotenv not installed. Install with: pip install python-dotenv")

# Gmail Configuration
GMAIL_CLIENT_ID = os.getenv('GMAIL_CLIENT_ID')
GMAIL_CLIENT_SECRET = os.getenv('GMAIL_CLIENT_SECRET')
GMAIL_REDIRECT_URI = os.getenv('GMAIL_REDIRECT_URI', 'http://localhost:8080/')

# LinkedIn Configuration
LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')

# Instagram Configuration
INSTAGRAM_APP_ID = os.getenv('INSTAGRAM_APP_ID')
INSTAGRAM_APP_SECRET = os.getenv('INSTAGRAM_APP_SECRET')
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME', 'm.saleem_ai_engineer')

# Facebook Configuration
FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')

# Session Paths
WHATSAPP_SESSION_PATH = os.getenv('WHATSAPP_SESSION_PATH', '.whatsapp_session')
LINKEDIN_SESSION_PATH = os.getenv('LINKEDIN_SESSION_PATH', '.linkedin_session')

# System Configuration
VAULT_PATH = os.getenv('VAULT_PATH', '.')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
DRY_RUN = os.getenv('DRY_RUN', 'false').lower() == 'true'

# Approval Settings
APPROVAL_EXPIRY_HOURS = int(os.getenv('APPROVAL_EXPIRY_HOURS', '24'))
AUTO_APPROVE_THRESHOLD = int(os.getenv('AUTO_APPROVE_THRESHOLD', '50'))

# Scheduling
ENABLE_SCHEDULER = os.getenv('ENABLE_SCHEDULER', 'true').lower() == 'true'
TIMEZONE = os.getenv('TIMEZONE', 'UTC')

# Demo Mode
DEMO_MODE = os.getenv('DEMO_MODE', 'false').lower() == 'true'


def validate_credentials():
    """Validate that all required credentials are set"""
    required = {
        'GMAIL_CLIENT_ID': GMAIL_CLIENT_ID,
        'GMAIL_CLIENT_SECRET': GMAIL_CLIENT_SECRET,
        'LINKEDIN_CLIENT_ID': LINKEDIN_CLIENT_ID,
        'LINKEDIN_CLIENT_SECRET': LINKEDIN_CLIENT_SECRET,
        'INSTAGRAM_ACCESS_TOKEN': INSTAGRAM_ACCESS_TOKEN,
        'INSTAGRAM_BUSINESS_ACCOUNT_ID': INSTAGRAM_BUSINESS_ACCOUNT_ID,
        'FACEBOOK_ACCESS_TOKEN': FACEBOOK_ACCESS_TOKEN,
        'FACEBOOK_PAGE_ID': FACEBOOK_PAGE_ID,
    }

    missing = [key for key, value in required.items() if not value]

    if missing:
        logger.warning(f"⚠️  Missing credentials: {', '.join(missing)}")
        logger.warning("Please set up .env file with real credentials")
        logger.warning("See INSTAGRAM_FACEBOOK_SETUP.md for instructions")
        return False

    logger.info("✅ All credentials configured")
    return True


def get_config_status():
    """Get current configuration status"""
    status = {
        'gmail_configured': bool(GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET),
        'linkedin_configured': bool(LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET),
        'instagram_configured': bool(INSTAGRAM_ACCESS_TOKEN and INSTAGRAM_BUSINESS_ACCOUNT_ID),
        'facebook_configured': bool(FACEBOOK_ACCESS_TOKEN and FACEBOOK_PAGE_ID),
        'whatsapp_session': os.path.exists(WHATSAPP_SESSION_PATH),
        'linkedin_session': os.path.exists(LINKEDIN_SESSION_PATH),
        'dry_run': DRY_RUN,
        'demo_mode': DEMO_MODE,
        'scheduler_enabled': ENABLE_SCHEDULER,
        'vault_path': VAULT_PATH,
    }
    return status


def print_config_status():
    """Print configuration status"""
    status = get_config_status()

    print("\n" + "=" * 60)
    print("AI EMPLOYEE VAULT - CONFIGURATION STATUS")
    print("=" * 60)

    print("\n[GMAIL] Gmail Configuration:")
    print(f"  [OK] Gmail API configured" if status['gmail_configured'] else "  [NO] Gmail API not configured")

    print("\n[LINKEDIN] LinkedIn Configuration:")
    print(f"  [OK] LinkedIn API configured" if status['linkedin_configured'] else "  [NO] LinkedIn API not configured")

    print("\n[INSTAGRAM] Instagram Configuration:")
    print(f"  [OK] Instagram API configured" if status['instagram_configured'] else "  [NO] Instagram API not configured")

    print("\n[FACEBOOK] Facebook Configuration:")
    print(f"  [OK] Facebook API configured" if status['facebook_configured'] else "  [NO] Facebook API not configured")

    print("\n[WHATSAPP] WhatsApp Configuration:")
    print(f"  [OK] WhatsApp session found" if status['whatsapp_session'] else "  [NO] WhatsApp session not found")

    print("\n[SESSION] LinkedIn Session:")
    print(f"  [OK] LinkedIn session found" if status['linkedin_session'] else "  [NO] LinkedIn session not found")

    print("\n[SYSTEM] System Settings:")
    print(f"  Dry Run: {'ON (no real actions)' if status['dry_run'] else 'OFF (real actions)'}")
    print(f"  Demo Mode: {'ON' if status['demo_mode'] else 'OFF'}")
    print(f"  Scheduler: {'Enabled' if status['scheduler_enabled'] else 'Disabled'}")
    print(f"  Vault Path: {status['vault_path']}")

    print("\n" + "=" * 60)

    if not (status['gmail_configured'] and status['linkedin_configured'] and status['instagram_configured'] and status['facebook_configured']):
        print("\n[WARNING] MISSING CREDENTIALS!")
        print("See INSTAGRAM_FACEBOOK_SETUP.md for setup instructions")
    else:
        print("\n[SUCCESS] All credentials configured!")

    print("=" * 60 + "\n")


if __name__ == '__main__':
    print_config_status()
