#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Post - Final Working Solution
This script will:
1. Open browser
2. Wait for you to login manually
3. Automatically post your message

Usage: python linkedin_post_final.py "Your message here"
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def post_to_linkedin(message):
    """Post to LinkedIn with manual login"""

    print("=" * 60)
    print("LinkedIn Auto Post - Final Solution")
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
            # Go to LinkedIn login
            print("Opening LinkedIn...")
            page.goto('https://www.linkedin.com/login', timeout=30000)
            time.sleep(3)

            print("\n" + "="*60)
            print("⚠️  STEP 1: LOGIN TO LINKEDIN")
            print("="*60)
            print("Please login in the browser window:")
            print("1. Enter your email and password")
            print("2. Complete 2FA if required")
            print("3. Wait until you see your feed")
            print("\nScript will wait 2 minutes for you to login...")
            print("="*60 + "\n")

            # Wait 2 minutes for login
            time.sleep(120)

            # Try to go to feed
            print("Checking if logged in...")
            page.goto('https://www.linkedin.com/feed/', timeout=30000)
            time.sleep(5)

            # Check if logged in by looking for feed content
            body_text = page.inner_text('body')

            if 'Sign in' in body_text or 'login' in page.url.lower():
                print("❌ Not logged in. Please run the script again and login faster.")
                time.sleep(10)
                browser.close()
                return False

            print("✓ Logged in successfully!\n")

            print("="*60)
            print("⚠️  STEP 2: POSTING")
            print("="*60)

            # Try to find and click share box
            print("Looking for 'Start a post' button...")

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
                print("⚠️  Could not find button automatically")
                print("Please click 'Start a post' manually NOW")
                print("Waiting 20 seconds...")
                time.sleep(20)

            # Look for text editor
            print("\nLooking for text editor...")
            editor = page.query_selector('[contenteditable="true"]')

            if not editor:
                print("⚠️  Trying again...")
                time.sleep(5)
                editor = page.query_selector('[contenteditable="true"]')

            if editor:
                print("✓ Found text editor")
                editor.click()
                time.sleep(1)

                # Type message
                print("✓ Typing message...")
                page.keyboard.type(message, delay=50)
                time.sleep(3)

                # Find Post button
                print("✓ Looking for Post button...")

                # Wait a bit for Post button to be enabled
                time.sleep(2)

                post_buttons = page.query_selector_all('button')

                posted = False
                for btn in post_buttons:
                    try:
                        if btn.is_visible() and btn.is_enabled():
                            btn_text = btn.text_content().strip()
                            if btn_text == 'Post':
                                print("✓ Clicking Post button...")
                                btn.click()
                                posted = True
                                break
                    except:
                        pass

                if posted:
                    time.sleep(5)
                    print("\n" + "="*60)
                    print("✅ SUCCESS! POST PUBLISHED TO LINKEDIN!")
                    print("="*60)
                    time.sleep(5)
                    browser.close()
                    return True
                else:
                    print("⚠️  Could not find Post button")
                    print("Please click 'Post' manually in the browser")
                    time.sleep(30)
                    browser.close()
                    return False
            else:
                print("❌ Could not find text editor")
                print("Please complete the post manually")
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

    print("\n" + "="*60)
    print("LINKEDIN AUTO POST")
    print("="*60)
    print("This script will help you post to LinkedIn automatically.")
    print("You need to login manually first, then it will post for you.")
    print("="*60 + "\n")

    success = post_to_linkedin(message)

    if success:
        print("\n✅ Done! Your post is live on LinkedIn.")
    else:
        print("\n❌ Could not complete automatically. Please post manually.")

    sys.exit(0 if success else 1)
