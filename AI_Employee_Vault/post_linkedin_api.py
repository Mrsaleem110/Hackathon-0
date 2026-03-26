#!/usr/bin/env python3
"""
LinkedIn API Direct Post - Using Access Token
Posts directly to Agentic Sphere company page
"""
import requests
import json
from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')
LINKEDIN_ORG_ID = '95234567'  # Agentic Sphere organization ID

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

def post_to_linkedin_api():
    """Post to LinkedIn using official API"""

    if not LINKEDIN_ACCESS_TOKEN:
        print("ERROR: LINKEDIN_ACCESS_TOKEN not found in .env")
        return False

    print("=" * 70)
    print("LinkedIn API - Direct Post to Agentic Sphere")
    print("=" * 70)
    print()

    # LinkedIn API endpoint for organization posts
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Payload for text post
    payload = {
        "author": f"urn:li:organization:{LINKEDIN_ORG_ID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": POST_TEXT
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    try:
        print("Sending post to LinkedIn API...")
        print(f"Organization ID: {LINKEDIN_ORG_ID}")
        print(f"Post text length: {len(POST_TEXT)} characters")
        print()

        response = requests.post(url, json=payload, headers=headers, timeout=30)

        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print()

        if response.status_code == 201:
            result = response.json()
            post_id = result.get('id', 'unknown')
            print("=" * 70)
            print("SUCCESS! Post published to LinkedIn!")
            print("=" * 70)
            print(f"Post ID: {post_id}")
            print(f"URL: https://www.linkedin.com/company/agentic-sphere/")
            print()

            # Log the success
            log_file = Path('Logs/2026-03-06.json')
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'linkedin_post_published',
                'post_title': 'Agentic Sphere - Your Personal AI Employee',
                'status': 'success',
                'platform': 'linkedin',
                'post_id': post_id,
                'method': 'linkedin_api'
            }

            try:
                if log_file.exists():
                    logs = json.loads(log_file.read_text())
                else:
                    logs = []
                logs.append(log_entry)
                log_file.write_text(json.dumps(logs, indent=2))
                print("Logged to vault successfully")
            except Exception as e:
                print(f"Warning: Could not log to vault: {e}")

            return True

        elif response.status_code == 400:
            print("ERROR: Bad Request")
            print(f"Response: {response.text}")
            print()
            print("Possible issues:")
            print("- Invalid organization ID")
            print("- Invalid access token")
            print("- Missing required fields")
            return False

        elif response.status_code == 401:
            print("ERROR: Unauthorized")
            print("Access token is invalid or expired")
            print("Please check your LINKEDIN_ACCESS_TOKEN in .env")
            return False

        elif response.status_code == 403:
            print("ERROR: Forbidden")
            print("You don't have permission to post to this organization")
            return False

        else:
            print(f"ERROR: Unexpected status code {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("ERROR: Request timeout - LinkedIn API not responding")
        return False

    except requests.exceptions.ConnectionError:
        print("ERROR: Connection error - check your internet connection")
        return False

    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == '__main__':
    success = post_to_linkedin_api()
    exit(0 if success else 1)
