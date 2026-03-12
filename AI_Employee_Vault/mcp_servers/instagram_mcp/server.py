"""
Instagram MCP Server
Exposes Instagram posting and insights via MCP protocol
"""

import json
import logging
from typing import Any
from instagram_client import InstagramClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstagramMCPServer:
    """MCP server for Instagram operations"""

    def __init__(self):
        self.client = InstagramClient()

    def post_feed(self, caption: str, image_url: str = None, media_type: str = "IMAGE") -> dict:
        """Post to Instagram feed"""
        return self.client.post_feed(caption, image_url, media_type)

    def post_story(self, image_url: str) -> dict:
        """Post to Instagram story"""
        return self.client.post_story(image_url)

    def get_insights(self) -> dict:
        """Get Instagram account insights"""
        return self.client.get_insights()

    def handle_request(self, request: dict) -> dict:
        """Handle MCP request"""
        method = request.get("method")
        params = request.get("params", {})

        try:
            if method == "post_feed":
                return self.post_feed(**params)
            elif method == "post_story":
                return self.post_story(**params)
            elif method == "get_insights":
                return self.get_insights()
            else:
                return {"success": False, "error": f"Unknown method: {method}"}
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    server = InstagramMCPServer()
    print("Instagram MCP Server initialized")
    print("Available methods: post_feed, post_story, get_insights")
