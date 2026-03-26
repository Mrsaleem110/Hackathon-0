"""
AgenticSphere - LinkedIn Direct Post Script
Logs in fresh and posts immediately
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

def post_to_linkedin():
    # Clear old broken session
    session_path = Path('.linkedin_session_new')
    if session_path.exists():
        shutil.rmtree(session_path)
    session_path.mkdir()

    print("=" * 60)
    print("AgenticSphere LinkedIn Post Script")
    print("=" * 60)
    print("\nOpening browser... Please login when prompted.\n")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            viewport={'width': 1280, 'height': 800},
            slow_mo=300,
            args=['--disable-blink-features=AutomationControlled']
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        # Go to LinkedIn
        page.goto('https://www.linkedin.com/login', timeout=30000)
        print("Browser opened. Please login with your LinkedIn credentials.")
        print("Waiting for you to login and reach the feed page...\n")

        # Wait until user reaches feed (up to 3 minutes)
        for i in range(36):
            time.sleep(5)
            current_url = page.url
            print(f"  [{i*5}s] Current URL: {current_url[:60]}")
            if '/feed' in current_url or ('linkedin.com' in current_url and 'login' not in current_url and 'signup' not in current_url):
                print("\nLogin detected! Starting post...")
                break
        else:
            print("Timeout waiting for login.")
            browser.close()
            return False

        time.sleep(3)

        try:
            # Try clicking 'Start a post'
            print("Looking for post button...")

            # Multiple selector attempts
            clicked = False
            selectors_to_try = [
                '.share-box-feed-entry__trigger',
                'button.share-box-feed-entry__trigger',
                '[aria-label="Start a post"]',
                'div.share-box-feed-entry__closed-share-box',
            ]

            for sel in selectors_to_try:
                try:
                    page.wait_for_selector(sel, timeout=5000)
                    page.click(sel)
                    clicked = True
                    print(f"Clicked share box: {sel}")
                    break
                except:
                    pass

            if not clicked:
                # Try text-based click
                try:
                    page.click('text=Start a post', timeout=5000)
                    clicked = True
                    print("Clicked 'Start a post' text")
                except:
                    pass

            if not clicked:
                print("Could not find post button. Trying JavaScript click...")
                page.evaluate("""
                    const btns = document.querySelectorAll('button');
                    for (const btn of btns) {
                        if (btn.textContent.includes('Start a post') || btn.textContent.includes('post')) {
                            btn.click();
                            break;
                        }
                    }
                """)
                time.sleep(2)

            time.sleep(3)

            # Type in editor
            print("Typing post content...")
            editor_selectors = [
                '.ql-editor',
                '[contenteditable="true"]',
                '.editor-content',
                '[data-placeholder="What do you want to talk about?"]',
            ]

            typed = False
            for esel in editor_selectors:
                try:
                    page.wait_for_selector(esel, timeout=5000)
                    page.click(esel)
                    time.sleep(1)
                    page.keyboard.type(POST_TEXT, delay=15)
                    typed = True
                    print(f"Content typed using: {esel}")
                    break
                except:
                    pass

            if not typed:
                print("Could not find editor. Please type manually and press Enter when done.")
                input("Press Enter after typing your post...")

            time.sleep(2)

            # Click Post button
            print("Clicking Post button...")
            post_selectors = [
                'button.share-actions__primary-action',
                '[data-control-name="share.post"]',
                'button.artdeco-button--primary[type="button"]',
            ]

            posted = False
            for pbtn in post_selectors:
                try:
                    page.wait_for_selector(pbtn, timeout=5000)
                    btn = page.query_selector(pbtn)
                    if btn and btn.is_visible() and btn.is_enabled():
                        btn.click()
                        posted = True
                        print(f"Clicked post button: {pbtn}")
                        break
                except:
                    pass

            if not posted:
                # Try text-based
                try:
                    page.click('button:has-text("Post")', timeout=5000)
                    posted = True
                    print("Clicked Post button by text")
                except:
                    print("Please click the Post button manually.")
                    input("Press Enter after post is published...")
                    posted = True

            time.sleep(5)

            if posted:
                print("\n" + "="*60)
                print("POST PUBLISHED SUCCESSFULLY on LinkedIn!")
                print("AgenticSphere post is now live!")
                print("="*60)

        except Exception as e:
            print(f"Error: {e}")
            print("Browser will stay open for 30 seconds for manual action.")
            time.sleep(30)

        # Save new session
        browser.close()

        # Replace old session with new one
        old_session = Path('.linkedin_session')
        if old_session.exists():
            shutil.rmtree(old_session)
        session_path.rename(old_session)
        print("\nSession saved for future use.")

    return True

if __name__ == '__main__':
    post_to_linkedin()
