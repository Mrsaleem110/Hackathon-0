#!/usr/bin/env python3
"""
LinkedIn Direct Login & Post
Login with credentials and post to Agentic Sphere company page
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
EMAIL = "sm6928234@gmail.com"
PASSWORD = "$@!eem1234"

def login_and_post():
    """Login to LinkedIn and post to company page"""

    print("=" * 70)
    print("LinkedIn - Auto Login & Post")
    print("=" * 70)
    print()

    session_path = Path('.linkedin_session_auto')

    # Clean old session
    if session_path.exists():
        shutil.rmtree(session_path)
    session_path.mkdir()

    print(f"Email: {EMAIL}")
    print(f"Session: {session_path}")
    print()

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

            print("Going to LinkedIn login page...")
            page.goto("https://www.linkedin.com/login", timeout=30000)
            time.sleep(2)

            print("Entering email...")
            email_input = page.query_selector('input[name="session_key"]')
            if email_input:
                email_input.fill(EMAIL)
                time.sleep(1)
            else:
                print("ERROR: Could not find email input")
                browser.close()
                return False

            print("Entering password...")
            password_input = page.query_selector('input[name="session_password"]')
            if password_input:
                password_input.fill(PASSWORD)
                time.sleep(1)
            else:
                print("ERROR: Could not find password input")
                browser.close()
                return False

            print("Clicking Sign in button...")
            sign_in_button = page.query_selector('button[type="submit"]')
            if sign_in_button:
                sign_in_button.click()
                time.sleep(5)
            else:
                print("ERROR: Could not find sign in button")
                browser.close()
                return False

            print("Waiting for login to complete...")
            page.wait_for_load_state('networkidle', timeout=30000)
            time.sleep(3)

            current_url = page.url
            print(f"Current URL: {current_url}")

            if 'login' in current_url.lower():
                print("ERROR: Login failed - still on login page")
                print("Checking for error messages...")
                error_elements = page.query_selector_all('[role="alert"]')
                for elem in error_elements:
                    print(f"  Error: {elem.text_content()}")
                browser.close()
                return False

            print("Login successful! Navigating to company page...")
            page.goto(COMPANY_URL, timeout=30000)
            time.sleep(3)

            print("Waiting for page to load...")
            page.wait_for_load_state('networkidle', timeout=15000)
            time.sleep(2)

            print("Looking for 'Create post' button...")

            # Try different selectors
            post_button_selectors = [
                'button[aria-label*="Create post"]',
                'button[aria-label*="Share"]',
                'button:has-text("Create post")',
                '.share-box-feed-entry__trigger',
                'button[aria-label*="Start a post"]',
                'div[data-test-id="share-box"]',
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
                print("Checking page content...")
                page_content = page.content()
                if 'Create post' in page_content:
                    print("'Create post' text found in page")
                if 'Share' in page_content:
                    print("'Share' text found in page")
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
            print("SUCCESS! Post published to Agentic Sphere!")
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
                'method': 'auto_login_and_post',
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
    success = login_and_post()
    exit(0 if success else 1)
