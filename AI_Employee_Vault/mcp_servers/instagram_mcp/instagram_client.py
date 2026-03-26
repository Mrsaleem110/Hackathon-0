"""
Instagram API Client
Handles posting, stories, and engagement metrics
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


class InstagramClient:
    """Instagram Graph API client"""

    def __init__(self, dry_run: bool = False):
        """
        Initialize Instagram client with Graph API credentials

        Args:
            dry_run: If True, simulate actions without posting
        """
        self.dry_run = dry_run or os.getenv("DRY_RUN", "false").lower() == "true"

        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.business_account_id = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
        self.api_version = "v18.0"
        self.base_url = f"https://graph.instagram.com/{self.api_version}"

        if not self.access_token or not self.business_account_id:
            if not dry_run:
                raise ValueError("Missing Instagram credentials: INSTAGRAM_ACCESS_TOKEN or INSTAGRAM_BUSINESS_ACCOUNT_ID")
            logger.warning("Running in dry-run mode without credentials")

        logger.info(f"Instagram client initialized for account {self.business_account_id}")

    def post_feed(
        self,
        caption: str,
        image_url: Optional[str] = None,
        media_type: str = "IMAGE"
    ) -> Dict[str, Any]:
        """
        Post to Instagram feed

        Args:
            caption: Post caption
            image_url: URL of image to post
            media_type: IMAGE or VIDEO

        Returns:
            Dict with post_id or error
        """
        try:
            if self.dry_run:
                logger.info(f"[DRY-RUN] Would post to Instagram: {caption[:50]}...")
                return {
                    "success": True,
                    "post_id": "dry_run_123456789",
                    "caption": caption,
                    "created_at": datetime.utcnow().isoformat(),
                    "dry_run": True
                }

            # Create media container
            container_payload = {
                "media_type": media_type,
                "caption": caption,
            }

            if image_url:
                container_payload["image_url"] = image_url

            container_payload["access_token"] = self.access_token

            response = requests.post(
                f"{self.base_url}/{self.business_account_id}/media",
                data=container_payload,
                timeout=10
            )

            if response.status_code != 200:
                error_msg = response.text
                logger.warning(f"Instagram API error: {error_msg}")

                # Check for common API restrictions
                if "RATE_LIMIT" in error_msg or "rate_limit" in error_msg:
                    return {
                        "success": False,
                        "error": "Rate limit exceeded. Please try again later.",
                        "status": "rate_limited"
                    }
                elif "PERMISSION" in error_msg or "permission" in error_msg:
                    return {
                        "success": False,
                        "error": "Permission denied. Account may need approval or paid promotion.",
                        "status": "permission_denied"
                    }
                elif "INVALID_TOKEN" in error_msg or "invalid_token" in error_msg:
                    return {
                        "success": False,
                        "error": "Invalid or expired access token.",
                        "status": "invalid_token"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to create media container: {error_msg}",
                        "status": "api_error"
                    }

            container_id = response.json()["id"]

            # Publish media
            publish_payload = {
                "creation_id": container_id,
                "access_token": self.access_token
            }

            publish_response = requests.post(
                f"{self.base_url}/{self.business_account_id}/media_publish",
                data=publish_payload,
                timeout=10
            )

            if publish_response.status_code != 200:
                error_msg = publish_response.text
                logger.warning(f"Instagram publish error: {error_msg}")
                return {
                    "success": False,
                    "error": f"Failed to publish: {error_msg}",
                    "status": "publish_failed"
                }

            post_id = publish_response.json()["id"]
            logger.info(f"Posted to Instagram: {post_id}")

            return {
                "success": True,
                "post_id": post_id,
                "caption": caption,
                "created_at": datetime.utcnow().isoformat()
            }

        except requests.exceptions.Timeout:
            logger.error("Instagram API request timeout")
            return {"success": False, "error": "Request timeout", "status": "timeout"}
        except Exception as e:
            logger.error(f"Error posting to Instagram: {e}")
            return {"success": False, "error": str(e), "status": "error"}

    def post_story(self, image_url: str) -> Dict[str, Any]:
        """
        Post to Instagram story

        Args:
            image_url: URL of image for story

        Returns:
            Dict with story_id or error
        """
        try:
            if self.dry_run:
                logger.info(f"[DRY-RUN] Would post story to Instagram")
                return {
                    "success": True,
                    "story_id": "dry_run_story_123",
                    "created_at": datetime.utcnow().isoformat(),
                    "dry_run": True
                }

            payload = {
                "media_type": "IMAGE",
                "image_url": image_url,
                "access_token": self.access_token
            }

            response = requests.post(
                f"{self.base_url}/{self.business_account_id}/media",
                data=payload
            )

            if response.status_code != 200:
                return {"success": False, "error": response.text}

            story_id = response.json()["id"]
            logger.info(f"Posted story to Instagram: {story_id}")

            return {
                "success": True,
                "story_id": story_id,
                "created_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error posting story: {e}")
            return {"success": False, "error": str(e)}

    def get_insights(self) -> Dict[str, Any]:
        """
        Get account insights and metrics

        Returns:
            Dict with engagement metrics
        """
        try:
            params = {
                "fields": "impressions,reach,profile_views,follower_count",
                "access_token": self.access_token
            }

            response = requests.get(
                f"{self.base_url}/{self.business_account_id}/insights",
                params=params
            )

            if response.status_code != 200:
                return {"success": False, "error": response.text}

            data = response.json()["data"]
            insights = {item["name"]: item["values"][0]["value"] for item in data}

            logger.info(f"Retrieved Instagram insights: {insights}")

            return {
                "success": True,
                "insights": insights,
                "retrieved_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error fetching insights: {e}")
            return {"success": False, "error": str(e)}
