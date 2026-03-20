#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post Automation Topic to Agentic Sphere LinkedIn Page
Direct posting with browser automation
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
    print("Error: Playwright not installed. Install with: pip install playwright")
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


def post_automation_topic():
    """Post automation topic to LinkedIn"""

    post = get_automation_post()
    full_message = f"{post['title']}\n\n{post['content']}"

    print("\n" + "="*70)
    print("AGENTIC SPHERE - AUTOMATION TOPIC POST")
    print("="*70)
    print(f"Title: {post['title']}\n")
    print(f"Content Preview:\n{post['content'][:200]}...\n")

    with sync_playwright() as p:
        print("Opening browser...")
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )

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
            body_text = page.inner_text('body')

            if 'Sign in' in body_text or 'login' in page.url.lower():
                print("\n" + "="*70)
                print("LOGIN REQUIRED")
                print("="*70)
                print("Please login to LinkedIn in the browser window")
                print("Waiting 2 minutes for you to login...")
                print("="*70 + "\n")

                time.sleep(120)

                # Check again
                page.goto('https://www.linkedin.com/feed/', timeout=30000)
                time.sleep(5)

                body_text = page.inner_text('body')
                if 'Sign in' in body_text or 'login' in page.url.lower():
                    print("Not logged in. Exiting.")
                    browser.close()
                    return False

            print("Logged in successfully!\n")

            print("="*70)
            print("POSTING TO LINKEDIN")
            print("="*70)

            # Find and click share box
            print("Looking for 'Start a post' button...")

            selectors = [
                '.share-box-feed-entry__trigger',
                'button.share-box-feed-entry__trigger',
                '[data-test-id="share-box-feed-entry__trigger"]',
                'button:has-text("Start a post")',
            ]

            clicked = False
            for selector in selectors:
                try:
                    page.click(selector, timeout=5000)
                    clicked = True
                    print(f"Clicked share box with selector: {selector}")
                    time.sleep(2)
                    break
                except:
                    continue

            if not clicked:
                print("Could not find share box. Trying alternative method...")
                # Try clicking on the text area directly
                try:
                    page.click('div[contenteditable="true"]', timeout=5000)
                    print("Clicked on text area")
                    time.sleep(1)
                except:
                    print("Could not click text area")

            # Type the message
            print("Typing message...")
            try:
                # Find the contenteditable div
                page.fill('div[contenteditable="true"]', full_message, timeout=10000)
                print("Message typed successfully")
                time.sleep(2)
            except Exception as e:
                print(f"Error typing message: {e}")
                print("Trying alternative typing method...")
                try:
                    page.click('div[contenteditable="true"]')
                    time.sleep(1)
                    page.keyboard.type(full_message)
                    print("Message typed using keyboard")
                    time.sleep(2)
                except Exception as e2:
                    print(f"Alternative typing failed: {e2}")

            # Find and click Post button
            print("Looking for Post button...")

            post_selectors = [
                'button:has-text("Post")',
                'button[type="submit"]',
                'button[aria-label*="Post"]',
            ]

            posted = False
            for selector in post_selectors:
                try:
                    page.click(selector, timeout=5000)
                    print(f"Clicked Post button with selector: {selector}")
                    time.sleep(3)
                    posted = True
                    break
                except:
                    continue

            if posted:
                print("\n" + "="*70)
                print("SUCCESS! Post published to LinkedIn")
                print("="*70 + "\n")

                # Log success
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
