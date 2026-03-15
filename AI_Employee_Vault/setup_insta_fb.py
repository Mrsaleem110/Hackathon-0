#!/usr/bin/env python3
"""
Instagram + Facebook Setup - Dono credentials ek saath add karo
"""

import os
from pathlib import Path

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_section(title):
    print(f"\n📌 {title}")
    print("-"*70)

def setup_instagram():
    print_section("INSTAGRAM SETUP")

    print("""
Instagram credentials ke liye:
1. https://business.facebook.com/ par jao
2. Settings → Apps and Websites
3. Instagram Business Account add karo
4. Business Account ID aur Access Token copy karo

Ya:
1. https://developers.facebook.com/
2. App create karo → Instagram Basic Display add karo
3. Access token generate karo
    """)

    access_token = input("\n🔑 INSTAGRAM_ACCESS_TOKEN: ").strip()
    business_account_id = input("🔑 INSTAGRAM_BUSINESS_ACCOUNT_ID: ").strip()

    if not access_token or not business_account_id:
        print("❌ Instagram credentials empty hain!")
        return None

    return {
        'INSTAGRAM_ACCESS_TOKEN': access_token,
        'INSTAGRAM_BUSINESS_ACCOUNT_ID': business_account_id
    }

def setup_facebook():
    print_section("FACEBOOK SETUP")

    print("""
Facebook credentials ke liye:
1. https://developers.facebook.com/ par jao
2. App create karo (type: Business)
3. Facebook Login product add karo
4. Settings → Basic mein App ID dekho
5. Token generate karo with scopes:
   - pages_manage_posts
   - pages_read_engagement

Ya:
1. https://developers.facebook.com/tools/explorer/
2. Get Token → Page Access Token select karo
3. Token copy karo
    """)

    access_token = input("\n🔑 FACEBOOK_ACCESS_TOKEN: ").strip()
    page_id = input("🔑 FACEBOOK_PAGE_ID: ").strip()

    if not access_token or not page_id:
        print("❌ Facebook credentials empty hain!")
        return None

    return {
        'FACEBOOK_ACCESS_TOKEN': access_token,
        'FACEBOOK_PAGE_ID': page_id
    }

def update_env(credentials):
    """Update .env file with credentials"""
    env_path = Path(__file__).parent / '.env'

    if not env_path.exists():
        print(f"❌ .env file nahi mila: {env_path}")
        return False

    with open(env_path, 'r') as f:
        content = f.read()

    # Update each credential
    for key, value in credentials.items():
        # Find and replace the line
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
            # Extract value
            for line in content.split('\n'):
                if line.startswith(f"{key}="):
                    value = line.split('=', 1)[1].strip()
                    if value and not value.startswith('demo_') and not value.startswith('IGAB_demo') and not value.startswith('EAAB_demo'):
                        print(f"✅ {label}: Set")
                    else:
                        print(f"⏳ {label}: Demo token (update needed)")
                        all_good = False
                    break
        else:
            print(f"❌ {label}: Not found")
            all_good = False

    return all_good

def main():
    print_header("INSTAGRAM + FACEBOOK SETUP")

    print("""
Yeh script tumhare Instagram aur Facebook credentials ko .env mein add karega.

Tumhe chahiye:
✓ Instagram Business Account ID aur Access Token
✓ Facebook Page ID aur Access Token

Chalo shuru karte hain!
    """)

    input("Enter daba ke continue karo...")

    # Get credentials
    instagram_creds = setup_instagram()
    if not instagram_creds:
        return False

    facebook_creds = setup_facebook()
    if not facebook_creds:
        return False

    all_creds = {**instagram_creds, **facebook_creds}

    # Update .env
    print_section("UPDATING .env FILE")
    if update_env(all_creds):
        print("✅ .env file update ho gaya!")
    else:
        print("❌ .env update nahi hua")
        return False

    # Verify
    verify_setup()

    # Next steps
    print_section("NEXT STEPS")
    print("""
Ab tum ye kar sakte ho:

1. Test credentials:
   python test_mcp_servers.py

2. Instagram post karo:
   python -c "from mcp_servers.instagram_mcp import InstagramClient; ig = InstagramClient(); print(ig.post_feed('Hello Instagram!', 'https://example.com/image.jpg'))"

3. Facebook post karo:
   python -c "from mcp_servers.facebook_mcp import FacebookClient; fb = FacebookClient(); print(fb.post_feed('Hello Facebook!', 'https://example.com/link'))"

4. Orchestrator start karo:
   python orchestrator.py
    """)

    print_header("SETUP COMPLETE ✅")
    return True

if __name__ == '__main__':
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancel ho gaya")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)
