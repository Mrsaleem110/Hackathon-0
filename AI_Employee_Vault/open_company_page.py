#!/usr/bin/env python3
"""
LinkedIn - Open Company Page for Manual Post
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

COMPANY_URL = "https://www.linkedin.com/company/agentic-sphere/"

POST_TEXT = """🚀 Introducing Agentic Sphere

Your autonomous AI employee that works 24/7.

Agentic Sphere monitors your emails, messages, and opportunities - then takes intelligent action with your approval.

✓ Autonomous Decision Making
✓ Multi-Channel Integration (Gmail, WhatsApp, LinkedIn)
✓ Intelligent Planning with Claude AI
✓ Complete Audit Trail
✓ Human-in-the-Loop Control

The future of productivity is here.

#AI #Automation #AgenticSphere #FutureOfWork #Innovation"""

def open_and_post():
    """Open company page and help with posting"""

    print("=" * 70)
    print("LinkedIn - Agentic Sphere Company Page")
    print("=" * 70)
    print()

    session_path = Path('.linkedin_session_manual')

    if not session_path.exists():
        print("ERROR: No existing session found.")
        print("Please run the manual login script first.")
        return False

    try:
        with sync_playwright() as p:
            print("Launching browser...")
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                viewport={'width': 1280, 'height': 900}
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            print("Navigating to Agentic Sphere company page...")
            page.goto(COMPANY_URL, timeout=30000)
            time.sleep(2)

            print()
            print("=" * 70)
            print("INSTRUCTIONS:")
            print("=" * 70)
            print()
            print("1. Click the 'Create post' button on the page")
            print("2. Paste this text in the editor:")
            print()
            print(POST_TEXT)
            print()
            print("3. Click 'Post' to publish")
            print()
            print("=" * 70)
            print()
            print("Keeping browser open... Press Ctrl+C to close when done.")
            print()

            # Keep browser open
            while True:
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nClosing browser...")
        browser.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == '__main__':
    open_and_post()
