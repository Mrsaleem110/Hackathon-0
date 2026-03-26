#!/usr/bin/env python3
"""
Get Agentic Sphere Organization ID from LinkedIn API
"""
import requests
import json

LINKEDIN_ACCESS_TOKEN = "AQWJ1GVoB_wg5FteqXtXNLJSQDOtGVU7v7a7CbqMvnat8RCCcEe34Mg7LXCVfOmjYehTPZJspKfDGiVsJojwJJ17fbxE6_7ODFfTtU2gd7PpIOg106_V6prNtTrcc8rmSLXaXJ05ROJqHrqxA4tdwYMgF0OwQZOsVl__BV7sLGNXM1eZdkEOFlsWGDbYnPHXQ9IVqtGRRkbDyqkMQnI8ko6WEcmfsSglqE_uXCR36PN0fAvPaj-ix6QN1NTcGRL7fuO9FvK63JFe96-WfPFbcDGUS42b8Rf0qIfgJ8UyQMKTWO_s-bm1_EOhikFJs46lU30VWV6CspLeRLabiOLHOo9ika4cyA"

def get_org_id():
    """Get organization ID for Agentic Sphere"""

    print("Fetching Agentic Sphere organization ID...")

    # Get user's organizations
    url = "https://api.linkedin.com/v2/me"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"User info status: {response.status_code}")

        if response.status_code == 200:
            user_data = response.json()
            print(f"User ID: {user_data.get('id')}")

            # Now get admin organizations
            admin_url = "https://api.linkedin.com/v2/organizationalEntityAcls?q=roleAssignee"
            response = requests.get(admin_url, headers=headers, timeout=10)
            print(f"Admin orgs status: {response.status_code}")

            if response.status_code == 200:
                orgs = response.json()
                print(json.dumps(orgs, indent=2))

                # Extract org IDs
                if 'elements' in orgs:
                    for org in orgs['elements']:
                        org_id = org.get('organizationalTarget', '').split(':')[-1]
                        print(f"Found org ID: {org_id}")
            else:
                print(f"Error: {response.text}")
        else:
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    get_org_id()
