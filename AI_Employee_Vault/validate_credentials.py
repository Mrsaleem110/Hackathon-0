#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate and Test Instagram & Facebook Credentials
"""

import os
import sys
import json
from pathlib import Path

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
    print(f"  ✓ {msg}")

def print_error(msg):
    print(f"  ✗ {msg}")

def print_info(msg):
    print(f"  ℹ {msg}")

def validate_instagram_token(token):
    """Validate Instagram token format"""
    if not token:
        return False, "Token is empty"

    if not (token.startswith('IGAB_') or token.startswith('EAAB_')):
        return False, "Token should start with IGAB_ or EAAB_"

    if len(token) < 50:
        return False, "Token seems too short (should be 100+ chars)"

    return True, "Token format valid"

def validate_instagram_account_id(account_id):
    """Validate Instagram Business Account ID"""
    if not account_id:
        return False, "Account ID is empty"

    if not account_id.isdigit():
        return False, "Account ID should be numeric"

    if len(account_id) < 10:
        return False, "Account ID should be at least 10 digits"

    return True, "Account ID format valid"

def validate_facebook_token(token):
    """Validate Facebook token format"""
    if not token:
        return False, "Token is empty"

    if not token.startswith('EAAB_'):
        return False, "Token should start with EAAB_"

    if len(token) < 50:
        return False, "Token seems too short (should be 100+ chars)"

    return True, "Token format valid"

def validate_facebook_page_id(page_id):
    """Validate Facebook Page ID"""
    if not page_id:
        return False, "Page ID is empty"

    if not page_id.isdigit():
        return False, "Page ID should be numeric"

    if len(page_id) < 5:
        return False, "Page ID should be at least 5 digits"

    return True, "Page ID format valid"

def load_env_credentials():
    """Load credentials from .env file"""
    env_path = Path(__file__).parent / '.env'

    credentials = {
        'INSTAGRAM_ACCESS_TOKEN': None,
        'INSTAGRAM_BUSINESS_ACCOUNT_ID': None,
        'FACEBOOK_ACCESS_TOKEN': None,
        'FACEBOOK_PAGE_ID': None,
    }

    if not env_path.exists():
        return credentials

    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    if key in credentials:
                        credentials[key] = value
    except Exception as e:
        print_error(f"Failed to read .env: {e}")

    return credentials

def test_instagram_api(token, account_id):
    """Test Instagram API connection"""
    print_section("Testing Instagram API")

    try:
        import requests
    except ImportError:
        print_error("requests library not installed")
        print_info("Install with: pip install requests")
        return False

    try:
        # Test basic API call
        url = f"https://graph.instagram.com/v18.0/{account_id}"
        params = {'access_token': token, 'fields': 'id,name,username'}

        response = requests.get(url, params=params, timeout=5)

        if response.status_code == 200:
            data = response.json()
            print_success(f"Instagram API connection successful")
            print_info(f"Account: {data.get('username', 'N/A')}")
            return True
        else:
            error = response.json().get('error', {})
            print_error(f"API Error: {error.get('message', 'Unknown error')}")
            return False

    except Exception as e:
        print_error(f"Connection test failed: {e}")
        return False

def test_facebook_api(token, page_id):
    """Test Facebook API connection"""
    print_section("Testing Facebook API")

    try:
        import requests
    except ImportError:
        print_error("requests library not installed")
        print_info("Install with: pip install requests")
        return False

    try:
        # Test basic API call
        url = f"https://graph.facebook.com/v18.0/{page_id}"
        params = {'access_token': token, 'fields': 'id,name,about'}

        response = requests.get(url, params=params, timeout=5)

        if response.status_code == 200:
            data = response.json()
            print_success(f"Facebook API connection successful")
            print_info(f"Page: {data.get('name', 'N/A')}")
            return True
        else:
            error = response.json().get('error', {})
            print_error(f"API Error: {error.get('message', 'Unknown error')}")
            return False

    except Exception as e:
        print_error(f"Connection test failed: {e}")
        return False

def main():
    print_header("VALIDATE INSTAGRAM & FACEBOOK CREDENTIALS")

    # Load credentials
    print_section("Loading Credentials from .env")
    credentials = load_env_credentials()

    # Validate Instagram
    print_section("Validating Instagram Credentials")

    ig_token = credentials['INSTAGRAM_ACCESS_TOKEN']
    ig_account = credentials['INSTAGRAM_BUSINESS_ACCOUNT_ID']

    ig_token_valid, ig_token_msg = validate_instagram_token(ig_token)
    ig_account_valid, ig_account_msg = validate_instagram_account_id(ig_account)

    if ig_token_valid:
        print_success(f"Access Token: {ig_token_msg}")
    else:
        print_error(f"Access Token: {ig_token_msg}")

    if ig_account_valid:
        print_success(f"Business Account ID: {ig_account_msg}")
    else:
        print_error(f"Business Account ID: {ig_account_msg}")

    # Validate Facebook
    print_section("Validating Facebook Credentials")

    fb_token = credentials['FACEBOOK_ACCESS_TOKEN']
    fb_page = credentials['FACEBOOK_PAGE_ID']

    fb_token_valid, fb_token_msg = validate_facebook_token(fb_token)
    fb_page_valid, fb_page_msg = validate_facebook_page_id(fb_page)

    if fb_token_valid:
        print_success(f"Access Token: {fb_token_msg}")
    else:
        print_error(f"Access Token: {fb_token_msg}")

    if fb_page_valid:
        print_success(f"Page ID: {fb_page_msg}")
    else:
        print_error(f"Page ID: {fb_page_msg}")

    # Test API connections
    all_valid = ig_token_valid and ig_account_valid and fb_token_valid and fb_page_valid

    if all_valid:
        print_section("Testing API Connections")

        ig_works = test_instagram_api(ig_token, ig_account)
        fb_works = test_facebook_api(fb_token, fb_page)

        if ig_works and fb_works:
            print_header("✓ ALL CREDENTIALS VALID AND WORKING")
            return True
        else:
            print_header("⚠ CREDENTIALS VALID BUT API TEST FAILED")
            print_info("Check token permissions or try regenerating tokens")
            return False
    else:
        print_header("✗ CREDENTIALS INVALID")
        print_info("Run: python add_real_credentials.py")
        return False

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[-] Validation cancelled")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
