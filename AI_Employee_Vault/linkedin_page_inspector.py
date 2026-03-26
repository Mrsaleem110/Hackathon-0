#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Page Inspector
Shows what's actually on the page
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def inspect_page():
    session_path = ".linkedin_session_fresh"

    with sync_playwright() as p:
        print("Opening LinkedIn...")
        browser = p.chromium.launch_persistent_context(
            session_path,
            headless=False,
            viewport={'width': 1280, 'height': 800}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        page.goto('https://www.linkedin.com/feed/', timeout=30000)
        time.sleep(5)

        print("\n" + "="*60)
        print("PAGE INSPECTION")
        print("="*60)

        # Get all text on page
        body_text = page.inner_text('body')

        # Check for key phrases
        print("\nChecking for posting capability...")

        if 'Start a post' in body_text:
            print("✓ Found 'Start a post' text")
        else:
            print("✗ No 'Start a post' text found")

        if 'Share' in body_text:
            print("✓ Found 'Share' text")
        else:
            print("✗ No 'Share' text found")

        # Count elements
        buttons = page.query_selector_all('button')
        print(f"\nTotal buttons on page: {len(buttons)}")

        # Show first 20 button texts
        print("\nFirst 20 button texts:")
        for i, btn in enumerate(buttons[:20]):
            try:
                text = btn.text_content().strip()
                if text:
                    print(f"  {i+1}. {text}")
            except:
                pass

        print("\n" + "="*60)
        print("Browser will stay open for 60 seconds...")
        print("Please check if you can manually click to post")
        print("="*60)

        time.sleep(60)
        browser.close()

if __name__ == '__main__':
    inspect_page()
