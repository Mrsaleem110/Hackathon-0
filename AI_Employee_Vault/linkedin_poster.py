#!/usr/bin/env python3
"""
Universal LinkedIn Poster - Post to LinkedIn directly
Posts content to your LinkedIn page/profile
"""

import requests
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class LinkedInPoster:
    def __init__(self):
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')

        if not self.access_token:
            print("Error: LINKEDIN_ACCESS_TOKEN not found in .env")
            self.access_token = None

        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }

    def get_profile_id(self):
        """Get your LinkedIn profile ID"""
        try:
            url = f"{self.base_url}/me"
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                profile_id = data.get('id')
                return profile_id
            else:
                print(f"Error getting profile: {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def post_to_linkedin(self, content):
        """Post content to LinkedIn"""
        try:
            # Get profile ID
            profile_id = self.get_profile_id()
            if not profile_id:
                print("Could not get profile ID")
                return False

            # Create post
            url = f"{self.base_url}/ugcPosts"

            payload = {
                "author": f"urn:li:person:{profile_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            response = requests.post(url, headers=self.headers, json=payload)

            if response.status_code == 201:
                data = response.json()
                post_id = data.get('id')

                print("\n" + "="*60)
                print("SUCCESS - LinkedIn Post Published!")
                print("="*60)
                print(f"Post ID: {post_id}")
                print(f"Content: {content[:100]}...")
                print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("="*60 + "\n")

                # Log the post
                self.log_post(post_id, content)
                return True
            else:
                print(f"Error posting to LinkedIn: {response.status_code}")
                print(response.text)
                return False

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return False

    def log_post(self, post_id, content):
        """Log the LinkedIn post"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'platform': 'linkedin',
                'post_id': post_id,
                'content': content[:200],
                'status': 'published'
            }

            log_file = Path('Logs/linkedin_posts_log.json')
            log_file.parent.mkdir(parents=True, exist_ok=True)

            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []

            logs.append(log_entry)

            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)

        except Exception as e:
            print(f"Error logging post: {e}")

def post_to_linkedin(content):
    """Post content to LinkedIn"""
    poster = LinkedInPoster()

    if not poster.access_token:
        print("Error: LinkedIn credentials not configured")
        return False

    return poster.post_to_linkedin(content)

def interactive_linkedin_poster():
    """Interactive mode - ask user for post content"""

    print("\n" + "="*60)
    print("LINKEDIN POSTER")
    print("="*60)

    print("\nLinkedIn par kya post karna hai?")
    print("(Enter ke baad Ctrl+D ya Ctrl+Z dabao jab khatam ho):")
    print()

    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    content = '\n'.join(lines).strip()
    if not content:
        print("Error: Post content required")
        return False

    # Confirm before posting
    print("\n" + "-"*60)
    print("Post Content:")
    print(content)
    print("-"*60)

    confirm = input("\nKya LinkedIn par post karna hai? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y', 'haan', 'ha']:
        print("Post cancelled.")
        return False

    # Post to LinkedIn
    return post_to_linkedin(content)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == '--help':
            print("Usage:")
            print("  Interactive mode: python linkedin_poster.py")
            print("  Direct mode: python linkedin_poster.py 'Your post content here'")
            print("\nExample:")
            print("  python linkedin_poster.py 'Hello LinkedIn! This is my first post.'")
        else:
            content = ' '.join(sys.argv[1:])
            post_to_linkedin(content)
    else:
        # Interactive mode
        interactive_linkedin_poster()
