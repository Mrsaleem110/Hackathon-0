#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check LinkedIn Access
Verify if you have admin access to post on company page
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_access():
    """Check if user has access to post on company page"""

    print("=" * 60)
    print("LinkedIn Access Check")
    print("=" * 60)

    session_path = ".linkedin_session"

    with sync_playwright() as p:
        print("Loading LinkedIn session...")
        browser = p.chromium.launch_persistent_context(
            session_path,
            headless=False,
            viewport={'width': 1280, 'height': 800}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            # Go to LinkedIn home
            print("Opening LinkedIn...")
            page.goto('https://www.linkedin.com/', timeout=30000)
            time.sleep(3)

            # Check if logged in
            current_url = page.url
            print(f"Current URL: {current_url}")

            if 'login' in current_url or 'authwall' in current_url:
                print("\n❌ NOT LOGGED IN")
                print("Please login manually in the browser window")
                time.sleep(60)
                browser.close()
                return False

            print("✓ Logged in successfully")

            # Go to company page
            print("\nGoing to Agentic Sphere page...")
            page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=30000)
            time.sleep(3)

            # Take screenshot
            page.screenshot(path='linkedin_access_check.png')
            print("Screenshot saved: linkedin_access_check.png")

            # Check page content
            page_text = page.inner_text('body')

            print("\n" + "="*60)
            print("ACCESS CHECK RESULTS")
            print("="*60)

            if 'Start a post' in page_text or 'Create a post' in page_text:
                print("✅ YOU HAVE ADMIN ACCESS!")
                print("You can post on this company page")
            else:
                print("❌ NO ADMIN ACCESS")
                print("You cannot post on this company page")
                print("\nYou need to:")
                print("1. Be added as an admin by the page owner")
                print("2. Or use your personal profile to post")

            print("\nBrowser will stay open for 30 seconds...")
            time.sleep(30)
            browser.close()

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(30)
            browser.close()
            return False

if __name__ == '__main__':
    check_access()
