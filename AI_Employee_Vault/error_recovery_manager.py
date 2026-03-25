"""Error Recovery Manager - Handle failures with fallback methods"""

import logging
from typing import Dict, Any, Optional, Callable, List
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Platform(Enum):
    """Supported platforms"""
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"


class ErrorRecoveryManager:
    """Manage errors with fallback methods"""

    def __init__(self):
        """Initialize error recovery manager"""
        self.fallback_methods = {
            Platform.EMAIL: ['gmail_api', 'smtp', 'manual'],
            Platform.WHATSAPP: ['whatsapp_api', 'selenium', 'manual'],
            Platform.LINKEDIN: ['linkedin_api', 'selenium', 'manual'],
            Platform.TWITTER: ['twitter_api', 'manual'],
            Platform.INSTAGRAM: ['instagram_api', 'manual'],
            Platform.FACEBOOK: ['facebook_api', 'manual'],
        }

        self.method_handlers = {}
        self.error_log = []

    def register_method_handler(self, platform: Platform, method: str, handler: Callable):
        """Register a method handler"""
        key = f"{platform.value}_{method}"
        self.method_handlers[key] = handler
        logger.info(f"Registered handler: {key}")

    def execute_with_fallback(self, action: str, platform: Platform, *args, **kwargs) -> Dict[str, Any]:
        """Execute action with fallback methods"""
        try:
            methods = self.fallback_methods.get(platform, [])

            for i, method in enumerate(methods):
                try:
                    logger.info(f"Attempting {action} on {platform.value} using {method} (attempt {i+1}/{len(methods)})")

                    result = self.execute_method(action, platform, method, *args, **kwargs)

                    if result.get('success'):
                        logger.info(f"✅ {action} succeeded using {method}")
                        return result

                    logger.warning(f"⚠️ {method} failed: {result.get('error')}")

                except Exception as e:
                    logger.warning(f"⚠️ Method {method} failed with exception: {e}")
                    continue

            # All methods failed
            logger.error(f"❌ All fallback methods failed for {action} on {platform.value}")
            self.notify_user_failure(action, platform, args, kwargs)

            return {
                'success': False,
                'error': f'All fallback methods failed for {action}',
                'platform': platform.value,
                'methods_tried': methods
            }

        except Exception as e:
            logger.error(f"Error in execute_with_fallback: {e}")
            return {'success': False, 'error': str(e)}

    def execute_method(self, action: str, platform: Platform, method: str, *args, **kwargs) -> Dict[str, Any]:
        """Execute specific method"""
        try:
            key = f"{platform.value}_{method}"

            if key in self.method_handlers:
                handler = self.method_handlers[key]
                return handler(action, *args, **kwargs)

            # Default implementation
            logger.warning(f"No handler registered for {key}, using default")
            return {
                'success': True,
                'method': method,
                'message': f'{action} executed via {method} (demo mode)'
            }

        except Exception as e:
            logger.error(f"Error executing method {method}: {e}")
            return {'success': False, 'error': str(e)}

    def notify_user_failure(self, action: str, platform: Platform, args: tuple, kwargs: dict):
        """Notify user of failure"""
        try:
            notification = {
                'type': 'error',
                'action': action,
                'platform': platform.value,
                'message': f'Failed to {action} on {platform.value}. All fallback methods exhausted.',
                'timestamp': logging.Formatter().formatTime(logging.LogRecord(
                    name='', level=0, pathname='', lineno=0, msg='', args=(), exc_info=None
                ))
            }

            self.error_log.append(notification)
            logger.error(f"User notification: {notification}")

            # In production, send email/WhatsApp to user
            self._send_notification(notification)

        except Exception as e:
            logger.error(f"Failed to notify user: {e}")

    def _send_notification(self, notification: Dict[str, Any]):
        """Send notification to user (placeholder)"""
        logger.info(f"Notification would be sent: {notification}")

    def get_error_log(self) -> List[Dict[str, Any]]:
        """Get error log"""
        return self.error_log

    def clear_error_log(self):
        """Clear error log"""
        self.error_log = []
        logger.info("Error log cleared")

    def get_recovery_stats(self) -> Dict[str, Any]:
        """Get recovery statistics"""
        total_errors = len(self.error_log)
        errors_by_platform = {}

        for error in self.error_log:
            platform = error.get('platform', 'unknown')
            errors_by_platform[platform] = errors_by_platform.get(platform, 0) + 1

        return {
            'total_errors': total_errors,
            'errors_by_platform': errors_by_platform,
            'recovery_rate': 100 - (total_errors * 5) if total_errors < 20 else 0  # Demo calculation
        }
