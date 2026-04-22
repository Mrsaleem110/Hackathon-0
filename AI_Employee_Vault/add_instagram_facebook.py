#!/usr/bin/env python3
"""Quick script to add Instagram and Facebook credentials"""

import os
from pathlib import Path

def add_credentials():
    env_path = Path(__file__).parent / '.env'

    print("\n" + "="*80)
    print("  ADD INSTAGRAM & FACEBOOK CREDENTIALS")
    print("="*80)

    print("\n📌 INSTAGRAM SETUP (2 minutes)")
    print("-"*80)
    print("""
1. Go to: https://developers.facebook.com/tools/explorer/
2. Top-right dropdown → Select your app
3. Click "Generate Access Token"
   - Choose scopes: instagram_basic, pages_manage_posts
   - Copy the token (starts with IGAB_)
4. In Graph API Explorer, run: GET /me/instagram_business_accounts
5. Copy the "id" field (17 digits)
    """)

    ig_token = input("Paste your Instagram Access Token (IGAB_...): ").strip()
    ig_account = input("Paste your Instagram Business Account ID (17 digits): ").strip()

    print("\n📌 FACEBOOK SETUP (2 minutes)")
    print("-"*80)
    print("""
1. Go to: https://developers.facebook.com/tools/explorer/
2. Top-right dropdown → Select your app
3. Click "Generate Access Token"
   - Choose scopes: pages_manage_posts, pages_read_engagement
   - Copy the token (starts with EAAB_)
4. In Graph API Explorer, run: GET /me/accounts
5. Copy the "id" field of your page
    """)

    fb_token = input("Paste your Facebook Access Token (EAAB_...): ").strip()
    fb_page = input("Paste your Facebook Page ID (numeric): ").strip()

    if not all([ig_token, ig_account, fb_token, fb_page]):
        print("\n✗ Error: All fields are required")
        return False

    # Read current .env
    with open(env_path, 'r') as f:
        lines = f.readlines()

    # Update credentials
    updated_lines = []
    for line in lines:
        if line.startswith('INSTAGRAM_ACCESS_TOKEN='):
            updated_lines.append(f'INSTAGRAM_ACCESS_TOKEN={ig_token}\n')
        elif line.startswith('INSTAGRAM_BUSINESS_ACCOUNT_ID='):
            updated_lines.append(f'INSTAGRAM_BUSINESS_ACCOUNT_ID={ig_account}\n')
        elif line.startswith('FACEBOOK_ACCESS_TOKEN='):
            updated_lines.append(f'FACEBOOK_ACCESS_TOKEN={fb_token}\n')
        elif line.startswith('FACEBOOK_PAGE_ID='):
            updated_lines.append(f'FACEBOOK_PAGE_ID={fb_page}\n')
        else:
            updated_lines.append(line)

    # Write back
    with open(env_path, 'w') as f:
        f.writelines(updated_lines)

    print("\n" + "="*80)
    print("  ✓ CREDENTIALS UPDATED")
    print("="*80)
    print(f"\n✓ Instagram Token: {ig_token[:30]}...")
    print(f"✓ Instagram Account ID: {ig_account}")
    print(f"✓ Facebook Token: {fb_token[:30]}...")
    print(f"✓ Facebook Page ID: {fb_page}")

    print("\n📌 NEXT STEPS")
    print("-"*80)
    print("""
1. Verify configuration:
   python config.py

2. Test credentials:
   python test_mcp_servers.py

3. Start orchestrator:
   python orchestrator.py
    """)

    return True

if __name__ == '__main__':
    try:
        add_credentials()
    except KeyboardInterrupt:
        print("\n\nCancelled")
    except Exception as e:
        print(f"\n✗ Error: {e}")
