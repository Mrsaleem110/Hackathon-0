#!/usr/bin/env python3
"""
LinkedIn API Post - Fully Automated
Posts to company page using LinkedIn API
"""
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')

def get_company_id():
    """Get Agentic Sphere company ID"""
    # Known company ID for agentic-sphere
    # You can also get this from: https://www.linkedin.com/company/agentic-sphere/
    return "104038393"  # Agentic Sphere company ID

def post_to_company_page(message):
    """Post to LinkedIn company page using API"""

    if not LINKEDIN_ACCESS_TOKEN:
        print("Error: LINKEDIN_ACCESS_TOKEN not found in .env file")
        return False

    company_id = get_company_id()

    # LinkedIn API endpoint for company shares
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Post data
    post_data = {
        "author": f"urn:li:organization:{company_id}",
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

    print(f"\nPosting to Agentic Sphere LinkedIn page...")
    print(f"Message: {message}\n")

    try:
        response = requests.post(url, headers=headers, json=post_data)

        if response.status_code == 201:
            print("=" * 60)
            print("SUCCESS! Post published to LinkedIn!")
            print("=" * 60)
            print(f"\nCheck: https://www.linkedin.com/company/agentic-sphere/")
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

    post_to_company_page(message)
