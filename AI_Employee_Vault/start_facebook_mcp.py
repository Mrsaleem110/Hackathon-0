#!/usr/bin/env python3
"""Start Facebook MCP Server on port 8078"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run
from mcp_servers.facebook_mcp.server import app
import uvicorn

if __name__ == "__main__":
    print("Starting Facebook MCP Server on port 8078...")
    uvicorn.run(app, host="0.0.0.0", port=8078)
