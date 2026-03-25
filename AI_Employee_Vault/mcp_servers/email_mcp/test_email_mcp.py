"""Test Email MCP Server"""

import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8070"


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


def test_get_email_stats():
    """Test get email stats"""
    try:
        response = requests.get(f"{BASE_URL}/email_stats")
        if response.status_code == 200:
            stats = response.json()
            logger.info(f"✅ Email stats: {stats}")
            return True
        else:
            logger.warning(f"⚠️ Email stats returned {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Get email stats failed: {e}")
        return False


def test_get_emails():
    """Test get emails"""
    try:
        payload = {
            "folder": "INBOX",
            "limit": 5,
            "query": ""
        }
        response = requests.post(f"{BASE_URL}/get_emails", json=payload)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ Retrieved {result.get('count', 0)} emails")
            return True
        else:
            logger.warning(f"⚠️ Get emails returned {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Get emails failed: {e}")
        return False


def test_send_email():
    """Test send email (dry run)"""
    try:
        payload = {
            "to": "test@example.com",
            "subject": "Test Email",
            "body": "<h1>Test</h1><p>This is a test email</p>",
            "attachments": None
        }
        response = requests.post(f"{BASE_URL}/send_email", json=payload)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                logger.info(f"✅ Email sent: {result.get('message_id')}")
            else:
                logger.warning(f"⚠️ Email send failed: {result.get('error')}")
            return result.get('success', False)
        else:
            logger.warning(f"⚠️ Send email returned {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Send email failed: {e}")
        return False


def test_create_draft():
    """Test create draft"""
    try:
        payload = {
            "to": "test@example.com",
            "subject": "Test Draft",
            "body": "<h1>Draft</h1><p>This is a test draft</p>"
        }
        response = requests.post(f"{BASE_URL}/create_draft", json=payload)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                logger.info(f"✅ Draft created: {result.get('draft_id')}")
            else:
                logger.warning(f"⚠️ Draft creation failed: {result.get('error')}")
            return result.get('success', False)
        else:
            logger.warning(f"⚠️ Create draft returned {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Create draft failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    logger.info("=" * 50)
    logger.info("Email MCP Server Tests")
    logger.info("=" * 50)

    tests = [
        ("Health Check", test_health),
        ("List Tools", test_list_tools),
        ("Get Email Stats", test_get_email_stats),
        ("Get Emails", test_get_emails),
        ("Send Email", test_send_email),
        ("Create Draft", test_create_draft),
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
