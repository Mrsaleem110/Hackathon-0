"""
Facebook MCP Server
Exposes Facebook posting and insights via MCP protocol
"""

import json
import logging
from typing import Any
from .facebook_client import FacebookClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FacebookMCPServer:
    """MCP server for Facebook operations"""

    def __init__(self):
        self.client = FacebookClient()

    def post_feed(self, message: str, link: str = None, picture: str = None, name: str = None, description: str = None) -> dict:
        """Post to Facebook page feed"""
        return self.client.post_feed(message, link, picture, name, description)

    def post_video(self, video_url: str, title: str, description: str) -> dict:
        """Post video to Facebook page"""
        return self.client.post_video(video_url, title, description)

    def get_page_insights(self) -> dict:
        """Get Facebook page insights"""
        return self.client.get_page_insights()

    def get_feed(self, limit: int = 10) -> dict:
        """Get recent posts from Facebook feed"""
        return self.client.get_feed(limit)

    def handle_request(self, request: dict) -> dict:
        """Handle MCP request"""
        method = request.get("method")
        params = request.get("params", {})

        try:
            if method == "post_feed":
                return self.post_feed(**params)
            elif method == "post_video":
                return self.post_video(**params)
            elif method == "get_page_insights":
                return self.get_page_insights()
            elif method == "get_feed":
                return self.get_feed(**params)
            else:
                return {"success": False, "error": f"Unknown method: {method}"}
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    server = FacebookMCPServer()
    print("Facebook MCP Server initialized")
    print("Available methods: post_feed, post_video, get_page_insights, get_feed")
