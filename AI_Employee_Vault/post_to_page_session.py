#!/usr/bin/env python3
"""
Post to Agentic Sphere LinkedIn Page using existing session
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

    # Use existing LinkedIn session
    session_path = Path('.linkedin_session')
    if not session_path.exists():
        print("Error: No LinkedIn session found. Please login first.")
        return False

    print("\nUsing existing LinkedIn session...")
    print("Opening Agentic Sphere page...\n")

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
            print("Page loaded. Looking for 'Create a post' button...")
            time.sleep(3)

            # Look for "Create a post" button
            buttons = page.query_selector_all('button')
            clicked = False

            for btn in buttons:
                if btn.is_visible():
                    btn_text = btn.text_content()
                    if 'Create a post' in btn_text or 'create a post' in btn_text.lower():
                        print(f"Found 'Create a post' button")
                        btn.click()
                        clicked = True
                        break

            if not clicked:
                print("Could not find 'Create a post' button automatically.")
                print("Please click 'Create a post' button manually...")
                input("Press Enter after clicking...")

            time.sleep(2)

            # Find and click the text editor
            print("Finding text editor...")
            editors = page.query_selector_all('[contenteditable="true"]')

            if editors:
                editor = editors[0]
                editor.click()
                time.sleep(1)

                # Type the summary
                print("Typing post content...")
                page.keyboard.type(SHORT_SUMMARY, delay=2)
                time.sleep(2)

                # Click Post button
                print("Clicking Post button...")
                post_buttons = page.query_selector_all('button')

                posted = False
                for btn in post_buttons:
                    if btn.is_visible() and btn.is_enabled():
                        btn_text = btn.text_content().strip()
                        if btn_text == 'Post' or btn_text == 'post':
                            btn.click()
                            posted = True
                            print("Post button clicked!")
                            break

                if posted:
                    time.sleep(5)
                    print("\n" + "="*60)
                    print("✓ POST PUBLISHED TO AGENTIC SPHERE PAGE!")
                    print("="*60)
                    return True
                else:
                    print("Could not find Post button. Please click manually.")
                    input("Press Enter after posting...")
                    return True
            else:
                print("Could not find text editor.")
                input("Please post manually and press Enter...")
                return True

        except Exception as e:
            print(f"Error: {e}")
            print("Please complete the post manually.")
            input("Press Enter when done...")
            return False

        finally:
            browser.close()

if __name__ == '__main__':
    post_to_page()
