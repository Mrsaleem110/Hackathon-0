"""
Social Media Briefing Generator
Queries Twitter MCP for engagement data and generates weekly social summary
"""

import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SocialBriefingGenerator:
    """Generate social media briefing from Twitter MCP"""

    def __init__(self, twitter_mcp_url: str = "http://localhost:8071"):
        """
        Initialize social briefing generator

        Args:
            twitter_mcp_url: URL of Twitter MCP server
        """
        self.twitter_mcp_url = twitter_mcp_url
        self.briefings_dir = Path(__file__).parent / "Briefings"
        self.briefings_dir.mkdir(exist_ok=True)

    def query_twitter_mcp(self, endpoint: str, payload: dict) -> Optional[Dict[str, Any]]:
        """
        Query Twitter MCP server

        Args:
            endpoint: Tool endpoint (e.g., 'get_user_timeline_summary')
            payload: Request payload

        Returns:
            Response dict or None on error
        """
        try:
            url = f"{self.twitter_mcp_url}/tools/{endpoint}"
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            logger.warning(f"Twitter MCP server not running at {self.twitter_mcp_url}")
            return None
        except Exception as e:
            logger.error(f"Error querying Twitter MCP: {e}")
            return None

    def get_timeline_summary(self, days: int = 7) -> Optional[Dict[str, Any]]:
        """Get timeline summary from Twitter MCP"""
        return self.query_twitter_mcp(
            "get_user_timeline_summary",
            {"days": days}
        )

    def get_mentions(self, since_days: int = 7) -> Optional[Dict[str, Any]]:
        """Get mentions from Twitter MCP"""
        return self.query_twitter_mcp(
            "get_mentions",
            {"since_days": since_days}
        )

    def get_engagement_summary(self) -> Optional[Dict[str, Any]]:
        """Get engagement summary from Twitter MCP"""
        return self.query_twitter_mcp(
            "get_engagement_summary",
            {"tweet_id": None}
        )

    def format_social_section(self, days: int = 7) -> str:
        """
        Format social media section for briefing

        Args:
            days: Number of days to summarize

        Returns:
            Formatted markdown section
        """
        section = f"## Social Media (Twitter/X)\n\n"
        section += f"**Period**: Last {days} days\n"
        section += f"**Generated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"

        # Get timeline summary
        timeline = self.get_timeline_summary(days=days)
        if timeline and timeline.get("success"):
            section += "### Posting Activity\n\n"
            section += f"- **Tweets Posted**: {timeline.get('tweets_count', 0)}\n"
            section += f"- **Total Likes**: {timeline.get('total_likes', 0)}\n"
            section += f"- **Total Retweets**: {timeline.get('total_retweets', 0)}\n"
            section += f"- **Total Replies**: {timeline.get('total_replies', 0)}\n"
            section += f"- **Avg Likes/Tweet**: {timeline.get('avg_likes', 0)}\n\n"

            # Top tweet
            if timeline.get("top_tweet"):
                top = timeline["top_tweet"]
                section += "### Top Performing Tweet\n\n"
                section += f"> {top['text']}\n\n"
                section += f"- **Likes**: {top['likes']}\n"
                section += f"- **Retweets**: {top['retweets']}\n"
                section += f"- **Posted**: {top['created_at']}\n\n"
        else:
            section += "### Posting Activity\n\n"
            section += "No posting data available (Twitter MCP not running)\n\n"

        # Get mentions
        mentions = self.get_mentions(since_days=days)
        if mentions and mentions.get("success"):
            mention_count = mentions.get("count", 0)
            section += "### Mentions & Engagement\n\n"
            section += f"- **New Mentions**: {mention_count}\n"

            if mentions.get("mentions"):
                section += "- **Recent Mentions**:\n"
                for mention in mentions["mentions"][:5]:
                    section += f"  - @{mention['author']}: {mention['text'][:80]}...\n"
                section += "\n"
        else:
            section += "### Mentions & Engagement\n\n"
            section += "No mention data available\n\n"

        # Get engagement summary
        engagement = self.get_engagement_summary()
        if engagement and engagement.get("success"):
            summary = engagement.get("summary", {})
            section += "### Overall Engagement\n\n"
            section += f"- **Total Tweets (recent)**: {summary.get('total_tweets', 0)}\n"
            section += f"- **Total Likes**: {summary.get('total_likes', 0)}\n"
            section += f"- **Total Retweets**: {summary.get('total_retweets', 0)}\n"
            section += f"- **Avg Likes/Tweet**: {summary.get('avg_likes_per_tweet', 0)}\n\n"

        return section

    def generate_weekly_briefing(self) -> str:
        """
        Generate complete weekly social briefing

        Returns:
            Formatted briefing markdown
        """
        briefing = "# Weekly Social Media Briefing\n\n"
        briefing += f"**Generated**: {datetime.utcnow().isoformat()}\n"
        briefing += f"**Period**: Last 7 days\n\n"

        briefing += self.format_social_section(days=7)

        briefing += "---\n\n"
        briefing += "## Recommendations\n\n"

        # Get timeline for recommendations
        timeline = self.get_timeline_summary(days=7)
        if timeline and timeline.get("success"):
            tweets_count = timeline.get("tweets_count", 0)
            avg_likes = timeline.get("avg_likes", 0)

            if tweets_count == 0:
                briefing += "- 📝 **Increase posting frequency** - No tweets this week\n"
            elif tweets_count < 3:
                briefing += "- 📝 **Post more regularly** - Only {tweets_count} tweets this week\n"
            elif avg_likes < 5:
                briefing += "- 💡 **Improve content quality** - Average engagement is low\n"
            else:
                briefing += "- ✅ **Good posting cadence** - Keep up the momentum\n"

            # Check for top performer
            if timeline.get("top_tweet"):
                top = timeline["top_tweet"]
                briefing += f"- 🎯 **Replicate success** - Top tweet got {top['likes']} likes\n"

        briefing += "- 🔄 **Monitor mentions** - Respond to community engagement\n"
        briefing += "- 📊 **Track trends** - Share relevant industry insights\n\n"

        return briefing

    def save_weekly_briefing(self) -> Path:
        """
        Generate and save weekly social briefing

        Returns:
            Path to saved briefing file
        """
        briefing = self.generate_weekly_briefing()

        # Generate filename with date
        today = datetime.utcnow().strftime("%Y-%m-%d")
        filename = f"Social_X_Weekly_{today}.md"
        filepath = self.briefings_dir / filename

        with open(filepath, "w") as f:
            f.write(briefing)

        logger.info(f"Saved weekly social briefing to {filepath}")
        return filepath

    def append_to_ceo_briefing(self, ceo_briefing_path: Path) -> bool:
        """
        Append social section to existing CEO briefing

        Args:
            ceo_briefing_path: Path to CEO briefing file

        Returns:
            True if successful
        """
        try:
            social_section = self.format_social_section(days=7)

            # Read existing briefing
            with open(ceo_briefing_path, "r") as f:
                content = f.read()

            # Check if social section already exists
            if "## Social Media (Twitter/X)" in content:
                logger.info("Social section already in briefing, skipping")
                return True

            # Append social section
            with open(ceo_briefing_path, "a") as f:
                f.write("\n" + social_section)

            logger.info(f"Appended social section to {ceo_briefing_path}")
            return True

        except Exception as e:
            logger.error(f"Error appending to CEO briefing: {e}")
            return False


def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("Social Media Briefing Generator")
    logger.info("=" * 60)

    generator = SocialBriefingGenerator()

    # Generate weekly briefing
    logger.info("\nGenerating weekly social briefing...")
    briefing_path = generator.save_weekly_briefing()
    logger.info(f"✓ Saved to {briefing_path}")

    # Try to append to CEO briefing
    ceo_briefing_dir = Path(__file__).parent / "Briefings"
    ceo_briefing_files = list(ceo_briefing_dir.glob("CEO_Weekly_*.md"))

    if ceo_briefing_files:
        latest_ceo_briefing = sorted(ceo_briefing_files)[-1]
        logger.info(f"\nAppending to CEO briefing: {latest_ceo_briefing.name}")
        if generator.append_to_ceo_briefing(latest_ceo_briefing):
            logger.info("✓ Successfully appended social section")
        else:
            logger.warning("✗ Failed to append to CEO briefing")
    else:
        logger.info("No CEO briefing found, skipping append")

    logger.info("\n" + "=" * 60)
    logger.info("Done!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
