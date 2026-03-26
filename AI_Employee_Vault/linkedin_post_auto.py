#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Auto Post - Fully Automated
Posts directly to Agentic Sphere LinkedIn page
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def auto_post(message):
    """Automatically post to LinkedIn company page"""

    print("=" * 60)
    print("LinkedIn Auto Post - Agentic Sphere")
    print("=" * 60)
    print(f"\nMessage: {message}\n")

    with sync_playwright() as p:
        # Launch browser (headless=False so you can see what's happening)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Go to Agentic Sphere page
            print("Opening Agentic Sphere LinkedIn page...")
            page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=30000)
            time.sleep(3)

            # Click "Create a post" button
            print("Looking for 'Create a post' button...")

            # Try multiple ways to find the button
            clicked = False
            selectors = [
                'button:has-text("Create a post")',
                'text=Create a post',
                '[aria-label*="Create"]',
            ]

            for selector in selectors:
                try:
                    if page.query_selector(selector):
                        page.click(selector, timeout=5000)
                        print(f"✓ Clicked 'Create a post' button")
                        clicked = True
                        break
                except:
                    continue

            if not clicked:
                print("⚠ Could not find button automatically")
                print("Please click 'Create a post' manually...")
                input("Press Enter after clicking...")

            time.sleep(2)

            # Find text editor and type message
            print("Finding text editor...")
            page.wait_for_selector('[contenteditable="true"]', timeout=10000)

            editor = page.query_selector('[contenteditable="true"]')
            if editor:
                print("✓ Found editor, typing message...")
                editor.click()
                time.sleep(1)
                page.keyboard.type(message, delay=50)
                time.sleep(2)

                # Click Post button
                print("Looking for Post button...")
                post_buttons = page.query_selector_all('button')

                for btn in post_buttons:
                    try:
                        if btn.is_visible() and btn.is_enabled():
                            text = btn.text_content().strip()
                            if text == 'Post' or text == 'پوسٹ':
                                print("✓ Clicking Post button...")
                                btn.click()
                                time.sleep(3)

                                print("\n" + "="*60)
                                print("✅ POST PUBLISHED SUCCESSFULLY!")
                                print("="*60)
                                return True
                    except:
                        continue

                print("⚠ Could not find Post button")
                print("Please click 'Post' manually...")
                input("Press Enter after posting...")
                return True
            else:
                print("❌ Could not find text editor")
                return False

        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please complete manually...")
            input("Press Enter when done...")
            return False

        finally:
            time.sleep(2)
            browser.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = "Hello from Agentic Sphere! 🤖"

    auto_post(message)
