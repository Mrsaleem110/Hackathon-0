#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive Setup - Add Real Credentials for All Platforms
Supports: Gmail, LinkedIn, Instagram, Facebook, Twitter, WhatsApp
"""

import os
import sys
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_header(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def print_section(title):
    print(f"\n>>> {title}")
    print("-"*80)

def print_success(msg):
    print(f"✓ {msg}")

def print_error(msg):
    print(f"✗ {msg}")

def print_info(msg):
    print(f"ℹ {msg}")

def show_gmail_guide():
    """Show Gmail setup guide"""
    print_section("GMAIL SETUP GUIDE")
    print("""
FASTEST WAY (5 minutes):

1. Open: https://console.cloud.google.com/

2. Create new project (or select existing)

3. Enable Gmail API:
   - Search "Gmail API"
   - Click "Enable"

4. Create OAuth 2.0 credentials:
   - Go to Credentials → Create Credentials → OAuth 2.0 Client ID
   - Choose "Desktop application"
   - Download JSON file

5. Extract from JSON:
   - client_id → GMAIL_CLIENT_ID
   - client_secret → GMAIL_CLIENT_SECRET
    """)

def show_linkedin_guide():
    """Show LinkedIn setup guide"""
    print_section("LINKEDIN SETUP GUIDE")
    print("""
FASTEST WAY (5 minutes):

1. Open: https://www.linkedin.com/developers/apps

2. Create new app:
   - App name: "AI Employee Vault"
   - LinkedIn Page: Select or create
   - Accept legal agreement

3. Go to "Auth" tab:
   - Copy Client ID → LINKEDIN_CLIENT_ID
   - Copy Client secret → LINKEDIN_CLIENT_SECRET

4. Generate access token:
   - Add redirect URL: http://localhost:8080/callback
   - Use OAuth flow to get LINKEDIN_ACCESS_TOKEN
    """)

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
    """)

def show_twitter_guide():
    """Show Twitter/X setup guide"""
    print_section("TWITTER/X SETUP GUIDE")
    print("""
FASTEST WAY (5 minutes):

1. Open: https://developer.twitter.com/en/portal/dashboard

2. Create app (if not exists)

3. Go to "Keys and tokens" tab

4. Copy the following:
   - Bearer Token → TWITTER_BEARER_TOKEN
   - API Key → TWITTER_API_KEY
   - API Secret → TWITTER_API_SECRET
   - Access Token → TWITTER_ACCESS_TOKEN
   - Access Token Secret → TWITTER_ACCESS_SECRET

5. Ensure app has "Read and Write" permissions
    """)

def show_whatsapp_guide():
    """Show WhatsApp setup guide"""
    print_section("WHATSAPP SETUP GUIDE")
    print("""
WhatsApp uses session-based authentication (no API key needed).

SETUP (First run):

1. Start orchestrator:
   python orchestrator.py

2. A QR code will appear in terminal

3. Scan with WhatsApp mobile app

4. Session saved to .whatsapp_session

⚠️  IMPORTANT:
  - Keep .whatsapp_session file safe
  - Don't share or commit to git
  - Session expires after 30 days of inactivity
    """)

def get_gmail_credentials():
    """Get Gmail credentials interactively"""
    print_section("ENTER GMAIL CREDENTIALS")
    show_gmail_guide()
    print("\n[?] Enter your Gmail credentials:\n")

    client_id = input("  Gmail Client ID: ").strip()
    if not client_id:
        print_error("Client ID cannot be empty")
        return None

    client_secret = input("  Gmail Client Secret: ").strip()
    if not client_secret:
        print_error("Client Secret cannot be empty")
        return None

    return {
        'GMAIL_CLIENT_ID': client_id,
        'GMAIL_CLIENT_SECRET': client_secret
    }

def get_linkedin_credentials():
    """Get LinkedIn credentials interactively"""
    print_section("ENTER LINKEDIN CREDENTIALS")
    show_linkedin_guide()
    print("\n[?] Enter your LinkedIn credentials:\n")

    client_id = input("  LinkedIn Client ID: ").strip()
    if not client_id:
        print_error("Client ID cannot be empty")
        return None

    client_secret = input("  LinkedIn Client Secret: ").strip()
    if not client_secret:
        print_error("Client Secret cannot be empty")
        return None

    access_token = input("  LinkedIn Access Token: ").strip()
    if not access_token:
        print_error("Access Token cannot be empty")
        return None

    return {
        'LINKEDIN_CLIENT_ID': client_id,
        'LINKEDIN_CLIENT_SECRET': client_secret,
        'LINKEDIN_ACCESS_TOKEN': access_token
    }

def get_instagram_credentials():
    """Get Instagram credentials interactively"""
    print_section("ENTER INSTAGRAM CREDENTIALS")
    show_instagram_guide()
    print("\n[?] Enter your Instagram credentials:\n")

    token = input("  Instagram Access Token (IGAB_...): ").strip()
    if not token:
        print_error("Token cannot be empty")
        return None

    account_id = input("  Instagram Business Account ID (17 digits): ").strip()
    if not account_id or not account_id.isdigit():
        print_error("Account ID must be numeric")
        return None

    return {
        'INSTAGRAM_ACCESS_TOKEN': token,
        'INSTAGRAM_BUSINESS_ACCOUNT_ID': account_id
    }

def get_facebook_credentials():
    """Get Facebook credentials interactively"""
    print_section("ENTER FACEBOOK CREDENTIALS")
    show_facebook_guide()
    print("\n[?] Enter your Facebook credentials:\n")

    token = input("  Facebook Access Token (EAAB_...): ").strip()
    if not token:
        print_error("Token cannot be empty")
        return None

    page_id = input("  Facebook Page ID (numeric): ").strip()
    if not page_id or not page_id.isdigit():
        print_error("Page ID must be numeric")
        return None

    return {
        'FACEBOOK_ACCESS_TOKEN': token,
        'FACEBOOK_PAGE_ID': page_id
    }

def get_twitter_credentials():
    """Get Twitter credentials interactively"""
    print_section("ENTER TWITTER/X CREDENTIALS")
    show_twitter_guide()
    print("\n[?] Enter your Twitter credentials:\n")

    bearer_token = input("  Twitter Bearer Token: ").strip()
    if not bearer_token:
        print_error("Bearer Token cannot be empty")
        return None

    api_key = input("  Twitter API Key: ").strip()
    if not api_key:
        print_error("API Key cannot be empty")
        return None

    api_secret = input("  Twitter API Secret: ").strip()
    if not api_secret:
        print_error("API Secret cannot be empty")
        return None

    access_token = input("  Twitter Access Token: ").strip()
    if not access_token:
        print_error("Access Token cannot be empty")
        return None

    access_secret = input("  Twitter Access Token Secret: ").strip()
    if not access_secret:
        print_error("Access Token Secret cannot be empty")
        return None

    return {
        'TWITTER_BEARER_TOKEN': bearer_token,
        'TWITTER_API_KEY': api_key,
        'TWITTER_API_SECRET': api_secret,
        'TWITTER_ACCESS_TOKEN': access_token,
        'TWITTER_ACCESS_SECRET': access_secret
    }

def select_platforms():
    """Let user select which platforms to configure"""
    print_section("SELECT PLATFORMS TO CONFIGURE")
    print("""
Which platforms do you want to add credentials for?

  1) Gmail
  2) LinkedIn
  3) Instagram
  4) Facebook
  5) Twitter/X
  6) WhatsApp (session-based, no setup needed)
  7) All platforms
  0) Cancel
    """)

    choice = input("  Enter choice (0-7): ").strip()

    mapping = {
        '0': [],
        '1': ['gmail'],
        '2': ['linkedin'],
        '3': ['instagram'],
        '4': ['facebook'],
        '5': ['twitter'],
        '6': ['whatsapp'],
        '7': ['gmail', 'linkedin', 'instagram', 'facebook', 'twitter', 'whatsapp'],
    }

    return mapping.get(choice, [])

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

        # Update credentials
        updated_lines = []
        updated_keys = set()

        for line in lines:
            updated = False
            for key, value in credentials.items():
                if line.startswith(f"{key}="):
                    updated_lines.append(f"{key}={value}\n")
                    updated_keys.add(key)
                    updated = True
                    break
            if not updated:
                updated_lines.append(line)

        # Add any new credentials not in file
        for key, value in credentials.items():
            if key not in updated_keys:
                updated_lines.append(f"{key}={value}\n")

        # Write back
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)

        print_success(".env file updated")
        return True

    except Exception as e:
        print_error(f"Failed to update .env: {e}")
        return False

def verify_credentials(credentials):
    """Verify credentials are valid"""
    print_section("VERIFICATION")

    all_valid = True
    for key, value in credentials.items():
        if value and not value.startswith('your_'):
            display_value = value[:30] + '...' if len(value) > 30 else value
            print_success(f"{key}: {display_value}")
        else:
            print_error(f"{key}: Empty or invalid")
            all_valid = False

    return all_valid

def show_next_steps():
    """Show what to do next"""
    print_section("NEXT STEPS")
    print("""
1. Verify configuration:
   python config.py

2. Test MCP servers:
   python test_mcp_servers.py

3. Start orchestrator:
   python orchestrator.py

4. Monitor logs:
   tail -f Logs/YYYY-MM-DD.json
    """)

def main():
    print_header("ADD REAL CREDENTIALS FOR ALL PLATFORMS")

    print("""
This script will help you add real production credentials.

⚠️  SECURITY NOTES:
  • Never commit .env to git
  • Keep tokens secret (like passwords)
  • Tokens expire after 60 days
  • Rotate tokens every 90 days
    """)

    input("\nPress Enter to continue...")

    # Select platforms
    platforms = select_platforms()
    if not platforms:
        print_error("No platforms selected. Setup cancelled.")
        return False

    # Get credentials
    all_credentials = {}

    try:
        if 'gmail' in platforms:
            creds = get_gmail_credentials()
            if creds:
                all_credentials.update(creds)

        if 'linkedin' in platforms:
            creds = get_linkedin_credentials()
            if creds:
                all_credentials.update(creds)

        if 'instagram' in platforms:
            creds = get_instagram_credentials()
            if creds:
                all_credentials.update(creds)

        if 'facebook' in platforms:
            creds = get_facebook_credentials()
            if creds:
                all_credentials.update(creds)

        if 'twitter' in platforms:
            creds = get_twitter_credentials()
            if creds:
                all_credentials.update(creds)

        if 'whatsapp' in platforms:
            show_whatsapp_guide()

    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        return False

    if not all_credentials:
        print_error("No credentials entered.")
        return False

    # Show summary
    print_section("SUMMARY")
    for key, value in all_credentials.items():
        display_value = value[:40] + '...' if len(value) > 40 else value
        print(f"  {key}: {display_value}")

    # Confirm
    confirm = input("\n[?] Proceed with updating .env? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print_error("Setup cancelled")
        return False

    # Update .env
    print_section("UPDATING .env FILE")
    if not update_env_file(all_credentials):
        return False

    # Verify
    if verify_credentials(all_credentials):
        print_success("All credentials verified!")
    else:
        print_error("Some credentials may not be correct")

    # Show next steps
    show_next_steps()

    print_header("✓ SETUP COMPLETE")
    print("\nYour credentials have been saved to .env")
    print("Run: python config.py")

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
