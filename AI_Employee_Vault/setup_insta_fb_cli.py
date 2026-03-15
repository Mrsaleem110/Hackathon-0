#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram + Facebook Setup - Non-interactive version
Usage: python setup_insta_fb_cli.py --instagram-token YOUR_TOKEN --instagram-id YOUR_ID --facebook-token YOUR_TOKEN --facebook-id YOUR_ID
"""

import os
import sys
import argparse
from pathlib import Path

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_section(title):
    print(f"\n[*] {title}")
    print("-"*70)

def update_env(credentials):
    """Update .env file with credentials"""
    env_path = Path(__file__).parent / '.env'

    if not env_path.exists():
        print(f"[!] .env file nahi mila: {env_path}")
        return False

    with open(env_path, 'r') as f:
        content = f.read()

    # Update each credential
    for key, value in credentials.items():
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith(f"{key}="):
                new_lines.append(f"{key}={value}")
            else:
                new_lines.append(line)
        content = '\n'.join(new_lines)

    with open(env_path, 'w') as f:
        f.write(content)

    return True

def verify_setup():
    """Verify credentials are set in .env"""
    env_path = Path(__file__).parent / '.env'

    with open(env_path, 'r') as f:
        content = f.read()

    print_section("VERIFICATION")

    checks = {
        'INSTAGRAM_ACCESS_TOKEN': 'Instagram Access Token',
        'INSTAGRAM_BUSINESS_ACCOUNT_ID': 'Instagram Business Account ID',
        'FACEBOOK_ACCESS_TOKEN': 'Facebook Access Token',
        'FACEBOOK_PAGE_ID': 'Facebook Page ID'
    }

    all_good = True
    for key, label in checks.items():
        if f"{key}=" in content:
            for line in content.split('\n'):
                if line.startswith(f"{key}="):
                    value = line.split('=', 1)[1].strip()
                    if value and not value.startswith('demo_') and not value.startswith('IGAB_demo') and not value.startswith('EAAB_demo'):
                        print(f"[+] {label}: Set")
                    else:
                        print(f"[~] {label}: Demo token")
                        all_good = False
                    break
        else:
            print(f"[-] {label}: Not found")
            all_good = False

    return all_good

def main():
    parser = argparse.ArgumentParser(description='Setup Instagram and Facebook credentials')
    parser.add_argument('--instagram-token', help='Instagram Access Token')
    parser.add_argument('--instagram-id', help='Instagram Business Account ID')
    parser.add_argument('--facebook-token', help='Facebook Access Token')
    parser.add_argument('--facebook-id', help='Facebook Page ID')
    parser.add_argument('--verify', action='store_true', help='Only verify credentials')
    parser.add_argument('--show-guide', action='store_true', help='Show setup guide')

    args = parser.parse_args()

    if args.show_guide:
        print_header("INSTAGRAM + FACEBOOK SETUP GUIDE")
        print("""
INSTAGRAM CREDENTIALS:
1. Go to https://business.facebook.com/
2. Settings -> Apps and Websites
3. Add Instagram Business Account
4. Copy Business Account ID and Access Token

FACEBOOK CREDENTIALS:
1. Go to https://developers.facebook.com/tools/explorer/
2. Get Token -> Page Access Token
3. Copy token and Page ID

COMMAND:
python setup_insta_fb_cli.py \\
  --instagram-token YOUR_INSTAGRAM_TOKEN \\
  --instagram-id YOUR_INSTAGRAM_ID \\
  --facebook-token YOUR_FACEBOOK_TOKEN \\
  --facebook-id YOUR_FACEBOOK_ID
        """)
        return True

    if args.verify:
        print_header("VERIFY CREDENTIALS")
        verify_setup()
        return True

    if not args.instagram_token or not args.instagram_id or not args.facebook_token or not args.facebook_id:
        print_header("INSTAGRAM + FACEBOOK SETUP")
        print("""
Usage:
  python setup_insta_fb_cli.py \\
    --instagram-token TOKEN \\
    --instagram-id ID \\
    --facebook-token TOKEN \\
    --facebook-id ID

Or show guide:
  python setup_insta_fb_cli.py --show-guide

Or verify:
  python setup_insta_fb_cli.py --verify
        """)
        return False

    print_header("INSTAGRAM + FACEBOOK SETUP")

    credentials = {
        'INSTAGRAM_ACCESS_TOKEN': args.instagram_token,
        'INSTAGRAM_BUSINESS_ACCOUNT_ID': args.instagram_id,
        'FACEBOOK_ACCESS_TOKEN': args.facebook_token,
        'FACEBOOK_PAGE_ID': args.facebook_id
    }

    print_section("UPDATING .env FILE")
    if update_env(credentials):
        print("[+] .env file update ho gaya!")
    else:
        print("[-] .env update nahi hua")
        return False

    verify_setup()

    print_section("NEXT STEPS")
    print("""
Ab tum ye kar sakte ho:

1. Test credentials:
   python test_insta_fb.py

2. Instagram post karo:
   python auto_post_social.py

3. Dashboard dekho:
   python social_dashboard.py
    """)

    print_header("SETUP COMPLETE")
    return True

if __name__ == '__main__':
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n[-] Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
