#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Poster with Saved Session
Uses existing LinkedIn session to post directly
"""

import sys
import time
import io
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def post_to_linkedin_with_session(message, session_path='.linkedin_session'):
    """Post to LinkedIn using saved session"""

    session_dir = Path(session_path)

    if not session_dir.exists():
        print(f"Error: LinkedIn session not found at {session_path}")
        print("Please run setup_linkedin_session.py first to create a session")
        return False

    print("\n" + "="*60)
    print("LINKEDIN POSTER - USING SAVED SESSION")
    print("="*60)
    print(f"Message: {message[:100]}...\n")

    with sync_playwright() as p:
        print("Opening LinkedIn with saved session...")

        try:
            browser = p.chromium.launch_persistent_context(
                str(session_dir),
                headless=False,
                viewport={'width': 1920, 'height': 1080}
            )

            page = browser.new_page()

            # Go to LinkedIn feed
            print("Loading LinkedIn feed...")
            page.goto('https://www.linkedin.com/feed/', timeout=30000)
            time.sleep(5)

            # Check if logged in
            body_text = page.inner_text('body')

            if 'Sign in' in body_text or 'login' in page.url.lower():
                print("❌ Session expired. Please run setup_linkedin_session.py again")
                browser.close()
                return False

            print("✓ Session loaded successfully!\n")

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
                page.keyboard.type(message, delay=20)
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
                    print(f"Message: {message[:80]}...")
                    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                    print("="*60 + "\n")
                    time.sleep(2)
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
            try:
                browser.close()
            except:
                pass
            return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print("Usage:")
            print("  python linkedin_poster_session.py 'Your post content here'")
            print("\nExample:")
            print("  python linkedin_poster_session.py 'Hello LinkedIn! Agentic Sphere AI'")
            print("\nNote: Requires saved LinkedIn session at .linkedin_session")
            print("Run setup_linkedin_session.py first to create a session")
        else:
            message = ' '.join(sys.argv[1:])
            success = post_to_linkedin_with_session(message)
            sys.exit(0 if success else 1)
    else:
        print("Usage: python linkedin_poster_session.py 'Your message here'")
        print("Run with --help for more information")
