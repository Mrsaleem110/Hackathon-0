"""
Twitter/X MCP Quick Start Script
Interactive setup wizard for Twitter integration
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def print_header(text: str):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_step(num: int, text: str):
    """Print step"""
    print(f"[{num}] {text}")


def check_dependencies():
    """Check if required packages are installed"""
    print_header("Checking Dependencies")

    required = ["tweepy", "requests", "python-dotenv", "fastapi", "uvicorn"]
    missing = []

    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (missing)")
            missing.append(package)

    if missing:
        print(f"\n⚠ Missing packages: {', '.join(missing)}")
        print("\nInstall with:")
        print(f"  pip install {' '.join(missing)}")
        return False

    print("\n✓ All dependencies installed")
    return True


def check_credentials():
    """Check if Twitter credentials are configured"""
    print_header("Checking Twitter Credentials")

    required_keys = [
        "TWITTER_API_KEY",
        "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_SECRET"
    ]

    missing = []
    for key in required_keys:
        value = os.getenv(key)
        if value and value != f"your_{key.lower()}_here":
            print(f"✓ {key}")
        else:
            print(f"✗ {key} (not configured)")
            missing.append(key)

    if missing:
        print(f"\n⚠ Missing credentials: {', '.join(missing)}")
        print("\nUpdate .env with your Twitter API credentials:")
        print("  1. Go to https://developer.twitter.com/en/portal/dashboard")
        print("  2. Create app or use existing")
        print("  3. Generate OAuth 1.0a credentials")
        print("  4. Copy to .env file")
        return False

    print("\n✓ All credentials configured")
    return True


def test_server():
    """Test Twitter MCP server"""
    print_header("Testing Twitter MCP Server")

    twitter_mcp_dir = Path(__file__).parent / "mcp_servers" / "twitter_mcp"

    print_step(1, "Running test suite (dry-run mode)...")
    print()

    try:
        result = subprocess.run(
            [sys.executable, "test_twitter_mcp.py"],
            cwd=twitter_mcp_dir,
            capture_output=True,
            text=True,
            timeout=30,
            env={**os.environ, "DRY_RUN": "true"}
        )

        print(result.stdout)

        if result.returncode == 0:
            print("✓ All tests passed!")
            return True
        else:
            print("✗ Tests failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("✗ Tests timed out")
        return False
    except Exception as e:
        print(f"✗ Error running tests: {e}")
        return False


def start_server():
    """Start Twitter MCP server"""
    print_header("Starting Twitter MCP Server")

    twitter_mcp_dir = Path(__file__).parent / "mcp_servers" / "twitter_mcp"
    port = os.getenv("TWITTER_MCP_PORT", "8071")

    print(f"Starting server on port {port}...")
    print("Press Ctrl+C to stop\n")

    try:
        subprocess.run(
            [sys.executable, "server.py"],
            cwd=twitter_mcp_dir,
            env={**os.environ}
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped")


def show_next_steps():
    """Show next steps"""
    print_header("Next Steps")

    print("""
1. Start Twitter MCP Server (in separate terminal):
   cd mcp_servers/twitter_mcp
   python server.py

2. Verify server is running:
   curl http://localhost:8071/health

3. Create a test post in Needs_Action/:
   Create file: Needs_Action/X_POST_test.md
   Content:
     # Twitter/X Post
     ## Content
     Testing Twitter integration! 🚀

4. Run orchestrator to process posts:
   python orchestrator.py

5. Check logs:
   tail -f Logs/2026-03-12.json

6. View completed posts:
   ls Done/X_POST_*

7. Generate social briefing:
   python social_briefing_generator.py

For more details, see:
  - TWITTER_SETUP.md
  - TWITTER_INTEGRATION_GUIDE.md
  - Plans/TWITTER_INTEGRATION_PLAN.md
    """)


def main():
    """Main entry point"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  Twitter/X MCP Integration - Quick Start".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")

    # Check dependencies
    if not check_dependencies():
        print("\n⚠ Please install missing dependencies and try again")
        return False

    # Check credentials
    if not check_credentials():
        print("\n⚠ Please configure Twitter credentials in .env and try again")
        return False

    # Test server
    if not test_server():
        print("\n⚠ Tests failed. Check configuration and try again")
        return False

    # Ask to start server
    print_header("Ready to Start")
    print("Twitter MCP server is ready to run!")
    print("\nOptions:")
    print("  1. Start server now")
    print("  2. Show next steps")
    print("  3. Exit")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == "1":
        start_server()
    elif choice == "2":
        show_next_steps()
    else:
        print("Exiting")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
