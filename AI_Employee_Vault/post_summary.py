#!/usr/bin/env python3
"""
Post short Agentic Sphere summary to LinkedIn
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

def post_summary():
    print("=" * 60)
    print("Posting Agentic Sphere Summary to LinkedIn")
    print("=" * 60)
    print("\nOpening LinkedIn...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to LinkedIn feed
        page.goto('https://www.linkedin.com/feed/', timeout=30000)
        print("Waiting for feed to load...")
        time.sleep(3)

        try:
            # Wait for and click "Start a post"
            print("Looking for 'Start a post' button...")
            page.wait_for_selector('[aria-label="Start a post"]', timeout=15000)
            page.click('[aria-label="Start a post"]')
            print("Clicked 'Start a post'")
            time.sleep(2)

            # Find the text editor
            print("Finding text editor...")
            page.wait_for_selector('[contenteditable="true"]', timeout=10000)
            editor = page.query_selector('[contenteditable="true"]')

            if editor:
                editor.click()
                time.sleep(1)

                # Type the summary
                print("Typing post content...")
                page.keyboard.type(SHORT_SUMMARY, delay=3)
                time.sleep(2)

                # Click Post button
                print("Clicking Post button...")
                post_buttons = page.query_selector_all('button')

                posted = False
                for btn in post_buttons:
                    if btn.is_visible() and btn.is_enabled():
                        btn_text = btn.text_content()
                        if 'Post' in btn_text and 'Share' not in btn_text:
                            btn.click()
                            posted = True
                            print("Post button clicked!")
                            break

                if posted:
                    time.sleep(5)
                    print("\n" + "="*60)
                    print("✓ POST PUBLISHED SUCCESSFULLY!")
                    print("="*60)
                else:
                    print("Could not find Post button. Please click manually.")
                    input("Press Enter after posting...")
            else:
                print("Could not find text editor.")
                input("Please post manually and press Enter...")

        except Exception as e:
            print(f"Error: {e}")
            print("Please complete the post manually.")
            input("Press Enter when done...")

        finally:
            time.sleep(2)
            browser.close()

if __name__ == '__main__':
    post_summary()
