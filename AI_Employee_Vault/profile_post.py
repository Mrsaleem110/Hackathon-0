#!/usr/bin/env python3
"""
LinkedIn API Post - Personal Profile
Posts to personal profile using new LinkedIn API
"""
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')

def post_to_profile(message):
    """Post to personal LinkedIn profile using new API"""

    if not LINKEDIN_ACCESS_TOKEN:
        print("Error: LINKEDIN_ACCESS_TOKEN not found")
        return False

    # New LinkedIn API endpoint
    url = "https://api.linkedin.com/rest/posts"

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Add version as query parameter instead
    url = "https://api.linkedin.com/rest/posts?linkedin-version=202401"
    post_data = {
        "author": "urn:li:person:CURRENT",  # Current authenticated user
        "commentary": message,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    print(f"\nPosting to LinkedIn...")
    print(f"Message: {message}\n")

    try:
        response = requests.post(url, headers=headers, json=post_data)

        if response.status_code in [200, 201]:
            print("=" * 60)
            print("SUCCESS! Post published to LinkedIn!")
            print("=" * 60)
            return True
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = "Hello from AgenticSphere"

    post_to_profile(message)
