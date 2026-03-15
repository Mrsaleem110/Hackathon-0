#!/usr/bin/env python3
"""
Auto-Post to Instagram + Facebook
Tumhara content automatically post hoga
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_section(title):
    print(f"\n📌 {title}")
    print("-"*70)

class SocialMediaPoster:
    def __init__(self):
        self.instagram_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.instagram_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        self.facebook_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.facebook_page_id = os.getenv('FACEBOOK_PAGE_ID')

    def validate_credentials(self):
        """Check if credentials are set"""
        print_section("CREDENTIAL CHECK")

        checks = {
            'Instagram Access Token': self.instagram_token,
            'Instagram Account ID': self.instagram_account_id,
            'Facebook Access Token': self.facebook_token,
            'Facebook Page ID': self.facebook_page_id
        }

        all_valid = True
        for name, value in checks.items():
            if value and not value.startswith('demo_') and not value.startswith('IGAB_demo') and not value.startswith('EAAB_demo'):
                print(f"✅ {name}: Valid")
            else:
                print(f"❌ {name}: Invalid or demo token")
                all_valid = False

        return all_valid

    def post_to_instagram(self, caption, image_url=None):
        """Post to Instagram"""
        try:
            from mcp_servers.instagram_mcp import InstagramClient

            ig = InstagramClient(dry_run=False)
            result = ig.post_feed(caption=caption, image_url=image_url)

            if result.get('success'):
                print(f"✅ Instagram post successful!")
                print(f"   Post ID: {result.get('post_id')}")
                return True
            else:
                print(f"❌ Instagram post failed: {result.get('error')}")
                return False
        except Exception as e:
            print(f"❌ Instagram error: {e}")
            return False

    def post_to_facebook(self, message, link=None):
        """Post to Facebook"""
        try:
            from mcp_servers.facebook_mcp import FacebookClient

            fb = FacebookClient(dry_run=False)
            result = fb.post_feed(message=message, link=link)

            if result.get('success'):
                print(f"✅ Facebook post successful!")
                print(f"   Post ID: {result.get('post_id')}")
                return True
            else:
                print(f"❌ Facebook post failed: {result.get('error')}")
                return False
        except Exception as e:
            print(f"❌ Facebook error: {e}")
            return False

    def post_to_both(self, caption, message=None, image_url=None, link=None):
        """Post to both Instagram and Facebook"""
        print_section("POSTING TO SOCIAL MEDIA")

        results = {
            'instagram': False,
            'facebook': False
        }

        # Post to Instagram
        print("\n📱 Instagram par post kar rahe hain...")
        if image_url:
            results['instagram'] = self.post_to_instagram(caption, image_url)
        else:
            print("⏭️  Instagram skip (image URL chahiye)")

        # Post to Facebook
        print("\n📘 Facebook par post kar rahe hain...")
        if message:
            results['facebook'] = self.post_to_facebook(message, link)
        else:
            results['facebook'] = self.post_to_facebook(caption, link)

        return results

def interactive_mode():
    """Interactive posting"""
    print_header("INTERACTIVE SOCIAL MEDIA POSTING")

    poster = SocialMediaPoster()

    if not poster.validate_credentials():
        print("\n⚠️  Credentials set nahi hain!")
        print("Pehle setup_insta_fb.py run karo")
        return False

    print_section("POST CONTENT")

    caption = input("\n📝 Instagram caption enter karo: ").strip()
    image_url = input("🖼️  Image URL (optional): ").strip() or None

    message = input("\n📝 Facebook message enter karo (ya Instagram caption use hoga): ").strip() or caption
    link = input("🔗 Facebook link (optional): ").strip() or None

    if not caption and not message:
        print("❌ Kuch content enter karo!")
        return False

    # Confirm
    print_section("CONFIRMATION")
    print(f"\n📱 Instagram: {caption[:50]}...")
    if image_url:
        print(f"   Image: {image_url}")
    print(f"\n📘 Facebook: {message[:50]}...")
    if link:
        print(f"   Link: {link}")

    confirm = input("\n✅ Post karo? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return False

    # Post
    results = poster.post_to_both(caption, message, image_url, link)

    # Summary
    print_section("SUMMARY")
    print(f"Instagram: {'✅ Success' if results['instagram'] else '❌ Failed'}")
    print(f"Facebook: {'✅ Success' if results['facebook'] else '❌ Failed'}")

    return True

def batch_mode(content_file):
    """Post from file"""
    print_header("BATCH POSTING FROM FILE")

    if not Path(content_file).exists():
        print(f"❌ File nahi mila: {content_file}")
        return False

    poster = SocialMediaPoster()

    if not poster.validate_credentials():
        print("\n⚠️  Credentials set nahi hain!")
        return False

    # Read content
    with open(content_file, 'r') as f:
        lines = f.readlines()

    print(f"📄 {len(lines)} posts process honge")

    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        print(f"\n[{i}] {line[:50]}...")
        poster.post_to_both(line)

    return True

def main():
    if len(sys.argv) > 1:
        # Batch mode
        batch_mode(sys.argv[1])
    else:
        # Interactive mode
        interactive_mode()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)
