#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Post - Direct Admin Page
Posts directly from company admin page
Usage: python linkedin_post_admin.py "Your message here"
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Direct URL to company admin post page
ADMIN_POST_URL = "https://www.linkedin.com/company/112056250/admin/page-posts/published/?share=true"

def post_to_linkedin(message):
    """Post to LinkedIn via admin page"""

    print("=" * 60)
    print("LinkedIn Admin Post - Direct")
    print("=" * 60)
    print(f"\nMessage: {message}\n")

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
            # Go directly to admin post page
            print("Opening LinkedIn admin page...")
            page.goto(ADMIN_POST_URL, timeout=30000)
            time.sleep(5)

            # Check if need to login
            if 'login' in page.url.lower():
                print("\n" + "="*60)
                print("Please login in the browser")
                print("="*60)
                input("Press Enter after logging in...")

                # Go to admin page again
                page.goto(ADMIN_POST_URL, timeout=30000)
                time.sleep(5)

            print("✓ On admin page\n")

            # The ?share=true parameter should open the post dialog automatically
            # Wait for the dialog to appear
            print("Waiting for post dialog...")
            time.sleep(5)

            # Look for text editor
            print("Looking for text editor...")
            editor = page.query_selector('[contenteditable="true"]')

            if not editor:
                print("Waiting a bit more...")
                time.sleep(5)
                editor = page.query_selector('[contenteditable="true"]')

            if editor:
                print("✓ Found text editor")
                editor.click()
                time.sleep(1)

                # Type message
                print("✓ Typing message...")
                page.keyboard.type(message, delay=50)
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
                            if btn_text == 'Post' or btn_text == 'Publish':
                                print(f"✓ Clicking '{btn_text}' button...")
                                btn.click()
                                posted = True
                                break
                    except:
                        pass

                if posted:
                    time.sleep(5)
                    print("\n" + "="*60)
                    print("✅ SUCCESS! POST PUBLISHED!")
                    print("="*60)
                    time.sleep(3)
                    browser.close()
                    return True
                else:
                    print("Could not find Post button automatically")
                    print("Please click Post manually in the browser")
                    input("Press Enter after posting...")
                    browser.close()
                    return True
            else:
                print("❌ Could not find text editor")
                print("The post dialog might not have opened automatically")
                print("\nPlease:")
                print("1. Click 'Create a post' button manually")
                print("2. Type your message")
                print("3. Click Post")
                input("\nPress Enter when done...")
                browser.close()
                return False

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            print("\nPlease complete the post manually")
            input("Press Enter when done...")
            browser.close()
            return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = "Hello from Agentic Sphere! 🚀"

    print("\n" + "="*60)
    print("LINKEDIN ADMIN POST")
    print("="*60)
    print("Posting directly to Agentic Sphere company page")
    print("="*60 + "\n")

    success = post_to_linkedin(message)

    if success:
        print("\n✅ Done!")
    else:
        print("\n⚠️  Please complete manually")

    sys.exit(0 if success else 1)
