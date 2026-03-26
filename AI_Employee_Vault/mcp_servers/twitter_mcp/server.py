"""
Twitter/X MCP Server
FastAPI server exposing Twitter tools via Model Context Protocol
Port: 8071
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, List
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from twitter_client import TwitterClient

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Twitter/X MCP Server",
    description="Model Context Protocol server for X API v2",
    version="1.0.0"
)

# Initialize Twitter client
try:
    twitter_client = TwitterClient()
    logger.info("Twitter client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Twitter client: {e}")
    twitter_client = None


# ============================================================================
# Request/Response Models
# ============================================================================

class PostTweetRequest(BaseModel):
    text: str
    in_reply_to: Optional[str] = None
    media_ids: Optional[List[str]] = None


class PostThreadRequest(BaseModel):
    tweets: List[str]


class GetMentionsRequest(BaseModel):
    since_days: int = 7


class GetEngagementRequest(BaseModel):
    tweet_id: Optional[str] = None


class GetTimelineSummaryRequest(BaseModel):
    days: int = 7


# ============================================================================
# Logging Helper
# ============================================================================

def log_action(action_type: str, params: dict, result: dict):
    """Log action to /Logs/YYYY-MM-DD.json"""
    try:
        logs_dir = Path(__file__).parent.parent.parent / "Logs"
        logs_dir.mkdir(exist_ok=True)

        today = datetime.utcnow().strftime("%Y-%m-%d")
        log_file = logs_dir / f"{today}.json"

        # Read existing logs
        logs = []
        if log_file.exists():
            with open(log_file, "r") as f:
                logs = json.load(f)

        # Append new entry
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action_type": f"TWITTER_{action_type}",
            "params": params,
            "result": result
        }
        logs.append(entry)

        # Write back
        with open(log_file, "w") as f:
            json.dump(logs, f, indent=2)

        logger.info(f"Logged {action_type} to {log_file}")

    except Exception as e:
        logger.error(f"Failed to log action: {e}")


# ============================================================================
# HITL Approval Helper
# ============================================================================

def needs_approval(text: str, is_reply: bool = False) -> bool:
    """
    Determine if tweet needs human approval

    Rules:
    - Contains URLs (http://, https://)
    - Contains price/currency symbols ($, €, £, ₹)
    - Is a reply to another tweet
    """
    if is_reply:
        return True

    if any(url in text for url in ["http://", "https://", "bit.ly", "t.co"]):
        return True

    if any(symbol in text for symbol in ["$", "€", "£", "₹", "¥"]):
        return True

    return False


def create_approval_request(text: str, action_type: str, params: dict):
    """Create approval request in /Pending_Approval/"""
    try:
        approval_dir = Path(__file__).parent.parent.parent / "Pending_Approval"
        approval_dir.mkdir(exist_ok=True)

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"X_POST_{action_type}_{timestamp}.md"
        filepath = approval_dir / filename

        content = f"""# Twitter/X Post - Pending Approval

**Timestamp**: {datetime.utcnow().isoformat()}
**Action**: {action_type}
**Status**: PENDING_APPROVAL

## Content

{text}

## Parameters

```json
{json.dumps(params, indent=2)}
```

## Approval

- [ ] Approved
- [ ] Rejected

**Reviewer**:
**Review Date**:
**Notes**:
"""

        with open(filepath, "w") as f:
            f.write(content)

        logger.info(f"Created approval request: {filepath}")
        return str(filepath)

    except Exception as e:
        logger.error(f"Failed to create approval request: {e}")
        return None


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Twitter/X MCP Server",
        "port": 8071,
        "authenticated": twitter_client is not None
    }


# ============================================================================
# MCP Tools
# ============================================================================

@app.post("/tools/post_tweet")
async def post_tweet(request: PostTweetRequest):
    """
    Post a single tweet

    MCP Tool: post_tweet
    """
    if not twitter_client:
        raise HTTPException(status_code=503, detail="Twitter client not initialized")

    try:
        # Check if approval needed
        if needs_approval(request.text, is_reply=bool(request.in_reply_to)):
            approval_path = create_approval_request(
                request.text,
                "SINGLE",
                request.dict()
            )
            return {
                "success": False,
                "status": "PENDING_APPROVAL",
                "message": "Tweet requires human approval (contains links, prices, or is a reply)",
                "approval_request": approval_path
            }

        # Post tweet
        result = twitter_client.post_tweet(
            text=request.text,
            in_reply_to=request.in_reply_to,
            media_ids=request.media_ids
        )

        # Log action
        log_action("POST_TWEET", request.dict(), result)

        return result

    except Exception as e:
        logger.error(f"Error in post_tweet: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/post_thread")
async def post_thread(request: PostThreadRequest):
    """
    Post a thread of tweets

    MCP Tool: post_thread
    """
    if not twitter_client:
        raise HTTPException(status_code=503, detail="Twitter client not initialized")

    try:
        # Check if any tweet needs approval
        for i, text in enumerate(request.tweets):
            if needs_approval(text):
                approval_path = create_approval_request(
                    f"Tweet {i+1}/{len(request.tweets)}:\n{text}",
                    "THREAD",
                    {"tweets": request.tweets, "tweet_index": i}
                )
                return {
                    "success": False,
                    "status": "PENDING_APPROVAL",
                    "message": f"Tweet {i+1} requires approval",
                    "approval_request": approval_path
                }

        # Post thread
        result = twitter_client.post_thread(request.tweets)

        # Log action
        log_action("POST_THREAD", {"count": len(request.tweets)}, result)

        return result

    except Exception as e:
        logger.error(f"Error in post_thread: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/get_mentions")
async def get_mentions(request: GetMentionsRequest):
    """
    Get recent mentions

    MCP Tool: get_mentions
    """
    if not twitter_client:
        raise HTTPException(status_code=503, detail="Twitter client not initialized")

    try:
        result = twitter_client.get_mentions(since_days=request.since_days)

        # Log action
        log_action("GET_MENTIONS", {"since_days": request.since_days}, result)

        return result

    except Exception as e:
        logger.error(f"Error in get_mentions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/get_engagement_summary")
async def get_engagement_summary(request: GetEngagementRequest):
    """
    Get engagement metrics for tweet(s)

    MCP Tool: get_engagement_summary
    """
    if not twitter_client:
        raise HTTPException(status_code=503, detail="Twitter client not initialized")

    try:
        result = twitter_client.get_engagement_summary(tweet_id=request.tweet_id)

        # Log action
        log_action("GET_ENGAGEMENT", {"tweet_id": request.tweet_id}, result)

        return result

    except Exception as e:
        logger.error(f"Error in get_engagement_summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/get_user_timeline_summary")
async def get_user_timeline_summary(request: GetTimelineSummaryRequest):
    """
    Get weekly engagement summary

    MCP Tool: get_user_timeline_summary
    """
    if not twitter_client:
        raise HTTPException(status_code=503, detail="Twitter client not initialized")

    try:
        result = twitter_client.get_user_timeline_summary(days=request.days)

        # Log action
        log_action("GET_TIMELINE_SUMMARY", {"days": request.days}, result)

        return result

    except Exception as e:
        logger.error(f"Error in get_user_timeline_summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# MCP Protocol Discovery
# ============================================================================

@app.get("/mcp/tools")
async def list_tools():
    """
    List available MCP tools
    """
    return {
        "tools": [
            {
                "name": "post_tweet",
                "description": "Post a single tweet",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Tweet content (max 280 chars)"},
                        "in_reply_to": {"type": "string", "description": "Tweet ID to reply to (optional)"},
                        "media_ids": {"type": "array", "items": {"type": "string"}, "description": "Media IDs (optional)"}
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "post_thread",
                "description": "Post a thread of tweets",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "tweets": {"type": "array", "items": {"type": "string"}, "description": "List of tweet texts"}
                    },
                    "required": ["tweets"]
                }
            },
            {
                "name": "get_mentions",
                "description": "Get recent mentions of the account",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "since_days": {"type": "integer", "description": "Look back N days (default 7, max 30)"}
                    }
                }
            },
            {
                "name": "get_engagement_summary",
                "description": "Get engagement metrics for tweet(s)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "tweet_id": {"type": "string", "description": "Specific tweet ID, or null for recent tweets"}
                    }
                }
            },
            {
                "name": "get_user_timeline_summary",
                "description": "Get weekly engagement summary",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "days": {"type": "integer", "description": "Number of days to look back (default 7)"}
                    }
                }
            }
        ]
    }


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("TWITTER_MCP_PORT", 8071))
    logger.info(f"Starting Twitter MCP Server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
