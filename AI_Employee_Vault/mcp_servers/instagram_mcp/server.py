"""
Instagram MCP Server - FastAPI
Exposes Instagram posting and insights via MCP protocol
Port: 8077
"""

import os
import logging
from datetime import datetime
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from .instagram_client import InstagramClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Instagram MCP Server", version="1.0.0")
instagram_client = InstagramClient(dry_run=True)

class PostFeedRequest(BaseModel):
    caption: str
    image_url: Optional[str] = None
    media_type: str = "IMAGE"

class PostStoryRequest(BaseModel):
    image_url: str

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "instagram_mcp",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/post_feed")
async def post_feed(request: PostFeedRequest):
    """Post to Instagram feed"""
    try:
        result = instagram_client.post_feed(
            caption=request.caption,
            image_url=request.image_url,
            media_type=request.media_type
        )
        return result
    except Exception as e:
        logger.error(f"Error posting to feed: {e}")
        return {"success": False, "error": str(e)}

@app.post("/post_story")
async def post_story(request: PostStoryRequest):
    """Post to Instagram story"""
    try:
        result = instagram_client.post_story(image_url=request.image_url)
        return result
    except Exception as e:
        logger.error(f"Error posting story: {e}")
        return {"success": False, "error": str(e)}

@app.get("/get_insights")
async def get_insights():
    """Get Instagram account insights"""
    try:
        result = instagram_client.get_insights()
        return result
    except Exception as e:
        logger.error(f"Error getting insights: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    port = int(os.getenv('INSTAGRAM_MCP_PORT', 8077))
    uvicorn.run(app, host="0.0.0.0", port=port)
