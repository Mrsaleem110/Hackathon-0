"""
Instagram Direct API Integration - No Selenium needed
Uses Instagram Graph API for posting
"""

import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv, set_key
from datetime import datetime

load_dotenv()

ENV_PATH = Path(__file__).parent / '.env'

# Instagram Graph API Configuration
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', '')
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN', '')
INSTAGRAM_USERNAME = 'm.saleem_ai_engineer'

# API endpoints
GRAPH_API_VERSION = 'v18.0'
GRAPH_API_URL = f'https://graph.instagram.com/{GRAPH_API_VERSION}'


def get_access_token_from_browser():
    """
    Get Instagram access token manually from browser

    Steps:
    1. Go to: https://developers.facebook.com/tools/explorer/
    2. Select your app
    3. Get User Token with instagram_business_basic,instagram_business_content_publish scopes
    4. Copy the token
    """
    print("\n" + "=" * 60)
    print("GET INSTAGRAM ACCESS TOKEN")
    print("=" * 60)

    print("\n📱 Manual Token Generation:")
    print("1. Go to: https://developers.facebook.com/tools/explorer/")
    print("2. Select your app from dropdown")
    print("3. Click 'Generate Access Token'")
    print("4. Select scopes:")
    print("   - instagram_business_basic")
    print("   - instagram_business_content_publish")
    print("5. Copy the token")

    token = input("\n🔑 Paste your access token here: ").strip()

    if not token:
        print("❌ No token provided")
        return None

    # Save token
    try:
        set_key(ENV_PATH, 'INSTAGRAM_ACCESS_TOKEN', token)
        print("✅ Token saved to .env")
        return token
    except Exception as e:
        print(f"❌ Error saving token: {e}")
        return None


def get_business_account_id(access_token):
    """Get Instagram Business Account ID"""
    try:
        print("\n📊 Fetching business account ID...")

        url = f'{GRAPH_API_URL}/me'
        params = {
            'fields': 'id,username,name',
            'access_token': access_token
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        account_id = data.get('id')
        username = data.get('username')

        print(f"✅ Account: @{username} (ID: {account_id})")

        # Save account ID
        set_key(ENV_PATH, 'INSTAGRAM_BUSINESS_ACCOUNT_ID', account_id)
        set_key(ENV_PATH, 'INSTAGRAM_USERNAME', username)

        return account_id

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def upload_image(access_token, account_id, image_url, caption):
    """Upload image to Instagram"""
    try:
        print(f"\n📸 Uploading image...")

        url = f'{GRAPH_API_URL}/{account_id}/media'

        data = {
            'image_url': image_url,
            'caption': caption,
            'access_token': access_token
        }

        response = requests.post(url, data=data)
        response.raise_for_status()

        media_id = response.json().get('id')
        print(f"✅ Media uploaded (ID: {media_id})")

        return media_id

    except Exception as e:
        print(f"❌ Error uploading: {e}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response.text}")
        return None


def publish_media(access_token, account_id, media_id):
    """Publish uploaded media"""
    try:
        print(f"\n📤 Publishing media...")

        url = f'{GRAPH_API_URL}/{account_id}/media_publish'

        data = {
            'creation_id': media_id,
            'access_token': access_token
        }

        response = requests.post(url, data=data)
        response.raise_for_status()

        post_id = response.json().get('id')
        print(f"✅ Post published! (ID: {post_id})")

        return post_id

    except Exception as e:
        print(f"❌ Error publishing: {e}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response.text}")
        return None


def post_to_instagram(caption, image_url):
    """Main function to post to Instagram"""
    print("\n" + "=" * 60)
    print("INSTAGRAM POSTER - API METHOD")
    print("=" * 60)

    access_token = INSTAGRAM_ACCESS_TOKEN
    account_id = INSTAGRAM_BUSINESS_ACCOUNT_ID

    # If no token, get it from user
    if not access_token:
        print("\n⚠️  No access token found in .env")
        access_token = get_access_token_from_browser()
        if not access_token:
            return False

    # If no account ID, fetch it
    if not account_id:
        print("\n⚠️  No account ID found in .env")
        account_id = get_business_account_id(access_token)
        if not account_id:
            return False

    # Upload image
    media_id = upload_image(access_token, account_id, image_url, caption)
    if not media_id:
        return False

    # Publish
    post_id = publish_media(access_token, account_id, media_id)
    if not post_id:
        return False

    print("\n" + "=" * 60)
    print("✅ POST SUCCESSFUL!")
    print("=" * 60)
    print(f"\n📱 Posted to: @{INSTAGRAM_USERNAME}")
    print(f"📝 Caption: {caption[:50]}...")
    print(f"🔗 Post ID: {post_id}")
    print("=" * 60 + "\n")

    return True


def setup_instagram_api():
    """Setup Instagram API credentials"""
    print("\n" + "=" * 60)
    print("INSTAGRAM API SETUP")
    print("=" * 60)

    print("\n📋 Steps to get credentials:")
    print("\n1. Go to Facebook Developers: https://developers.facebook.com/")
    print("2. Create an app (or use existing)")
    print("3. Add 'Instagram Graph API' product")
    print("4. Go to Settings → Basic")
    print("5. Copy App ID and App Secret")
    print("6. Add to .env:")
    print("   INSTAGRAM_APP_ID=your_app_id")
    print("   INSTAGRAM_APP_SECRET=your_app_secret")

    print("\n7. Then run this script to get access token")

    # Get token
    token = get_access_token_from_browser()
    if token:
        # Get account ID
        account_id = get_business_account_id(token)
        if account_id:
            print("\n✅ SETUP COMPLETE!")
            print("You can now post to Instagram")
            return True

    return False


if __name__ == '__main__':
    # Example usage
    caption = "🚀 AI Employee Vault - Automating business workflows!\n\n#AI #Automation #Business"
    image_url = "https://via.placeholder.com/1080x1080?text=AI+Employee+Vault"

    # First time: setup
    # setup_instagram_api()

    # Post
    post_to_instagram(caption, image_url)
