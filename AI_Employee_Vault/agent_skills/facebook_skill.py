"""Facebook Agent Skill"""

import logging
from typing import Dict, Any, Optional
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FacebookSkill:
    """Facebook operations skill"""

    def __init__(self, mcp_url: str = "http://localhost:8077"):
        """Initialize Facebook skill"""
        self.mcp_url = mcp_url
        self.name = "facebook_skill"
        self.description = "Post to Facebook and manage engagement"

    def post_to_facebook(self, message: str, link: Optional[str] = None, image_url: Optional[str] = None) -> Dict[str, Any]:
        """Post to Facebook"""
        try:
            payload = {
                "message": message,
                "link": link,
                "image_url": image_url
            }
            response = requests.post(f"{self.mcp_url}/post_feed", json=payload)
            result = response.json()
            logger.info(f"Facebook post created: {result.get('post_id')}")
            return result
        except Exception as e:
            logger.error(f"Failed to post to Facebook: {e}")
            return {"success": False, "error": str(e)}

    def get_facebook_feed(self, limit: int = 10) -> Dict[str, Any]:
        """Get Facebook feed"""
        try:
            response = requests.get(f"{self.mcp_url}/feed?limit={limit}")
            result = response.json()
            logger.info(f"Retrieved {result.get('count', 0)} Facebook posts")
            return result
        except Exception as e:
            logger.error(f"Failed to get Facebook feed: {e}")
            return {"success": False, "error": str(e)}

    def get_page_insights(self) -> Dict[str, Any]:
        """Get Facebook page insights"""
        try:
            response = requests.get(f"{self.mcp_url}/page_insights")
            result = response.json()
            logger.info(f"Facebook page insights: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to get page insights: {e}")
            return {"success": False, "error": str(e)}

    def post_video(self, video_url: str, description: str) -> Dict[str, Any]:
        """Post Facebook video"""
        try:
            payload = {
                "video_url": video_url,
                "description": description
            }
            response = requests.post(f"{self.mcp_url}/post_video", json=payload)
            result = response.json()
            logger.info(f"Facebook video posted: {result.get('video_id')}")
            return result
        except Exception as e:
            logger.error(f"Failed to post video: {e}")
            return {"success": False, "error": str(e)}
