#!/usr/bin/env python3
"""
LinkedIn Share API - Direct Post
Using LinkedIn's Share endpoint which requires fewer permissions
"""
import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from pathlib import Path

load_dotenv()

LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')

POST_TEXT = """🤖 Meet Agentic Sphere - Your Personal AI Employee

Autonomous. Intelligent. Always Working.

Your AI employee monitors your emails, messages, and opportunities 24/7 - then takes intelligent action with your approval.

What makes Agentic Sphere different:
✓ 24/7 Autonomous Operation - Never miss an opportunity
✓ Multi-Channel Integration - Gmail, WhatsApp, LinkedIn all connected
✓ Intelligent Decision Making - Powered by Claude AI
✓ Complete Audit Trail - Full transparency on every action
✓ Human-in-the-Loop Control - You stay in charge

From detecting client inquiries to scheduling meetings, Agentic Sphere handles it all intelligently.

The future of productivity is here.

#AI #Automation #AgenticSphere #ArtificialIntelligence #Productivity #FutureOfWork #BusinessAutomation"""

def post_with_share_api():
    """Post using LinkedIn Share API"""

    if not LINKEDIN_ACCESS_TOKEN:
        print("ERROR: LINKEDIN_ACCESS_TOKEN not found in .env")
        return False

    print("=" * 70)
    print("LinkedIn Share API - Direct Post")
    print("=" * 70)
    print()

    # LinkedIn Share API endpoint
    url = "https://api.linkedin.com/v2/shares"

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Payload for share
    payload = {
        "owner": "urn:li:person:YOUR_PERSON_ID",  # Will be replaced
        "text": {
            "text": POST_TEXT
        },
        "distribution": {
            "linkedInDistributionTarget": {}
        }
    }

    try:
        print("Method 1: Trying Share API with person URN...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")

        if response.status_code in [201, 200]:
            print("SUCCESS!")
            print(response.json())
            return True
        else:
            print(f"Response: {response.text[:300]}")
            print()

    except Exception as e:
        print(f"Error: {e}")

    # Try alternative - get person ID first
    print("\nMethod 2: Getting person ID first...")
    try:
        me_url = "https://api.linkedin.com/v2/me"
        response = requests.get(me_url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            user_data = response.json()
            person_id = user_data.get('id')
            print(f"Person ID: {person_id}")

            if person_id:
                payload["owner"] = f"urn:li:person:{person_id}"
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                print(f"Post Status: {response.status_code}")

                if response.status_code in [201, 200]:
                    print("SUCCESS!")
                    result = response.json()
                    print(f"Post ID: {result.get('id')}")
                    return True
                else:
                    print(f"Response: {response.text[:300]}")
        else:
            print(f"Error getting person ID: {response.text[:200]}")

    except Exception as e:
        print(f"Error: {e}")

    return False

if __name__ == '__main__':
    success = post_with_share_api()
    exit(0 if success else 1)
