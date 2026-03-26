#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Post - Click Anywhere Approach
Finds ANY clickable element that opens post dialog
Usage: python linkedin_post_click_and_post.py "Your message here"
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def post_to_linkedin(message):
    """Post to LinkedIn by finding any post trigger"""

    print("=" * 60)
    print("LinkedIn Post - Smart Click")
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

            # Take screenshot
            page.screenshot(path='linkedin_before_click.png')
            print("Screenshot saved: linkedin_before_click.png")

            # Try to find the share box (the area you click to start posting)
            print("\nLooking for share box...")

            # LinkedIn usually has a clickable area at top of feed
            # Try clicking on various elements that might trigger post dialog
            selectors_to_try = [
                # Share box selectors
                '.share-box-feed-entry__trigger',
                'button.share-box-feed-entry__trigger',
                '[data-control-name="share_box_trigger"]',
                # Text input that opens dialog
                'input[placeholder*="post"]',
                'input[placeholder*="share"]',
                # Any button with "Start" text
                'button:has-text("Start")',
                # Fallback: any clickable in share area
                '.share-box-feed-entry',
            ]

            clicked = False
            for selector in selectors_to_try:
                try:
                    elem = page.wait_for_selector(selector, timeout=3000)
                    if elem:
                        print(f"✓ Found: {selector}")
                        elem.click()
                        clicked = True
                        time.sleep(3)
                        break
                except:
                    continue

            if not clicked:
                print("❌ Automatic click failed")
                print("\nPlease manually click to start a post...")
                print("Waiting 30 seconds...")
                time.sleep(30)

            # Now look for the text editor
            print("\nLooking for text editor...")
            try:
                editor = page.wait_for_selector('[contenteditable="true"]', timeout=10000)

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

                    # Take screenshot before posting
                    page.screenshot(path='linkedin_before_post.png')

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
                        print("✅ POST PUBLISHED!")
                        print("="*60)
                        browser.close()
                        return True
                    else:
                        print("❌ Could not find Post button")
                        print("Browser staying open...")
                        time.sleep(60)
                        browser.close()
                        return False
                else:
                    print("❌ Could not find text editor")
                    time.sleep(60)
                    browser.close()
                    return False

            except Exception as e:
                print(f"❌ Error finding editor: {e}")
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

    success = post_to_linkedin(message)
    sys.exit(0 if success else 1)
