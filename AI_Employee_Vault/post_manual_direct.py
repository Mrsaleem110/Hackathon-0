#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct LinkedIn Post - Manual Submission
Opens LinkedIn with post content ready, you click Post
"""
import time
from playwright.sync_api import sync_playwright

POST_TEXT = "hello from Agentic Sphere FTE"
COMPANY_PAGE = "https://www.linkedin.com/company/agentic-sphere/"

def post_manually():
    print("=" * 70)
    print("LINKEDIN POST - MANUAL SUBMISSION")
    print("=" * 70)
    print(f"\nPost content: {POST_TEXT}")
    print(f"Target: Agentic Sphere Company Page\n")
    print("Instructions:")
    print("1. Browser will open to Agentic Sphere page")
    print("2. Log in if needed")
    print("3. Click 'Create a post' button")
    print("4. Paste the post text (already copied to clipboard)")
    print("5. Click 'Post' button")
    print("6. Close browser when done\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            print("Opening Agentic Sphere page...")
            page.goto(COMPANY_PAGE, timeout=30000)
            time.sleep(3)

            print("Page loaded. Please log in and create the post manually.")
            print(f"\nPost text to use:\n{POST_TEXT}\n")
            print("Press Ctrl+C or close the browser when done...")

            # Keep browser open
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nClosing browser...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

    print("\n" + "=" * 70)
    print("Done! Post should be published to Agentic Sphere page.")
    print("=" * 70)

if __name__ == '__main__':
    post_manually()
