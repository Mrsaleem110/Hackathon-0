#!/usr/bin/env python3
"""
LinkedIn Post - Debug Version
Tries multiple approaches and takes screenshots
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def debug_post(message="Hello from AgenticSphere"):
    """Debug version with screenshots"""

    session_path = Path('.linkedin_session_auto')

    print("=" * 60)
    print("LinkedIn Post - Debug Mode")
    print("=" * 60)
    print(f"\nMessage: {message}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            viewport={'width': 1280, 'height': 800}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            # Step 1: Open page
            print("Step 1: Opening Agentic Sphere page...")
            page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=60000)
            time.sleep(5)

            # Take screenshot
            page.screenshot(path='step1_page_loaded.png')
            print("  Screenshot saved: step1_page_loaded.png")

            # Step 2: Try to find post button
            print("\nStep 2: Looking for post button...")

            # Try different button texts
            button_texts = [
                "Create a post",
                "Start a post",
                "Create post",
                "Post",
                "Share"
            ]

            button_found = None
            for text in button_texts:
                try:
                    btn = page.get_by_text(text, exact=False)
                    if btn.count() > 0:
                        print(f"  Found button with text: {text}")
                        button_found = btn.first
                        break
                except:
                    pass

            if button_found:
                print("\nStep 3: Clicking button...")
                button_found.click()
                time.sleep(3)
                page.screenshot(path='step2_after_click.png')
                print("  Screenshot saved: step2_after_click.png")

                # Try to find text area
                print("\nStep 4: Looking for text editor...")
                editor = page.locator('[contenteditable="true"]').first
                if editor:
                    editor.click()
                    time.sleep(1)

                    print("\nStep 5: Typing message...")
                    page.keyboard.type(message, delay=50)
                    time.sleep(2)

                    page.screenshot(path='step3_typed.png')
                    print("  Screenshot saved: step3_typed.png")

                    print("\nStep 6: Looking for Post button...")
                    # Try to find and click Post button
                    post_buttons = page.get_by_role("button", name="Post")
                    if post_buttons.count() > 0:
                        post_buttons.first.click()
                        time.sleep(3)
                        print("\n" + "=" * 60)
                        print("SUCCESS! Post published!")
                        print("=" * 60)
                    else:
                        print("  Could not find Post button")
                        print("  Please click it manually")
                        time.sleep(30)
            else:
                print("\n  Could not find post button automatically")
                print("  Please check screenshots and post manually")
                time.sleep(60)

            browser.close()

        except Exception as e:
            print(f"\nError: {e}")
            page.screenshot(path='error.png')
            print("Screenshot saved: error.png")
            time.sleep(30)
            browser.close()

if __name__ == '__main__':
    debug_post()
    print("\nCheck screenshots to see what happened!")
