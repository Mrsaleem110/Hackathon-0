#!/usr/bin/env python3
"""
Simple LinkedIn Post - Uses existing session
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
from datetime import datetime

POST_TEXT = """🚀 Introducing Agentic Sphere

Your autonomous AI employee that works 24/7.

Agentic Sphere monitors your emails, messages, and opportunities - then takes intelligent action with your approval.

✓ Autonomous Decision Making
✓ Multi-Channel Integration (Gmail, WhatsApp, LinkedIn)
✓ Intelligent Planning with Claude AI
✓ Complete Audit Trail
✓ Human-in-the-Loop Control

The future of productivity is here.

#AI #Automation #AgenticSphere #FutureOfWork #Innovation"""

COMPANY_URL = "https://www.linkedin.com/company/agentic-sphere/"

def post_to_page():
    """Post to Agentic Sphere company page using existing session"""

    print("=" * 70)
    print("LinkedIn - Post to Agentic Sphere Page")
    print("=" * 70)
    print()

    # Try to use existing session
    session_path = Path('.linkedin_session_manual')

    if not session_path.exists():
        print("ERROR: No existing session found. Please log in first.")
        return False

    try:
        with sync_playwright() as p:
            print("Launching browser with existing session...")
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                viewport={'width': 1280, 'height': 800}
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            print("Navigating to Agentic Sphere company page...")
            page.goto(COMPANY_URL, timeout=30000)
            time.sleep(3)

            print("Waiting for page to load...")
            try:
                page.wait_for_load_state('networkidle', timeout=15000)
            except:
                pass
            time.sleep(2)

            print("Looking for 'Create post' button...")

            # Try different selectors
            post_button_selectors = [
                'button[aria-label*="Create post"]',
                'button[aria-label*="Share"]',
                'button:has-text("Create post")',
                '.share-box-feed-entry__trigger',
                'button[aria-label*="Start a post"]',
            ]

            post_button = None
            for selector in post_button_selectors:
                try:
                    post_button = page.query_selector(selector)
                    if post_button and post_button.is_visible():
                        print(f"Found button: {selector}")
                        break
                except:
                    pass

            if not post_button:
                print("ERROR: Could not find post button")
                browser.close()
                return False

            print("Clicking post button...")
            post_button.click()
            time.sleep(2)

            print("Looking for text editor...")
            editor = page.query_selector('[contenteditable="true"]')

            if not editor:
                print("ERROR: Could not find editor")
                browser.close()
                return False

            print("Clicking editor...")
            editor.click()
            time.sleep(1)

            print(f"Typing post ({len(POST_TEXT)} characters)...")
            editor.type(POST_TEXT, delay=1)
            time.sleep(2)

            print("Looking for Post button...")
            publish_button = page.query_selector('button[aria-label*="Post"]')

            if not publish_button:
                publish_button = page.query_selector('button:has-text("Post")')

            if not publish_button:
                print("ERROR: Could not find Post button")
                browser.close()
                return False

            print("Clicking Post button...")
            publish_button.click()
            time.sleep(5)

            print()
            print("=" * 70)
            print("✅ SUCCESS! Post published to Agentic Sphere!")
            print("=" * 70)
            print()

            # Log success
            log_file = Path('Logs/2026-03-06.json')
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'linkedin_post_published',
                'post_title': 'Agentic Sphere Introduction',
                'status': 'success',
                'platform': 'linkedin',
                'method': 'simple_post',
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
                print(f"Warning: Could not log: {e}")

            browser.close()
            return True

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = post_to_page()
    exit(0 if success else 1)
