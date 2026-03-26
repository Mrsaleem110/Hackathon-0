#!/usr/bin/env python3
"""
LinkedIn Personal Profile Post
"""
import requests
import json
from pathlib import Path
from datetime import datetime

LINKEDIN_ACCESS_TOKEN = "AQWJ1GVoB_wg5FteqXtXNLJSQDOtGVU7v7a7CbqMvnat8RCCcEe34Mg7LXCVfOmjYehTPZJspKfDGiVsJojwJJ17fbxE6_7ODFfTtU2gd7PpIOg106_V6prNtTrcc8rmSLXaXJ05ROJqHrqxA4tdwYMgF0OwQZOsVl__BV7sLGNXM1eZdkEOFlsWGDbYnPHXQ9IVqtGRRkbDyqkMQnI8ko6WEcmfsSglqE_uXCR36PN0fAvPaj-ix6QN1NTcGRL7fuO9FvK63JFe96-WfPFbcDGUS42b8Rf0qIfgJ8UyQMKTWO_s-bm1_EOhikFJs46lU30VWV6CspLeRLabiOLHOo9ika4cyA"

POST_TEXT = """🚀 Introducing Agentic Sphere

Your autonomous AI employee that works 24/7.

Agentic Sphere monitors your emails, messages, and opportunities - then takes intelligent action with your approval.

✓ Autonomous Decision Making
✓ Multi-Channel Integration (Gmail, WhatsApp, LinkedIn)
✓ Intelligent Planning with Claude AI
✓ Complete Audit Trail
✓ Human-in-the-Loop Control

The future of productivity is here.

#AI #Automation #AgenticSphere #FutureOfWork #Innovation"""

def post_to_profile():
    """Post to personal profile"""

    print("=" * 70)
    print("LinkedIn - Post to Personal Profile")
    print("=" * 70)
    print()

    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Post to personal profile (no author specified = current user)
    payload = {
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
        print(f"Post text length: {len(POST_TEXT)} characters")
        print()

        response = requests.post(url, json=payload, headers=headers, timeout=30)

        print(f"Response Status: {response.status_code}")

        if response.status_code == 201:
            result = response.json()
            post_id = result.get('id', 'unknown')
            print()
            print("=" * 70)
            print("✅ SUCCESS! Post published to your profile!")
            print("=" * 70)
            print(f"Post ID: {post_id}")
            print()

            # Log the success
            log_file = Path('Logs/2026-03-06.json')
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'linkedin_post_published',
                'post_title': 'Agentic Sphere Introduction',
                'status': 'success',
                'platform': 'linkedin',
                'post_id': post_id,
                'method': 'linkedin_api_personal'
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

        else:
            print(f"ERROR: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == '__main__':
    success = post_to_profile()
    exit(0 if success else 1)
