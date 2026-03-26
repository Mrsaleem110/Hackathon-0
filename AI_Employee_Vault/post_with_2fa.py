#!/usr/bin/env python3
"""
LinkedIn Login with 2FA Support
Handles 2FA/Security verification and posts to company page
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

def login_with_2fa_and_post():
    """Login with 2FA support and post"""

    print("=" * 70)
    print("LinkedIn - Login with 2FA Support & Auto Post")
    print("=" * 70)
    print()

    session_path = Path('.linkedin_session_2fa')

    # Clean old session
    if session_path.exists():
        shutil.rmtree(session_path)
    session_path.mkdir()

    print(f"Email: {EMAIL}")
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
                time.sleep(3)
            else:
                print("ERROR: Could not find sign in button")
                browser.close()
                return False

            print()
            print("=" * 70)
            print("CHECKING FOR 2FA/SECURITY VERIFICATION...")
            print("=" * 70)
            print()

            # Wait for 2FA or security check
            current_url = page.url
            print(f"Current URL: {current_url}")

            # Check if we're on 2FA page
            if 'checkpoint' in current_url or 'verify' in current_url.lower():
                print("2FA/Security verification detected!")
                print()
                print("PLEASE COMPLETE THE VERIFICATION IN THE BROWSER:")
                print("- Enter the code from your email/phone")
                print("- Or approve the login request")
                print("- Or answer security questions")
                print()
                print("Waiting for verification to complete...")
                print()

                # Wait for verification to complete
                verified = False
                for i in range(120):  # Wait up to 10 minutes
                    time.sleep(5)
                    current_url = page.url

                    if i % 4 == 0:  # Print every 20 seconds
                        print(f"[{i*5}s] Waiting... URL: {current_url[:60]}")

                    # Check if verification is done
                    if 'checkpoint' not in current_url and 'verify' not in current_url.lower():
                        if '/feed' in current_url or '/company/' in current_url or '/dashboard' in current_url:
                            verified = True
                            print("\nVerification complete!")
                            break

                if not verified:
                    print("\nVerification timeout. Please try again.")
                    browser.close()
                    return False

            else:
                print("Waiting for login to complete...")
                page.wait_for_load_state('networkidle', timeout=30000)
                time.sleep(2)

                current_url = page.url
                print(f"Current URL: {current_url}")

                if 'login' in current_url.lower():
                    print("ERROR: Login failed")
                    error_elements = page.query_selector_all('[role="alert"]')
                    for elem in error_elements:
                        error_text = elem.text_content()
                        if error_text.strip():
                            print(f"  Error: {error_text}")
                    browser.close()
                    return False

            time.sleep(2)

            print("Login successful! Navigating to company page...")
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
                'method': 'login_with_2fa_support',
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
    success = login_with_2fa_and_post()
    exit(0 if success else 1)
