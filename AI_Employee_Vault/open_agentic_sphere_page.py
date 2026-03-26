#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open Agentic Sphere LinkedIn Company Page in Browser Session
"""
import sys
import time
import io
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def open_agentic_sphere_page():
    """Open Agentic Sphere company page in browser"""

    print("=" * 60)
    print("Opening Agentic Sphere LinkedIn Company Page")
    print("=" * 60)

    session_paths = [
        '.linkedin_session_auto',
        '.linkedin_session',
        '.linkedin_session_fresh',
        '.linkedin_session_manual',
    ]

    for session_path in session_paths:
        session_dir = Path(session_path)
        if not session_dir.exists():
            continue

        print(f"\nUsing session: {session_path}")

        try:
            with sync_playwright() as p:
                # Launch browser with persistent context
                context = p.chromium.launch_persistent_context(
                    str(session_dir),
                    headless=False,
                    viewport={'width': 1920, 'height': 1080}
                )

                page = context.new_page()

                try:
                    # Go to Agentic Sphere company page
                    print("Opening Agentic Sphere company page...")
                    page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=30000)

                    print("✓ Page opened successfully")
                    print("\n" + "=" * 60)
                    print("Browser is now open with Agentic Sphere page")
                    print("You can now manually post or interact with the page")
                    print("=" * 60)

                    # Keep browser open for 10 minutes
                    print("\nBrowser will stay open for 10 minutes...")
                    time.sleep(600)

                    context.close()
                    return True

                except Exception as e:
                    print(f"❌ Error: {e}")
                    context.close()
                    continue

        except Exception as e:
            print(f"❌ Session error: {e}")
            continue

    print("\n❌ Could not open page with any available session")
    return False

if __name__ == '__main__':
    open_agentic_sphere_page()
