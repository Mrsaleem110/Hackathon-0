"""Instagram Agent Skill"""

import logging
from typing import Dict, Any, Optional
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstagramSkill:
    """Instagram operations skill"""

    def __init__(self, mcp_url: str = "http://localhost:8076"):
        """Initialize Instagram skill"""
        self.mcp_url = mcp_url
        self.name = "instagram_skill"
        self.description = "Post to Instagram and manage engagement"

    def post_to_instagram(self, caption: str, image_url: str, hashtags: Optional[list] = None) -> Dict[str, Any]:
        """Post to Instagram"""
        try:
            payload = {
                "caption": caption,
                "image_url": image_url,
                "hashtags": hashtags or []
            }
            response = requests.post(f"{self.mcp_url}/post_feed", json=payload)
            result = response.json()
            logger.info(f"Instagram post created: {result.get('post_id')}")
            return result
        except Exception as e:
            logger.error(f"Failed to post to Instagram: {e}")
            return {"success": False, "error": str(e)}

    def get_instagram_feed(self, limit: int = 10) -> Dict[str, Any]:
        """Get Instagram feed"""
        try:
            response = requests.get(f"{self.mcp_url}/feed?limit={limit}")
            result = response.json()
            logger.info(f"Retrieved {result.get('count', 0)} Instagram posts")
            return result
        except Exception as e:
            logger.error(f"Failed to get Instagram feed: {e}")
            return {"success": False, "error": str(e)}

    def get_instagram_insights(self) -> Dict[str, Any]:
        """Get Instagram insights"""
        try:
            response = requests.get(f"{self.mcp_url}/insights")
            result = response.json()
            logger.info(f"Instagram insights: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to get Instagram insights: {e}")
            return {"success": False, "error": str(e)}

    def post_story(self, image_url: str, duration: int = 24) -> Dict[str, Any]:
        """Post Instagram story"""
        try:
            payload = {
                "image_url": image_url,
                "duration": duration
            }
            response = requests.post(f"{self.mcp_url}/post_story", json=payload)
            result = response.json()
            logger.info(f"Instagram story posted: {result.get('story_id')}")
            return result
        except Exception as e:
            logger.error(f"Failed to post story: {e}")
            return {"success": False, "error": str(e)}
