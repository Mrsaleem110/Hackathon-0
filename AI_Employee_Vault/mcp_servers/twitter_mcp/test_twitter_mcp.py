"""
Twitter/X MCP Server - Test Suite
Tests all MCP tools in dry-run mode
"""

import os
import sys
import json
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from twitter_client import TwitterClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_client_initialization():
    """Test Twitter client initialization"""
    logger.info("=" * 60)
    logger.info("TEST 1: Client Initialization")
    logger.info("=" * 60)

    try:
        client = TwitterClient(dry_run=True)
        logger.info("✓ Client initialized successfully")
        logger.info(f"  Authenticated user ID: {client.user_id}")
        logger.info(f"  Username: {client.user.data.username}")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to initialize client: {e}")
        return False


def test_post_tweet(client: TwitterClient):
    """Test posting a single tweet"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 2: Post Single Tweet (Dry-Run)")
    logger.info("=" * 60)

    try:
        result = client.post_tweet(
            text="🚀 Testing Twitter MCP integration! #AI #Automation"
        )
        logger.info(f"✓ Result: {json.dumps(result, indent=2)}")
        return result.get("success", False)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        return False


def test_post_thread(client: TwitterClient):
    """Test posting a thread"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 3: Post Thread (Dry-Run)")
    logger.info("=" * 60)

    try:
        tweets = [
            "Thread: AI Employee Vault - Gold Tier Integration 🧵",
            "Part 1: We've integrated Twitter/X API v2 with our MCP server",
            "Part 2: Now we can post, search mentions, and track engagement",
            "Part 3: All actions are logged and require human approval for sensitive posts",
            "Part 4: This enables autonomous social media management with safety guardrails ✨"
        ]

        result = client.post_thread(tweets)
        logger.info(f"✓ Result: {json.dumps(result, indent=2)}")
        return result.get("success", False)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        return False


def test_get_mentions(client: TwitterClient):
    """Test fetching mentions"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 4: Get Mentions (Last 7 Days)")
    logger.info("=" * 60)

    try:
        result = client.get_mentions(since_days=7)
        if result.get("success"):
            logger.info(f"✓ Found {result.get('count', 0)} mentions")
            if result.get("mentions"):
                logger.info("  Sample mentions:")
                for mention in result["mentions"][:3]:
                    logger.info(f"    - @{mention['author']}: {mention['text'][:60]}...")
        else:
            logger.info(f"✓ Query completed: {result.get('error', 'No mentions')}")
        return result.get("success", False)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        return False


def test_get_engagement_summary(client: TwitterClient):
    """Test fetching engagement summary"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 5: Get Engagement Summary (Recent Tweets)")
    logger.info("=" * 60)

    try:
        result = client.get_engagement_summary()
        if result.get("success"):
            summary = result.get("summary", {})
            logger.info(f"✓ Engagement Summary:")
            logger.info(f"  Total tweets: {summary.get('total_tweets', 0)}")
            logger.info(f"  Total likes: {summary.get('total_likes', 0)}")
            logger.info(f"  Total retweets: {summary.get('total_retweets', 0)}")
            logger.info(f"  Avg likes/tweet: {summary.get('avg_likes_per_tweet', 0)}")
        else:
            logger.info(f"✓ Query completed: {result.get('error', 'No data')}")
        return result.get("success", False)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        return False


def test_get_timeline_summary(client: TwitterClient):
    """Test fetching timeline summary"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 6: Get Timeline Summary (Last 7 Days)")
    logger.info("=" * 60)

    try:
        result = client.get_user_timeline_summary(days=7)
        if result.get("success"):
            logger.info(f"✓ Timeline Summary:")
            logger.info(f"  Period: {result.get('period_days', 0)} days")
            logger.info(f"  Tweets: {result.get('tweets_count', 0)}")
            logger.info(f"  Total likes: {result.get('total_likes', 0)}")
            logger.info(f"  Total retweets: {result.get('total_retweets', 0)}")
            logger.info(f"  Avg likes: {result.get('avg_likes', 0)}")
            if result.get("top_tweet"):
                logger.info(f"  Top tweet: {result['top_tweet']['text'][:60]}...")
        else:
            logger.info(f"✓ Query completed: {result.get('error', 'No data')}")
        return result.get("success", False)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        return False


def test_tweet_length_validation(client: TwitterClient):
    """Test tweet length validation"""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 7: Tweet Length Validation")
    logger.info("=" * 60)

    try:
        long_text = "x" * 300  # Exceeds 280 char limit
        result = client.post_tweet(text=long_text)
        if not result.get("success"):
            logger.info(f"✓ Correctly rejected long tweet: {result.get('error')}")
            return True
        else:
            logger.error("✗ Should have rejected long tweet")
            return False
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    logger.info("\n")
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║" + " " * 58 + "║")
    logger.info("║" + "  Twitter/X MCP Server - Test Suite".center(58) + "║")
    logger.info("║" + " " * 58 + "║")
    logger.info("╚" + "=" * 58 + "╝")

    # Initialize client
    if not test_client_initialization():
        logger.error("Failed to initialize client. Aborting tests.")
        return False

    client = TwitterClient(dry_run=True)

    # Run tests
    tests = [
        ("Post Tweet", lambda: test_post_tweet(client)),
        ("Post Thread", lambda: test_post_thread(client)),
        ("Get Mentions", lambda: test_get_mentions(client)),
        ("Get Engagement", lambda: test_get_engagement_summary(client)),
        ("Get Timeline", lambda: test_get_timeline_summary(client)),
        ("Length Validation", lambda: test_tweet_length_validation(client)),
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"Test '{test_name}' crashed: {e}")
            results[test_name] = False

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {test_name}")

    logger.info("=" * 60)
    logger.info(f"Results: {passed}/{total} tests passed")
    logger.info("=" * 60)

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
