"""
Email Skills - Email operations for agent
"""

from typing import Dict, Any, List
import logging
from skill import Skill, SkillParameter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SendEmailSkill(Skill):
    """Send email via Gmail MCP"""

    def __init__(self):
        super().__init__(
            name='send_email',
            description='Send email to recipient',
            group='email',
            version='1.0.0',
        )
        self.parameters = [
            SkillParameter('to', 'string', 'Recipient email address', required=True),
            SkillParameter('subject', 'string', 'Email subject', required=True),
            SkillParameter('body', 'string', 'Email body', required=True),
            SkillParameter('cc', 'array', 'CC recipients', required=False),
            SkillParameter('bcc', 'array', 'BCC recipients', required=False),
            SkillParameter('attachments', 'array', 'File attachments', required=False),
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute email sending"""
        try:
            self.validate_parameters(**kwargs)

            to = kwargs.get('to')
            subject = kwargs.get('subject')
            body = kwargs.get('body')
            cc = kwargs.get('cc', [])
            bcc = kwargs.get('bcc', [])
            attachments = kwargs.get('attachments', [])

            logger.info(f"Sending email to {to}: {subject}")

            # Call Gmail MCP
            result = self._send_via_gmail_mcp({
                'to': to,
                'subject': subject,
                'body': body,
                'cc': cc,
                'bcc': bcc,
                'attachments': attachments,
            })

            self.log_execution(kwargs, result)
            return result

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            result = {'status': 'error', 'error': str(e)}
            self.log_execution(kwargs, result)
            return result

    def _send_via_gmail_mcp(self, params: Dict) -> Dict[str, Any]:
        """Send via Gmail MCP server"""
        import requests
        try:
            response = requests.post(
                'http://localhost:8070/tools/send_email',
                json=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Gmail MCP error: {e}")
            return {'status': 'error', 'error': str(e)}


class GetEmailsSkill(Skill):
    """Get emails from Gmail"""

    def __init__(self):
        super().__init__(
            name='get_emails',
            description='Get emails from Gmail inbox',
            group='email',
            version='1.0.0',
        )
        self.parameters = [
            SkillParameter('query', 'string', 'Search query', required=False),
            SkillParameter('max_results', 'number', 'Max results to return', required=False, default=10),
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute email retrieval"""
        try:
            query = kwargs.get('query', '')
            max_results = kwargs.get('max_results', 10)

            logger.info(f"Getting emails with query: {query}")

            # Call Gmail MCP
            result = self._get_from_gmail_mcp({
                'query': query,
                'max_results': max_results,
            })

            self.log_execution(kwargs, result)
            return result

        except Exception as e:
            logger.error(f"Failed to get emails: {e}")
            result = {'status': 'error', 'error': str(e)}
            self.log_execution(kwargs, result)
            return result

    def _get_from_gmail_mcp(self, params: Dict) -> Dict[str, Any]:
        """Get emails from Gmail MCP server"""
        import requests
        try:
            response = requests.get(
                'http://localhost:8070/tools/get_emails',
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Gmail MCP error: {e}")
            return {'status': 'error', 'error': str(e)}


class ReplyEmailSkill(Skill):
    """Reply to email"""

    def __init__(self):
        super().__init__(
            name='reply_email',
            description='Reply to email message',
            group='email',
            version='1.0.0',
        )
        self.parameters = [
            SkillParameter('message_id', 'string', 'Message ID to reply to', required=True),
            SkillParameter('body', 'string', 'Reply body', required=True),
            SkillParameter('attachments', 'array', 'File attachments', required=False),
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute email reply"""
        try:
            self.validate_parameters(**kwargs)

            message_id = kwargs.get('message_id')
            body = kwargs.get('body')
            attachments = kwargs.get('attachments', [])

            logger.info(f"Replying to message {message_id}")

            # Call Gmail MCP
            result = self._reply_via_gmail_mcp({
                'message_id': message_id,
                'body': body,
                'attachments': attachments,
            })

            self.log_execution(kwargs, result)
            return result

        except Exception as e:
            logger.error(f"Failed to reply to email: {e}")
            result = {'status': 'error', 'error': str(e)}
            self.log_execution(kwargs, result)
            return result

    def _reply_via_gmail_mcp(self, params: Dict) -> Dict[str, Any]:
        """Reply via Gmail MCP server"""
        import requests
        try:
            response = requests.post(
                'http://localhost:8070/tools/reply_email',
                json=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Gmail MCP error: {e}")
            return {'status': 'error', 'error': str(e)}
