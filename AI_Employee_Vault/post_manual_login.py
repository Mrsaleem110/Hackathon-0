#!/usr/bin/env python3
"""
LinkedIn Manual Login & Auto Post
Opens browser for manual login, then auto-posts
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
from datetime import datetime
import shutil

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

def manual_login_and_post():
    """Manual login then auto post"""

    print("=" * 70)
    print("LinkedIn - Manual Login & Auto Post")
    print("=" * 70)
    print()

    session_path = Path('.linkedin_session_manual')

    # Clean old session
    if session_path.exists():
        shutil.rmtree(session_path)
    session_path.mkdir()

    try:
        with sync_playwright() as p:
            print("Launching browser...")
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                viewport={'width': 1280, 'height': 800},
                args=['--disable-blink-features=AutomationControlled']
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            print("Going to LinkedIn...")
            page.goto("https://www.linkedin.com/", timeout=30000)

            print()
            print("=" * 70)
            print("PLEASE LOGIN MANUALLY IN THE BROWSER")
            print("=" * 70)
            print()
            print("After login, I will automatically post to the company page")
            print()

            # Wait for login
            logged_in = False
            for i in range(120):  # Wait up to 10 minutes
                time.sleep(5)
                current_url = page.url

                if i % 4 == 0:  # Print every 20 seconds
                    print(f"[{i*5}s] Waiting for login... URL: {current_url[:60]}")

                # Check if logged in
                if '/feed' in current_url or '/company/' in current_url or '/dashboard' in current_url:
                    if 'login' not in current_url.lower():
                        logged_in = True
                        print("\nLogin detected!")
                        break

            if not logged_in:
                print("\nLogin timeout. Please try again.")
                browser.close()
                return False

            time.sleep(2)

            print("Navigating to company page...")
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
                print("Please click 'Create post' manually and I'll type the content")
                input("Press Enter after clicking Create post...")
            else:
                print("Clicking post button...")
                post_button.click()
                time.sleep(2)

            print("Looking for text editor...")
            editor = page.query_selector('[contenteditable="true"]')

            if not editor:
                print("ERROR: Could not find editor")
                print("Please type the post manually")
                input("Press Enter after posting...")
                browser.close()
                return True

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
                print("Please click Post manually")
                input("Press Enter after posting...")
                browser.close()
                return True

            print("Clicking Post button...")
            publish_button.click()
            time.sleep(5)

            print()
            print("=" * 70)
            print("SUCCESS! Post published!")
            print("=" * 70)
            print()

            # Log success
            log_file = Path('Logs/2026-03-06.json')
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'linkedin_post_published',
                'post_title': 'Agentic Sphere - Your Personal AI Employee',
                'status': 'success',
                'platform': 'linkedin',
                'method': 'manual_login_auto_post'
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
    success = manual_login_and_post()
    exit(0 if success else 1)
