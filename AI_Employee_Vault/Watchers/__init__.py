"""
Watchers Package - All watcher implementations
"""

from .base_watcher import BaseWatcher
from .gmail_watcher import GmailWatcher
from .whatsapp_watcher import WhatsAppWatcher
from .linkedin_watcher import LinkedInWatcher
from .linkedin_poster import LinkedInPoster

__all__ = [
    'BaseWatcher',
    'GmailWatcher',
    'WhatsAppWatcher',
    'LinkedInWatcher',
    'LinkedInPoster'
]
