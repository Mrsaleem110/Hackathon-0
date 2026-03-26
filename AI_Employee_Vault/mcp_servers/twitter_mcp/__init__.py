"""
Twitter/X MCP Server Package
Model Context Protocol server for X API v2 integration
"""

__version__ = "1.0.0"
__author__ = "AI Employee Vault"
__description__ = "Twitter/X MCP Server for autonomous social media management"

from .twitter_client import TwitterClient

__all__ = ["TwitterClient"]
