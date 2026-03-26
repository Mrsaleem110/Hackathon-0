#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Post - With Fresh Login
Handles login and posts to personal profile
Usage: python linkedin_post_fresh.py "Your message here"
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def post_with_login(message):
    """Post to LinkedIn with fresh login"""

    print("=" * 60)
    print("LinkedIn Post - Fresh Login")
    print("=" * 60)
    print(f"\nMessage: {message}\n")

    session_path = ".linkedin_session_fresh"

    with sync_playwright() as p:
        print("Opening browser...")
        browser = p.chromium.launch_persistent_context(
            session_path,
            headless=False,
            viewport={'width': 1280, 'height': 800}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            # Go to LinkedIn
            print("Opening LinkedIn...")
            page.goto('https://www.linkedin.com/', timeout=30000)
            time.sleep(3)

            # Check if we need to login
            current_url = page.url
            if 'login' in current_url or 'authwall' in current_url:
                print("\n⏳ Please login manually in the browser...")
                print("Waiting 60 seconds for you to login...\n")
                time.sleep(60)

                # Check again
                current_url = page.url
                if 'login' in current_url or 'authwall' in current_url:
                    print("❌ Still not logged in. Please try again.")
                    browser.close()
                    return False

            print("✓ Logged in successfully")

            # Go to feed
            print("\nGoing to LinkedIn feed...")
            page.goto('https://www.linkedin.com/feed/', timeout=30000)
            time.sleep(3)

            # Take screenshot
            page.screenshot(path='linkedin_feed_logged_in.png')
            print("Screenshot saved: linkedin_feed_logged_in.png")

            # Look for "Start a post" button
            print("\nLooking for 'Start a post' button...")

            # Try clicking the share box
            selectors = [
                'button.share-box-feed-entry__trigger',
                '.share-box-feed-entry__trigger',
                'button:has-text("Start a post")',
                '[aria-label*="Start a post"]',
                'div.share-box-feed-entry__trigger',
            ]

            clicked = False
            for selector in selectors:
                try:
                    elem = page.wait_for_selector(selector, timeout=5000)
                    if elem and elem.is_visible():
                        print(f"✓ Found: {selector}")
                        elem.click()
                        clicked = True
                        break
                except:
                    pass

            if not clicked:
                print("❌ Could not find 'Start a post' button")
                print("Browser staying open - please click manually...")
                time.sleep(60)
                browser.close()
                return False

            print("✓ Clicked 'Start a post'")
            time.sleep(3)

            # Find text editor
            print("Finding text editor...")
            editor = page.wait_for_selector('[contenteditable="true"]', timeout=10000)

            if editor:
                editor.click()
                time.sleep(1)

                # Type message
                print("Typing message...")
                page.keyboard.type(message, delay=50)
                time.sleep(2)

                # Find Post button
                print("Looking for Post button...")

                # Wait for Post button to be enabled
                time.sleep(2)

                post_buttons = page.query_selector_all('button')
                posted = False

                for btn in post_buttons:
                    try:
                        if btn.is_visible() and btn.is_enabled():
                            btn_text = btn.text_content().strip()
                            if btn_text == 'Post':
                                print(f"✓ Found Post button")
                                btn.click()
                                posted = True
                                break
                    except:
                        pass

                if posted:
                    time.sleep(5)
                    print("\n" + "="*60)
                    print("✅ POST PUBLISHED TO LINKEDIN!")
                    print("="*60)
                    browser.close()
                    return True
                else:
                    print("❌ Could not find Post button")
                    print("Browser staying open for manual posting...")
                    time.sleep(60)
                    browser.close()
                    return False
            else:
                print("❌ Could not find text editor")
                time.sleep(60)
                browser.close()
                return False

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(60)
            browser.close()
            return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = "Hello from Agentic Sphere! 🚀"

    success = post_with_login(message)
    sys.exit(0 if success else 1)
