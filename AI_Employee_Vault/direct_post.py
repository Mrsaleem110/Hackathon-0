"""
AgenticSphere - LinkedIn Direct Post with Credentials
"""
import time
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

EMAIL = "sm6928234@gmail.com"
PASSWORD = "$@!eem1234"

POST_TEXT = """Just launched Agentic Sphere! 🚀

Agentic Sphere is an autonomous AI system that acts on your behalf. It integrates with Gmail, WhatsApp, and LinkedIn to intelligently plan, manage tasks, and execute actions independently with human-in-the-loop approval workflows.

The future of productivity is here! #AI #Innovation #AgenticSphere #FutureOfWork"""

def run():
    session_path = Path('.linkedin_session_fresh')
    if session_path.exists():
        shutil.rmtree(session_path)
    session_path.mkdir()

    print("Starting LinkedIn post process...")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            viewport={'width': 1280, 'height': 800},
            slow_mo=200,
            args=['--disable-blink-features=AutomationControlled']
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        # Step 1: Go to login page
        print("Opening LinkedIn login page...")
        page.goto('https://www.linkedin.com/login', timeout=30000)
        page.wait_for_load_state('domcontentloaded')
        time.sleep(2)

        # Step 2: Enter email
        print("Entering email...")
        page.fill('#username', EMAIL)
        time.sleep(1)

        # Step 3: Enter password
        print("Entering password...")
        page.fill('#password', PASSWORD)
        time.sleep(1)

        # Step 4: Click Sign in
        print("Clicking Sign in...")
        page.click('button[type="submit"]')
        time.sleep(5)

        print("Current URL after login:", page.url)

        # Step 5: Handle verification if needed
        if 'checkpoint' in page.url or 'challenge' in page.url or 'verify' in page.url:
            print("\n*** VERIFICATION REQUIRED ***")
            print("Please complete the verification in the browser window.")
            print("Waiting up to 180 seconds for you to complete it...")
            for i in range(36):
                time.sleep(5)
                print(f"  [{(i+1)*5}s] URL: {page.url[:70]}")
                if '/feed' in page.url:
                    print("Verification complete!")
                    break

        # Step 6: Wait for feed
        print("Waiting for feed to load...")
        for i in range(20):
            time.sleep(3)
            if '/feed' in page.url:
                print("Feed loaded! Logged in successfully.")
                break
            print(f"  Waiting... URL: {page.url[:60]}")
        else:
            print("Could not reach feed. Current URL:", page.url)
            time.sleep(15)
            browser.close()
            return

        time.sleep(3)

        # Step 7: Click Start a post
        print("Looking for Start a post button...")
        try:
            page.wait_for_selector('.share-box-feed-entry__trigger', timeout=10000)
            page.click('.share-box-feed-entry__trigger')
            print("Clicked Start a post!")
        except:
            try:
                page.click('text=Start a post', timeout=5000)
                print("Clicked Start a post by text!")
            except Exception as e:
                print("Could not click Start a post:", e)
                time.sleep(10)
                browser.close()
                return

        time.sleep(3)

        # Step 8: Type post content
        print("Typing post content...")
        try:
            page.wait_for_selector('.ql-editor', timeout=8000)
            page.click('.ql-editor')
            time.sleep(1)
            page.keyboard.type(POST_TEXT, delay=10)
            print("Content typed successfully!")
        except Exception as e:
            print("Editor error:", e)
            try:
                editor = page.query_selector('[contenteditable="true"]')
                if editor:
                    editor.click()
                    page.keyboard.type(POST_TEXT, delay=10)
                    print("Typed using contenteditable!")
            except Exception as e2:
                print("Could not type:", e2)
                time.sleep(10)
                browser.close()
                return

        time.sleep(2)

        # Step 9: Click Post button
        print("Clicking Post button...")
        try:
            page.wait_for_selector('button.share-actions__primary-action', timeout=8000)
            page.click('button.share-actions__primary-action')
            print("Clicked Post button!")
        except:
            try:
                page.click('button:has-text("Post")', timeout=5000)
                print("Clicked Post by text!")
            except Exception as e:
                print("Could not click Post:", e)
                time.sleep(10)
                browser.close()
                return

        time.sleep(5)
        print("\n" + "="*60)
        print("POST PUBLISHED SUCCESSFULLY!")
        print("AgenticSphere post is now LIVE on LinkedIn!")
        print("="*60)

        time.sleep(3)
        browser.close()

if __name__ == '__main__':
    run()
