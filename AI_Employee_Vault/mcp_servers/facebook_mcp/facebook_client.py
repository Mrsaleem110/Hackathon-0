"""
Facebook API Client
Handles posting, page management, and engagement metrics
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class FacebookClient:
    """Facebook Graph API client"""

    def __init__(self, dry_run: bool = False):
        """
        Initialize Facebook client with Graph API credentials

        Args:
            dry_run: If True, simulate actions without posting
        """
        self.dry_run = dry_run or os.getenv("DRY_RUN", "false").lower() == "true"

        self.access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.page_id = os.getenv("FACEBOOK_PAGE_ID")
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"

        if not self.access_token or not self.page_id:
            if not dry_run:
                raise ValueError("Missing Facebook credentials: FACEBOOK_ACCESS_TOKEN or FACEBOOK_PAGE_ID")
            logger.warning("Running in dry-run mode without credentials")

        logger.info(f"Facebook client initialized for page {self.page_id}")

    def post_feed(
        self,
        message: str,
        link: Optional[str] = None,
        picture: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Post to Facebook page feed

        Args:
            message: Post message
            link: URL to link to
            picture: Picture URL
            name: Link name
            description: Link description

        Returns:
            Dict with post_id or error
        """
        try:
            if self.dry_run:
                logger.info(f"[DRY-RUN] Would post to Facebook: {message[:50]}...")
                return {
                    "success": True,
                    "post_id": "dry_run_123456789",
                    "message": message,
                    "created_at": datetime.utcnow().isoformat(),
                    "dry_run": True
                }

            payload = {
                "message": message,
                "access_token": self.access_token
            }

            if link:
                payload["link"] = link
            if picture:
                payload["picture"] = picture
            if name:
                payload["name"] = name
            if description:
                payload["description"] = description

            response = requests.post(
                f"{self.base_url}/{self.page_id}/feed",
                data=payload,
                timeout=10
            )

            if response.status_code != 200:
                error_msg = response.text
                logger.warning(f"Facebook API error: {error_msg}")

                # Check for common API restrictions
                if "RATE_LIMIT" in error_msg or "rate_limit" in error_msg:
                    return {
                        "success": False,
                        "error": "Rate limit exceeded. Please try again later.",
                        "status": "rate_limited"
                    }
                elif "PERMISSION" in error_msg or "permission" in error_msg or "permission_error" in error_msg:
                    return {
                        "success": False,
                        "error": "Permission denied. Page may require paid promotion or account approval.",
                        "status": "permission_denied"
                    }
                elif "INVALID_TOKEN" in error_msg or "invalid_token" in error_msg:
                    return {
                        "success": False,
                        "error": "Invalid or expired access token.",
                        "status": "invalid_token"
                    }
                elif "INVALID_PARAM" in error_msg or "invalid_param" in error_msg:
                    return {
                        "success": False,
                        "error": "Invalid parameters. Check page ID and token.",
                        "status": "invalid_param"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to post: {error_msg}",
                        "status": "api_error"
                    }

            post_id = response.json()["id"]
            logger.info(f"Posted to Facebook: {post_id}")

            return {
                "success": True,
                "post_id": post_id,
                "message": message,
                "created_at": datetime.utcnow().isoformat()
            }

        except requests.exceptions.Timeout:
            logger.error("Facebook API request timeout")
            return {"success": False, "error": "Request timeout", "status": "timeout"}
        except Exception as e:
            logger.error(f"Error posting to Facebook: {e}")
            return {"success": False, "error": str(e), "status": "error"}

    def post_video(
        self,
        video_url: str,
        title: str,
        description: str
    ) -> Dict[str, Any]:
        """
        Post video to Facebook page

        Args:
            video_url: URL of video file
            title: Video title
            description: Video description

        Returns:
            Dict with video_id or error
        """
        try:
            if self.dry_run:
                logger.info(f"[DRY-RUN] Would post video to Facebook: {title}")
                return {
                    "success": True,
                    "video_id": "dry_run_video_123",
                    "created_at": datetime.utcnow().isoformat(),
                    "dry_run": True
                }

            payload = {
                "source": video_url,
                "title": title,
                "description": description,
                "access_token": self.access_token
            }

            response = requests.post(
                f"{self.base_url}/{self.page_id}/videos",
                data=payload
            )

            if response.status_code != 200:
                return {"success": False, "error": response.text}

            video_id = response.json()["id"]
            logger.info(f"Posted video to Facebook: {video_id}")

            return {
                "success": True,
                "video_id": video_id,
                "title": title,
                "created_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error posting video: {e}")
            return {"success": False, "error": str(e)}

    def get_page_insights(self) -> Dict[str, Any]:
        """
        Get page insights and metrics

        Returns:
            Dict with engagement metrics
        """
        try:
            params = {
                "fields": "impressions,reach,engaged_users,page_fans",
                "period": "day",
                "access_token": self.access_token
            }

            response = requests.get(
                f"{self.base_url}/{self.page_id}/insights",
                params=params
            )

            if response.status_code != 200:
                return {"success": False, "error": response.text}

            data = response.json()["data"]
            insights = {item["name"]: item["values"][0]["value"] for item in data}

            logger.info(f"Retrieved Facebook insights: {insights}")

            return {
                "success": True,
                "insights": insights,
                "retrieved_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error fetching insights: {e}")
            return {"success": False, "error": str(e)}

    def get_feed(self, limit: int = 10) -> Dict[str, Any]:
        """
        Get recent posts from page feed

        Args:
            limit: Number of posts to retrieve

        Returns:
            Dict with posts list
        """
        try:
            params = {
                "fields": "id,message,created_time,likes.summary(true).limit(0),comments.summary(true).limit(0)",
                "limit": limit,
                "access_token": self.access_token
            }

            response = requests.get(
                f"{self.base_url}/{self.page_id}/feed",
                params=params
            )

            if response.status_code != 200:
                return {"success": False, "error": response.text}

            posts = response.json()["data"]
            logger.info(f"Retrieved {len(posts)} posts from Facebook feed")

            return {
                "success": True,
                "posts": posts,
                "count": len(posts),
                "retrieved_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error fetching feed: {e}")
            return {"success": False, "error": str(e)}
