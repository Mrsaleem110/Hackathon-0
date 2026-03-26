#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Post - Simple Direct Approach
Usage: python linkedin_post_simple.py "Your message here"
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def post_to_linkedin(message):
    """Post to LinkedIn"""

    print("=" * 60)
    print("LinkedIn Post")
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
            # Go to feed
            print("Opening LinkedIn feed...")
            page.goto('https://www.linkedin.com/feed/', timeout=30000)
            time.sleep(5)

            print("\nLooking for share box...")

            # Try different selectors
            selectors = [
                '.share-box-feed-entry__trigger',
                'button.share-box-feed-entry__trigger',
                '[data-control-name="share_box_trigger"]',
            ]

            clicked = False
            for selector in selectors:
                try:
                    elem = page.query_selector(selector)
                    if elem and elem.is_visible():
                        print(f"✓ Found: {selector}")
                        elem.click()
                        clicked = True
                        time.sleep(3)
                        break
                except:
                    pass

            if not clicked:
                print("❌ Could not find share box automatically")
                print("\nPlease click 'Start a post' manually in the browser...")
                print("Waiting 30 seconds for you to click...")
                time.sleep(30)

            # Look for text editor
            print("\nLooking for text editor...")
            editor = page.query_selector('[contenteditable="true"]')

            if editor:
                print("✓ Found text editor")
                editor.click()
                time.sleep(1)

                # Type message
                print("Typing message...")
                page.keyboard.type(message, delay=50)
                time.sleep(2)

                # Find Post button
                print("Looking for Post button...")
                post_buttons = page.query_selector_all('button')

                posted = False
                for btn in post_buttons:
                    try:
                        if btn.is_visible() and btn.is_enabled():
                            btn_text = btn.text_content().strip()
                            if btn_text == 'Post':
                                print(f"✓ Clicking Post button")
                                btn.click()
                                posted = True
                                break
                    except:
                        pass

                if posted:
                    time.sleep(5)
                    print("\n" + "="*60)
                    print("✅ POST PUBLISHED!")
                    print("="*60)
                    browser.close()
                    return True
                else:
                    print("❌ Could not find Post button")
                    print("Please click Post manually...")
                    time.sleep(30)
                    browser.close()
                    return False
            else:
                print("❌ Could not find text editor")
                print("Please complete manually...")
                time.sleep(30)
                browser.close()
                return False

        except Exception as e:
            print(f"\n❌ Error: {e}")
            time.sleep(30)
            browser.close()
            return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = "Hello from Agentic Sphere! 🚀"

    success = post_to_linkedin(message)
    sys.exit(0 if success else 1)
