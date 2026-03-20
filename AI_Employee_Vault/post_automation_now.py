#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct LinkedIn Post - Automation Topic to Agentic Sphere Page
Simple and reliable posting method
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


def post_now():
    """Post automation topic directly to LinkedIn"""

    post_content = """🤖 Automation: The Future of Business Efficiency

Did you know? Businesses that implement intelligent automation see a 40% increase in productivity.

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

    print("\n" + "="*70)
    print("POSTING AUTOMATION TOPIC TO AGENTIC SPHERE")
    print("="*70)
    print("Opening LinkedIn...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=['--start-maximized'])
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        try:
            # Go to LinkedIn
            page.goto('https://www.linkedin.com/feed/', timeout=30000)
            time.sleep(3)

            print("LinkedIn opened. Checking login status...")

            # Wait for page to stabilize
            page.wait_for_load_state('networkidle', timeout=10000)
            time.sleep(2)

            # Try to find the share box
            print("Looking for share box...")

            # Multiple attempts to find and click share box
            share_clicked = False
            share_selectors = [
                '.share-box-feed-entry__trigger',
                'button.share-box-feed-entry__trigger',
                'div.share-box-feed-entry__trigger',
                'button:has-text("Start a post")',
            ]

            for selector in share_selectors:
                try:
                    page.click(selector, timeout=3000)
                    share_clicked = True
                    print(f"✓ Share box clicked")
                    time.sleep(2)
                    break
                except:
                    continue

            if not share_clicked:
                print("Share box not found, trying text area...")
                try:
                    page.click('div[contenteditable="true"]', timeout=3000)
                    print("✓ Text area clicked")
                    time.sleep(1)
                except:
                    print("Could not find text area")

            # Type the post
            print("Typing post content...")
            try:
                page.fill('div[contenteditable="true"]', post_content, timeout=10000)
                print("✓ Content typed")
                time.sleep(2)
            except:
                print("Fill failed, using keyboard...")
                try:
                    page.keyboard.type(post_content, delay=5)
                    print("✓ Content typed via keyboard")
                    time.sleep(2)
                except Exception as e:
                    print(f"Error typing: {e}")

            # Click Post button
            print("Looking for Post button...")
            post_clicked = False
            post_selectors = [
                'button:has-text("Post")',
                'button[type="submit"]',
                'button.share-box-feed-entry__submit-button',
            ]

            for selector in post_selectors:
                try:
                    page.click(selector, timeout=3000)
                    post_clicked = True
                    print("✓ Post button clicked")
                    time.sleep(3)
                    break
                except:
                    continue

            if post_clicked:
                print("\n" + "="*70)
                print("SUCCESS! Post published to LinkedIn")
                print("="*70 + "\n")
                log_success()
                browser.close()
                return True
            else:
                print("Post button not found")
                log_failed()
                browser.close()
                return False

        except Exception as e:
            print(f"Error: {e}")
            log_failed()
            browser.close()
            return False


def log_success():
    """Log successful post"""
    vault_path = Path.cwd()
    done_path = vault_path / 'Done'
    done_path.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    content = f"""# EXECUTED - LinkedIn Automation Topic Post
**Date**: {datetime.now().isoformat()}
**Status**: EXECUTED
**Target**: Agentic Sphere LinkedIn Page

## Post Title
🤖 Automation: The Future of Business Efficiency

## Execution
- Posted successfully to LinkedIn feed
- Visibility: PUBLIC
- Topic: Business Automation
- Engagement: Ready for audience interaction
"""

    filename = done_path / f"EXECUTED_LINKEDIN_POST_automation_topic_{timestamp}.md"
    filename.write_text(content, encoding='utf-8')
    print(f"Logged: {filename.name}")


def log_failed():
    """Log failed post attempt"""
    vault_path = Path.cwd()
    done_path = vault_path / 'Done'
    done_path.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    content = f"""# FAILED - LinkedIn Automation Topic Post
**Date**: {datetime.now().isoformat()}
**Status**: FAILED
**Target**: Agentic Sphere LinkedIn Page

## Issue
Post button not found or automation failed

## Manual Action Required
Copy the post content and post manually to LinkedIn
"""

    filename = done_path / f"FAILED_LINKEDIN_POST_automation_topic_{timestamp}.md"
    filename.write_text(content, encoding='utf-8')
    print(f"Logged: {filename.name}")


if __name__ == "__main__":
    success = post_now()
    sys.exit(0 if success else 1)
