#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WhatsApp Message Sender - Telenore Chat
Send hello message to Telenore on WhatsApp
"""

import sys
import time
import io
from pathlib import Path
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: Playwright not installed")
    sys.exit(1)


def send_whatsapp_message():
    """Send hello message to Telenore on WhatsApp"""

    message = "Hello"
    contact_name = "Telenore"

    print("\n" + "="*70)
    print("WHATSAPP MESSAGE SENDER")
    print("="*70)
    print(f"Contact: {contact_name}")
    print(f"Message: {message}\n")

    with sync_playwright() as p:
        print("Opening browser...")
        browser = p.chromium.launch(headless=False, args=['--start-maximized'])
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        try:
            # Go to WhatsApp Web
            print("Opening WhatsApp Web...")
            page.goto('https://web.whatsapp.com/', timeout=60000, wait_until='domcontentloaded')
            time.sleep(5)

            print("WhatsApp Web opened. Please scan QR code if needed...")
            print("Waiting for chat list to load...")
            time.sleep(10)

            # Search for Telenore
            print(f"Searching for {contact_name}...")

            # Click on search box
            search_selectors = [
                'input[placeholder="Search or start new chat"]',
                'input[placeholder*="Search"]',
                'div[contenteditable="true"]',
            ]

            search_clicked = False
            for selector in search_selectors:
                try:
                    page.click(selector, timeout=3000)
                    search_clicked = True
                    print("✓ Search box clicked")
                    time.sleep(1)
                    break
                except:
                    continue

            if search_clicked:
                # Type contact name
                print(f"Typing {contact_name}...")
                try:
                    page.keyboard.type(contact_name, delay=50)
                    print("✓ Contact name typed")
                    time.sleep(2)
                except Exception as e:
                    print(f"Error typing: {e}")

                # Click on the contact from search results
                print("Looking for contact in search results...")
                time.sleep(2)

                try:
                    # Click on first search result
                    page.click('div[role="option"]', timeout=3000)
                    print("✓ Contact selected")
                    time.sleep(2)
                except:
                    print("Could not find contact in search results")

            # Find message input box
            print("Looking for message input box...")
            message_selectors = [
                'div[contenteditable="true"][data-tab="10"]',
                'div[contenteditable="true"]',
                'input[placeholder*="message"]',
            ]

            message_box_found = False
            for selector in message_selectors:
                try:
                    page.click(selector, timeout=3000)
                    message_box_found = True
                    print("✓ Message box clicked")
                    time.sleep(1)
                    break
                except:
                    continue

            if message_box_found:
                # Type message
                print(f"Typing message: {message}")
                try:
                    page.keyboard.type(message, delay=50)
                    print("✓ Message typed")
                    time.sleep(1)
                except Exception as e:
                    print(f"Error typing message: {e}")

                # Send message
                print("Looking for send button...")
                send_selectors = [
                    'button[aria-label="Send"]',
                    'button[aria-label*="Send"]',
                    'span[data-icon="send"]',
                ]

                message_sent = False
                for selector in send_selectors:
                    try:
                        page.click(selector, timeout=3000)
                        message_sent = True
                        print("✓ Send button clicked")
                        time.sleep(2)
                        break
                    except:
                        continue

                # Try pressing Enter as fallback
                if not message_sent:
                    try:
                        page.keyboard.press('Enter')
                        print("✓ Message sent via Enter key")
                        time.sleep(2)
                        message_sent = True
                    except:
                        pass

                if message_sent:
                    print("\n" + "="*70)
                    print("SUCCESS! Message sent to Telenore")
                    print("="*70 + "\n")
                    log_success(contact_name, message)
                    browser.close()
                    return True
                else:
                    print("Could not send message")
                    log_failed(contact_name, message)
                    browser.close()
                    return False
            else:
                print("Could not find message input box")
                log_failed(contact_name, message)
                browser.close()
                return False

        except Exception as e:
            print(f"Error: {e}")
            log_failed(contact_name, message)
            browser.close()
            return False


def log_success(contact, message):
    """Log successful message"""
    vault_path = Path.cwd()
    done_path = vault_path / 'Done'
    done_path.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    content = f"""# EXECUTED - WhatsApp Message to Telenore
**Date**: {datetime.now().isoformat()}
**Status**: EXECUTED
**Contact**: {contact}
**Message**: {message}

## Details
- Platform: WhatsApp Web
- Message Type: Text
- Status: Sent successfully
- Time: {datetime.now().strftime("%H:%M:%S")}
"""

    filename = done_path / f"EXECUTED_WHATSAPP_telenore_{timestamp}.md"
    filename.write_text(content, encoding='utf-8')
    print(f"Logged: {filename.name}")


def log_failed(contact, message):
    """Log failed message"""
    vault_path = Path.cwd()
    done_path = vault_path / 'Done'
    done_path.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    content = f"""# FAILED - WhatsApp Message to Telenore
**Date**: {datetime.now().isoformat()}
**Status**: FAILED
**Contact**: {contact}
**Message**: {message}

## Issue
Could not complete WhatsApp message sending

## Manual Action Required
Send message manually to {contact} on WhatsApp
"""

    filename = done_path / f"FAILED_WHATSAPP_telenore_{timestamp}.md"
    filename.write_text(content, encoding='utf-8')
    print(f"Logged: {filename.name}")


if __name__ == "__main__":
    success = send_whatsapp_message()
    sys.exit(0 if success else 1)
