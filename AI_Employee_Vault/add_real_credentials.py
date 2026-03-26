#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Real Instagram & Facebook Credentials
Interactive setup for production credentials
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_section(title):
    print(f"\n[*] {title}")
    print("-"*70)

def print_success(msg):
    print(f"[✓] {msg}")

def print_error(msg):
    print(f"[✗] {msg}")

def print_info(msg):
    print(f"[i] {msg}")

def get_instagram_credentials():
    """Get Instagram credentials from user"""
    print_section("INSTAGRAM CREDENTIALS")

    print("""
📱 Instagram Setup Guide:

Option 1: Using Facebook Business Manager (Recommended)
  1. Go to https://business.facebook.com/
  2. Click "Settings" → "Apps and Websites"
  3. Find your Instagram Business Account
  4. Click on it and copy:
     - Business Account ID (17-digit number)
     - Access Token (long string starting with IGAB_)

Option 2: Using Facebook Developers
  1. Go to https://developers.facebook.com/
  2. Create/Select your app
  3. Add "Instagram Basic Display" product
  4. Go to Settings → Basic
  5. Copy App ID and generate Access Token
  6. Get your Instagram Business Account ID

Option 3: Using Graph API Explorer
  1. Go to https://developers.facebook.com/tools/explorer/
  2. Select your app and page
  3. Generate a Page Access Token
  4. Use it for Instagram posting
    """)

    print("\n[?] Enter your Instagram credentials:")

    access_token = input("\n  Instagram Access Token (starts with IGAB_): ").strip()
    business_account_id = input("  Instagram Business Account ID (17 digits): ").strip()

    # Validate
    if not access_token:
        print_error("Access token is required!")
        return None

    if not business_account_id:
        print_error("Business Account ID is required!")
        return None

    # Basic validation
    if not access_token.startswith('IGAB_') and not access_token.startswith('EAAB_'):
        print_info("Note: Token doesn't start with IGAB_ or EAAB_, but continuing...")

    if not business_account_id.isdigit() or len(business_account_id) < 10:
        print_error("Business Account ID should be numeric (17 digits)")
        return None

    return {
        'INSTAGRAM_ACCESS_TOKEN': access_token,
        'INSTAGRAM_BUSINESS_ACCOUNT_ID': business_account_id
    }

def get_facebook_credentials():
    """Get Facebook credentials from user"""
    print_section("FACEBOOK CREDENTIALS")

    print("""
📘 Facebook Setup Guide:

Option 1: Using Facebook Developers (Recommended)
  1. Go to https://developers.facebook.com/
  2. Create/Select your app (type: Business)
  3. Add "Facebook Login" product
  4. Go to Settings → Basic
  5. Copy App ID and App Secret
  6. Generate a Page Access Token with scopes:
     - pages_manage_posts
     - pages_read_engagement
     - pages_manage_metadata

Option 2: Using Graph API Explorer
  1. Go to https://developers.facebook.com/tools/explorer/
  2. Select your app
  3. Select your page from dropdown
  4. Click "Generate Access Token"
  5. Copy the token (valid for 60 days)
  6. Get your Page ID from page settings

Option 3: Using Facebook Business Manager
  1. Go to https://business.facebook.com/
  2. Select your page
  3. Settings → Access Tokens
  4. Generate new token with required permissions
  5. Copy Page ID from page settings
    """)

    print("\n[?] Enter your Facebook credentials:")

    access_token = input("\n  Facebook Access Token (starts with EAAB_): ").strip()
    page_id = input("  Facebook Page ID (numeric): ").strip()

    # Validate
    if not access_token:
        print_error("Access token is required!")
        return None

    if not page_id:
        print_error("Page ID is required!")
        return None

    # Basic validation
    if not access_token.startswith('EAAB_'):
        print_info("Note: Token doesn't start with EAAB_, but continuing...")

    if not page_id.isdigit():
        print_error("Page ID should be numeric")
        return None

    return {
        'FACEBOOK_ACCESS_TOKEN': access_token,
        'FACEBOOK_PAGE_ID': page_id
    }

def update_env_file(credentials):
    """Update .env file with new credentials"""
    env_path = Path(__file__).parent / '.env'

    if not env_path.exists():
        print_error(f".env file not found at {env_path}")
        return False

    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Create a mapping of keys to update
        updates = {}
        for key, value in credentials.items():
            updates[key] = value

        # Update lines
        new_lines = []
        for line in lines:
            updated = False
            for key, value in updates.items():
                if line.startswith(f"{key}="):
                    new_lines.append(f"{key}={value}\n")
                    updated = True
                    break
            if not updated:
                new_lines.append(line)

        # Write back
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print_success(f".env file updated successfully")
        return True

    except Exception as e:
        print_error(f"Failed to update .env: {e}")
        return False

def verify_credentials():
    """Verify credentials in .env file"""
    env_path = Path(__file__).parent / '.env'

    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print_section("VERIFICATION")

        checks = {
            'INSTAGRAM_ACCESS_TOKEN': 'Instagram Access Token',
            'INSTAGRAM_BUSINESS_ACCOUNT_ID': 'Instagram Business Account ID',
            'FACEBOOK_ACCESS_TOKEN': 'Facebook Access Token',
            'FACEBOOK_PAGE_ID': 'Facebook Page ID'
        }

        all_configured = True
        for key, label in checks.items():
            for line in content.split('\n'):
                if line.startswith(f"{key}="):
                    value = line.split('=', 1)[1].strip()

                    # Check if it's a demo token
                    is_demo = (
                        value.startswith('IGAB_demo') or
                        value.startswith('EAAB_demo') or
                        value == '17841400000000' or
                        value == '1048264368365205'
                    )

                    if value and not is_demo:
                        print_success(f"{label}: ✓ Configured")
                    elif is_demo:
                        print_error(f"{label}: ✗ Still using demo token")
                        all_configured = False
                    else:
                        print_error(f"{label}: ✗ Not set")
                        all_configured = False
                    break

        return all_configured

    except Exception as e:
        print_error(f"Verification failed: {e}")
        return False

def test_credentials():
    """Test if credentials work"""
    print_section("TESTING CREDENTIALS")

    try:
        from config import (
            INSTAGRAM_ACCESS_TOKEN,
            INSTAGRAM_BUSINESS_ACCOUNT_ID,
            FACEBOOK_ACCESS_TOKEN,
            FACEBOOK_PAGE_ID
        )

        print_info("Testing Instagram credentials...")
        if INSTAGRAM_ACCESS_TOKEN and INSTAGRAM_BUSINESS_ACCOUNT_ID:
            print_success("Instagram credentials loaded")
        else:
            print_error("Instagram credentials not loaded")

        print_info("Testing Facebook credentials...")
        if FACEBOOK_ACCESS_TOKEN and FACEBOOK_PAGE_ID:
            print_success("Facebook credentials loaded")
        else:
            print_error("Facebook credentials not loaded")

        return True

    except Exception as e:
        print_error(f"Test failed: {e}")
        return False

def show_next_steps():
    """Show next steps"""
    print_section("NEXT STEPS")

    print("""
Now that you have real credentials, you can:

1. Test the credentials:
   python test_insta_fb.py

2. Post to Instagram:
   python auto_post_social.py --platform instagram

3. Post to Facebook:
   python auto_post_social.py --platform facebook

4. View the dashboard:
   python social_dashboard.py

5. Start the orchestrator:
   python orchestrator.py

6. Check configuration status:
   python config.py
    """)

def main():
    print_header("ADD REAL INSTAGRAM & FACEBOOK CREDENTIALS")

    print("""
This script will help you add real production credentials
for Instagram and Facebook to your .env file.

⚠️  IMPORTANT SECURITY NOTES:
  • Never commit .env file to git
  • Keep your tokens secret
  • Tokens should be treated like passwords
  • Rotate tokens regularly
  • Use environment variables in production
    """)

    input("\nPress Enter to continue...")

    # Get credentials
    instagram_creds = get_instagram_credentials()
    if not instagram_creds:
        print_error("Instagram setup cancelled")
        return False

    facebook_creds = get_facebook_credentials()
    if not facebook_creds:
        print_error("Facebook setup cancelled")
        return False

    # Combine credentials
    all_creds = {**instagram_creds, **facebook_creds}

    # Show summary
    print_section("SUMMARY")
    print(f"Instagram Account ID: {instagram_creds['INSTAGRAM_BUSINESS_ACCOUNT_ID']}")
    print(f"Instagram Token: {instagram_creds['INSTAGRAM_ACCESS_TOKEN'][:20]}...")
    print(f"Facebook Page ID: {facebook_creds['FACEBOOK_PAGE_ID']}")
    print(f"Facebook Token: {facebook_creds['FACEBOOK_ACCESS_TOKEN'][:20]}...")

    confirm = input("\n[?] Proceed with updating .env? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print_error("Setup cancelled")
        return False

    # Update .env
    print_section("UPDATING .env FILE")
    if not update_env_file(all_creds):
        return False

    # Verify
    if verify_credentials():
        print_success("All credentials verified!")
    else:
        print_error("Some credentials may not be configured correctly")

    # Show next steps
    show_next_steps()

    print_header("SETUP COMPLETE ✓")
    print(f"\nTimestamp: {datetime.now().isoformat()}")

    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[-] Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
