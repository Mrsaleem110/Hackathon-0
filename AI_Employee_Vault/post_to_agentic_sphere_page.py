#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post to Agentic Sphere LinkedIn Page
Usage: python post_to_agentic_sphere_page.py "Your message here"
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SHORT_SUMMARY = """🤖 Agentic Sphere - Your Personal AI Employee

Autonomous. Intelligent. Always Working.

Agentic Sphere monitors your emails, messages, and opportunities - then takes action on your behalf with your approval.

✓ 24/7 Autonomous Operation
✓ Multi-Channel Integration (Gmail, WhatsApp, LinkedIn)
✓ Intelligent Decision Making with Claude AI
✓ Complete Audit Trail & Transparency
✓ Human-in-the-Loop Control

The future of productivity is here.

#AI #Automation #AgenticSphere #ArtificialIntelligence #Productivity"""

def post_to_page(message=None):
    if message is None:
        message = SHORT_SUMMARY

    print("=" * 60)
    print("Posting to Agentic Sphere LinkedIn Page")
    print("=" * 60)
    print(f"\nMessage: {message[:100]}...\n")
    print("Opening Agentic Sphere page...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to Agentic Sphere page
        page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=30000)
        print("Page loaded. Waiting for 'Create a post' button...")
        time.sleep(3)

        try:
            # Look for "Create a post" button
            print("Looking for 'Create a post' button...")

            # Try multiple selectors for the create post button
            selectors = [
                'button:has-text("Create a post")',
                '[aria-label="Create a post"]',
                'button[aria-label*="post"]',
                'text=Create a post',
            ]

            clicked = False
            for selector in selectors:
                try:
                    btn = page.query_selector(selector)
                    if btn and btn.is_visible():
                        print(f"Found button with selector: {selector}")
                        btn.click()
                        clicked = True
                        break
                except:
                    pass

            if not clicked:
                # Try clicking by text content
                buttons = page.query_selector_all('button')
                for btn in buttons:
                    if btn.is_visible() and 'Create a post' in btn.text_content():
                        print("Found 'Create a post' button by text")
                        btn.click()
                        clicked = True
                        break

            if not clicked:
                print("Could not find 'Create a post' button. Please click it manually.")
                input("Press Enter after clicking 'Create a post'...")

            time.sleep(2)

            # Find and click the text editor
            print("Finding text editor...")
            page.wait_for_selector('[contenteditable="true"]', timeout=10000)
            editor = page.query_selector('[contenteditable="true"]')

            if editor:
                editor.click()
                time.sleep(1)

                # Type the message
                print("Typing post content...")
                page.keyboard.type(message, delay=3)
                time.sleep(2)

                # Click Post button
                print("Clicking Post button...")
                post_buttons = page.query_selector_all('button')

                posted = False
                for btn in post_buttons:
                    if btn.is_visible() and btn.is_enabled():
                        btn_text = btn.text_content()
                        if 'Post' in btn_text and len(btn_text) < 20:
                            btn.click()
                            posted = True
                            print("Post button clicked!")
                            break

                if posted:
                    time.sleep(5)
                    print("\n" + "="*60)
                    print("✓ POST PUBLISHED TO AGENTIC SPHERE PAGE!")
                    print("="*60)
                else:
                    print("Could not find Post button. Please click manually.")
                    input("Press Enter after posting...")
            else:
                print("Could not find text editor.")
                input("Please post manually and press Enter...")

        except Exception as e:
            print(f"Error: {e}")
            print("Please complete the post manually.")
            input("Press Enter when done...")

        finally:
            time.sleep(2)
            browser.close()

if __name__ == '__main__':
    # Get message from command line or use default
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = SHORT_SUMMARY

    post_to_page(message)
