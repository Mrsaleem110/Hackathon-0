"""
Read Real WhatsApp Messages from WhatsApp Web
"""
import sys
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

session_path = Path(".whatsapp_session")

print("="*60)
print("Reading Real WhatsApp Messages")
print("="*60)

try:
    with sync_playwright() as p:
        print("\nOpening WhatsApp Web with saved session...")

        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,  # Show browser so you can see
            viewport={'width': 1280, 'height': 720}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        print("Loading WhatsApp Web...")
        page.goto('https://web.whatsapp.com', timeout=30000)

        print("Waiting for chats to load...")
        try:
            page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
            print("✅ WhatsApp loaded!\n")

            # Get all chats
            chats = page.query_selector_all('[data-testid="chat-list-item"]')
            print(f"Found {len(chats)} chats\n")

            print("="*60)
            print("Recent Messages:")
            print("="*60)

            messages = []

            for i, chat in enumerate(chats[:10]):  # First 10 chats
                try:
                    name_elem = chat.query_selector('[data-testid="chat-list-item-title"]')
                    preview_elem = chat.query_selector('[data-testid="chat-list-item-message"]')

                    if name_elem and preview_elem:
                        name = name_elem.inner_text()
                        preview = preview_elem.inner_text()

                        print(f"\n{i+1}. {name}")
                        print(f"   {preview[:80]}...")

                        messages.append({
                            'name': name,
                            'preview': preview
                        })

                except Exception as e:
                    continue

            print("\n" + "="*60)
            print(f"Total messages found: {len(messages)}")
            print("="*60)

            # Save to file
            output_file = Path("whatsapp_messages_real.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Real WhatsApp Messages\n")
                f.write("="*60 + "\n\n")
                for i, msg in enumerate(messages, 1):
                    f.write(f"{i}. {msg['name']}\n")
                    f.write(f"   {msg['preview']}\n\n")

            print(f"\n✅ Messages saved to: {output_file}")

            print("\nKeeping browser open for 10 seconds...")
            time.sleep(10)

        except Exception as e:
            print(f"❌ Error loading WhatsApp: {e}")
            print("Session might be expired. Run whatsapp_login.py again.")
            time.sleep(5)

        browser.close()

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("\n✅ Done!")
