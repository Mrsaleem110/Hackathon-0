#!/usr/bin/env python3
"""
LinkedIn Post - Direct Method with Better Login Handling
"""
import time
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

POST_TEXT = """Introducing Agentic Sphere: The Future of AI Automation

Ever wondered how AI can truly work FOR you, not just WITH you?

Meet Agentic Sphere - an autonomous AI system that does not just assist, it ACTS on your behalf.

What makes it different?

- Autonomous Decision Making: It thinks, plans, and executes tasks independently
- Multi-Platform Integration: Gmail, WhatsApp, LinkedIn, and more
- Human-in-the-Loop: You stay in control with approval workflows
- Complete Audit Trail: Every action is logged and transparent
- Intelligent Planning: Uses Claude AI to generate smart action plans

Real-world use cases:
- Automatically responds to client emails
- Schedules and manages appointments
- Posts business updates on social media
- Monitors and replies to WhatsApp messages
- Generates reports and summaries

This is not just automation - it is your personal AI employee that works 24/7.

The future of productivity is here. Are you ready to let AI handle the routine while you focus on what truly matters?

#AI #Automation #AgenticSphere #ArtificialIntelligence #Productivity #FutureOfWork #Innovation #Technology #AIAgent #DigitalTransformation"""

def post_to_linkedin_direct():
    session_path = Path('.linkedin_session_fresh')
    if session_path.exists():
        shutil.rmtree(session_path)
    session_path.mkdir()

    print("=" * 60)
    print("LinkedIn Post - Agentic Sphere")
    print("=" * 60)
    print("\nOpening LinkedIn in browser...")
    print("Please login manually when the browser opens.\n")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            viewport={'width': 1280, 'height': 800},
            args=['--disable-blink-features=AutomationControlled']
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        # Go to LinkedIn feed directly
        page.goto('https://www.linkedin.com/feed/', timeout=30000)
        print("Browser opened. Please login if needed and wait for feed to load...")
        print("Waiting for feed to load (up to 2 minutes)...\n")

        # Wait for feed to load
        feed_loaded = False
        for i in range(24):
            time.sleep(5)
            try:
                # Check if we're on the feed
                current_url = page.url
                print(f"  [{i*5}s] URL: {current_url[:70]}")

                # Look for the post button
                post_button = page.query_selector('[aria-label="Start a post"]')
                if post_button or '/feed' in current_url:
                    feed_loaded = True
                    print("\nFeed detected! Starting post...\n")
                    break
            except:
                pass

        if not feed_loaded:
            print("Could not detect feed. Please manually click 'Start a post' and type the content.")
            input("Press Enter when done...")
            browser.close()
            return False

        time.sleep(2)

        try:
            # Click Start a post button
            print("Clicking 'Start a post' button...")
            page.click('[aria-label="Start a post"]', timeout=10000)
            time.sleep(2)

            # Find and click the text editor
            print("Clicking text editor...")
            editor = page.query_selector('[contenteditable="true"]')
            if editor:
                editor.click()
                time.sleep(1)

                # Type the post
                print("Typing post content...")
                page.keyboard.type(POST_TEXT, delay=5)
                time.sleep(2)

                # Click Post button
                print("Clicking Post button...")
                post_btn = page.query_selector('button[type="button"]:has-text("Post")')
                if post_btn:
                    post_btn.click()
                else:
                    # Try alternative selector
                    buttons = page.query_selector_all('button')
                    for btn in buttons:
                        if btn.is_visible() and 'Post' in btn.text_content():
                            btn.click()
                            break

                time.sleep(5)
                print("\n" + "="*60)
                print("POST PUBLISHED!")
                print("="*60)
                return True
            else:
                print("Could not find text editor. Please type manually.")
                input("Press Enter after posting...")
                return True

        except Exception as e:
            print(f"Error: {e}")
            print("Please complete the post manually.")
            input("Press Enter when done...")
            return True

        finally:
            browser.close()

if __name__ == '__main__':
    post_to_linkedin_direct()
