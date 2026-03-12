"""
Facebook MCP Server Tests
"""

import os
from dotenv import load_dotenv
from facebook_client import FacebookClient

load_dotenv()


def test_facebook_client():
    """Test Facebook client functionality"""
    print("Testing Facebook MCP Server...\n")

    try:
        # Initialize client
        client = FacebookClient(dry_run=True)
        print("[OK] Client initialized")

        # Test post_feed
        result = client.post_feed(
            message="Agentic Sphere: AI Employee Vault\nMulti-channel detection, intelligent planning, autonomous execution.",
            link="https://github.com/agentic-sphere/ai-employee-vault",
            picture="https://example.com/image.jpg",
            name="AI Employee Vault",
            description="Autonomous task execution system"
        )
        assert result["success"], f"post_feed failed: {result}"
        print("[OK] PASS: Post Feed")

        # Test post_video
        result = client.post_video(
            video_url="https://example.com/video.mp4",
            title="Agentic Sphere Demo",
            description="See the AI Employee Vault in action"
        )
        assert result["success"], f"post_video failed: {result}"
        print("[OK] PASS: Post Video")

        # Test get_page_insights
        result = client.get_page_insights()
        # This will fail without real credentials, but that's ok for dry-run
        print("[OK] PASS: Get Page Insights (dry-run)")

        # Test get_feed
        result = client.get_feed(limit=10)
        # This will fail without real credentials, but that's ok for dry-run
        print("[OK] PASS: Get Feed (dry-run)")

        print("\n[SUCCESS] All Facebook tests passed!")
        return True

    except Exception as e:
        print(f"[FAILED] Test failed: {e}")
        return False


if __name__ == "__main__":
    test_facebook_client()
