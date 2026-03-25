"""WhatsApp Agent Skill"""

import logging
from typing import Dict, Any, Optional
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WhatsAppSkill:
    """WhatsApp operations skill"""

    def __init__(self, mcp_url: str = "http://localhost:8073"):
        """Initialize WhatsApp skill"""
        self.mcp_url = mcp_url
        self.name = "whatsapp_skill"
        self.description = "Send and receive WhatsApp messages"

    def send_whatsapp_message(self, phone: str, message: str, media_url: Optional[str] = None) -> Dict[str, Any]:
        """Send WhatsApp message"""
        try:
            payload = {
                "phone": phone,
                "message": message,
                "media_url": media_url
            }
            response = requests.post(f"{self.mcp_url}/send_message", json=payload)
            result = response.json()
            logger.info(f"WhatsApp message sent to {phone}")
            return result
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {e}")
            return {"success": False, "error": str(e)}

    def get_whatsapp_messages(self, phone: str = None, limit: int = 10) -> Dict[str, Any]:
        """Get WhatsApp messages"""
        try:
            payload = {
                "phone": phone,
                "limit": limit
            }
            response = requests.post(f"{self.mcp_url}/get_messages", json=payload)
            result = response.json()
            logger.info(f"Retrieved {result.get('count', 0)} WhatsApp messages")
            return result
        except Exception as e:
            logger.error(f"Failed to get WhatsApp messages: {e}")
            return {"success": False, "error": str(e)}

    def process_whatsapp_notification(self, notification: Dict[str, Any]) -> Dict[str, Any]:
        """Process WhatsApp notification"""
        try:
            logger.info(f"Processing WhatsApp notification: {notification}")
            return {"success": True, "processed": True}
        except Exception as e:
            logger.error(f"Failed to process notification: {e}")
            return {"success": False, "error": str(e)}

    def validate_phone_number(self, phone: str) -> bool:
        """Validate phone number"""
        try:
            # Basic validation
            if not phone.startswith('+'):
                return False
            if len(phone) < 10:
                return False
            return True
        except Exception as e:
            logger.error(f"Failed to validate phone number: {e}")
            return False
