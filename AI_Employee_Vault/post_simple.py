#!/usr/bin/env python3
"""
Post to Agentic Sphere Page - Manual button click, auto type and post
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SHORT_SUMMARY = """🤖 Agentic Sphere - Your Personal AI Employee

Autonomous. Intelligent. Always Working.

Agentic Sphere monitors your emails, messages, and opportunities - then takes action on your behalf with your approval.

✓ 24/7 Autonomous Operation
✓ Multi-Channel Integration (Gmail, WhatsApp, LinkedIn)
✓ Intelligent Decision Making with Claude AI
✓ Complete Audit Trail & Transparency
✓ Human-in-the-Loop Control

The future of productivity is here.

#AI #Automation #AgenticSphere #ArtificialIntelligence #Productivity"""

def post_to_page():
    print("=" * 60)
    print("Posting to Agentic Sphere LinkedIn Page")
    print("=" * 60)

    session_path = Path('.linkedin_session')
    if not session_path.exists():
        print("Error: No LinkedIn session found.")
        return False

    print("\nOpening Agentic Sphere page...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            viewport={'width': 1280, 'height': 800}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            # Go to Agentic Sphere page
            page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=60000, wait_until='domcontentloaded')
            print("Page loaded!")
            print("\nPlease click the 'Create a post' button on the page...")
            print("I will wait for the text editor to appear, then automatically type and post.\n")

            # Wait for the text editor to appear (which appears after clicking "Create a post")
            print("Waiting for text editor...")
            page.wait_for_selector('[contenteditable="true"]', timeout=60000)
            print("Text editor found! Typing post content...\n")

            time.sleep(1)

            # Click the editor
            editor = page.query_selector('[contenteditable="true"]')
            if editor:
                editor.click()
                time.sleep(1)

                # Type the summary
                print("Typing post...")
                page.keyboard.type(SHORT_SUMMARY, delay=2)
                time.sleep(2)

                # Look for and click Post button
                print("Looking for Post button...")
                time.sleep(1)

                # Try to find Post button
                post_buttons = page.query_selector_all('button')
                posted = False

                for btn in post_buttons:
                    if btn.is_visible() and btn.is_enabled():
                        btn_text = btn.text_content().strip()
                        if btn_text == 'Post':
                            print("Found Post button! Clicking...")
                            btn.click()
                            posted = True
                            break

                if posted:
                    time.sleep(5)
                    print("\n" + "="*60)
                    print("✓ POST PUBLISHED SUCCESSFULLY!")
                    print("="*60)
                    return True
                else:
                    print("Could not find Post button.")
                    print("Please click the Post button manually.")
                    input("Press Enter after posting...")
                    return True

        except Exception as e:
            print(f"Error: {e}")
            return False

        finally:
            time.sleep(2)
            browser.close()

if __name__ == '__main__':
    post_to_page()
