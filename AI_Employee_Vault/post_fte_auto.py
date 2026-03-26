#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated LinkedIn Post - Agentic Sphere FTE
Posts "hello from Agentic Sphere FTE" to the company page
"""
import time
import sys
from playwright.sync_api import sync_playwright

# Force UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

POST_TEXT = "hello from Agentic Sphere FTE"

def post_to_linkedin():
    print("=" * 70)
    print("POSTING TO AGENTIC SPHERE LINKEDIN PAGE")
    print("=" * 70)
    print(f"\nPost content: {POST_TEXT}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Navigate to Agentic Sphere page
            print("1. Loading Agentic Sphere page...")
            page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=30000)
            time.sleep(4)

            # Click "Create a post" button
            print("2. Looking for 'Create a post' button...")

            button_clicked = False

            # Try to find and click the button
            try:
                # Wait for any button that might be the create post button
                page.wait_for_selector('button', timeout=5000)
                buttons = page.query_selector_all('button')

                for btn in buttons:
                    if btn.is_visible():
                        btn_text = btn.text_content().lower()
                        if 'create' in btn_text or 'post' in btn_text:
                            print(f"   Found button: {btn_text}")
                            btn.click()
                            button_clicked = True
                            time.sleep(2)
                            break

                if not button_clicked:
                    print("   Trying aria-label approach...")
                    page.click('[aria-label*="post"]', timeout=3000)
                    button_clicked = True
                    time.sleep(2)

            except Exception as e:
                print(f"   Button click failed: {str(e)}")

            if not button_clicked:
                print("   Could not click button, trying to find editor directly...")

            # Find and click the text editor
            print("3. Finding text editor...")
            try:
                page.wait_for_selector('[contenteditable="true"]', timeout=15000)
                editor = page.query_selector('[contenteditable="true"]')

                if editor:
                    editor.click()
                    time.sleep(1)

                    # Type the post
                    print(f"4. Typing post: '{POST_TEXT}'")
                    page.keyboard.type(POST_TEXT, delay=1)
                    time.sleep(2)

                    # Find and click Post button
                    print("5. Looking for Post button...")
                    post_buttons = page.query_selector_all('button')

                    posted = False
                    for btn in post_buttons:
                        if btn.is_visible() and btn.is_enabled():
                            btn_text = btn.text_content().strip()
                            if btn_text == 'Post':
                                print("   Found Post button")
                                btn.click()
                                posted = True
                                time.sleep(5)
                                break

                    if posted:
                        print("\n" + "=" * 70)
                        print("SUCCESS: POST PUBLISHED!")
                        print("=" * 70)
                        return True
                    else:
                        print("   Could not find Post button")
                        return False
                else:
                    print("   Could not find text editor")
                    return False

            except Exception as e:
                print(f"   Error with text editor: {str(e)}")
                return False

        except Exception as e:
            print(f"Error: {str(e)}")
            return False
        finally:
            time.sleep(2)
            browser.close()

if __name__ == '__main__':
    success = post_to_linkedin()
    exit(0 if success else 1)
