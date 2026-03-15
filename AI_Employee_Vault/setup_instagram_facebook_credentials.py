#!/usr/bin/env python3
"""
Setup script for Instagram and Facebook credentials
Guides you through getting and adding credentials to .env
"""

import os
import sys
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_section(title):
    """Print a section header"""
    print(f"\n📌 {title}")
    print("-" * 70)

def get_instagram_credentials():
    """Guide user through getting Instagram credentials"""
    print_section("INSTAGRAM CREDENTIALS")

    print("""
Instagram credentials come from Facebook Business Manager or Facebook Developers.

OPTION A: Business Account (Recommended)
1. Go to https://business.facebook.com/
2. Click Settings → Apps and Websites
3. Add your Instagram Business Account
4. Go to Roles → Assign Users
5. Get your Business Account ID and Access Token

OPTION B: Personal Account
1. Go to https://developers.facebook.com/
2. Create an app (type: Business)
3. Add Instagram Basic Display product
4. Generate access token with 'instagram_basic' scope
    """)

    access_token = input("\n🔑 Enter INSTAGRAM_ACCESS_TOKEN: ").strip()
    business_account_id = input("🔑 Enter INSTAGRAM_BUSINESS_ACCOUNT_ID: ").strip()

    return {
        'INSTAGRAM_ACCESS_TOKEN': access_token,
        'INSTAGRAM_BUSINESS_ACCOUNT_ID': business_account_id
    }

def get_facebook_credentials():
    """Guide user through getting Facebook credentials"""
    print_section("FACEBOOK CREDENTIALS")

    print("""
Facebook credentials come from Facebook Developers portal.

Steps:
1. Go to https://developers.facebook.com/
2. Create an app (type: Business)
3. Add Facebook Login product
4. Get your Page ID and Access Token
5. Token needs these scopes:
   - pages_manage_posts
   - pages_read_engagement
    """)

    access_token = input("\n🔑 Enter FACEBOOK_ACCESS_TOKEN: ").strip()
    page_id = input("🔑 Enter FACEBOOK_PAGE_ID: ").strip()

    return {
        'FACEBOOK_ACCESS_TOKEN': access_token,
        'FACEBOOK_PAGE_ID': page_id
    }

def update_env_file(credentials):
    """Update .env file with new credentials"""
    env_path = Path(__file__).parent / '.env'

    if not env_path.exists():
        print(f"\n❌ .env file not found at {env_path}")
        return False

    # Read current .env
    with open(env_path, 'r') as f:
        lines = f.readlines()

    # Update credentials
    updated_lines = []
    for line in lines:
        updated = False
        for key, value in credentials.items():
            if line.startswith(f"{key}="):
                updated_lines.append(f"{key}={value}\n")
                updated = True
                break
        if not updated:
            updated_lines.append(line)

    # Write back
    with open(env_path, 'w') as f:
        f.writelines(updated_lines)

    return True

def verify_credentials(credentials):
    """Verify credentials are set"""
    print_section("VERIFICATION")

    all_set = True
    for key, value in credentials.items():
        if value and value != "your_" + key.lower() + "_here":
            print(f"✅ {key}: Set")
        else:
            print(f"❌ {key}: Not set")
            all_set = False

    return all_set

def main():
    """Main setup flow"""
    print_header("INSTAGRAM & FACEBOOK CREDENTIALS SETUP")

    print("""
This script will help you add Instagram and Facebook credentials to your .env file.

You'll need:
- Instagram Business Account ID and Access Token
- Facebook Page ID and Access Token

Let's get started!
    """)

    input("Press Enter to continue...")

    # Get credentials
    instagram_creds = get_instagram_credentials()
    facebook_creds = get_facebook_credentials()

    all_creds = {**instagram_creds, **facebook_creds}

    # Verify
    if not verify_credentials(all_creds):
        print("\n⚠️  Some credentials are missing or invalid")
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            return False

    # Update .env
    print_section("UPDATING .env FILE")
    if update_env_file(all_creds):
        print("✅ .env file updated successfully!")
    else:
        print("❌ Failed to update .env file")
        return False

    # Test
    print_section("TESTING CREDENTIALS")
    print("""
To test your credentials, run:
    python test_mcp_servers.py

Or test individually:
    python mcp_servers/instagram_mcp/test_instagram_mcp.py
    python mcp_servers/facebook_mcp/test_facebook_mcp.py
    """)

    print_header("SETUP COMPLETE ✅")
    print("""
Your Instagram and Facebook credentials have been added to .env

Next steps:
1. Test credentials: python test_mcp_servers.py
2. Start orchestrator: python orchestrator.py
3. Monitor logs: tail -f Logs/YYYY-MM-DD.json
    """)

    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
