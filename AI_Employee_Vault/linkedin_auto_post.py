#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Auto Post - Uses Saved Session
Posts to Agentic Sphere company page automatically
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def post_to_linkedin(message):
    """Post to LinkedIn using saved session"""

    print("=" * 60)
    print("LinkedIn Auto Post")
    print("=" * 60)
    print(f"\nMessage: {message}\n")

    session_path = ".linkedin_session"

    with sync_playwright() as p:
        # Use saved session
        print("Loading saved LinkedIn session...")
        browser = p.chromium.launch_persistent_context(
            session_path,
            headless=False,
            viewport={'width': 1280, 'height': 800}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            # Go to company page
            print("Opening Agentic Sphere page...")
            page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=30000)
            time.sleep(3)

            # Wait for page to load
            page.wait_for_load_state('networkidle')
            time.sleep(2)

            # Try to find and click "Start a post" or "Create a post" button
            print("Looking for post button...")

            # Multiple selectors to try
            button_selectors = [
                'button:has-text("Start a post")',
                'button:has-text("Create a post")',
                '[aria-label*="Start a post"]',
                '[aria-label*="Create a post"]',
                'button.share-box-feed-entry__trigger',
                '.share-box-feed-entry__trigger',
            ]

            clicked = False
            for selector in button_selectors:
                try:
                    element = page.query_selector(selector)
                    if element and element.is_visible():
                        print(f"Found button: {selector}")
                        element.click()
                        clicked = True
                        break
                except Exception as e:
                    continue

            if not clicked:
                print("Trying to find button by scanning all buttons...")
                buttons = page.query_selector_all('button')
                for btn in buttons:
                    try:
                        if btn.is_visible():
                            text = btn.text_content().lower()
                            if 'start a post' in text or 'create a post' in text or 'share' in text:
                                print(f"Found button with text: {text}")
                                btn.click()
                                clicked = True
                                break
                    except:
                        continue

            if not clicked:
                print("❌ Could not find post button")
                print("Make sure you're logged in and on the company page")
                browser.close()
                return False

            print("✓ Clicked post button")
            time.sleep(2)

            # Find editor
            print("Looking for text editor...")
            editor_selectors = [
                '[contenteditable="true"]',
                '.ql-editor',
                '[role="textbox"]',
                'div[data-placeholder]'
            ]

            editor = None
            for selector in editor_selectors:
                try:
                    editor = page.query_selector(selector)
                    if editor and editor.is_visible():
                        print(f"Found editor: {selector}")
                        break
                except:
                    continue

            if not editor:
                print("❌ Could not find text editor")
                browser.close()
                return False

            # Type message
            print("Typing message...")
            editor.click()
            time.sleep(1)
            editor.fill(message)
            time.sleep(2)

            # Find and click Post button
            print("Looking for Post button...")
            post_button_selectors = [
                'button:has-text("Post")',
                '[aria-label*="Post"]',
                'button[type="submit"]'
            ]

            posted = False
            for selector in post_button_selectors:
                try:
                    btn = page.query_selector(selector)
                    if btn and btn.is_visible() and btn.is_enabled():
                        btn_text = btn.text_content().strip()
                        if btn_text == 'Post' or len(btn_text) < 10:
                            print(f"Clicking Post button: {btn_text}")
                            btn.click()
                            posted = True
                            break
                except:
                    continue

            if not posted:
                # Try scanning all buttons
                buttons = page.query_selector_all('button')
                for btn in buttons:
                    try:
                        if btn.is_visible() and btn.is_enabled():
                            text = btn.text_content().strip()
                            if text == 'Post':
                                print(f"Found Post button: {text}")
                                btn.click()
                                posted = True
                                break
                    except:
                        continue

            if posted:
                time.sleep(3)
                print("\n" + "="*60)
                print("✅ POST PUBLISHED SUCCESSFULLY!")
                print("="*60)
                browser.close()
                return True
            else:
                print("❌ Could not find Post button")
                time.sleep(5)
                browser.close()
                return False

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            browser.close()
            return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = "Hello from Agentic Sphere!"

    success = post_to_linkedin(message)
    sys.exit(0 if success else 1)
