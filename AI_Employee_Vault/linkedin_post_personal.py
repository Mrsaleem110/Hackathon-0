#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Post - Personal Profile
Posts to your personal LinkedIn feed
Usage: python linkedin_post_personal.py "Your message here"
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def post_to_personal_profile(message):
    """Post to personal LinkedIn profile"""

    print("=" * 60)
    print("LinkedIn Personal Post")
    print("=" * 60)
    print(f"\nMessage: {message}\n")

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
            # Go to LinkedIn feed
            print("Opening LinkedIn feed...")
            page.goto('https://www.linkedin.com/feed/', timeout=30000)
            time.sleep(3)

            # Look for "Start a post" button on feed
            print("Looking for 'Start a post' button...")

            selectors = [
                'button:has-text("Start a post")',
                '[aria-label*="Start a post"]',
                '.share-box-feed-entry__trigger',
                'button.share-box-feed-entry__trigger',
            ]

            clicked = False
            for selector in selectors:
                try:
                    btn = page.wait_for_selector(selector, timeout=5000)
                    if btn and btn.is_visible():
                        print(f"Found button: {selector}")
                        btn.click()
                        clicked = True
                        break
                except:
                    pass

            if not clicked:
                # Try finding by text
                buttons = page.query_selector_all('button, div[role="button"]')
                for btn in buttons:
                    try:
                        if btn.is_visible():
                            text = btn.text_content().lower()
                            if 'start a post' in text or 'share' in text:
                                print("Found 'Start a post' by text")
                                btn.click()
                                clicked = True
                                break
                    except:
                        pass

            if not clicked:
                print("❌ Could not find 'Start a post' button")
                time.sleep(30)
                browser.close()
                return False

            print("✓ Clicked 'Start a post'")
            time.sleep(2)

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

                # Find and click Post button
                print("Looking for Post button...")
                post_buttons = page.query_selector_all('button')

                posted = False
                for btn in post_buttons:
                    try:
                        if btn.is_visible() and btn.is_enabled():
                            btn_text = btn.text_content().strip()
                            # Look for "Post" button (not "Repost" or other variants)
                            if btn_text == 'Post' or (btn_text.lower() == 'post' and len(btn_text) < 10):
                                print(f"Found Post button: '{btn_text}'")
                                btn.click()
                                posted = True
                                break
                    except:
                        pass

                if posted:
                    time.sleep(5)
                    print("\n" + "="*60)
                    print("✅ POST PUBLISHED TO YOUR LINKEDIN PROFILE!")
                    print("="*60)
                    browser.close()
                    return True
                else:
                    print("❌ Could not find Post button")
                    print("Browser staying open for manual posting...")
                    time.sleep(30)
                    browser.close()
                    return False
            else:
                print("❌ Could not find text editor")
                time.sleep(30)
                browser.close()
                return False

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(30)
            browser.close()
            return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = "Hello from Agentic Sphere! 🚀"

    success = post_to_personal_profile(message)
    sys.exit(0 if success else 1)
