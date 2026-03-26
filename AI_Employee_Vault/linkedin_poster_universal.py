#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal LinkedIn Poster - Post to LinkedIn directly
Uses browser automation to post content
"""

import sys
import time
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def post_to_linkedin(message):
    """Post to LinkedIn with browser automation"""

    print("\n" + "="*60)
    print("LINKEDIN POSTER")
    print("="*60)
    print(f"Message: {message}\n")

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
            page.goto('https://www.linkedin.com/feed/', timeout=30000)
            time.sleep(3)

            # Check if already logged in
            body_text = page.inner_text('body')

            if 'Sign in' in body_text or 'login' in page.url.lower():
                print("\n" + "="*60)
                print("LOGIN REQUIRED")
                print("="*60)
                print("Please login to LinkedIn in the browser window")
                print("Waiting 2 minutes for you to login...")
                print("="*60 + "\n")

                time.sleep(120)

                # Check again
                page.goto('https://www.linkedin.com/feed/', timeout=30000)
                time.sleep(5)

                body_text = page.inner_text('body')
                if 'Sign in' in body_text or 'login' in page.url.lower():
                    print("❌ Not logged in. Please try again.")
                    browser.close()
                    return False

            print("✓ Logged in successfully!\n")

            print("="*60)
            print("POSTING TO LINKEDIN")
            print("="*60)

            # Find and click share box
            print("Looking for 'Start a post' button...")

            clicked = False
            selectors = [
                '.share-box-feed-entry__trigger',
                'button.share-box-feed-entry__trigger',
                '[data-test-id="share-box-feed-entry__trigger"]',
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
                print("Please click 'Start a post' manually")
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
                page.keyboard.type(message, delay=30)
                time.sleep(3)

                # Find Post button
                print("✓ Looking for Post button...")
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
                    print("SUCCESS - POST PUBLISHED TO LINKEDIN!")
                    print("="*60)
                    print(f"Message: {message[:100]}...")
                    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                    print("="*60 + "\n")
                    time.sleep(3)
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
            time.sleep(10)
            browser.close()
            return False

def interactive_mode():
    """Interactive mode - ask user for post content"""

    print("\n" + "="*60)
    print("LINKEDIN POSTER - INTERACTIVE MODE")
    print("="*60)

    print("\nLinkedIn par kya post karna hai?")
    print("(Enter ke baad Ctrl+D ya Ctrl+Z dabao jab khatam ho):")
    print()

    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    message = '\n'.join(lines).strip()
    if not message:
        print("Error: Post content required")
        return False

    # Confirm before posting
    print("\n" + "-"*60)
    print("Post Content:")
    print(message)
    print("-"*60)

    confirm = input("\nKya LinkedIn par post karna hai? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y', 'haan', 'ha']:
        print("Post cancelled.")
        return False

    # Post to LinkedIn
    return post_to_linkedin(message)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == '--help':
            print("Usage:")
            print("  Interactive mode: python linkedin_poster_universal.py")
            print("  Direct mode: python linkedin_poster_universal.py 'Your post content here'")
            print("\nExample:")
            print("  python linkedin_poster_universal.py 'Hello LinkedIn! Agentic Sphere AI'")
        else:
            message = ' '.join(sys.argv[1:])
            success = post_to_linkedin(message)
            sys.exit(0 if success else 1)
    else:
        # Interactive mode
        success = interactive_mode()
        sys.exit(0 if success else 1)
