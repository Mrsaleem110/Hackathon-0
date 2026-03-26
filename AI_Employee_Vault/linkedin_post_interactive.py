#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Post - Interactive Solution
Waits for you to press Enter after login
Usage: python linkedin_post_interactive.py "Your message here"
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def post_to_linkedin(message):
    """Post to LinkedIn with interactive login"""

    print("=" * 60)
    print("LinkedIn Auto Post - Interactive")
    print("=" * 60)
    print(f"\nMessage: {message}\n")

    with sync_playwright() as p:
        print("Opening browser...")
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
            page.goto('https://www.linkedin.com/login', timeout=30000)
            time.sleep(3)

            print("\n" + "="*60)
            print("STEP 1: LOGIN TO LINKEDIN")
            print("="*60)
            print("1. Login in the browser window")
            print("2. Complete 2FA if needed")
            print("3. Wait until you see your feed")
            print("4. Then come back here and press Enter")
            print("="*60)

            input("\nPress Enter after you've logged in...")

            # Go to feed
            print("\nGoing to feed...")
            page.goto('https://www.linkedin.com/feed/', timeout=30000)
            time.sleep(5)

            # Check if logged in
            if 'login' in page.url.lower():
                print("❌ Still not logged in")
                browser.close()
                return False

            print("✓ Logged in!\n")

            # Try to post
            print("="*60)
            print("STEP 2: POSTING")
            print("="*60)

            print("Looking for share box...")

            clicked = False
            selectors = [
                '.share-box-feed-entry__trigger',
                'button.share-box-feed-entry__trigger',
            ]

            for selector in selectors:
                try:
                    elem = page.query_selector(selector)
                    if elem and elem.is_visible():
                        print(f"✓ Found share box")
                        elem.click()
                        clicked = True
                        time.sleep(3)
                        break
                except:
                    pass

            if not clicked:
                print("Could not find button automatically")
                print("Please click 'Start a post' in the browser")
                input("Press Enter after clicking...")

            # Look for editor
            print("\nLooking for text editor...")
            editor = page.query_selector('[contenteditable="true"]')

            if not editor:
                time.sleep(3)
                editor = page.query_selector('[contenteditable="true"]')

            if editor:
                print("✓ Found editor")
                editor.click()
                time.sleep(1)

                print("✓ Typing message...")
                page.keyboard.type(message, delay=50)
                time.sleep(3)

                print("✓ Looking for Post button...")
                time.sleep(2)

                post_buttons = page.query_selector_all('button')
                posted = False

                for btn in post_buttons:
                    try:
                        if btn.is_visible() and btn.is_enabled():
                            btn_text = btn.text_content().strip()
                            if btn_text == 'Post':
                                print("✓ Clicking Post...")
                                btn.click()
                                posted = True
                                break
                    except:
                        pass

                if posted:
                    time.sleep(5)
                    print("\n" + "="*60)
                    print("✅ SUCCESS! POST PUBLISHED!")
                    print("="*60)
                    time.sleep(3)
                    browser.close()
                    return True
                else:
                    print("Could not find Post button")
                    print("Please click Post manually")
                    input("Press Enter after posting...")
                    browser.close()
                    return True
            else:
                print("❌ Could not find editor")
                print("Please complete manually")
                input("Press Enter when done...")
                browser.close()
                return False

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            browser.close()
            return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = "Hello from Agentic Sphere! 🚀"

    success = post_to_linkedin(message)
    sys.exit(0 if success else 1)
