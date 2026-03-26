#!/usr/bin/env python3
"""
Simple LinkedIn Post Helper
Opens browser and waits for you to post manually
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def simple_post(message="Hello from AgenticSphere"):
    """Simple helper - opens LinkedIn and waits"""

    session_path = Path('.linkedin_session_auto')

    print("=" * 60)
    print("LinkedIn Post Helper")
    print("=" * 60)
    print(f"\nMessage to post: {message}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            viewport={'width': 1280, 'height': 800}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            # Open Agentic Sphere page
            print("Opening Agentic Sphere LinkedIn page...")
            page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=60000)
            time.sleep(5)

            print("\n" + "=" * 60)
            print("MANUAL STEPS:")
            print("=" * 60)
            print("\n1. Make sure you're logged in")
            print("2. Look for 'Create a post' or 'Start a post' button")
            print("3. Click it")
            print(f"4. Type: {message}")
            print("5. Click 'Post' button")
            print("\nBrowser will stay open for 2 minutes...")
            print("=" * 60)

            # Wait 2 minutes
            time.sleep(120)

            print("\nClosing browser...")
            browser.close()

        except Exception as e:
            print(f"\nError: {e}")
            print("Browser will stay open for 2 minutes anyway...")
            time.sleep(120)
            browser.close()

if __name__ == '__main__':
    simple_post()
    print("\nDone! Check your Agentic Sphere page.")
