#!/usr/bin/env python3
"""
LinkedIn API - Get Organization ID
Fetches the correct organization ID for Agentic Sphere
"""
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')

def get_organization_id():
    """Get organization ID from LinkedIn API"""

    if not LINKEDIN_ACCESS_TOKEN:
        print("ERROR: LINKEDIN_ACCESS_TOKEN not found")
        return None

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    print("=" * 70)
    print("LinkedIn API - Get Organization ID")
    print("=" * 70)
    print()

    # Try to get user's organizations
    endpoints = [
        ("https://api.linkedin.com/v2/me", "User Info"),
        ("https://api.linkedin.com/v2/organizationalEntityAcls", "Organization ACLs"),
        ("https://api.linkedin.com/v2/adAccountsForUser", "Ad Accounts"),
    ]

    for endpoint, name in endpoints:
        print(f"Trying: {name}")
        print(f"URL: {endpoint}")
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)[:500]}")
                print()
                return data
            else:
                print(f"Error: {response.text[:200]}")
                print()
        except Exception as e:
            print(f"Exception: {e}")
            print()

    print("\nTo find your organization ID:")
    print("1. Go to: https://www.linkedin.com/developers/apps")
    print("2. Select your app")
    print("3. Go to 'Auth' tab")
    print("4. Look for 'Authorized organizations'")
    print("5. Or go to: https://www.linkedin.com/company/agentic-sphere/admin/")
    print("6. Check the URL - organization ID is in the URL")

if __name__ == '__main__':
    get_organization_id()
