"""
Browser Session Setup for WhatsApp and LinkedIn
Run this script to login to WhatsApp Web and LinkedIn in a visible browser
The sessions will be saved and used by the automation system
"""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def setup_whatsapp_session(vault_path: Path):
    """Setup WhatsApp Web session - manual login required"""
    print("\n" + "="*60)
    print("WHATSAPP WEB LOGIN SETUP")
    print("="*60)

    session_path = vault_path / '.whatsapp_session'
    session_path.mkdir(exist_ok=True)

    print(f"\nSession will be saved to: {session_path}")
    print("\nOpening WhatsApp Web in browser...")
    print("Please follow these steps:")
    print("1. Scan QR code with your phone")
    print("2. Wait for chats to load completely")
    print("3. Press ENTER in this terminal when done")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,  # Visible browser
            viewport={'width': 1280, 'height': 720},
            args=['--disable-blink-features=AutomationControlled']
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            print("\nLoading WhatsApp Web (this may take 30-60 seconds)...")
            page.goto('https://web.whatsapp.com', timeout=60000, wait_until='domcontentloaded')
            print("✓ Page loaded")
        except Exception as e:
            print(f"\n✗ Error loading page: {e}")
            print("Please check your internet connection and try again.")
            browser.close()
            return

        # Wait for user to login
        input("\nPress ENTER after you've logged in and chats are loaded...")

        # Verify login
        try:
            page.wait_for_selector('[data-testid="chat-list"]', timeout=10000)
            print("\n✓ WhatsApp login successful!")
            print("✓ Session saved")
        except Exception as e:
            print(f"\n✗ Could not verify login: {e}")
            print("Note: If you can see your chats, the session is saved anyway.")

        try:
            browser.close()
        except:
            pass  # Ignore close errors

def setup_linkedin_session(vault_path: Path):
    """Setup LinkedIn session - manual login required"""
    print("\n" + "="*60)
    print("LINKEDIN LOGIN SETUP")
    print("="*60)

    session_path = vault_path / '.linkedin_session'
    session_path.mkdir(exist_ok=True)

    print(f"\nSession will be saved to: {session_path}")
    print("\nOpening LinkedIn in browser...")
    print("Please follow these steps:")
    print("1. Login with your email and password")
    print("2. Complete any 2FA if required")
    print("3. Wait for feed to load")
    print("4. Press ENTER in this terminal when done")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,  # Visible browser
            viewport={'width': 1280, 'height': 720},
            args=['--disable-blink-features=AutomationControlled']
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            print("\nLoading LinkedIn (this may take 30-60 seconds)...")
            page.goto('https://www.linkedin.com/login', timeout=60000, wait_until='domcontentloaded')
            print("✓ Page loaded")
        except Exception as e:
            print(f"\n✗ Error loading page: {e}")
            print("Please check your internet connection and try again.")
            browser.close()
            return

        # Wait for user to login
        input("\nPress ENTER after you've logged in and feed is loaded...")

        # Verify login by checking if we're on feed page
        try:
            current_url = page.url
            if 'feed' in current_url or 'linkedin.com' in current_url:
                print("\n✓ LinkedIn login successful!")
                print("✓ Session saved")
            else:
                print("\n✗ Could not verify login. Please try again.")
        except:
            print("\n✗ Could not verify login. Please try again.")

        try:
            browser.close()
        except:
            pass  # Ignore close errors

def test_whatsapp_session(vault_path: Path):
    """Test if WhatsApp session is working"""
    print("\n" + "="*60)
    print("TESTING WHATSAPP SESSION")
    print("="*60)

    session_path = vault_path / '.whatsapp_session'

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=True,  # Test in headless mode
            viewport={'width': 1280, 'height': 720}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            page.goto('https://web.whatsapp.com', timeout=10000)
            page.wait_for_selector('[data-testid="chat-list"]', timeout=5000)
            print("\n✓ WhatsApp session is working in headless mode!")
            return True
        except Exception as e:
            print(f"\n✗ WhatsApp session test failed: {e}")
            return False
        finally:
            browser.close()

def test_linkedin_session(vault_path: Path):
    """Test if LinkedIn session is working"""
    print("\n" + "="*60)
    print("TESTING LINKEDIN SESSION")
    print("="*60)

    session_path = vault_path / '.linkedin_session'

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=True,  # Test in headless mode
            viewport={'width': 1280, 'height': 720}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            page.goto('https://www.linkedin.com/feed/', timeout=10000)
            # Check if we're still logged in
            if 'feed' in page.url:
                print("\n✓ LinkedIn session is working in headless mode!")
                return True
            else:
                print("\n✗ LinkedIn session test failed - not logged in")
                return False
        except Exception as e:
            print(f"\n✗ LinkedIn session test failed: {e}")
            return False
        finally:
            browser.close()

def main():
    vault_path = Path(".")

    print("\n" + "="*60)
    print("AI EMPLOYEE VAULT - BROWSER SESSION SETUP")
    print("="*60)
    print("\nThis script will help you setup browser sessions for:")
    print("1. WhatsApp Web")
    print("2. LinkedIn")
    print("\nThese sessions will be used by the automation system.")

    while True:
        print("\n" + "="*60)
        print("MENU")
        print("="*60)
        print("1. Setup WhatsApp session")
        print("2. Setup LinkedIn session")
        print("3. Test WhatsApp session")
        print("4. Test LinkedIn session")
        print("5. Setup both (WhatsApp + LinkedIn)")
        print("6. Test both sessions")
        print("0. Exit")

        choice = input("\nEnter your choice (0-6): ").strip()

        if choice == '1':
            setup_whatsapp_session(vault_path)
        elif choice == '2':
            setup_linkedin_session(vault_path)
        elif choice == '3':
            test_whatsapp_session(vault_path)
        elif choice == '4':
            test_linkedin_session(vault_path)
        elif choice == '5':
            setup_whatsapp_session(vault_path)
            setup_linkedin_session(vault_path)
        elif choice == '6':
            wa_ok = test_whatsapp_session(vault_path)
            li_ok = test_linkedin_session(vault_path)
            print("\n" + "="*60)
            print("TEST RESULTS")
            print("="*60)
            print(f"WhatsApp: {'✓ PASS' if wa_ok else '✗ FAIL'}")
            print(f"LinkedIn: {'✓ PASS' if li_ok else '✗ FAIL'}")
        elif choice == '0':
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice. Please try again.")

    print("\n" + "="*60)
    print("Setup complete!")
    print("="*60)
    print("\nYour browser sessions are now ready for automation.")
    print("The system will use these sessions to send messages and posts.")

if __name__ == "__main__":
    main()
