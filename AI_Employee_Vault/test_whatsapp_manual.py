"""
Quick WhatsApp Web Test - Manual Browser
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

session_path = Path(".whatsapp_session")

print("Opening WhatsApp Web in visible browser...")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        headless=False,  # Show browser
        viewport={'width': 1280, 'height': 720}
    )

    page = browser.pages[0] if browser.pages else browser.new_page()

    print("Loading WhatsApp Web...")
    page.goto('https://web.whatsapp.com', timeout=30000)

    print("Waiting for chat list...")
    try:
        page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
        print("✅ Chat list loaded!")

        # Get chats
        chats = page.query_selector_all('[data-testid="chat-list-item"]')
        print(f"Found {len(chats)} chats")

        # Show first 5 chat names
        for i, chat in enumerate(chats[:5]):
            try:
                name_elem = chat.query_selector('[data-testid="chat-list-item-title"]')
                if name_elem:
                    print(f"  {i+1}. {name_elem.inner_text()}")
            except:
                pass

        print("\nKeeping browser open for 10 seconds...")
        time.sleep(10)

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Keeping browser open for 30 seconds to check...")
        time.sleep(30)

    browser.close()
    print("Done!")
