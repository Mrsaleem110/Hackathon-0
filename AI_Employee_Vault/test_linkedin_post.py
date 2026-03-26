"""
Test LinkedIn Session and Post
Opens browser in visible mode to debug the issue
"""

from pathlib import Path
from playwright.sync_api import sync_playwright
import time
import sys

def test_linkedin_post():
    vault_path = Path(".")
    session_path = vault_path / '.linkedin_session'

    post_content = """🚀 Welcome to the future with Agentic Sphere! Where AI Meets Innovation!

Ever wondered how AI can truly work FOR you, not just WITH you?

Meet Agentic Sphere - an autonomous AI system that doesn't just assist, it ACTS on your behalf.

🎯 What makes it different?

✨ Autonomous Decision Making - It thinks, plans, and executes tasks independently
✨ Multi-Platform Integration - Seamlessly manages Gmail, WhatsApp, LinkedIn, and more
✨ Human-in-the-Loop - You stay in full control with approval workflows
✨ Intelligent Planning - Powered by advanced AI to generate smart action plans

💡 Real-world use cases:
• Automatically responds to client emails
• Schedules and manages appointments
• Posts business updates on social media
• Monitors and replies to WhatsApp messages

This isn't just automation - it's your personal AI employee that works 24/7.

The future of productivity is here. Are you ready to let AI handle the routine while you focus on what matters? Let's connect and explore the endless possibilities together!

#AI #Innovation #AgenticSphere #ArtificialIntelligence #Productivity #FutureOfWork #TechTrends #AIAgent #DigitalTransformation"""

    print("Opening LinkedIn in visible browser...")
    print("You can manually post if automation fails.")
    print("\n" + "="*60)
    print("POST CONTENT:")
    print("="*60)
    try:
        print(post_content.encode('utf-8', errors='ignore').decode('utf-8'))
    except:
        print("[Content contains emojis which cannot be printed in this terminal]")
    print("="*60)

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,  # Visible browser
            viewport={'width': 1280, 'height': 720}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            print("\nLoading LinkedIn feed...")
            page.goto('https://www.linkedin.com/feed/', timeout=30000)

            # Check if logged in
            current_url = page.url
            if 'login' in current_url or 'authwall' in current_url:
                print("\nNOT LOGGED IN!")
                print("Please wait up to 60 seconds to login manually...")
                for i in range(12):
                    time.sleep(5)
                    print(f"Waiting for login... {i*5}s")
                    if '/feed' in page.url:
                        break
                page.goto('https://www.linkedin.com/feed/')

            print("LinkedIn feed loaded")
            print("\nWaiting 3 seconds...")
            page.wait_for_timeout(3000)

            # Try to find and click "Start a post"
            print("\nLooking for 'Start a post' button...")

            # Try multiple selectors
            selectors = [
                'button[aria-label*="Start a post"]',
                '.share-box-feed-entry__trigger',
                'button.share-box-feed-entry__trigger',
                '[data-control-name="share_box_trigger"]',
                '.artdeco-button--secondary'
            ]

            start_post = None
            for selector in selectors:
                start_post = page.query_selector(selector)
                if start_post:
                    print(f"Found button with selector: {selector}")
                    break

            if start_post:
                print("Clicking 'Start a post'...")
                start_post.click()
                page.wait_for_timeout(3000)

                # Try to find editor
                print("\nLooking for post editor...")
                editor_selectors = [
                    '.ql-editor',
                    '[contenteditable="true"]',
                    '[role="textbox"]',
                    '.mentions-texteditor__content'
                ]

                editor = None
                for selector in editor_selectors:
                    editor = page.query_selector(selector)
                    if editor:
                        print(f"Found editor with selector: {selector}")
                        break

                if editor:
                    print("Filling post content...")
                    editor.click()
                    page.wait_for_timeout(500)
                    editor.fill(post_content)
                    page.wait_for_timeout(2000)

                    print("\nContent filled!")
                    
                    # Try to find and click Post button
                    post_button_selectors = [
                        'button[aria-label*="Post"]',
                        '.share-actions__primary-action',
                        'button.share-actions__primary-action',
                        '[data-control-name="share.post"]'
                    ]

                    post_button = None
                    for selector in post_button_selectors:
                        post_button = page.query_selector(selector)
                        if post_button:
                            print(f"Found Post button with selector: {selector}")
                            break

                    if post_button:
                        print("Clicking Post button...")
                        post_button.click()
                        page.wait_for_timeout(5000)
                        print("\nPOST PUBLISHED!")
                    else:
                        print("\nCould not find Post button")
                        time.sleep(30)
                else:
                    print("\nCould not find post editor")
                    time.sleep(30)
            else:
                print("\nCould not find 'Start a post' button")
                time.sleep(30)

        except Exception as e:
            try:
                print(f"\nError: {e}")
            except:
                print("\nError occurred")
            print("\nBrowser will stay open for 30 seconds. You can post manually.")
            time.sleep(30)
        finally:
            print("\nClosing browser...")
            browser.close()
            print("Done!")

if __name__ == "__main__":
    test_linkedin_post()
