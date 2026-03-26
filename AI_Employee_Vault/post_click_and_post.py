#!/usr/bin/env python3
"""
LinkedIn Post - Manual Button Click, Auto Post
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
    """Post to Agentic Sphere company page"""

    print("=" * 70)
    print("LinkedIn - Post to Agentic Sphere Page")
    print("=" * 70)
    print()

    session_path = Path('.linkedin_session_manual')

    if not session_path.exists():
        print("ERROR: No existing session found.")
        return False

    try:
        with sync_playwright() as p:
            print("Launching browser...")
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                viewport={'width': 1280, 'height': 800}
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            print("Navigating to Agentic Sphere company page...")
            page.goto(COMPANY_URL, timeout=30000)
            time.sleep(3)

            print()
            print("=" * 70)
            print("PLEASE CLICK THE 'CREATE POST' BUTTON")
            print("=" * 70)
            print()
            print("I will automatically type and post the content after you click it.")
            print()

            # Wait for user to click the button and editor to appear
            print("Waiting for editor to appear...")
            for i in range(60):  # Wait up to 60 seconds
                time.sleep(1)
                editor = page.query_selector('[contenteditable="true"]')
                if editor:
                    print("Editor found! Starting to type...")
                    break
                if i % 10 == 0:
                    print(f"  [{i}s] Still waiting...")
            else:
                print("Timeout waiting for editor")
                browser.close()
                return False

            time.sleep(1)

            print(f"Typing post ({len(POST_TEXT)} characters)...")
            editor.click()
            time.sleep(0.5)
            editor.type(POST_TEXT, delay=1)
            time.sleep(2)

            print("Looking for Post button...")
            publish_button = None

            # Try multiple selectors
            selectors = [
                'button[aria-label*="Post"]',
                'button:has-text("Post")',
                'button[type="submit"]',
            ]

            for selector in selectors:
                try:
                    btn = page.query_selector(selector)
                    if btn and btn.is_visible():
                        publish_button = btn
                        print(f"Found Post button: {selector}")
                        break
                except:
                    pass

            if not publish_button:
                print("ERROR: Could not find Post button")
                print("Please click Post manually")
                input("Press Enter after posting...")
                browser.close()
                return True

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
                'company_page': COMPANY_URL
            }

            try:
                if log_file.exists():
                    logs = json.loads(log_file.read_text())
                else:
                    logs = []
                logs.append(log_entry)
                log_file.write_text(json.dumps(logs, indent=2))
                print("Logged to vault")
            except Exception as e:
                print(f"Warning: {e}")

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
