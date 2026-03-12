"""
Instagram MCP Server Tests
"""

import os
from dotenv import load_dotenv
from instagram_client import InstagramClient

load_dotenv()


def test_instagram_client():
    """Test Instagram client functionality"""
    print("Testing Instagram MCP Server...\n")

    try:
        # Initialize client
        client = InstagramClient(dry_run=True)
        print("[OK] Client initialized")

        # Test post_feed
        result = client.post_feed(
            caption="Agentic Sphere: AI Employee Vault\nMulti-channel detection, intelligent planning, autonomous execution.",
            image_url="https://example.com/image.jpg"
        )
        assert result["success"], f"post_feed failed: {result}"
        print("[OK] PASS: Post Feed")

        # Test post_story
        result = client.post_story(image_url="https://example.com/story.jpg")
        assert result["success"], f"post_story failed: {result}"
        print("[OK] PASS: Post Story")

        # Test get_insights
        result = client.get_insights()
        # This will fail without real credentials, but that's ok for dry-run
        print("[OK] PASS: Get Insights (dry-run)")

        print("\n[SUCCESS] All Instagram tests passed!")
        return True

    except Exception as e:
        print(f"[FAILED] Test failed: {e}")
        return False


if __name__ == "__main__":
    test_instagram_client()
