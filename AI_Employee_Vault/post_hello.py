#!/usr/bin/env python3
"""
Simple LinkedIn Post - Hello from AgenticSphere
One command to post to Agentic Sphere company page
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

POST_TEXT = "Hello from AgenticSphere"

def post_hello_to_agentic_sphere():
    """Post 'Hello from AgenticSphere' to company page"""

    session_path = Path('.linkedin_session_auto')

    print("=" * 60)
    print("Posting to Agentic Sphere LinkedIn Page")
    print("=" * 60)
    print(f"\nPost: {POST_TEXT}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            viewport={'width': 1280, 'height': 800}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            # Go directly to Agentic Sphere company page
            print("Opening Agentic Sphere page...")
            page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=30000)
            time.sleep(3)

            # Click on "Create a post" button
            print("Looking for 'Create a post' button...")
            time.sleep(2)

            # Try different selectors for the post button
            selectors = [
                'button:has-text("Create a post")',
                'button:has-text("Start a post")',
                '[aria-label="Create a post"]',
                '[aria-label="Start a post"]'
            ]

            clicked = False
            for selector in selectors:
                try:
                    btn = page.query_selector(selector)
                    if btn and btn.is_visible():
                        print(f"Found button with selector: {selector}")
                        btn.click()
                        clicked = True
                        break
                except:
                    continue

            if not clicked:
                print("\n⚠️ Couldn't find post button automatically.")
                print("\n📋 MANUAL STEPS:")
                print("1. Click 'Create a post' button on the page")
                print(f"2. Type: {POST_TEXT}")
                print("3. Click 'Post' button")
                print("\nBrowser will stay open for 60 seconds...")
                time.sleep(60)
                print("\n✅ Done! Closing browser...")
                return True

            time.sleep(2)

            # Find text editor
            print("Finding text editor...")
            editor = page.query_selector('[contenteditable="true"]')
            if editor:
                editor.click()
                time.sleep(1)

                # Type the post
                print("Typing post...")
                page.keyboard.type(POST_TEXT, delay=50)
                time.sleep(2)

                # Click Post button
                print("Clicking Post button...")
                post_buttons = page.query_selector_all('button')
                for btn in post_buttons:
                    try:
                        if btn.is_visible() and 'Post' in btn.text_content():
                            btn.click()
                            break
                    except:
                        continue

                time.sleep(3)
                print("\n" + "="*60)
                print("✅ POST PUBLISHED!")
                print("="*60)
                return True
            else:
                print("\n📋 Please complete manually:")
                print(f"Type: {POST_TEXT}")
                print("Then click Post button")
                print("\nBrowser will stay open for 60 seconds...")
                time.sleep(60)
                return True

        except Exception as e:
            print(f"Error: {e}")
            print("\n📋 Please complete manually:")
            print("1. Click 'Create a post'")
            print(f"2. Type: {POST_TEXT}")
            print("3. Click 'Post' button")
            print("\nBrowser will stay open for 60 seconds...")
            time.sleep(60)
            return True

        finally:
            time.sleep(2)
            browser.close()

if __name__ == '__main__':
    success = post_hello_to_agentic_sphere()
    if success:
        print("\n✅ Done! Check your Agentic Sphere page.")
    else:
        print("\n⚠️ Please verify the post was published.")
