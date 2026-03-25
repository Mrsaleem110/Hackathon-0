"""Email MCP Server - FastAPI server for email operations
Port: 8070
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

from email_client import EmailClient

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Email MCP Server", version="1.0.0")

# Initialize Email client
email_client = None

# Request/Response models
class SendEmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    attachments: Optional[List[str]] = None

class GetEmailsRequest(BaseModel):
    folder: str = "INBOX"
    limit: int = 10
    query: str = ""

class MarkAsReadRequest(BaseModel):
    message_id: str

class CreateDraftRequest(BaseModel):
    to: str
    subject: str
    body: str


@app.on_event("startup")
async def startup_event():
    """Initialize email client on startup"""
    global email_client
    try:
        email_client = EmailClient()
        logger.info("Email MCP Server started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize email client: {e}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Email MCP Server",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/send_email")
async def send_email(request: SendEmailRequest):
    """Send email via Gmail"""
    if not email_client:
        raise HTTPException(status_code=503, detail="Email client not initialized")

    try:
        result = email_client.send_email(
            to=request.to,
            subject=request.subject,
            body=request.body,
            attachments=request.attachments
        )
        return result
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_emails")
async def get_emails(request: GetEmailsRequest):
    """Get emails from folder"""
    if not email_client:
        raise HTTPException(status_code=503, detail="Email client not initialized")

    try:
        result = email_client.get_emails(
            folder=request.folder,
            limit=request.limit,
            query=request.query
        )
        return result
    except Exception as e:
        logger.error(f"Error getting emails: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mark_as_read")
async def mark_as_read(request: MarkAsReadRequest):
    """Mark email as read"""
    if not email_client:
        raise HTTPException(status_code=503, detail="Email client not initialized")

    try:
        result = email_client.mark_as_read(request.message_id)
        return result
    except Exception as e:
        logger.error(f"Error marking email as read: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_draft")
async def create_draft(request: CreateDraftRequest):
    """Create email draft"""
    if not email_client:
        raise HTTPException(status_code=503, detail="Email client not initialized")

    try:
        result = email_client.create_draft(
            to=request.to,
            subject=request.subject,
            body=request.body
        )
        return result
    except Exception as e:
        logger.error(f"Error creating draft: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/email_stats")
async def get_email_stats():
    """Get email statistics"""
    if not email_client:
        raise HTTPException(status_code=503, detail="Email client not initialized")

    try:
        result = email_client.get_email_stats()
        return result
    except Exception as e:
        logger.error(f"Error getting email stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools():
    """List available MCP tools"""
    return {
        "tools": [
            {
                "name": "send_email",
                "description": "Send email via Gmail",
                "method": "POST",
                "endpoint": "/send_email"
            },
            {
                "name": "get_emails",
                "description": "Get emails from folder",
                "method": "POST",
                "endpoint": "/get_emails"
            },
            {
                "name": "mark_as_read",
                "description": "Mark email as read",
                "method": "POST",
                "endpoint": "/mark_as_read"
            },
            {
                "name": "create_draft",
                "description": "Create email draft",
                "method": "POST",
                "endpoint": "/create_draft"
            },
            {
                "name": "get_email_stats",
                "description": "Get email statistics",
                "method": "GET",
                "endpoint": "/email_stats"
            }
        ]
    }


if __name__ == "__main__":
    port = int(os.getenv('EMAIL_MCP_PORT', 8070))
    uvicorn.run(app, host="0.0.0.0", port=port)
