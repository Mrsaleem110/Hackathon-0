"""
LinkedIn Login Script - Real Credentials Setup
Logs into LinkedIn and saves session for future use
"""

import time
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def login_linkedin():
    """Login to LinkedIn and save session"""

    session_path = Path(".linkedin_session")
    session_path.mkdir(exist_ok=True)

    print("\n" + "="*60)
    print("LinkedIn Login - Real Credentials Setup")
    print("="*60)
    print("\nStarting LinkedIn...")
    print("A browser window will open shortly.\n")

    try:
        with sync_playwright() as p:
            # Launch browser with persistent session
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,  # Show browser window
                viewport={'width': 1280, 'height': 720}
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            print("Opening https://www.linkedin.com...")
            page.goto('https://www.linkedin.com', timeout=30000)

            print("\n" + "-"*60)
            print("INSTRUCTIONS:")
            print("-"*60)
            print("1. A browser window has opened to LinkedIn")
            print("2. Enter your LinkedIn email address")
            print("3. Enter your LinkedIn password")
            print("4. Complete any 2-factor authentication if prompted")
            print("5. Wait for login to complete")
            print("-"*60 + "\n")

            # Wait for user to login
            print("Waiting for login... (this may take 2-3 minutes)")
            print("Keep the browser window open and complete login manually.\n")

            # Try multiple selectors to detect successful login
            login_success = False
            selectors = [
                '[data-testid="feed"]',  # Feed page
                '[data-testid="global-nav"]',  # Navigation bar
                'a[href*="/feed/"]',  # Feed link
                '.global-nav',  # Global navigation
            ]

            for attempt in range(6):  # Try for up to 3 minutes (6 x 30 seconds)
                try:
                    for selector in selectors:
                        try:
                            page.wait_for_selector(selector, timeout=5000)
                            print(f"✓ Login detected! Found: {selector}")
                            login_success = True
                            break
                        except:
                            pass

                    if login_success:
                        break

                    print(f"Waiting... ({(attempt+1)*30} seconds elapsed)")
                    time.sleep(30)

                except Exception as e:
                    print(f"Check attempt {attempt+1}: {str(e)[:50]}")
                    time.sleep(5)

            if login_success:
                print("\n✓ Success! LinkedIn logged in!")
                print("Session saved to: .linkedin_session/")
                time.sleep(3)
            else:
                print("\n⚠ Login detection timeout.")
                print("If you're logged in, the session may still be saved.")
                print("Press Enter to continue...")
                input()

            browser.close()

    except Exception as e:
        print(f"\nError during login: {e}")
        return False

    print("\n" + "="*60)
    print("LinkedIn session setup complete!")
    print("="*60)
    print("\nYour LinkedIn session is now saved and ready to use.")
    print("The AI Employee Vault can now monitor your LinkedIn messages.\n")

    return True

if __name__ == "__main__":
    success = login_linkedin()
    sys.exit(0 if success else 1)
