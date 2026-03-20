#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post Automation Topic to Agentic Sphere LinkedIn Page
Uses existing LinkedIn session for authentication
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


def get_automation_post():
    """Get automation topic post content"""
    return {
        "title": "🤖 Automation: The Future of Business Efficiency",
        "content": """Did you know? Businesses that implement intelligent automation see a 40% increase in productivity.

At Agentic Sphere, we're revolutionizing how companies work by automating repetitive tasks and enabling teams to focus on strategic initiatives.

Key benefits of automation:
✅ 24/7 Operations - Never miss an opportunity
✅ Error Reduction - Eliminate human mistakes
✅ Cost Savings - Reduce operational expenses
✅ Scalability - Grow without proportional headcount increase
✅ Employee Satisfaction - Let AI handle the mundane

The future isn't about replacing humans—it's about empowering them with intelligent systems.

Ready to transform your business? Let's talk automation.

#Automation #AI #BusinessEfficiency #DigitalTransformation #FutureOfWork"""
    }


def find_session_dir():
    """Find an existing LinkedIn session directory"""
    vault_path = Path.cwd()
    session_dirs = [
        vault_path / '.linkedin_session_auto',
        vault_path / '.linkedin_session_fresh',
        vault_path / '.linkedin_session_manual',
        vault_path / '.linkedin_session_new',
        vault_path / '.linkedin_session_setup',
        vault_path / '.linkedin_session',
    ]

    for session_dir in session_dirs:
        if session_dir.exists():
            print(f"Found session: {session_dir.name}")
            return session_dir

    return None


def post_automation_topic():
    """Post automation topic to LinkedIn using existing session"""

    post = get_automation_post()
    full_message = f"{post['title']}\n\n{post['content']}"

    print("\n" + "="*70)
    print("AGENTIC SPHERE - AUTOMATION TOPIC POST")
    print("="*70)
    print(f"Title: {post['title']}\n")

    # Find existing session
    session_dir = find_session_dir()
    if not session_dir:
        print("No existing LinkedIn session found")
        print("Creating new session...")
        session_dir = None
    else:
        print(f"Using session: {session_dir}")

    with sync_playwright() as p:
        print("Opening browser...")
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )

        # Use existing session if available
        if session_dir and (session_dir / 'Default').exists():
            print(f"Loading session from {session_dir}...")
            context = browser.new_context(
                storage_state=str(session_dir / 'storage_state.json') if (session_dir / 'storage_state.json').exists() else None
            )
        else:
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )

        page = context.new_page()

        try:
            # Navigate to LinkedIn
            print("Opening LinkedIn...")
            page.goto('https://www.linkedin.com/feed/', timeout=30000)
            time.sleep(3)

            # Check if logged in
            try:
                body_text = page.inner_text('body')
                if 'Sign in' in body_text or 'login' in page.url.lower():
                    print("Not logged in. Please login manually in the browser.")
                    print("Waiting 3 minutes for manual login...")
                    time.sleep(180)
            except:
                pass

            print("Proceeding to post...\n")

            print("="*70)
            print("POSTING TO LINKEDIN")
            print("="*70)

            # Find and click share box
            print("Looking for 'Start a post' button...")
            time.sleep(2)

            selectors = [
                '.share-box-feed-entry__trigger',
                'button.share-box-feed-entry__trigger',
                '[data-test-id="share-box-feed-entry__trigger"]',
                'button:has-text("Start a post")',
                'div.share-box-feed-entry__trigger',
            ]

            clicked = False
            for selector in selectors:
                try:
                    page.click(selector, timeout=5000)
                    clicked = True
                    print(f"Clicked share box")
                    time.sleep(2)
                    break
                except:
                    continue

            if not clicked:
                print("Trying to click on text area directly...")
                try:
                    page.click('div[contenteditable="true"]', timeout=5000)
                    print("Clicked on text area")
                    time.sleep(1)
                except:
                    print("Could not find share box")

            # Type the message
            print("Typing message...")
            time.sleep(1)

            try:
                # Try to find and fill the contenteditable div
                page.fill('div[contenteditable="true"]', full_message, timeout=10000)
                print("Message typed successfully")
                time.sleep(2)
            except Exception as e:
                print(f"Fill method failed, trying keyboard input...")
                try:
                    page.keyboard.type(full_message, delay=10)
                    print("Message typed using keyboard")
                    time.sleep(2)
                except Exception as e2:
                    print(f"Keyboard input failed: {e2}")

            # Find and click Post button
            print("Looking for Post button...")
            time.sleep(1)

            post_selectors = [
                'button:has-text("Post")',
                'button[type="submit"]',
                'button[aria-label*="Post"]',
                'button.share-box-feed-entry__submit-button',
            ]

            posted = False
            for selector in post_selectors:
                try:
                    page.click(selector, timeout=5000)
                    print(f"Clicked Post button")
                    time.sleep(3)
                    posted = True
                    break
                except:
                    continue

            if posted:
                print("\n" + "="*70)
                print("SUCCESS! Post published to LinkedIn")
                print("="*70 + "\n")
                log_post(post, True)
                browser.close()
                return True
            else:
                print("Could not find Post button")
                log_post(post, False)
                browser.close()
                return False

        except Exception as e:
            print(f"Error: {e}")
            log_post(post, False)
            browser.close()
            return False


def log_post(post, success):
    """Log the post to Done folder"""
    vault_path = Path.cwd()
    done_path = vault_path / 'Done'
    done_path.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    status = "EXECUTED" if success else "FAILED"

    log_content = f"""# {status} - LinkedIn Automation Topic Post
**Date**: {datetime.now().isoformat()}
**Status**: {status}

## Post Title
{post['title']}

## Post Content
{post['content']}

## Execution Details
- Target: Agentic Sphere LinkedIn Page
- Topic: Business Automation
- Visibility: PUBLIC
"""

    filename = done_path / f"{status}_LINKEDIN_POST_automation_topic_{timestamp}.md"
    filename.write_text(log_content, encoding='utf-8')
    print(f"Logged to: {filename}")


if __name__ == "__main__":
    success = post_automation_topic()
    sys.exit(0 if success else 1)
