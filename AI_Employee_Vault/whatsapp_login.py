"""
WhatsApp Login Script - Real Credentials Setup
Logs into WhatsApp Web and saves session for future use
"""

import time
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def login_whatsapp():
    """Login to WhatsApp Web and save session"""

    session_path = Path(".whatsapp_session")
    session_path.mkdir(exist_ok=True)

    print("\n" + "="*60)
    print("WhatsApp Web Login - Real Credentials Setup")
    print("="*60)
    print("\nStarting WhatsApp Web...")
    print("A browser window will open shortly.\n")

    try:
        with sync_playwright() as p:
            # Launch browser with persistent session
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,  # Show browser window
                viewport={'width': 1280, 'height': 720},
                args=['--disable-blink-features=AutomationControlled']
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            print("Opening https://web.whatsapp.com...")
            try:
                page.goto('https://web.whatsapp.com', timeout=60000, wait_until='domcontentloaded')
            except Exception as e:
                print(f"Navigation warning: {e}")
                print("Continuing anyway...")

            print("\n" + "-"*60)
            print("INSTRUCTIONS:")
            print("-"*60)
            print("1. A browser window has opened")
            print("2. Scan the QR code with your phone's WhatsApp")
            print("3. Go to: Settings > Linked Devices > Link a Device")
            print("4. Point your phone camera at the QR code")
            print("5. Wait for login to complete")
            print("-"*60 + "\n")

            # Wait for user to scan QR code and login
            print("Waiting for QR code scan... (this may take 30-60 seconds)")

            # Wait for chat list to appear (indicates successful login)
            try:
                page.wait_for_selector('[data-testid="chat-list"]', timeout=180000)
                print("\nSuccess! WhatsApp logged in!")
                print("Session saved to: .whatsapp_session/")

                # Keep browser open for a few seconds to ensure session is saved
                time.sleep(3)

            except Exception as e:
                print(f"\nTimeout waiting for login. Error: {e}")
                print("Make sure you scanned the QR code with your phone.")
                print("Keeping browser open - you can still scan the QR code manually.")
                print("Press Ctrl+C when done, or wait 5 more minutes...")
                try:
                    time.sleep(300)  # Wait 5 more minutes
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=10000)
                    print("\nSuccess! WhatsApp logged in!")
                except:
                    return False

            browser.close()

    except Exception as e:
        print(f"\nError during login: {e}")
        return False

    print("\n" + "="*60)
    print("WhatsApp session setup complete!")
    print("="*60)
    print("\nYour WhatsApp session is now saved and ready to use.")
    print("The AI Employee Vault can now monitor your WhatsApp messages.\n")

    return True

if __name__ == "__main__":
    success = login_whatsapp()
    sys.exit(0 if success else 1)
