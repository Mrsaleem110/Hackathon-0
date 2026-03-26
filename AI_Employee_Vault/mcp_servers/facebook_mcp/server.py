"""
Facebook MCP Server - FastAPI
Exposes Facebook posting and insights via MCP protocol
Port: 8078
"""

import os
import logging
from datetime import datetime
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from .facebook_client import FacebookClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Facebook MCP Server", version="1.0.0")
facebook_client = FacebookClient(dry_run=True)

class PostFeedRequest(BaseModel):
    message: str
    link: Optional[str] = None
    picture: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

class PostVideoRequest(BaseModel):
    video_url: str
    title: str
    description: str

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "facebook_mcp",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/post_feed")
async def post_feed(request: PostFeedRequest):
    """Post to Facebook page feed"""
    try:
        result = facebook_client.post_feed(
            message=request.message,
            link=request.link,
            picture=request.picture,
            name=request.name,
            description=request.description
        )
        return result
    except Exception as e:
        logger.error(f"Error posting to feed: {e}")
        return {"success": False, "error": str(e)}

@app.post("/post_video")
async def post_video(request: PostVideoRequest):
    """Post video to Facebook page"""
    try:
        result = facebook_client.post_video(
            video_url=request.video_url,
            title=request.title,
            description=request.description
        )
        return result
    except Exception as e:
        logger.error(f"Error posting video: {e}")
        return {"success": False, "error": str(e)}

@app.get("/get_page_insights")
async def get_page_insights():
    """Get Facebook page insights"""
    try:
        result = facebook_client.get_page_insights()
        return result
    except Exception as e:
        logger.error(f"Error getting insights: {e}")
        return {"success": False, "error": str(e)}

@app.get("/get_feed")
async def get_feed(limit: int = 10):
    """Get recent posts from Facebook feed"""
    try:
        result = facebook_client.get_feed(limit=limit)
        return result
    except Exception as e:
        logger.error(f"Error getting feed: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    port = int(os.getenv('FACEBOOK_MCP_PORT', 8078))
    uvicorn.run(app, host="0.0.0.0", port=port)
