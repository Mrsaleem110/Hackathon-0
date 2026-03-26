#!/usr/bin/env python3
"""
Fully Automated LinkedIn Post
No manual steps - just run and it posts!
"""
import time
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def auto_post_linkedin(message="Hello from AgenticSphere"):
    """Fully automated LinkedIn posting to Agentic Sphere page"""

    session_path = Path('.linkedin_session_auto')

    print("=" * 60)
    print("AUTOMATED LINKEDIN POST")
    print("=" * 60)
    print(f"\nMessage: {message}")
    print("\nStarting automation...\n")

    with sync_playwright() as p:
        # Launch browser with saved session
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            viewport={'width': 1280, 'height': 800},
            args=['--disable-blink-features=AutomationControlled']
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            # Step 1: Go to LinkedIn feed first (faster than company page)
            print("[1/6] Opening LinkedIn feed...")
            page.goto('https://www.linkedin.com/feed/', timeout=60000)
            time.sleep(3)

            # Check if we need to login
            if 'login' in page.url or 'checkpoint' in page.url:
                print("    Login required - please login manually in the browser")
                print("    Waiting 30 seconds for login...")
                time.sleep(30)

            # Step 2: Navigate to Agentic Sphere company page
            print("[2/6] Navigating to Agentic Sphere page...")
            page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=60000)
            time.sleep(4)

            # Step 3: Look for "Create a post" or "Start a post" button
            print("[3/6] Finding post button...")

            # Try multiple selectors
            post_button = None
            selectors = [
                'button:has-text("Create a post")',
                'button:has-text("Start a post")',
                'button[aria-label*="post" i]',
                '.share-box-feed-entry__trigger',
                '[data-control-name="share_box"]'
            ]

            for selector in selectors:
                try:
                    btn = page.wait_for_selector(selector, timeout=3000)
                    if btn and btn.is_visible():
                        post_button = btn
                        print(f"    Found button: {selector}")
                        break
                except:
                    continue

            if not post_button:
                print("    Could not find post button automatically")
                print("    Taking screenshot for debugging...")
                page.screenshot(path='linkedin_page.png')
                print("    Screenshot saved: linkedin_page.png")

                # Keep browser open for manual posting
                print("\n    Please click 'Create a post' manually")
                print("    Browser will stay open for 60 seconds...")
                time.sleep(60)
                browser.close()
                return False

            # Step 4: Click the post button
            print("[4/6] Clicking post button...")
            post_button.click()
            time.sleep(2)

            # Step 5: Find and fill the editor
            print("[5/6] Typing message...")

            # Wait for editor to appear
            editor = page.wait_for_selector('[contenteditable="true"]', timeout=5000)
            if editor:
                editor.click()
                time.sleep(1)

                # Type the message
                page.keyboard.type(message, delay=30)
                time.sleep(2)

                # Step 6: Click Post button
                print("[6/6] Publishing post...")

                # Find and click the Post button
                post_buttons = page.query_selector_all('button')
                posted = False

                for btn in post_buttons:
                    try:
                        text = btn.text_content()
                        if text and 'Post' in text and btn.is_visible() and btn.is_enabled():
                            btn.click()
                            posted = True
                            break
                    except:
                        continue

                if posted:
                    time.sleep(4)
                    print("\n" + "=" * 60)
                    print("SUCCESS! Post published to Agentic Sphere")
                    print("=" * 60)
                    time.sleep(2)
                    browser.close()
                    return True
                else:
                    print("    Could not find Post button")
                    print("    Browser will stay open for 30 seconds...")
                    time.sleep(30)
                    browser.close()
                    return False
            else:
                print("    Could not find text editor")
                browser.close()
                return False

        except Exception as e:
            print(f"\nError: {e}")
            print("Taking screenshot for debugging...")
            try:
                page.screenshot(path='error_screenshot.png')
                print("Screenshot saved: error_screenshot.png")
            except:
                pass

            print("\nBrowser will stay open for 30 seconds...")
            time.sleep(30)
            browser.close()
            return False

if __name__ == '__main__':
    # Get message from command line or use default
    message = sys.argv[1] if len(sys.argv) > 1 else "Hello from AgenticSphere"

    success = auto_post_linkedin(message)

    if success:
        print("\nDone! Check: https://www.linkedin.com/company/agentic-sphere/")
    else:
        print("\nFailed to post automatically. Please check the screenshots.")
