#!/usr/bin/env python3
"""
LinkedIn Direct Post - Using Saved Session
Posts directly to Agentic Sphere company page using browser automation
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
from datetime import datetime

POST_TEXT = """🤖 Meet Agentic Sphere - Your Personal AI Employee

Autonomous. Intelligent. Always Working.

Your AI employee monitors your emails, messages, and opportunities 24/7 - then takes intelligent action with your approval.

What makes Agentic Sphere different:
✓ 24/7 Autonomous Operation - Never miss an opportunity
✓ Multi-Channel Integration - Gmail, WhatsApp, LinkedIn all connected
✓ Intelligent Decision Making - Powered by Claude AI
✓ Complete Audit Trail - Full transparency on every action
✓ Human-in-the-Loop Control - You stay in charge

From detecting client inquiries to scheduling meetings, Agentic Sphere handles it all intelligently.

The future of productivity is here.

#AI #Automation #AgenticSphere #ArtificialIntelligence #Productivity #FutureOfWork #BusinessAutomation"""

COMPANY_URL = "https://www.linkedin.com/company/agentic-sphere/"

def post_to_company_page():
    """Post to Agentic Sphere company page using saved session"""

    print("=" * 70)
    print("LinkedIn - Post to Agentic Sphere Company Page")
    print("=" * 70)
    print()

    session_path = Path('.linkedin_session')

    if not session_path.exists():
        print("ERROR: LinkedIn session not found at .linkedin_session")
        print("Please login to LinkedIn first")
        return False

    print(f"Using session: {session_path}")
    print(f"Company URL: {COMPANY_URL}")
    print()

    try:
        with sync_playwright() as p:
            print("Launching browser with saved session...")
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                viewport={'width': 1280, 'height': 800},
                args=['--disable-blink-features=AutomationControlled']
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            print("Navigating to company page...")
            page.goto(COMPANY_URL, timeout=30000)
            time.sleep(3)

            print("Waiting for page to load...")
            page.wait_for_load_state('networkidle', timeout=15000)
            time.sleep(2)

            print("Looking for 'Create post' or 'Share' button...")

            # Try different selectors for the post button
            post_button_selectors = [
                'button[aria-label*="Create post"]',
                'button[aria-label*="Share"]',
                'button:has-text("Create post")',
                'button:has-text("Share")',
                '[data-test-id="share-box"]',
                '.share-box-feed-entry__trigger',
                'button[aria-label*="Start a post"]',
            ]

            post_button = None
            for selector in post_button_selectors:
                try:
                    post_button = page.query_selector(selector)
                    if post_button and post_button.is_visible():
                        print(f"Found button with selector: {selector}")
                        break
                except:
                    pass

            if not post_button:
                print("ERROR: Could not find post button")
                print("Available buttons on page:")
                buttons = page.query_selector_all('button')
                for i, btn in enumerate(buttons[:10]):
                    try:
                        text = btn.text_content()
                        aria = btn.get_attribute('aria-label')
                        print(f"  {i}: {text[:30]} | aria-label: {aria}")
                    except:
                        pass
                browser.close()
                return False

            print("Clicking post button...")
            post_button.click()
            time.sleep(2)

            print("Looking for text editor...")
            # Try different editor selectors
            editor_selectors = [
                '[contenteditable="true"]',
                '.ql-editor',
                '[data-test-id="post-editor"]',
                'div[role="textbox"]',
            ]

            editor = None
            for selector in editor_selectors:
                try:
                    editor = page.query_selector(selector)
                    if editor and editor.is_visible():
                        print(f"Found editor with selector: {selector}")
                        break
                except:
                    pass

            if not editor:
                print("ERROR: Could not find text editor")
                browser.close()
                return False

            print("Clicking editor and typing post...")
            editor.click()
            time.sleep(1)

            # Type the post text
            print(f"Typing {len(POST_TEXT)} characters...")
            editor.type(POST_TEXT, delay=2)
            time.sleep(2)

            print("Looking for Post/Publish button...")
            # Try different post button selectors
            publish_selectors = [
                'button[aria-label*="Post"]',
                'button:has-text("Post")',
                'button:has-text("Publish")',
                'button[type="button"]:has-text("Post")',
                '.share-actions__primary-action',
            ]

            publish_button = None
            for selector in publish_selectors:
                try:
                    publish_button = page.query_selector(selector)
                    if publish_button and publish_button.is_visible():
                        print(f"Found publish button with selector: {selector}")
                        break
                except:
                    pass

            if not publish_button:
                print("ERROR: Could not find publish button")
                print("Please click the Post button manually...")
                input("Press Enter after posting...")
                browser.close()
                return True

            print("Clicking publish button...")
            publish_button.click()
            time.sleep(5)

            print()
            print("=" * 70)
            print("SUCCESS! Post published to Agentic Sphere!")
            print("=" * 70)
            print()

            # Log the success
            log_file = Path('Logs/2026-03-06.json')
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'linkedin_post_published',
                'post_title': 'Agentic Sphere - Your Personal AI Employee',
                'status': 'success',
                'platform': 'linkedin',
                'method': 'browser_automation',
                'company_page': COMPANY_URL
            }

            try:
                if log_file.exists():
                    logs = json.loads(log_file.read_text())
                else:
                    logs = []
                logs.append(log_entry)
                log_file.write_text(json.dumps(logs, indent=2))
                print("Logged to vault successfully")
            except Exception as e:
                print(f"Warning: Could not log to vault: {e}")

            browser.close()
            return True

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = post_to_company_page()
    exit(0 if success else 1)
