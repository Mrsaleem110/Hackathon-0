"""LinkedIn MCP Server - FastAPI server for LinkedIn operations
Port: 8075
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

from linkedin_client import LinkedInClient

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="LinkedIn MCP Server", version="1.0.0")

# Initialize LinkedIn client
linkedin_client = None

# Request/Response models
class PostContentRequest(BaseModel):
    text: str
    media_url: Optional[str] = None
    visibility: str = "PUBLIC"

class SendMessageRequest(BaseModel):
    recipient_id: str
    message: str

class GetEngagementStatsRequest(BaseModel):
    post_id: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize LinkedIn client on startup"""
    global linkedin_client
    try:
        linkedin_client = LinkedInClient()
        logger.info("LinkedIn MCP Server started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize LinkedIn client: {e}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "LinkedIn MCP Server",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/post_content")
async def post_content(request: PostContentRequest):
    """Post content to LinkedIn"""
    if not linkedin_client:
        raise HTTPException(status_code=503, detail="LinkedIn client not initialized")

    try:
        result = linkedin_client.post_content(
            text=request.text,
            media_url=request.media_url,
            visibility=request.visibility
        )
        return result
    except Exception as e:
        logger.error(f"Error posting content: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/feed")
async def get_feed(limit: int = 10):
    """Get LinkedIn feed"""
    if not linkedin_client:
        raise HTTPException(status_code=503, detail="LinkedIn client not initialized")

    try:
        result = linkedin_client.get_feed(limit=limit)
        return result
    except Exception as e:
        logger.error(f"Error getting feed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/profile_stats")
async def get_profile_stats():
    """Get LinkedIn profile statistics"""
    if not linkedin_client:
        raise HTTPException(status_code=503, detail="LinkedIn client not initialized")

    try:
        result = linkedin_client.get_profile_stats()
        return result
    except Exception as e:
        logger.error(f"Error getting profile stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/send_message")
async def send_message(request: SendMessageRequest):
    """Send LinkedIn message"""
    if not linkedin_client:
        raise HTTPException(status_code=503, detail="LinkedIn client not initialized")

    try:
        result = linkedin_client.send_message(
            recipient_id=request.recipient_id,
            message=request.message
        )
        return result
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/engagement_stats")
async def get_engagement_stats(request: GetEngagementStatsRequest):
    """Get engagement statistics"""
    if not linkedin_client:
        raise HTTPException(status_code=503, detail="LinkedIn client not initialized")

    try:
        result = linkedin_client.get_engagement_stats(post_id=request.post_id)
        return result
    except Exception as e:
        logger.error(f"Error getting engagement stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools():
    """List available MCP tools"""
    return {
        "tools": [
            {
                "name": "post_content",
                "description": "Post content to LinkedIn",
                "method": "POST",
                "endpoint": "/post_content"
            },
            {
                "name": "get_feed",
                "description": "Get LinkedIn feed",
                "method": "GET",
                "endpoint": "/feed"
            },
            {
                "name": "get_profile_stats",
                "description": "Get LinkedIn profile statistics",
                "method": "GET",
                "endpoint": "/profile_stats"
            },
            {
                "name": "send_message",
                "description": "Send LinkedIn message",
                "method": "POST",
                "endpoint": "/send_message"
            },
            {
                "name": "get_engagement_stats",
                "description": "Get engagement statistics",
                "method": "POST",
                "endpoint": "/engagement_stats"
            }
        ]
    }


if __name__ == "__main__":
    port = int(os.getenv('LINKEDIN_MCP_PORT', 8075))
    uvicorn.run(app, host="0.0.0.0", port=port)
