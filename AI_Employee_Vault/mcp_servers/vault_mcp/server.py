"""Vault MCP Server - FastAPI server for vault operations
Port: 8072
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

from vault_client import VaultClient

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Vault MCP Server", version="1.0.0")

# Initialize Vault client
vault_client = None

# Request/Response models
class CreateTaskRequest(BaseModel):
    title: str
    description: str
    folder: str = "Needs_Action"

class ListTasksRequest(BaseModel):
    folder: str = "Needs_Action"
    status: Optional[str] = None

class UpdateTaskRequest(BaseModel):
    task_id: str
    updates: Dict[str, Any]

class MoveTaskRequest(BaseModel):
    task_id: str
    from_folder: str
    to_folder: str


@app.on_event("startup")
async def startup_event():
    """Initialize vault client on startup"""
    global vault_client
    try:
        vault_path = os.getenv('VAULT_PATH', '.')
        vault_client = VaultClient(vault_path)
        logger.info("Vault MCP Server started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize vault client: {e}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Vault MCP Server",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/create_task")
async def create_task(request: CreateTaskRequest):
    """Create a new task"""
    if not vault_client:
        raise HTTPException(status_code=503, detail="Vault client not initialized")

    try:
        result = vault_client.create_task(
            title=request.title,
            description=request.description,
            folder=request.folder
        )
        return result
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/list_tasks")
async def list_tasks(request: ListTasksRequest):
    """List tasks in folder"""
    if not vault_client:
        raise HTTPException(status_code=503, detail="Vault client not initialized")

    try:
        result = vault_client.list_tasks(
            folder=request.folder,
            status=request.status
        )
        return result
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update_task")
async def update_task(request: UpdateTaskRequest):
    """Update task"""
    if not vault_client:
        raise HTTPException(status_code=503, detail="Vault client not initialized")

    try:
        result = vault_client.update_task(
            task_id=request.task_id,
            updates=request.updates
        )
        return result
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/move_task")
async def move_task(request: MoveTaskRequest):
    """Move task between folders"""
    if not vault_client:
        raise HTTPException(status_code=503, detail="Vault client not initialized")

    try:
        result = vault_client.move_task(
            task_id=request.task_id,
            from_folder=request.from_folder,
            to_folder=request.to_folder
        )
        return result
    except Exception as e:
        logger.error(f"Error moving task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/vault_stats")
async def get_vault_stats():
    """Get vault statistics"""
    if not vault_client:
        raise HTTPException(status_code=503, detail="Vault client not initialized")

    try:
        result = vault_client.get_vault_stats()
        return result
    except Exception as e:
        logger.error(f"Error getting vault stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools():
    """List available MCP tools"""
    return {
        "tools": [
            {
                "name": "create_task",
                "description": "Create a new task",
                "method": "POST",
                "endpoint": "/create_task"
            },
            {
                "name": "list_tasks",
                "description": "List tasks in folder",
                "method": "POST",
                "endpoint": "/list_tasks"
            },
            {
                "name": "update_task",
                "description": "Update task",
                "method": "POST",
                "endpoint": "/update_task"
            },
            {
                "name": "move_task",
                "description": "Move task between folders",
                "method": "POST",
                "endpoint": "/move_task"
            },
            {
                "name": "get_vault_stats",
                "description": "Get vault statistics",
                "method": "GET",
                "endpoint": "/vault_stats"
            }
        ]
    }


if __name__ == "__main__":
    port = int(os.getenv('VAULT_MCP_PORT', 8072))
    uvicorn.run(app, host="0.0.0.0", port=port)
