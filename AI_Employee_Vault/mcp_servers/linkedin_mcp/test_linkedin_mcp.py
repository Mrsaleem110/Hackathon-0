"""Test LinkedIn MCP Server"""

import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8075"


def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        logger.info("✅ Health check passed")
        return True
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return False


def test_list_tools():
    """Test list tools endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/tools")
        assert response.status_code == 200
        tools = response.json()
        logger.info(f"✅ Available tools: {len(tools['tools'])}")
        return True
    except Exception as e:
        logger.error(f"❌ List tools failed: {e}")
        return False


def test_profile_stats():
    """Test get profile stats"""
    try:
        response = requests.get(f"{BASE_URL}/profile_stats")
        if response.status_code == 200:
            stats = response.json()
            logger.info(f"✅ Profile stats: {stats}")
            return True
        else:
            logger.warning(f"⚠️ Profile stats returned {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Get profile stats failed: {e}")
        return False


def test_get_feed():
    """Test get feed"""
    try:
        response = requests.get(f"{BASE_URL}/feed?limit=5")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ Retrieved {result.get('count', 0)} feed items")
            return True
        else:
            logger.warning(f"⚠️ Get feed returned {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Get feed failed: {e}")
        return False


def test_post_content():
    """Test post content"""
    try:
        payload = {
            "text": "Test post from LinkedIn MCP server",
            "media_url": None,
            "visibility": "PUBLIC"
        }
        response = requests.post(f"{BASE_URL}/post_content", json=payload)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                logger.info(f"✅ Post created: {result.get('post_id')}")
            else:
                logger.warning(f"⚠️ Post creation failed: {result.get('error')}")
            return result.get('success', False)
        else:
            logger.warning(f"⚠️ Post content returned {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Post content failed: {e}")
        return False


def test_engagement_stats():
    """Test get engagement stats"""
    try:
        payload = {"post_id": None}
        response = requests.post(f"{BASE_URL}/engagement_stats", json=payload)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ Engagement stats: {result}")
            return True
        else:
            logger.warning(f"⚠️ Engagement stats returned {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Get engagement stats failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    logger.info("=" * 50)
    logger.info("LinkedIn MCP Server Tests")
    logger.info("=" * 50)

    tests = [
        ("Health Check", test_health),
        ("List Tools", test_list_tools),
        ("Profile Stats", test_profile_stats),
        ("Get Feed", test_get_feed),
        ("Post Content", test_post_content),
        ("Engagement Stats", test_engagement_stats),
    ]

    results = []
    for test_name, test_func in tests:
        logger.info(f"\nRunning: {test_name}")
        result = test_func()
        results.append((test_name, result))

    logger.info("\n" + "=" * 50)
    logger.info("Test Summary")
    logger.info("=" * 50)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    logger.info(f"Passed: {passed}/{total}")

    for test_name, result in results:
        status = "✅" if result else "❌"
        logger.info(f"{status} {test_name}")


if __name__ == "__main__":
    run_all_tests()
