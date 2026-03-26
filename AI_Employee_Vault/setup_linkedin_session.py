#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Session Setup - Manual Authentication
Sets up a persistent browser session for LinkedIn posting
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def setup_linkedin_session():
    """Set up LinkedIn session with manual login"""
    vault_path = Path(".")
    session_path = vault_path / '.linkedin_session_setup'
    session_path.mkdir(exist_ok=True)

    print("=" * 70)
    print("LINKEDIN SESSION SETUP")
    print("=" * 70)
    print("\nThis will open LinkedIn in a browser.")
    print("Please log in manually, then close the browser when done.\n")
    print("The session will be saved for future automated posts.\n")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            viewport={'width': 1280, 'height': 720}
        )

        page = browser.new_page()

        try:
            print("Opening LinkedIn...")
            page.goto('https://www.linkedin.com/feed/', timeout=30000)

            print("\nPlease log in to LinkedIn in the browser window.")
            print("Once logged in, close the browser window to save the session.\n")

            # Keep browser open until user closes it
            while not browser.is_closed():
                time.sleep(1)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            try:
                browser.close()
            except:
                pass

    print("\n" + "=" * 70)
    print("Session saved to:", session_path)
    print("=" * 70)
    print("\nNow copy this session to the main location:")
    print(f"  cp -r {session_path} .linkedin_session")
    print("\nThen run the orchestrator again to post.")

if __name__ == '__main__':
    setup_linkedin_session()
