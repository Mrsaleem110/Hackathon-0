#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Real Instagram & Facebook Credentials - Non-Interactive Version
Just edit this file with your credentials and run it
"""

import sys
from pathlib import Path

# ============================================================================
# STEP 1: ADD YOUR CREDENTIALS HERE
# ============================================================================

# Get these from: https://developers.facebook.com/tools/explorer/
# See SETUP_REAL_CREDENTIALS.md for detailed instructions

INSTAGRAM_ACCESS_TOKEN = "IGAB_"  # Replace with your token (starts with IGAB_)
INSTAGRAM_BUSINESS_ACCOUNT_ID = ""  # Replace with your account ID (17 digits)

FACEBOOK_ACCESS_TOKEN = "EAAB_"  # Replace with your token (starts with EAAB_)
FACEBOOK_PAGE_ID = ""  # Replace with your page ID (numeric)

# ============================================================================
# STEP 2: RUN THIS SCRIPT
# ============================================================================
# python add_credentials_manual.py

# ============================================================================

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

def validate_credentials():
    """Validate credentials before saving"""
    print_section("VALIDATING CREDENTIALS")

    errors = []

    # Validate Instagram
    if not INSTAGRAM_ACCESS_TOKEN or INSTAGRAM_ACCESS_TOKEN == "IGAB_":
        errors.append("Instagram Access Token is empty or not set")
    elif not (INSTAGRAM_ACCESS_TOKEN.startswith('IGAB_') or INSTAGRAM_ACCESS_TOKEN.startswith('EAAB_')):
        errors.append("Instagram token should start with IGAB_ or EAAB_")
    elif len(INSTAGRAM_ACCESS_TOKEN) < 50:
        errors.append("Instagram token seems too short")
    else:
        print_success("Instagram Access Token: Valid format")

    if not INSTAGRAM_BUSINESS_ACCOUNT_ID:
        errors.append("Instagram Business Account ID is empty")
    elif not INSTAGRAM_BUSINESS_ACCOUNT_ID.isdigit():
        errors.append("Instagram Account ID should be numeric")
    elif len(INSTAGRAM_BUSINESS_ACCOUNT_ID) < 10:
        errors.append("Instagram Account ID seems too short")
    else:
        print_success("Instagram Business Account ID: Valid format")

    # Validate Facebook
    if not FACEBOOK_ACCESS_TOKEN or FACEBOOK_ACCESS_TOKEN == "EAAB_":
        errors.append("Facebook Access Token is empty or not set")
    elif not FACEBOOK_ACCESS_TOKEN.startswith('EAAB_'):
        errors.append("Facebook token should start with EAAB_")
    elif len(FACEBOOK_ACCESS_TOKEN) < 50:
        errors.append("Facebook token seems too short")
    else:
        print_success("Facebook Access Token: Valid format")

    if not FACEBOOK_PAGE_ID:
        errors.append("Facebook Page ID is empty")
    elif not FACEBOOK_PAGE_ID.isdigit():
        errors.append("Facebook Page ID should be numeric")
    else:
        print_success("Facebook Page ID: Valid format")

    if errors:
        print_section("ERRORS FOUND")
        for error in errors:
            print_error(error)
        return False

    return True

def update_env_file():
    """Update .env file with credentials"""
    env_path = Path(__file__).parent / '.env'

    if not env_path.exists():
        print_error(f".env file not found at {env_path}")
        return False

    try:
        # Read current .env
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Create updates map
        updates = {
            'INSTAGRAM_ACCESS_TOKEN': INSTAGRAM_ACCESS_TOKEN,
            'INSTAGRAM_BUSINESS_ACCOUNT_ID': INSTAGRAM_BUSINESS_ACCOUNT_ID,
            'FACEBOOK_ACCESS_TOKEN': FACEBOOK_ACCESS_TOKEN,
            'FACEBOOK_PAGE_ID': FACEBOOK_PAGE_ID,
        }

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

        print_success(".env file updated successfully")
        return True

    except Exception as e:
        print_error(f"Failed to update .env: {e}")
        return False

def verify_update():
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
                        value == '1048264368365205' or
                        value.startswith('IGAB_') and len(value) < 50 or
                        value.startswith('EAAB_') and len(value) < 50
                    )

                    if value and not is_demo and value != key:
                        print_success(f"{label}: Configured")
                    else:
                        print_error(f"{label}: Not properly configured")
                        all_good = False
                    break

        return all_good

    except Exception as e:
        print_error(f"Verification failed: {e}")
        return False

def main():
    print_header("ADD REAL INSTAGRAM & FACEBOOK CREDENTIALS")

    print("""
This script will update your .env file with real credentials.

BEFORE RUNNING:
  1. Edit this file (add_credentials_manual.py)
  2. Replace the placeholder values with your real credentials
  3. Save the file
  4. Run: python add_credentials_manual.py

HOW TO GET CREDENTIALS:
  See: SETUP_REAL_CREDENTIALS.md
  Or: CREDENTIALS_QUICK_REFERENCE.md
    """)

    # Validate
    if not validate_credentials():
        print_section("SETUP FAILED")
        print("""
Please edit this file and add your credentials:

1. Open: add_credentials_manual.py
2. Find the STEP 1 section
3. Replace the placeholder values:
   - INSTAGRAM_ACCESS_TOKEN = "IGAB_your_real_token"
   - INSTAGRAM_BUSINESS_ACCOUNT_ID = "17841400000000"
   - FACEBOOK_ACCESS_TOKEN = "EAAB_your_real_token"
   - FACEBOOK_PAGE_ID = "1048264368365205"
4. Save and run again
        """)
        return False

    # Update .env
    print_section("UPDATING .env FILE")
    if not update_env_file():
        return False

    # Verify
    if verify_update():
        print_success("All credentials verified!")
    else:
        print_error("Some credentials may not be correct")

    # Next steps
    print_section("NEXT STEPS")
    print("""
1. Validate credentials:
   python validate_credentials.py

2. Test posting:
   python auto_post_social.py --platform instagram --caption "Test!"
   python auto_post_social.py --platform facebook --message "Test!"

3. View dashboard:
   python social_dashboard.py

4. Start orchestrator:
   python orchestrator.py
    """)

    print_header("✓ SETUP COMPLETE")
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
