"""Test WhatsApp MCP Server"""

import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8073"


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


def test_whatsapp_stats():
    """Test get WhatsApp stats"""
    try:
        response = requests.get(f"{BASE_URL}/whatsapp_stats")
        if response.status_code == 200:
            stats = response.json()
            logger.info(f"✅ WhatsApp stats: {stats}")
            return True
        else:
            logger.warning(f"⚠️ WhatsApp stats returned {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Get WhatsApp stats failed: {e}")
        return False


def test_get_contact_list():
    """Test get contact list"""
    try:
        response = requests.get(f"{BASE_URL}/contact_list")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ Retrieved {result.get('count', 0)} contacts")
            return True
        else:
            logger.warning(f"⚠️ Get contact list returned {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Get contact list failed: {e}")
        return False


def test_send_message():
    """Test send message"""
    try:
        payload = {
            "phone": "+1234567890",
            "message": "Test message from MCP server",
            "media_url": None
        }
        response = requests.post(f"{BASE_URL}/send_message", json=payload)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                logger.info(f"✅ Message sent: {result.get('message_id')}")
            else:
                logger.warning(f"⚠️ Message send failed: {result.get('error')}")
            return result.get('success', False)
        else:
            logger.warning(f"⚠️ Send message returned {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Send message failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    logger.info("=" * 50)
    logger.info("WhatsApp MCP Server Tests")
    logger.info("=" * 50)

    tests = [
        ("Health Check", test_health),
        ("List Tools", test_list_tools),
        ("WhatsApp Stats", test_whatsapp_stats),
        ("Get Contact List", test_get_contact_list),
        ("Send Message", test_send_message),
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
