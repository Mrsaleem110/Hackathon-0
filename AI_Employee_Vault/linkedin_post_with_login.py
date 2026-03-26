#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Login and Post
First login manually, then post automatically
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def login_and_post(message):
    """Login to LinkedIn and post"""

    print("=" * 60)
    print("LinkedIn Login & Post")
    print("=" * 60)
    print(f"\nMessage: {message}\n")

    session_path = ".linkedin_session"

    with sync_playwright() as p:
        print("Opening browser with saved session...")
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

            # Check if logged in
            if 'login' in page.url or 'authwall' in page.url:
                print("\n⚠ You need to login first")
                print("Please login in the browser window...")
                print("Waiting 30 seconds for you to login...")
                time.sleep(30)

            # Go to company page
            print("\nGoing to Agentic Sphere page...")
            page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=30000)
            time.sleep(3)

            # Take screenshot to see what's on page
            page.screenshot(path='linkedin_page_debug.png')
            print("Screenshot saved: linkedin_page_debug.png")

            # Check if we're on the right page
            print(f"Current URL: {page.url}")
            print(f"Page title: {page.title()}")

            # Wait for page to fully load
            page.wait_for_load_state('networkidle')
            time.sleep(2)

            # Try to find post button - be more flexible
            print("\nLooking for any way to create a post...")

            # Get all visible text on page
            page_text = page.inner_text('body')

            if 'Start a post' in page_text:
                print("Found 'Start a post' text on page")
            if 'Create a post' in page_text:
                print("Found 'Create a post' text on page")

            # Try clicking any element with post-related text
            all_elements = page.query_selector_all('button, a, div[role="button"]')
            print(f"Found {len(all_elements)} clickable elements")

            clicked = False
            for element in all_elements:
                try:
                    if element.is_visible():
                        text = element.inner_text().lower().strip()
                        if any(keyword in text for keyword in ['start a post', 'create a post', 'share an update']):
                            print(f"Found element with text: '{text}'")
                            element.click()
                            clicked = True
                            print("✓ Clicked!")
                            break
                except:
                    continue

            if not clicked:
                print("\n❌ Could not find post button automatically")
                print("Please click 'Start a post' or 'Create a post' button manually")
                print("Browser will stay open for 60 seconds...")
                time.sleep(60)
                browser.close()
                return False

            time.sleep(3)

            # Find editor
            print("\nLooking for text editor...")
            editor = page.query_selector('[contenteditable="true"]')

            if not editor:
                print("Trying alternative editor selectors...")
                editor = page.query_selector('.ql-editor, [role="textbox"], div[data-placeholder]')

            if editor and editor.is_visible():
                print("✓ Found editor")
                editor.click()
                time.sleep(1)

                print("Typing message...")
                editor.fill(message)
                time.sleep(2)

                # Find Post button
                print("Looking for Post button...")
                buttons = page.query_selector_all('button')

                for btn in buttons:
                    try:
                        if btn.is_visible() and btn.is_enabled():
                            text = btn.inner_text().strip()
                            if text == 'Post':
                                print(f"Found Post button: '{text}'")
                                btn.click()
                                print("✓ Clicked Post!")
                                time.sleep(5)

                                print("\n" + "="*60)
                                print("✅ POST PUBLISHED!")
                                print("="*60)

                                time.sleep(3)
                                browser.close()
                                return True
                    except:
                        continue

                print("❌ Could not find Post button")
                print("Browser will stay open - please click Post manually")
                time.sleep(30)
            else:
                print("❌ Could not find text editor")
                print("Browser will stay open for 30 seconds...")
                time.sleep(30)

            browser.close()
            return False

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            print("\nBrowser will stay open for 30 seconds...")
            time.sleep(30)
            browser.close()
            return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = "Hello from Agentic Sphere!"

    success = login_and_post(message)
    sys.exit(0 if success else 1)
