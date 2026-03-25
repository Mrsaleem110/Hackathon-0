"""Test Vault MCP Server"""

import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8072"


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


def test_vault_stats():
    """Test get vault stats"""
    try:
        response = requests.get(f"{BASE_URL}/vault_stats")
        if response.status_code == 200:
            stats = response.json()
            logger.info(f"✅ Vault stats: {stats}")
            return True
        else:
            logger.warning(f"⚠️ Vault stats returned {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Get vault stats failed: {e}")
        return False


def test_create_task():
    """Test create task"""
    try:
        payload = {
            "title": "Test Task",
            "description": "This is a test task",
            "folder": "Needs_Action"
        }
        response = requests.post(f"{BASE_URL}/create_task", json=payload)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                logger.info(f"✅ Task created: {result.get('task_id')}")
            else:
                logger.warning(f"⚠️ Task creation failed: {result.get('error')}")
            return result.get('success', False)
        else:
            logger.warning(f"⚠️ Create task returned {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Create task failed: {e}")
        return False


def test_list_tasks():
    """Test list tasks"""
    try:
        payload = {
            "folder": "Needs_Action",
            "status": None
        }
        response = requests.post(f"{BASE_URL}/list_tasks", json=payload)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ Listed {result.get('count', 0)} tasks")
            return True
        else:
            logger.warning(f"⚠️ List tasks returned {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ List tasks failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    logger.info("=" * 50)
    logger.info("Vault MCP Server Tests")
    logger.info("=" * 50)

    tests = [
        ("Health Check", test_health),
        ("List Tools", test_list_tools),
        ("Vault Stats", test_vault_stats),
        ("Create Task", test_create_task),
        ("List Tasks", test_list_tasks),
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
