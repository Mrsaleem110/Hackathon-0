#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post to LinkedIn using API directly
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def post_to_linkedin_api(message):
    """Post to LinkedIn using API"""

    print("=" * 60)
    print("Posting to LinkedIn via API")
    print("=" * 60)
    print(f"\nMessage:\n{message}\n")

    # Get credentials from .env
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')

    if not access_token:
        print("❌ No LinkedIn access token found in .env")
        return False

    print(f"✓ Found access token: {access_token[:20]}...")

    # LinkedIn API endpoint for posts
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    # Prepare the post payload
    payload = {
        "author": "urn:li:organization:ORGANIZATION_ID",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    try:
        print("Sending POST request to LinkedIn API...")
        response = requests.post(url, headers=headers, json=payload)

        print(f"Response Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code in [200, 201]:
            print("\n" + "="*60)
            print("✅ SUCCESS! POST PUBLISHED TO LINKEDIN!")
            print("="*60)
            return True
        else:
            print(f"❌ Failed to post: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    message = """🤖 Automation: The Future of Work

Automation is revolutionizing how businesses operate. At Agentic Sphere, we're building intelligent systems that:

✅ Handle repetitive tasks automatically
✅ Improve operational efficiency
✅ Reduce human error
✅ Free up teams for strategic work

From email management to social media posting to customer communication, automation enables businesses to scale without scaling headcount.

The future isn't about replacing people—it's about empowering them with smarter tools.

#Automation #AI #BusinessEfficiency #FutureOfWork"""

    post_to_linkedin_api(message)
