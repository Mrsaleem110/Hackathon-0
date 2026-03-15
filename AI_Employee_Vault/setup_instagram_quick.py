#!/usr/bin/env python3
"""
Quick Instagram Setup - Add your credentials
"""

import os
from pathlib import Path

def setup_instagram():
    print("\n" + "="*70)
    print("  INSTAGRAM SETUP")
    print("="*70)

    print("""
📱 Instagram ke credentials kaise milenge:

OPTION 1: Business Account (Recommended)
1. https://business.facebook.com/ par jao
2. Settings → Apps and Websites
3. Apna Instagram Business Account add karo
4. Business Account ID aur Access Token copy karo

OPTION 2: Personal Account
1. https://developers.facebook.com/ par jao
2. App create karo (type: Business)
3. Instagram Basic Display add karo
4. Access token generate karo

OPTION 3: Facebook Developers
1. https://developers.facebook.com/
2. App → Settings → Basic
3. App ID aur App Secret copy karo
4. Token generate karo
    """)

    print("\n" + "-"*70)
    access_token = input("🔑 INSTAGRAM_ACCESS_TOKEN enter karo: ").strip()
    business_account_id = input("🔑 INSTAGRAM_BUSINESS_ACCOUNT_ID enter karo: ").strip()

    if not access_token or not business_account_id:
        print("❌ Credentials empty hain!")
        return False

    # Update .env
    env_path = Path(__file__).parent / '.env'

    with open(env_path, 'r') as f:
        content = f.read()

    # Replace Instagram credentials
    content = content.replace(
        f'INSTAGRAM_ACCESS_TOKEN=IGAB_demo_token_123456789',
        f'INSTAGRAM_ACCESS_TOKEN={access_token}'
    )
    content = content.replace(
        f'INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000',
        f'INSTAGRAM_BUSINESS_ACCOUNT_ID={business_account_id}'
    )

    with open(env_path, 'w') as f:
        f.write(content)

    print("\n✅ Instagram credentials .env mein add ho gaye!")
    print(f"   Access Token: {access_token[:20]}...")
    print(f"   Business Account ID: {business_account_id}")

    return True

if __name__ == '__main__':
    try:
        setup_instagram()
    except Exception as e:
        print(f"❌ Error: {e}")
