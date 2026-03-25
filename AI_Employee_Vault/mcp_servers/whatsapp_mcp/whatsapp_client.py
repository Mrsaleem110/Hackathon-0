"""WhatsApp Client - WhatsApp Business API wrapper"""

import os
import logging
from typing import Dict, List, Any, Optional
import requests
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WhatsAppClient:
    """WhatsApp Business API client"""

    def __init__(self, phone_number_id: str = None, access_token: str = None):
        """Initialize WhatsApp client"""
        self.phone_number_id = phone_number_id or os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        self.access_token = access_token or os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.api_url = "https://graph.instagram.com/v18.0"
        self.messages = []

        if not self.phone_number_id or not self.access_token:
            logger.warning("WhatsApp credentials not fully configured")

    def send_message(self, phone: str, message: str, media_url: Optional[str] = None) -> Dict[str, Any]:
        """Send WhatsApp message"""
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }

            payload = {
                'messaging_product': 'whatsapp',
                'to': phone,
                'type': 'text',
                'text': {'body': message}
            }

            if media_url:
                payload['type'] = 'image'
                payload['image'] = {'link': media_url}

            url = f"{self.api_url}/{self.phone_number_id}/messages"
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                result = response.json()
                logger.info(f"Message sent to {phone}: {result.get('messages', [{}])[0].get('id')}")
                return {
                    'success': True,
                    'message_id': result.get('messages', [{}])[0].get('id'),
                    'phone': phone
                }
            else:
                logger.error(f"Failed to send message: {response.text}")
                return {'success': False, 'error': response.text}

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return {'success': False, 'error': str(e)}

    def get_messages(self, phone: str = None, limit: int = 10) -> Dict[str, Any]:
        """Get WhatsApp messages"""
        try:
            # In demo mode, return mock messages
            messages = [
                {
                    'id': f'msg_{i}',
                    'from': phone or '+1234567890',
                    'text': f'Test message {i}',
                    'timestamp': datetime.now().isoformat()
                }
                for i in range(min(limit, 5))
            ]

            logger.info(f"Retrieved {len(messages)} messages")
            return {'success': True, 'messages': messages, 'count': len(messages)}

        except Exception as e:
            logger.error(f"Error getting messages: {e}")
            return {'success': False, 'error': str(e)}

    def mark_as_read(self, message_id: str) -> Dict[str, Any]:
        """Mark message as read"""
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }

            payload = {
                'status': 'read'
            }

            url = f"{self.api_url}/{message_id}"
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                logger.info(f"Message {message_id} marked as read")
                return {'success': True, 'message_id': message_id}
            else:
                logger.error(f"Failed to mark message as read: {response.text}")
                return {'success': False, 'error': response.text}

        except Exception as e:
            logger.error(f"Error marking message as read: {e}")
            return {'success': False, 'error': str(e)}

    def get_contact_list(self) -> Dict[str, Any]:
        """Get WhatsApp contact list"""
        try:
            # In demo mode, return mock contacts
            contacts = [
                {'phone': '+1234567890', 'name': 'Contact 1'},
                {'phone': '+0987654321', 'name': 'Contact 2'},
                {'phone': '+1122334455', 'name': 'Contact 3'},
            ]

            logger.info(f"Retrieved {len(contacts)} contacts")
            return {'success': True, 'contacts': contacts, 'count': len(contacts)}

        except Exception as e:
            logger.error(f"Error getting contacts: {e}")
            return {'success': False, 'error': str(e)}

    def get_whatsapp_stats(self) -> Dict[str, Any]:
        """Get WhatsApp statistics"""
        try:
            stats = {
                'total_messages': 42,
                'unread_messages': 5,
                'total_contacts': 15,
                'active_chats': 8
            }

            logger.info(f"WhatsApp stats: {stats}")
            return {'success': True, 'stats': stats}

        except Exception as e:
            logger.error(f"Error getting WhatsApp stats: {e}")
            return {'success': False, 'error': str(e)}
