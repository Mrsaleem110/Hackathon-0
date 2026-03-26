#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Post Debug - Find all clickable elements
"""
import sys
import time
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def debug_linkedin():
    session_path = ".linkedin_session"

    with sync_playwright() as p:
        print("Opening LinkedIn...")
        browser = p.chromium.launch_persistent_context(
            session_path,
            headless=False,
            viewport={'width': 1280, 'height': 800}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        # Go to feed
        page.goto('https://www.linkedin.com/feed/', timeout=30000)
        time.sleep(5)

        # Take screenshot
        page.screenshot(path='linkedin_feed_debug.png')
        print("Screenshot saved: linkedin_feed_debug.png")

        # Get page HTML
        html = page.content()
        with open('linkedin_feed_page.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("HTML saved: linkedin_feed_page.html")

        # Find all buttons and divs with role=button
        print("\n" + "="*60)
        print("SEARCHING FOR POST BUTTONS")
        print("="*60)

        all_elements = page.query_selector_all('button, div[role="button"], span[role="button"]')
        print(f"\nFound {len(all_elements)} clickable elements\n")

        post_related = []
        for i, elem in enumerate(all_elements):
            try:
                if elem.is_visible():
                    text = elem.text_content().strip()
                    aria_label = elem.get_attribute('aria-label') or ''
                    class_name = elem.get_attribute('class') or ''

                    # Look for post-related elements
                    if any(keyword in text.lower() for keyword in ['post', 'share', 'start']):
                        post_related.append({
                            'index': i,
                            'text': text[:100],
                            'aria_label': aria_label[:100],
                            'class': class_name[:100]
                        })
            except:
                pass

        print(f"Found {len(post_related)} post-related elements:\n")
        for elem in post_related:
            print(f"[{elem['index']}]")
            print(f"  Text: {elem['text']}")
            print(f"  Aria: {elem['aria_label']}")
            print(f"  Class: {elem['class']}")
            print()

        print("\nBrowser staying open for 60 seconds...")
        time.sleep(60)
        browser.close()

if __name__ == '__main__':
    debug_linkedin()
