#!/usr/bin/env python3
"""
Quick Facebook Setup - Add your credentials
"""

import os
from pathlib import Path

def setup_facebook():
    print("\n" + "="*70)
    print("  FACEBOOK SETUP")
    print("="*70)

    print("""
📘 Facebook ke credentials kaise milenge:

OPTION 1: Facebook Page (Recommended)
1. https://developers.facebook.com/ par jao
2. App create karo (type: Business)
3. Facebook Login product add karo
4. Settings → Basic mein App ID aur App Secret dekho
5. Token generate karo with scopes:
   - pages_manage_posts
   - pages_read_engagement

OPTION 2: Existing App
1. https://developers.facebook.com/apps/
2. Apna app select karo
3. Settings → Basic
4. App ID aur App Secret copy karo
5. Tools → Access Token Generator
6. Page select karo aur token generate karo

OPTION 3: Graph API Explorer
1. https://developers.facebook.com/tools/explorer/
2. Get Token button click karo
3. Page Access Token select karo
4. Token copy karo

Tumhe chahiye:
- FACEBOOK_ACCESS_TOKEN (Page Access Token)
- FACEBOOK_PAGE_ID (Tumhara page ka ID)
    """)

    print("\n" + "-"*70)
    access_token = input("🔑 FACEBOOK_ACCESS_TOKEN enter karo: ").strip()
    page_id = input("🔑 FACEBOOK_PAGE_ID enter karo: ").strip()

    if not access_token or not page_id:
        print("❌ Credentials empty hain!")
        return False

    # Update .env
    env_path = Path(__file__).parent / '.env'

    with open(env_path, 'r') as f:
        content = f.read()

    # Replace Facebook credentials
    content = content.replace(
        f'FACEBOOK_ACCESS_TOKEN=EAAB_demo_token_987654321',
        f'FACEBOOK_ACCESS_TOKEN={access_token}'
    )
    content = content.replace(
        f'FACEBOOK_PAGE_ID=1048264368365205',
        f'FACEBOOK_PAGE_ID={page_id}'
    )

    with open(env_path, 'w') as f:
        f.write(content)

    print("\n✅ Facebook credentials .env mein add ho gaye!")
    print(f"   Access Token: {access_token[:20]}...")
    print(f"   Page ID: {page_id}")

    return True

if __name__ == '__main__':
    try:
        setup_facebook()
    except Exception as e:
        print(f"❌ Error: {e}")
