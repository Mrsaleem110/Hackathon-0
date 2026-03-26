#!/usr/bin/env python3
"""
LinkedIn Post Command - Simple CLI Tool
Usage: python post.py "Your message here"
"""
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def post_to_linkedin(message):
    """Post to Agentic Sphere LinkedIn page"""

    session_path = Path('.linkedin_session_auto')

    print(f"\nPosting: {message}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            viewport={'width': 1280, 'height': 800}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        print("Opening LinkedIn...")
        page.goto('https://www.linkedin.com/company/agentic-sphere/')

        print("\nBrowser is open. Please:")
        print("1. Login if needed")
        print("2. Click 'Create a post'")
        print(f"3. Type: {message}")
        print("4. Click 'Post'\n")
        print("Browser will stay open for 3 minutes...\n")

        time.sleep(180)
        browser.close()
        print("Done!")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = "Hello from AgenticSphere"

    post_to_linkedin(message)
