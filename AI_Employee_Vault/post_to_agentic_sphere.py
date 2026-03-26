#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post to Agentic Sphere LinkedIn Company Page using existing session
With extended wait time for page to fully load
"""
import sys
import time
import io
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def post_to_company_page(message):
    """Post to Agentic Sphere company page using saved session"""

    print("=" * 60)
    print("Posting to Agentic Sphere LinkedIn Company Page")
    print("=" * 60)
    print(f"\nMessage:\n{message}\n")

    # Try different session paths
    session_paths = [
        '.linkedin_session_auto',
        '.linkedin_session',
        '.linkedin_session_fresh',
        '.linkedin_session_manual',
    ]

    for session_path in session_paths:
        session_dir = Path(session_path)
        if not session_dir.exists():
            continue

        print(f"\nTrying session: {session_path}")

        try:
            with sync_playwright() as p:
                # Launch browser with persistent context
                context = p.chromium.launch_persistent_context(
                    str(session_dir),
                    headless=False,
                    viewport={'width': 1920, 'height': 1080}
                )

                page = context.new_page()

                try:
                    # Go to Agentic Sphere company page
                    print("Opening Agentic Sphere company page...")
                    page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=30000)

                    # Wait 3 minutes for page to fully load
                    print("⏳ Waiting 3 minutes for page to fully load...")
                    time.sleep(180)

                    # Check if logged in
                    if 'login' in page.url.lower() or 'authwall' in page.url.lower():
                        print(f"❌ Not logged in with {session_path}")
                        context.close()
                        continue

                    print("✓ Logged in successfully")

                    # Look for "Create a post" button
                    print("Looking for post button...")
                    time.sleep(2)

                    # Try multiple selectors
                    selectors = [
                        'button:has-text("Create a post")',
                        'button:has-text("Start a post")',
                        '[data-control-name="share_box_trigger"]',
                        '.share-box-feed-entry__trigger',
                        'button[aria-label*="Create"]',
                        'button[aria-label*="Start"]',
                    ]

                    post_button_found = False

                    for selector in selectors:
                        try:
                            elem = page.query_selector(selector)
                            if elem and elem.is_visible():
                                print(f"✓ Found button with selector: {selector}")
                                elem.click()
                                post_button_found = True
                                time.sleep(2)
                                break
                        except:
                            pass

                    if not post_button_found:
                        print("⚠️  Trying to find button by text content...")
                        buttons = page.query_selector_all('button')
                        for btn in buttons:
                            try:
                                text = btn.text_content().strip()
                                if 'Create' in text or 'Start' in text:
                                    print(f"✓ Found button: {text}")
                                    btn.click()
                                    post_button_found = True
                                    time.sleep(2)
                                    break
                            except:
                                pass

                    if not post_button_found:
                        print("❌ Could not find post button")
                        context.close()
                        continue

                    # Find text editor
                    print("Looking for text editor...")
                    editor = page.query_selector('[contenteditable="true"]')

                    if not editor:
                        time.sleep(2)
                        editor = page.query_selector('[contenteditable="true"]')

                    if editor:
                        print("✓ Found text editor")
                        editor.click()
                        time.sleep(1)

                        # Type message
                        print("✓ Typing message...")
                        page.keyboard.type(message, delay=30)
                        time.sleep(2)

                        # Find and click Post button
                        print("Looking for Post button...")
                        time.sleep(1)

                        post_buttons = page.query_selector_all('button')
                        posted = False

                        for btn in post_buttons:
                            try:
                                if btn.is_visible() and btn.is_enabled():
                                    btn_text = btn.text_content().strip()
                                    if btn_text == 'Post' or btn_text == 'پوسٹ':
                                        print("✓ Clicking Post button...")
                                        btn.click()
                                        posted = True
                                        time.sleep(3)
                                        break
                            except:
                                pass

                        if posted:
                            print("\n" + "="*60)
                            print("✅ SUCCESS! POST PUBLISHED TO AGENTIC SPHERE!")
                            print("="*60)
                            context.close()
                            return True
                        else:
                            print("❌ Could not find Post button")
                            context.close()
                            continue
                    else:
                        print("❌ Could not find text editor")
                        context.close()
                        continue

                except Exception as e:
                    print(f"❌ Error: {e}")
                    import traceback
                    traceback.print_exc()
                    context.close()
                    continue

        except Exception as e:
            print(f"❌ Session error: {e}")
            continue

    print("\n❌ Could not post with any available session")
    return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = "Hello from Agentic Sphere! 🚀"

    success = post_to_company_page(message)
    sys.exit(0 if success else 1)
