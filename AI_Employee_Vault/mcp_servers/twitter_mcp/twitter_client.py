"""
Twitter/X API v2 Client
Handles authentication, posting, mentions, and engagement metrics
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import tweepy
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class TwitterClient:
    """X API v2 client using Bearer Token (tweepy)"""

    def __init__(self, dry_run: bool = False):
        """
        Initialize Twitter client with Bearer Token credentials

        Args:
            dry_run: If True, simulate actions without posting
        """
        self.dry_run = dry_run or os.getenv("DRY_RUN", "false").lower() == "true"

        # Bearer Token credentials (preferred method)
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

        # Fallback to OAuth 1.0a if Bearer Token not available
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_secret = os.getenv("TWITTER_ACCESS_SECRET")

        # Validate credentials - Bearer Token preferred, OAuth 1.0a as fallback
        if self.bearer_token:
            logger.info("Using Bearer Token authentication")
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                wait_on_rate_limit=True
            )
        elif all([self.api_key, self.api_secret, self.access_token, self.access_secret]):
            logger.info("Using OAuth 1.0a authentication")
            self.client = tweepy.Client(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_secret,
                wait_on_rate_limit=True
            )
        else:
            raise ValueError("Missing Twitter credentials in .env. Provide either TWITTER_BEARER_TOKEN or OAuth 1.0a credentials")

        # Get authenticated user info
        try:
            self.user = self.client.get_me()
            self.user_id = self.user.data.id
            logger.info(f"Authenticated as @{self.user.data.username}")
        except Exception as e:
            logger.error(f"Failed to authenticate: {e}")
            raise

    def post_tweet(
        self,
        text: str,
        in_reply_to: Optional[str] = None,
        media_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Post a single tweet

        Args:
            text: Tweet content (max 280 chars)
            in_reply_to: Tweet ID to reply to (optional)
            media_ids: List of media IDs to attach (optional)

        Returns:
            Dict with tweet_id, text, created_at, or error
        """
        try:
            if len(text) > 280:
                return {
                    "success": False,
                    "error": f"Tweet too long: {len(text)} chars (max 280)"
                }

            if self.dry_run:
                logger.info(f"[DRY-RUN] Would post tweet: {text}")
                return {
                    "success": True,
                    "tweet_id": "dry_run_123456789",
                    "text": text,
                    "created_at": datetime.utcnow().isoformat(),
                    "dry_run": True
                }

            # Post tweet
            response = self.client.create_tweet(
                text=text,
                in_reply_to_tweet_id=in_reply_to,
                media_ids=media_ids
            )

            tweet_id = response.data["id"]
            logger.info(f"Posted tweet {tweet_id}: {text[:50]}...")

            return {
                "success": True,
                "tweet_id": tweet_id,
                "text": text,
                "created_at": datetime.utcnow().isoformat(),
                "in_reply_to": in_reply_to,
                "media_ids": media_ids
            }

        except tweepy.TweepyException as e:
            logger.error(f"Tweepy error posting tweet: {e}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return {"success": False, "error": str(e)}

    def post_thread(self, tweets: List[str]) -> Dict[str, Any]:
        """
        Post a thread of tweets sequentially

        Args:
            tweets: List of tweet texts (each max 280 chars)

        Returns:
            Dict with thread_ids, results, or error
        """
        try:
            if not tweets:
                return {"success": False, "error": "No tweets provided"}

            if self.dry_run:
                logger.info(f"[DRY-RUN] Would post thread of {len(tweets)} tweets")
                return {
                    "success": True,
                    "thread_ids": [f"dry_run_{i}" for i in range(len(tweets))],
                    "count": len(tweets),
                    "dry_run": True
                }

            thread_ids = []
            in_reply_to = None

            for i, text in enumerate(tweets):
                if len(text) > 280:
                    return {
                        "success": False,
                        "error": f"Tweet {i} too long: {len(text)} chars"
                    }

                response = self.client.create_tweet(
                    text=text,
                    in_reply_to_tweet_id=in_reply_to
                )

                tweet_id = response.data["id"]
                thread_ids.append(tweet_id)
                in_reply_to = tweet_id

                # Small delay between posts
                time.sleep(1)

            logger.info(f"Posted thread of {len(tweets)} tweets")

            return {
                "success": True,
                "thread_ids": thread_ids,
                "count": len(tweets),
                "created_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error posting thread: {e}")
            return {"success": False, "error": str(e)}

    def get_mentions(self, since_days: int = 7) -> Dict[str, Any]:
        """
        Get recent mentions of the authenticated user

        Args:
            since_days: Look back N days (max 30 for free tier)

        Returns:
            Dict with mentions list or error
        """
        try:
            since_days = min(since_days, 30)  # Free tier limit
            start_time = datetime.utcnow() - timedelta(days=since_days)

            # Search for mentions
            query = f"@{self.user.data.username} -is:retweet"

            response = self.client.search_recent_tweets(
                query=query,
                start_time=start_time,
                max_results=100,
                tweet_fields=["created_at", "public_metrics", "author_id"],
                expansions=["author_id"],
                user_fields=["username"]
            )

            if not response.data:
                logger.info(f"No mentions found in last {since_days} days")
                return {
                    "success": True,
                    "mentions": [],
                    "count": 0
                }

            # Build user lookup
            users = {u.id: u.username for u in response.includes["users"]} if response.includes else {}

            mentions = []
            for tweet in response.data:
                mentions.append({
                    "tweet_id": tweet.id,
                    "text": tweet.text,
                    "author": users.get(tweet.author_id, "unknown"),
                    "author_id": tweet.author_id,
                    "created_at": tweet.created_at.isoformat(),
                    "likes": tweet.public_metrics["like_count"],
                    "retweets": tweet.public_metrics["retweet_count"],
                    "replies": tweet.public_metrics["reply_count"]
                })

            logger.info(f"Found {len(mentions)} mentions in last {since_days} days")

            return {
                "success": True,
                "mentions": mentions,
                "count": len(mentions),
                "since_days": since_days
            }

        except Exception as e:
            logger.error(f"Error fetching mentions: {e}")
            return {"success": False, "error": str(e)}

    def get_engagement_summary(self, tweet_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get engagement metrics for a tweet or recent tweets

        Args:
            tweet_id: Specific tweet ID, or None for recent tweets

        Returns:
            Dict with engagement metrics
        """
        try:
            if tweet_id:
                # Get specific tweet
                response = self.client.get_tweet(
                    id=tweet_id,
                    tweet_fields=["created_at", "public_metrics"]
                )

                if not response.data:
                    return {"success": False, "error": f"Tweet {tweet_id} not found"}

                tweet = response.data
                return {
                    "success": True,
                    "tweet_id": tweet.id,
                    "text": tweet.text[:100] + "..." if len(tweet.text) > 100 else tweet.text,
                    "likes": tweet.public_metrics["like_count"],
                    "retweets": tweet.public_metrics["retweet_count"],
                    "replies": tweet.public_metrics["reply_count"],
                    "impressions": tweet.public_metrics.get("impression_count", 0),
                    "created_at": tweet.created_at.isoformat()
                }
            else:
                # Get recent tweets from user
                response = self.client.get_users_tweets(
                    id=self.user_id,
                    max_results=10,
                    tweet_fields=["created_at", "public_metrics"]
                )

                if not response.data:
                    return {
                        "success": True,
                        "tweets": [],
                        "summary": "No recent tweets"
                    }

                tweets = []
                total_likes = 0
                total_retweets = 0
                total_replies = 0

                for tweet in response.data:
                    likes = tweet.public_metrics["like_count"]
                    retweets = tweet.public_metrics["retweet_count"]
                    replies = tweet.public_metrics["reply_count"]

                    total_likes += likes
                    total_retweets += retweets
                    total_replies += replies

                    tweets.append({
                        "tweet_id": tweet.id,
                        "text": tweet.text[:80] + "..." if len(tweet.text) > 80 else tweet.text,
                        "likes": likes,
                        "retweets": retweets,
                        "replies": replies,
                        "created_at": tweet.created_at.isoformat()
                    })

                avg_likes = total_likes / len(tweets) if tweets else 0

                return {
                    "success": True,
                    "tweets": tweets,
                    "summary": {
                        "total_tweets": len(tweets),
                        "total_likes": total_likes,
                        "total_retweets": total_retweets,
                        "total_replies": total_replies,
                        "avg_likes_per_tweet": round(avg_likes, 1)
                    }
                }

        except Exception as e:
            logger.error(f"Error fetching engagement: {e}")
            return {"success": False, "error": str(e)}

    def get_user_timeline_summary(self, days: int = 7) -> Dict[str, Any]:
        """
        Get weekly engagement summary for user's tweets

        Args:
            days: Number of days to look back

        Returns:
            Dict with timeline summary
        """
        try:
            start_time = datetime.utcnow() - timedelta(days=days)

            response = self.client.get_users_tweets(
                id=self.user_id,
                start_time=start_time,
                max_results=100,
                tweet_fields=["created_at", "public_metrics"]
            )

            if not response.data:
                return {
                    "success": True,
                    "period_days": days,
                    "tweets_count": 0,
                    "summary": "No tweets in period"
                }

            tweets = response.data
            total_likes = sum(t.public_metrics["like_count"] for t in tweets)
            total_retweets = sum(t.public_metrics["retweet_count"] for t in tweets)
            total_replies = sum(t.public_metrics["reply_count"] for t in tweets)

            # Find top tweet
            top_tweet = max(
                tweets,
                key=lambda t: t.public_metrics["like_count"] + t.public_metrics["retweet_count"]
            )

            return {
                "success": True,
                "period_days": days,
                "tweets_count": len(tweets),
                "total_likes": total_likes,
                "total_retweets": total_retweets,
                "total_replies": total_replies,
                "avg_likes": round(total_likes / len(tweets), 1) if tweets else 0,
                "top_tweet": {
                    "text": top_tweet.text[:100] + "..." if len(top_tweet.text) > 100 else top_tweet.text,
                    "likes": top_tweet.public_metrics["like_count"],
                    "retweets": top_tweet.public_metrics["retweet_count"],
                    "created_at": top_tweet.created_at.isoformat()
                },
                "summary": f"{len(tweets)} tweets, {total_likes} likes, {total_retweets} retweets"
            }

        except Exception as e:
            logger.error(f"Error fetching timeline summary: {e}")
            return {"success": False, "error": str(e)}
