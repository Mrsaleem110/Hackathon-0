#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Interactive Setup - Add Real Instagram & Facebook Credentials
"""

import os
import sys
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_section(title):
    print(f"\n>>> {title}")
    print("-"*70)

def print_success(msg):
    print(f"✓ {msg}")

def print_error(msg):
    print(f"✗ {msg}")

def print_info(msg):
    print(f"ℹ {msg}")

def show_instagram_guide():
    """Show Instagram setup guide"""
    print_section("INSTAGRAM SETUP GUIDE")
    print("""
FASTEST WAY (2 minutes):

1. Open: https://developers.facebook.com/tools/explorer/

2. Top-right dropdown → Select your app

3. Click "Generate Access Token"
   - Choose scopes: instagram_basic, pages_manage_posts
   - Copy the token (starts with IGAB_)

4. In Graph API Explorer, run:
   GET /me/instagram_business_accounts

5. Copy the "id" field (17 digits)

RESULT:
  Token: IGAB_xxxxxxxxxxxxx...
  Account ID: 17841400000000
    """)

def show_facebook_guide():
    """Show Facebook setup guide"""
    print_section("FACEBOOK SETUP GUIDE")
    print("""
FASTEST WAY (2 minutes):

1. Open: https://developers.facebook.com/tools/explorer/

2. Top-right dropdown → Select your app

3. Click "Generate Access Token"
   - Choose scopes: pages_manage_posts, pages_read_engagement
   - Copy the token (starts with EAAB_)

4. In Graph API Explorer, run:
   GET /me/accounts

5. Copy the "id" field of your page

RESULT:
  Token: EAAB_xxxxxxxxxxxxx...
  Page ID: 1048264368365205
    """)

def get_instagram_credentials():
    """Get Instagram credentials interactively"""
    print_section("ENTER INSTAGRAM CREDENTIALS")

    show_instagram_guide()

    print("\n[?] Enter your Instagram credentials:\n")

    while True:
        token = input("  Instagram Access Token (IGAB_...): ").strip()
        if not token:
            print_error("Token cannot be empty")
            continue
        if not (token.startswith('IGAB_') or token.startswith('EAAB_')):
            print_info("Note: Token doesn't start with IGAB_ or EAAB_")
        break

    while True:
        account_id = input("  Instagram Business Account ID (17 digits): ").strip()
        if not account_id:
            print_error("Account ID cannot be empty")
            continue
        if not account_id.isdigit():
            print_error("Account ID must be numeric")
            continue
        if len(account_id) < 10:
            print_error("Account ID seems too short")
            continue
        break

    return {
        'INSTAGRAM_ACCESS_TOKEN': token,
        'INSTAGRAM_BUSINESS_ACCOUNT_ID': account_id
    }

def get_facebook_credentials():
    """Get Facebook credentials interactively"""
    print_section("ENTER FACEBOOK CREDENTIALS")

    show_facebook_guide()

    print("\n[?] Enter your Facebook credentials:\n")

    while True:
        token = input("  Facebook Access Token (EAAB_...): ").strip()
        if not token:
            print_error("Token cannot be empty")
            continue
        if not token.startswith('EAAB_'):
            print_info("Note: Token should start with EAAB_")
        break

    while True:
        page_id = input("  Facebook Page ID (numeric): ").strip()
        if not page_id:
            print_error("Page ID cannot be empty")
            continue
        if not page_id.isdigit():
            print_error("Page ID must be numeric")
            continue
        break

    return {
        'FACEBOOK_ACCESS_TOKEN': token,
        'FACEBOOK_PAGE_ID': page_id
    }

def update_env_file(credentials):
    """Update .env file with credentials"""
    env_path = Path(__file__).parent / '.env'

    if not env_path.exists():
        print_error(f".env file not found at {env_path}")
        return False

    try:
        # Read current .env
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Update lines
        new_lines = []
        for line in lines:
            updated = False
            for key, value in credentials.items():
                if line.startswith(f"{key}="):
                    new_lines.append(f"{key}={value}\n")
                    updated = True
                    break
            if not updated:
                new_lines.append(line)

        # Write back
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print_success(".env file updated")
        return True

    except Exception as e:
        print_error(f"Failed to update .env: {e}")
        return False

def verify_credentials():
    """Verify credentials were saved"""
    env_path = Path(__file__).parent / '.env'

    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print_section("VERIFICATION")

        checks = {
            'INSTAGRAM_ACCESS_TOKEN': 'Instagram Token',
            'INSTAGRAM_BUSINESS_ACCOUNT_ID': 'Instagram Account ID',
            'FACEBOOK_ACCESS_TOKEN': 'Facebook Token',
            'FACEBOOK_PAGE_ID': 'Facebook Page ID'
        }

        all_good = True
        for key, label in checks.items():
            for line in content.split('\n'):
                if line.startswith(f"{key}="):
                    value = line.split('=', 1)[1].strip()
                    is_demo = (
                        value.startswith('IGAB_demo') or
                        value.startswith('EAAB_demo') or
                        value == '17841400000000' or
                        value == '1048264368365205'
                    )

                    if value and not is_demo:
                        print_success(f"{label}: Configured")
                    else:
                        print_error(f"{label}: Still demo or empty")
                        all_good = False
                    break

        return all_good

    except Exception as e:
        print_error(f"Verification failed: {e}")
        return False

def show_next_steps():
    """Show what to do next"""
    print_section("NEXT STEPS")
    print("""
1. Validate credentials:
   python validate_credentials.py

2. Test posting to Instagram:
   python auto_post_social.py --platform instagram

3. Test posting to Facebook:
   python auto_post_social.py --platform facebook

4. View dashboard:
   python social_dashboard.py

5. Start orchestrator:
   python orchestrator.py
    """)

def main():
    print_header("ADD REAL INSTAGRAM & FACEBOOK CREDENTIALS")

    print("""
This script will help you add real production credentials.

⚠️  SECURITY NOTES:
  • Never commit .env to git
  • Keep tokens secret (like passwords)
  • Tokens expire after 60 days
  • Rotate tokens every 90 days
    """)

    input("\nPress Enter to continue...")

    # Get credentials
    try:
        instagram_creds = get_instagram_credentials()
        facebook_creds = get_facebook_credentials()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled")
        return False

    # Show summary
    print_section("SUMMARY")
    print(f"\nInstagram Account ID: {instagram_creds['INSTAGRAM_BUSINESS_ACCOUNT_ID']}")
    print(f"Instagram Token: {instagram_creds['INSTAGRAM_ACCESS_TOKEN'][:30]}...")
    print(f"\nFacebook Page ID: {facebook_creds['FACEBOOK_PAGE_ID']}")
    print(f"Facebook Token: {facebook_creds['FACEBOOK_ACCESS_TOKEN'][:30]}...")

    # Confirm
    confirm = input("\n[?] Proceed with updating .env? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print_error("Setup cancelled")
        return False

    # Update .env
    print_section("UPDATING .env FILE")
    all_creds = {**instagram_creds, **facebook_creds}

    if not update_env_file(all_creds):
        return False

    # Verify
    if verify_credentials():
        print_success("All credentials verified!")
    else:
        print_error("Some credentials may not be correct")

    # Show next steps
    show_next_steps()

    print_header("✓ SETUP COMPLETE")
    print("\nYour credentials have been saved to .env")
    print("Run: python validate_credentials.py")

    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print_error(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
