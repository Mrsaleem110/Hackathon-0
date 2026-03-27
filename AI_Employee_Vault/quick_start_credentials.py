#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Start - Add Real Instagram & Facebook Credentials
Run this to get started in 5 minutes!
"""

import subprocess
import sys
from pathlib import Path

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_section(title):
    print(f"\n>>> {title}")
    print("-"*70)

def print_success(msg):
    print(f"✓ {msg}")

def print_info(msg):
    print(f"ℹ {msg}")

def main():
    print_header("REAL CREDENTIALS - QUICK START")

    print("""
Welcome! This guide will help you add real Instagram & Facebook credentials
in just 5 minutes.

What you need:
  ✓ Instagram Business Account
  ✓ Facebook Page
  ✓ Facebook Developer Account (free)
  ✓ 5 minutes
    """)

    input("\nPress Enter to continue...")

    # Step 1: Get credentials
    print_section("STEP 1: GET YOUR CREDENTIALS (2 minutes)")
    print("""
Go to: https://developers.facebook.com/tools/explorer/

FOR INSTAGRAM:
  1. Generate Access Token
     - Scopes: instagram_basic, pages_manage_posts
  2. Run: GET /me/instagram_business_accounts
  3. Copy token (IGAB_...) and account ID (17 digits)

FOR FACEBOOK:
  1. Generate Access Token
     - Scopes: pages_manage_posts, pages_read_engagement
  2. Run: GET /me/accounts
  3. Copy token (EAAB_...) and page ID (numeric)
    """)

    input("Press Enter when you have your credentials...")

    # Step 2: Run setup script
    print_section("STEP 2: RUN SETUP SCRIPT (1 minute)")
    print("""
Running: python setup_real_credentials.py

This will:
  ✓ Show setup guides
  ✓ Prompt for credentials
  ✓ Validate input
  ✓ Update .env file
  ✓ Verify setup
    """)

    input("Press Enter to start setup...")

    try:
        result = subprocess.run(
            [sys.executable, 'setup_real_credentials.py'],
            cwd=Path(__file__).parent
        )
        if result.returncode != 0:
            print("\n[!] Setup script failed")
            return False
    except Exception as e:
        print(f"\n[!] Error running setup: {e}")
        return False

    # Step 3: Validate
    print_section("STEP 3: VALIDATE CREDENTIALS (1 minute)")
    print("""
Running: python validate_credentials.py

This will:
  ✓ Check credential format
  ✓ Test API connections
  ✓ Show any errors
    """)

    input("Press Enter to validate...")

    try:
        result = subprocess.run(
            [sys.executable, 'validate_credentials.py'],
            cwd=Path(__file__).parent
        )
        if result.returncode != 0:
            print("\n[!] Validation failed - check credentials")
            return False
    except Exception as e:
        print(f"\n[!] Error running validation: {e}")
        return False

    # Step 4: Test posting
    print_section("STEP 4: TEST POSTING (1 minute)")
    print("""
You can now test posting:

Instagram:
  python auto_post_social.py --platform instagram --caption "Test!"

Facebook:
  python auto_post_social.py --platform facebook --message "Test!"

Dashboard:
  python social_dashboard.py
    """)

    # Done
    print_header("✓ ALL DONE!")
    print("""
Your Instagram and Facebook credentials are now configured!

Next steps:
  1. Test posting: python auto_post_social.py
  2. View dashboard: python social_dashboard.py
  3. Start orchestrator: python orchestrator.py

For more info:
  - SETUP_REAL_CREDENTIALS.md - Complete guide
  - CREDENTIALS_QUICK_REFERENCE.md - Quick reference
  - validate_credentials.py - Test anytime
    """)

    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nQuick start cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
