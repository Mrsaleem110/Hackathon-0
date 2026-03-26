#!/usr/bin/env python3
"""
LinkedIn Direct Post - Navigate to composer
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

def post_direct():
    """Post directly using composer"""

    print("=" * 70)
    print("LinkedIn - Direct Post")
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

            print("Navigating to feed...")
            page.goto("https://www.linkedin.com/feed/", timeout=30000)
            time.sleep(3)

            print("Looking for share box...")

            # Look for the share box
            share_box = page.query_selector('[data-test-id="share-box"]')
            if share_box:
                print("Found share box, clicking...")
                share_box.click()
                time.sleep(2)
            else:
                print("Share box not found, trying alternative...")
                # Try clicking on any contenteditable area
                editors = page.query_selector_all('[contenteditable="true"]')
                if editors:
                    print(f"Found {len(editors)} editors, clicking first one...")
                    editors[0].click()
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
            print("✅ SUCCESS! Post published!")
            print("=" * 70)
            print()

            # Log success
            log_file = Path('Logs/2026-03-06.json')
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'linkedin_post_published',
                'post_title': 'Agentic Sphere Introduction',
                'status': 'success',
                'platform': 'linkedin'
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
    success = post_direct()
    exit(0 if success else 1)
