#!/usr/bin/env python3
"""
Add Real Instagram and Facebook Credentials
Interactive script to securely add real credentials to .env file
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load existing .env
env_path = Path('.env')
if env_path.exists():
    load_dotenv(env_path)

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(title.center(70))
    print("="*70 + "\n")

def print_section(title):
    """Print section header"""
    print(f"\n{title}")
    print("-" * 70)

def get_instagram_credentials():
    """Get Instagram credentials from user"""
    print_section("INSTAGRAM CREDENTIALS")

    print("\nTo get Instagram credentials:")
    print("1. Go to: https://business.facebook.com/")
    print("2. Create a Business Account (if you don't have one)")
    print("3. Go to Settings → Apps and Websites → Instagram")
    print("4. Generate an Access Token")
    print("5. Get your Instagram Business Account ID")

    print("\n" + "-"*70)

    access_token = input("\nEnter Instagram Access Token: ").strip()
    if not access_token:
        print("ERROR: Instagram Access Token is required!")
        return None

    business_account_id = input("Enter Instagram Business Account ID: ").strip()
    if not business_account_id:
        print("ERROR: Instagram Business Account ID is required!")
        return None

    username = input("Enter Instagram Username (optional): ").strip()
    if not username:
        username = "your_instagram_handle"

    return {
        'INSTAGRAM_ACCESS_TOKEN': access_token,
        'INSTAGRAM_BUSINESS_ACCOUNT_ID': business_account_id,
        'INSTAGRAM_USERNAME': username,
    }

def get_facebook_credentials():
    """Get Facebook credentials from user"""
    print_section("FACEBOOK CREDENTIALS")

    print("\nTo get Facebook credentials:")
    print("1. Go to: https://developers.facebook.com/")
    print("2. Create an App (if you don't have one)")
    print("3. Go to Settings → Basic → App ID and App Secret")
    print("4. Generate a Page Access Token")
    print("5. Get your Facebook Page ID")

    print("\n" + "-"*70)

    access_token = input("\nEnter Facebook Page Access Token: ").strip()
    if not access_token:
        print("ERROR: Facebook Access Token is required!")
        return None

    page_id = input("Enter Facebook Page ID: ").strip()
    if not page_id:
        print("ERROR: Facebook Page ID is required!")
        return None

    return {
        'FACEBOOK_ACCESS_TOKEN': access_token,
        'FACEBOOK_PAGE_ID': page_id,
    }

def update_env_file(credentials):
    """Update .env file with new credentials"""
    try:
        # Read existing .env
        env_content = ""
        if env_path.exists():
            with open(env_path, 'r') as f:
                env_content = f.read()

        # Update or add credentials
        for key, value in credentials.items():
            # Check if key exists
            if f"{key}=" in env_content:
                # Replace existing value
                lines = env_content.split('\n')
                new_lines = []
                for line in lines:
                    if line.startswith(f"{key}="):
                        new_lines.append(f"{key}={value}")
                    else:
                        new_lines.append(line)
                env_content = '\n'.join(new_lines)
            else:
                # Add new credential
                env_content += f"\n{key}={value}"

        # Write back to .env
        with open(env_path, 'w') as f:
            f.write(env_content)

        return True
    except Exception as e:
        print(f"ERROR: Failed to update .env file: {e}")
        return False

def verify_credentials():
    """Verify credentials are loaded"""
    try:
        # Reload .env
        load_dotenv(env_path, override=True)

        instagram_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        instagram_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        facebook_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        facebook_id = os.getenv('FACEBOOK_PAGE_ID')

        print_section("VERIFICATION")

        print("\nInstagram Configuration:")
        if instagram_token and instagram_token != "IGAB_demo_token_123456789":
            print(f"  [OK] Access Token: {instagram_token[:20]}...")
        else:
            print("  [NO] Access Token not set")

        if instagram_id and instagram_id != "17841400000000":
            print(f"  [OK] Business Account ID: {instagram_id}")
        else:
            print("  [NO] Business Account ID not set")

        print("\nFacebook Configuration:")
        if facebook_token and facebook_token != "FBAB_demo_token_123456789":
            print(f"  [OK] Access Token: {facebook_token[:20]}...")
        else:
            print("  [NO] Access Token not set")

        if facebook_id and facebook_id != "123456789":
            print(f"  [OK] Page ID: {facebook_id}")
        else:
            print("  [NO] Page ID not set")

        return (instagram_token and instagram_id and facebook_token and facebook_id)

    except Exception as e:
        print(f"ERROR: Verification failed: {e}")
        return False

def main():
    """Main function"""
    print_header("ADD REAL INSTAGRAM & FACEBOOK CREDENTIALS")

    print("This script will help you add real credentials to your .env file.")
    print("Your credentials will be stored securely in the .env file.")
    print("\nIMPORTANT: Keep your .env file secure and never commit it to git!")

    # Ask which credentials to add
    print_section("SELECT CREDENTIALS TO ADD")

    add_instagram = input("Add Instagram credentials? (y/n): ").strip().lower() == 'y'
    add_facebook = input("Add Facebook credentials? (y/n): ").strip().lower() == 'y'

    if not add_instagram and not add_facebook:
        print("\nNo credentials selected. Exiting.")
        return

    credentials = {}

    # Get Instagram credentials
    if add_instagram:
        insta_creds = get_instagram_credentials()
        if insta_creds:
            credentials.update(insta_creds)
        else:
            print("Skipping Instagram credentials.")

    # Get Facebook credentials
    if add_facebook:
        fb_creds = get_facebook_credentials()
        if fb_creds:
            credentials.update(fb_creds)
        else:
            print("Skipping Facebook credentials.")

    if not credentials:
        print("\nNo credentials to add. Exiting.")
        return

    # Confirm before saving
    print_section("CONFIRM CREDENTIALS")
    print("\nCredentials to be saved:")
    for key, value in credentials.items():
        if 'TOKEN' in key:
            print(f"  {key}: {value[:20]}...")
        else:
            print(f"  {key}: {value}")

    confirm = input("\nSave these credentials? (y/n): ").strip().lower() == 'y'
    if not confirm:
        print("Cancelled. No changes made.")
        return

    # Update .env file
    print("\nUpdating .env file...")
    if update_env_file(credentials):
        print("✅ .env file updated successfully!")
    else:
        print("❌ Failed to update .env file!")
        return

    # Verify credentials
    print("\nVerifying credentials...")
    if verify_credentials():
        print("\n✅ All credentials verified and loaded!")
        print("\nYour system is now ready to use real Instagram and Facebook credentials.")
        print("\nNext steps:")
        print("1. Test the credentials: python test_insta_fb.py")
        print("2. Start posting: python auto_post_social.py")
        print("3. Monitor dashboard: python audit_dashboard.py dashboard")
    else:
        print("\n⚠️  Some credentials may not be properly configured.")
        print("Please check your .env file and try again.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
