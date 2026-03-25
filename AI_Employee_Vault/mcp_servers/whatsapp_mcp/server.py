"""WhatsApp MCP Server - FastAPI server for WhatsApp operations
Port: 8073
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

from whatsapp_client import WhatsAppClient

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="WhatsApp MCP Server", version="1.0.0")

# Initialize WhatsApp client
whatsapp_client = None

# Request/Response models
class SendMessageRequest(BaseModel):
    phone: str
    message: str
    media_url: Optional[str] = None

class GetMessagesRequest(BaseModel):
    phone: Optional[str] = None
    limit: int = 10

class MarkAsReadRequest(BaseModel):
    message_id: str


@app.on_event("startup")
async def startup_event():
    """Initialize WhatsApp client on startup"""
    global whatsapp_client
    try:
        whatsapp_client = WhatsAppClient()
        logger.info("WhatsApp MCP Server started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize WhatsApp client: {e}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "WhatsApp MCP Server",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/send_message")
async def send_message(request: SendMessageRequest):
    """Send WhatsApp message"""
    if not whatsapp_client:
        raise HTTPException(status_code=503, detail="WhatsApp client not initialized")

    try:
        result = whatsapp_client.send_message(
            phone=request.phone,
            message=request.message,
            media_url=request.media_url
        )
        return result
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_messages")
async def get_messages(request: GetMessagesRequest):
    """Get WhatsApp messages"""
    if not whatsapp_client:
        raise HTTPException(status_code=503, detail="WhatsApp client not initialized")

    try:
        result = whatsapp_client.get_messages(
            phone=request.phone,
            limit=request.limit
        )
        return result
    except Exception as e:
        logger.error(f"Error getting messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mark_as_read")
async def mark_as_read(request: MarkAsReadRequest):
    """Mark message as read"""
    if not whatsapp_client:
        raise HTTPException(status_code=503, detail="WhatsApp client not initialized")

    try:
        result = whatsapp_client.mark_as_read(request.message_id)
        return result
    except Exception as e:
        logger.error(f"Error marking message as read: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/contact_list")
async def get_contact_list():
    """Get WhatsApp contact list"""
    if not whatsapp_client:
        raise HTTPException(status_code=503, detail="WhatsApp client not initialized")

    try:
        result = whatsapp_client.get_contact_list()
        return result
    except Exception as e:
        logger.error(f"Error getting contact list: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/whatsapp_stats")
async def get_whatsapp_stats():
    """Get WhatsApp statistics"""
    if not whatsapp_client:
        raise HTTPException(status_code=503, detail="WhatsApp client not initialized")

    try:
        result = whatsapp_client.get_whatsapp_stats()
        return result
    except Exception as e:
        logger.error(f"Error getting WhatsApp stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools():
    """List available MCP tools"""
    return {
        "tools": [
            {
                "name": "send_message",
                "description": "Send WhatsApp message",
                "method": "POST",
                "endpoint": "/send_message"
            },
            {
                "name": "get_messages",
                "description": "Get WhatsApp messages",
                "method": "POST",
                "endpoint": "/get_messages"
            },
            {
                "name": "mark_as_read",
                "description": "Mark message as read",
                "method": "POST",
                "endpoint": "/mark_as_read"
            },
            {
                "name": "get_contact_list",
                "description": "Get WhatsApp contact list",
                "method": "GET",
                "endpoint": "/contact_list"
            },
            {
                "name": "get_whatsapp_stats",
                "description": "Get WhatsApp statistics",
                "method": "GET",
                "endpoint": "/whatsapp_stats"
            }
        ]
    }


if __name__ == "__main__":
    port = int(os.getenv('WHATSAPP_MCP_PORT', 8073))
    uvicorn.run(app, host="0.0.0.0", port=port)
