#!/usr/bin/env python3
"""
Quick LinkedIn Post - Hello from AgenticSphere
Simple version with login first
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

POST_TEXT = "Hello from AgenticSphere"

def quick_post():
    session_path = Path('.linkedin_session_auto')

    print("=" * 60)
    print("Quick Post to Agentic Sphere")
    print("=" * 60)
    print(f"\nPost: {POST_TEXT}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            viewport={'width': 1280, 'height': 800}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            # First go to LinkedIn home
            print("Step 1: Opening LinkedIn...")
            page.goto('https://www.linkedin.com/', timeout=60000)
            time.sleep(5)

            # Check if logged in
            print("Step 2: Checking login status...")
            time.sleep(3)

            # Now go to company page
            print("Step 3: Going to Agentic Sphere page...")
            page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=60000)
            time.sleep(5)

            print("\nBrowser is open. Please:")
            print("1. Make sure you're logged in")
            print("2. Click 'Create a post' button")
            print(f"3. Type: {POST_TEXT}")
            print("4. Click 'Post' button")
            print("\nBrowser will stay open for 90 seconds...")

            time.sleep(90)

            print("\nDone! Closing browser...")
            return True

        except Exception as e:
            print(f"Error: {e}")
            print("\nBrowser will stay open for 90 seconds...")
            print("Please complete the post manually.")
            time.sleep(90)
            return True

        finally:
            browser.close()

if __name__ == '__main__':
    quick_post()
    print("\nCheck your Agentic Sphere page to verify!")
