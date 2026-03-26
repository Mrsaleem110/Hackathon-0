#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WhatsApp Message Preparation - Telenore
Prepare hello message for WhatsApp
"""

import sys
import io
from pathlib import Path
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def prepare_whatsapp_message():
    """Prepare WhatsApp message to Telenore"""

    contact = "Telenore"
    message = "Hello"

    print("\n" + "="*70)
    print("WHATSAPP MESSAGE - TELENORE")
    print("="*70)
    print(f"\nContact: {contact}")
    print(f"Message: {message}\n")

    print("="*70)
    print("MANUAL SENDING INSTRUCTIONS")
    print("="*70)
    print("""
1. Open WhatsApp (Web or Mobile)
2. Search for "Telenore" in your contacts
3. Click on the chat
4. Type: Hello
5. Press Send

OR use this direct link:
https://wa.me/?text=Hello

Then select Telenore from your contacts.
""")

    # Save to file
    vault_path = Path.cwd()
    done_path = vault_path / 'Done'
    done_path.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log_content = f"""# READY - WhatsApp Message to Telenore
**Date**: {datetime.now().isoformat()}
**Status**: READY FOR SENDING
**Contact**: {contact}
**Message**: {message}

## Message Details
- Recipient: Telenore
- Message Type: Text
- Content: Hello
- Platform: WhatsApp

## How to Send

### Option 1: WhatsApp Web
1. Go to https://web.whatsapp.com/
2. Search for "Telenore"
3. Click on the chat
4. Type: Hello
5. Press Send

### Option 2: WhatsApp Mobile
1. Open WhatsApp app
2. Go to Chats
3. Search for "Telenore"
4. Tap the chat
5. Type: Hello
6. Tap Send

### Option 3: Direct Link
https://wa.me/?text=Hello

Then select Telenore from your contacts.

## Status
- Prepared: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- Ready to send: YES
- Manual action required: YES
"""

    filename = done_path / f"READY_WHATSAPP_telenore_{timestamp}.md"
    filename.write_text(log_content, encoding='utf-8')

    print(f"Message prepared and saved to: {filename.name}\n")
    return True


if __name__ == "__main__":
    success = prepare_whatsapp_message()
    sys.exit(0 if success else 1)
