#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Post - Complete Solution with Manual Login
Usage: python linkedin_post_complete.py "Your message here"
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def post_to_linkedin(message):
    """Post to LinkedIn with manual login support"""

    print("=" * 60)
    print("LinkedIn Post - Complete Solution")
    print("=" * 60)
    print(f"\nMessage: {message}\n")

    with sync_playwright() as p:
        print("Opening browser...")
        # Use regular browser, not persistent context
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )

        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()

        try:
            # Go to LinkedIn
            print("Opening LinkedIn...")
            page.goto('https://www.linkedin.com/', timeout=30000)
            time.sleep(3)

            # Check if we need to login
            current_url = page.url
            if 'login' in current_url or 'authwall' in current_url or page.query_selector('input[name="session_key"]'):
                print("\n" + "="*60)
                print("⚠️  PLEASE LOGIN MANUALLY")
                print("="*60)
                print("1. Enter your email and password")
                print("2. Complete any 2FA if required")
                print("3. Wait until you see your LinkedIn feed")
                print("\nWaiting 90 seconds for you to login...")
                print("="*60 + "\n")
                time.sleep(90)

            # Go to feed
            print("Going to LinkedIn feed...")
            page.goto('https://www.linkedin.com/feed/', timeout=30000)
            time.sleep(5)

            # Check if still on login page
            if 'login' in page.url or 'authwall' in page.url:
                print("❌ Still not logged in. Please try again.")
                time.sleep(30)
                browser.close()
                return False

            print("✓ Logged in successfully\n")

            # Now try to post
            print("Looking for 'Start a post' button...")

            # Try multiple approaches
            clicked = False

            # Approach 1: Look for share box
            selectors = [
                '.share-box-feed-entry__trigger',
                'button.share-box-feed-entry__trigger',
                '[data-control-name="share_box_trigger"]',
            ]

            for selector in selectors:
                try:
                    elem = page.wait_for_selector(selector, timeout=5000)
                    if elem and elem.is_visible():
                        print(f"✓ Found share box: {selector}")
                        elem.click()
                        clicked = True
                        time.sleep(3)
                        break
                except:
                    pass

            # Approach 2: Look for any button with "Start" text
            if not clicked:
                buttons = page.query_selector_all('button')
                for btn in buttons:
                    try:
                        text = btn.text_content()
                        if text and 'Start a post' in text:
                            print("✓ Found 'Start a post' button")
                            btn.click()
                            clicked = True
                            time.sleep(3)
                            break
                    except:
                        pass

            if not clicked:
                print("❌ Could not find 'Start a post' button automatically")
                print("\n⚠️  Please click 'Start a post' manually in the browser")
                print("Waiting 30 seconds...")
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
                                print("✓ Clicking Post button")
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
                    time.sleep(5)
                    browser.close()
                    return True
                else:
                    print("❌ Could not find Post button")
                    print("⚠️  Please click 'Post' button manually")
                    time.sleep(30)
                    browser.close()
                    return False
            else:
                print("❌ Could not find text editor")
                print("⚠️  Please complete the post manually")
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

    success = post_to_linkedin(message)
    sys.exit(0 if success else 1)
