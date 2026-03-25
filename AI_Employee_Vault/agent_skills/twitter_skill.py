"""Twitter Agent Skill"""

import logging
from typing import Dict, Any, Optional, List
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterSkill:
    """Twitter operations skill"""

    def __init__(self, mcp_url: str = "http://localhost:8071"):
        """Initialize Twitter skill"""
        self.mcp_url = mcp_url
        self.name = "twitter_skill"
        self.description = "Post tweets and manage Twitter engagement"

    def post_tweet(self, text: str, media_urls: Optional[List[str]] = None, reply_to: Optional[str] = None) -> Dict[str, Any]:
        """Post tweet"""
        try:
            payload = {
                "text": text,
                "media_urls": media_urls or [],
                "reply_to": reply_to
            }
            response = requests.post(f"{self.mcp_url}/post_tweet", json=payload)
            result = response.json()
            logger.info(f"Tweet posted: {result.get('tweet_id')}")
            return result
        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            return {"success": False, "error": str(e)}

    def get_timeline(self, limit: int = 10) -> Dict[str, Any]:
        """Get Twitter timeline"""
        try:
            response = requests.get(f"{self.mcp_url}/timeline?limit={limit}")
            result = response.json()
            logger.info(f"Retrieved {result.get('count', 0)} tweets")
            return result
        except Exception as e:
            logger.error(f"Failed to get timeline: {e}")
            return {"success": False, "error": str(e)}

    def get_tweet_stats(self, tweet_id: str) -> Dict[str, Any]:
        """Get tweet statistics"""
        try:
            response = requests.get(f"{self.mcp_url}/tweet_stats/{tweet_id}")
            result = response.json()
            logger.info(f"Tweet stats for {tweet_id}: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to get tweet stats: {e}")
            return {"success": False, "error": str(e)}

    def retweet(self, tweet_id: str) -> Dict[str, Any]:
        """Retweet"""
        try:
            payload = {"tweet_id": tweet_id}
            response = requests.post(f"{self.mcp_url}/retweet", json=payload)
            result = response.json()
            logger.info(f"Retweeted: {tweet_id}")
            return result
        except Exception as e:
            logger.error(f"Failed to retweet: {e}")
            return {"success": False, "error": str(e)}
