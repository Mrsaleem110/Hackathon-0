"""
Social Media Skills - Social media operations for agent
"""

from typing import Dict, Any, List
import logging
from skill import Skill, SkillParameter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostTwitterSkill(Skill):
    """Post tweet to Twitter"""

    def __init__(self):
        super().__init__(
            name='post_twitter',
            description='Post tweet to Twitter',
            group='social',
            version='1.0.0',
        )
        self.parameters = [
            SkillParameter('text', 'string', 'Tweet text (max 280 chars)', required=True),
            SkillParameter('reply_to', 'string', 'Tweet ID to reply to', required=False),
            SkillParameter('dry_run', 'boolean', 'Test mode', required=False, default=False),
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute tweet posting"""
        try:
            self.validate_parameters(**kwargs)

            text = kwargs.get('text')
            reply_to = kwargs.get('reply_to')
            dry_run = kwargs.get('dry_run', False)

            if len(text) > 280:
                return {'status': 'error', 'error': 'Tweet exceeds 280 characters'}

            logger.info(f"Posting tweet: {text[:50]}...")

            result = self._post_via_twitter_mcp({
                'text': text,
                'reply_to': reply_to,
                'dry_run': dry_run,
            })

            self.log_execution(kwargs, result)
            return result

        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            result = {'status': 'error', 'error': str(e)}
            self.log_execution(kwargs, result)
            return result

    def _post_via_twitter_mcp(self, params: Dict) -> Dict[str, Any]:
        """Post via Twitter MCP server"""
        import requests
        try:
            response = requests.post(
                'http://localhost:8071/tools/post_tweet',
                json=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Twitter MCP error: {e}")
            return {'status': 'error', 'error': str(e)}


class PostInstagramSkill(Skill):
    """Post to Instagram"""

    def __init__(self):
        super().__init__(
            name='post_instagram',
            description='Post to Instagram feed',
            group='social',
            version='1.0.0',
        )
        self.parameters = [
            SkillParameter('caption', 'string', 'Post caption', required=True),
            SkillParameter('image_url', 'string', 'Image URL', required=True),
            SkillParameter('dry_run', 'boolean', 'Test mode', required=False, default=False),
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute Instagram post"""
        try:
            self.validate_parameters(**kwargs)

            caption = kwargs.get('caption')
            image_url = kwargs.get('image_url')
            dry_run = kwargs.get('dry_run', False)

            logger.info(f"Posting to Instagram: {caption[:50]}...")

            result = self._post_via_instagram_mcp({
                'caption': caption,
                'image_url': image_url,
                'dry_run': dry_run,
            })

            self.log_execution(kwargs, result)
            return result

        except Exception as e:
            logger.error(f"Failed to post to Instagram: {e}")
            result = {'status': 'error', 'error': str(e)}
            self.log_execution(kwargs, result)
            return result

    def _post_via_instagram_mcp(self, params: Dict) -> Dict[str, Any]:
        """Post via Instagram MCP server"""
        import requests
        try:
            response = requests.post(
                'http://localhost:8072/tools/post_feed',
                json=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Instagram MCP error: {e}")
            return {'status': 'error', 'error': str(e)}


class PostFacebookSkill(Skill):
    """Post to Facebook"""

    def __init__(self):
        super().__init__(
            name='post_facebook',
            description='Post to Facebook page',
            group='social',
            version='1.0.0',
        )
        self.parameters = [
            SkillParameter('message', 'string', 'Post message', required=True),
            SkillParameter('link', 'string', 'Link to share', required=False),
            SkillParameter('dry_run', 'boolean', 'Test mode', required=False, default=False),
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute Facebook post"""
        try:
            self.validate_parameters(**kwargs)

            message = kwargs.get('message')
            link = kwargs.get('link')
            dry_run = kwargs.get('dry_run', False)

            logger.info(f"Posting to Facebook: {message[:50]}...")

            result = self._post_via_facebook_mcp({
                'message': message,
                'link': link,
                'dry_run': dry_run,
            })

            self.log_execution(kwargs, result)
            return result

        except Exception as e:
            logger.error(f"Failed to post to Facebook: {e}")
            result = {'status': 'error', 'error': str(e)}
            self.log_execution(kwargs, result)
            return result

    def _post_via_facebook_mcp(self, params: Dict) -> Dict[str, Any]:
        """Post via Facebook MCP server"""
        import requests
        try:
            response = requests.post(
                'http://localhost:8073/tools/post_feed',
                json=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Facebook MCP error: {e}")
            return {'status': 'error', 'error': str(e)}


class GetSocialMetricsSkill(Skill):
    """Get social media metrics"""

    def __init__(self):
        super().__init__(
            name='get_social_metrics',
            description='Get social media engagement metrics',
            group='social',
            version='1.0.0',
        )
        self.parameters = [
            SkillParameter('platform', 'string', 'Platform (twitter, instagram, facebook)', required=True),
            SkillParameter('days', 'number', 'Days to look back', required=False, default=7),
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute metrics retrieval"""
        try:
            self.validate_parameters(**kwargs)

            platform = kwargs.get('platform')
            days = kwargs.get('days', 7)

            logger.info(f"Getting {platform} metrics for last {days} days")

            if platform == 'twitter':
                result = self._get_twitter_metrics(days)
            elif platform == 'instagram':
                result = self._get_instagram_metrics(days)
            elif platform == 'facebook':
                result = self._get_facebook_metrics(days)
            else:
                result = {'status': 'error', 'error': f'Unknown platform: {platform}'}

            self.log_execution(kwargs, result)
            return result

        except Exception as e:
            logger.error(f"Failed to get social metrics: {e}")
            result = {'status': 'error', 'error': str(e)}
            self.log_execution(kwargs, result)
            return result

    def _get_twitter_metrics(self, days: int) -> Dict[str, Any]:
        """Get Twitter metrics"""
        import requests
        try:
            response = requests.get(
                'http://localhost:8071/tools/get_engagement_summary',
                params={'days': days},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Twitter MCP error: {e}")
            return {'status': 'error', 'error': str(e)}

    def _get_instagram_metrics(self, days: int) -> Dict[str, Any]:
        """Get Instagram metrics"""
        import requests
        try:
            response = requests.get(
                'http://localhost:8072/tools/get_insights',
                params={'days': days},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Instagram MCP error: {e}")
            return {'status': 'error', 'error': str(e)}

    def _get_facebook_metrics(self, days: int) -> Dict[str, Any]:
        """Get Facebook metrics"""
        import requests
        try:
            response = requests.get(
                'http://localhost:8073/tools/get_page_insights',
                params={'days': days},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Facebook MCP error: {e}")
            return {'status': 'error', 'error': str(e)}
