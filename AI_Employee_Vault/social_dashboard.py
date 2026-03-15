#!/usr/bin/env python3
"""
Social Media Dashboard
Instagram + Facebook posts monitor karo real-time
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_section(title):
    print(f"\n📌 {title}")
    print("-"*70)

class SocialMediaDashboard:
    def __init__(self):
        self.log_dir = Path(__file__).parent / 'Logs'
        self.posts_file = Path(__file__).parent / 'social_posts.json'
        self.stats = {
            'instagram': {'total': 0, 'success': 0, 'failed': 0},
            'facebook': {'total': 0, 'success': 0, 'failed': 0}
        }

    def load_posts(self):
        """Load posts from JSON file"""
        if self.posts_file.exists():
            with open(self.posts_file, 'r') as f:
                return json.load(f)
        return {'instagram': [], 'facebook': []}

    def save_posts(self, posts):
        """Save posts to JSON file"""
        with open(self.posts_file, 'w') as f:
            json.dump(posts, f, indent=2)

    def add_post(self, platform, caption, status='pending', post_id=None):
        """Add a post record"""
        posts = self.load_posts()

        post = {
            'timestamp': datetime.utcnow().isoformat(),
            'caption': caption[:100],
            'status': status,
            'post_id': post_id
        }

        if platform.lower() == 'instagram':
            posts['instagram'].append(post)
        elif platform.lower() == 'facebook':
            posts['facebook'].append(post)

        self.save_posts(posts)

    def get_stats(self):
        """Calculate statistics"""
        posts = self.load_posts()

        stats = {
            'instagram': {
                'total': len(posts['instagram']),
                'success': len([p for p in posts['instagram'] if p['status'] == 'success']),
                'failed': len([p for p in posts['instagram'] if p['status'] == 'failed']),
                'pending': len([p for p in posts['instagram'] if p['status'] == 'pending'])
            },
            'facebook': {
                'total': len(posts['facebook']),
                'success': len([p for p in posts['facebook'] if p['status'] == 'success']),
                'failed': len([p for p in posts['facebook'] if p['status'] == 'failed']),
                'pending': len([p for p in posts['facebook'] if p['status'] == 'pending'])
            }
        }

        return stats

    def display_dashboard(self):
        """Display main dashboard"""
        print_header("SOCIAL MEDIA DASHBOARD")

        # Credentials status
        print_section("CREDENTIALS STATUS")
        self.display_credentials()

        # Statistics
        print_section("STATISTICS")
        self.display_stats()

        # Recent posts
        print_section("RECENT POSTS")
        self.display_recent_posts()

        # Quick actions
        print_section("QUICK ACTIONS")
        self.display_menu()

    def display_credentials(self):
        """Display credential status"""
        ig_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        ig_account = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        fb_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        fb_page = os.getenv('FACEBOOK_PAGE_ID')

        print("\n📱 Instagram:")
        if ig_token and not ig_token.startswith('IGAB_demo'):
            print(f"   ✅ Token: {ig_token[:20]}...")
        else:
            print(f"   ⏳ Token: Demo (setup karo)")

        if ig_account and ig_account != '17841400000000':
            print(f"   ✅ Account ID: {ig_account}")
        else:
            print(f"   ⏳ Account ID: Demo (setup karo)")

        print("\n📘 Facebook:")
        if fb_token and not fb_token.startswith('EAAB_demo'):
            print(f"   ✅ Token: {fb_token[:20]}...")
        else:
            print(f"   ⏳ Token: Demo (setup karo)")

        if fb_page and fb_page != '1048264368365205':
            print(f"   ✅ Page ID: {fb_page}")
        else:
            print(f"   ⏳ Page ID: Demo (setup karo)")

    def display_stats(self):
        """Display statistics"""
        stats = self.get_stats()

        print("\n📱 Instagram:")
        ig = stats['instagram']
        print(f"   Total Posts: {ig['total']}")
        print(f"   ✅ Success: {ig['success']}")
        print(f"   ❌ Failed: {ig['failed']}")
        print(f"   ⏳ Pending: {ig['pending']}")

        print("\n📘 Facebook:")
        fb = stats['facebook']
        print(f"   Total Posts: {fb['total']}")
        print(f"   ✅ Success: {fb['success']}")
        print(f"   ❌ Failed: {fb['failed']}")
        print(f"   ⏳ Pending: {fb['pending']}")

        total_success = ig['success'] + fb['success']
        total_posts = ig['total'] + fb['total']
        if total_posts > 0:
            success_rate = (total_success / total_posts) * 100
            print(f"\n📊 Overall Success Rate: {success_rate:.1f}%")

    def display_recent_posts(self):
        """Display recent posts"""
        posts = self.load_posts()

        all_posts = []
        for p in posts['instagram']:
            all_posts.append(('Instagram', p))
        for p in posts['facebook']:
            all_posts.append(('Facebook', p))

        # Sort by timestamp (newest first)
        all_posts.sort(key=lambda x: x[1]['timestamp'], reverse=True)

        if not all_posts:
            print("\nNo posts yet")
            return

        print("\nLast 5 posts:")
        for platform, post in all_posts[:5]:
            status_icon = '✅' if post['status'] == 'success' else '❌' if post['status'] == 'failed' else '⏳'
            timestamp = post['timestamp'][:10]
            caption = post['caption'][:40]
            print(f"\n{status_icon} {platform} ({timestamp})")
            print(f"   {caption}...")
            if post['post_id']:
                print(f"   ID: {post['post_id']}")

    def display_menu(self):
        """Display menu options"""
        print("""
1. Post to Instagram
2. Post to Facebook
3. Post to Both
4. View all posts
5. Clear stats
6. Setup credentials
7. Test credentials
8. Exit
        """)

    def view_all_posts(self):
        """View all posts"""
        posts = self.load_posts()

        print_section("ALL INSTAGRAM POSTS")
        for i, post in enumerate(posts['instagram'], 1):
            status = '✅' if post['status'] == 'success' else '❌' if post['status'] == 'failed' else '⏳'
            print(f"\n{i}. {status} {post['timestamp']}")
            print(f"   {post['caption']}")
            if post['post_id']:
                print(f"   ID: {post['post_id']}")

        print_section("ALL FACEBOOK POSTS")
        for i, post in enumerate(posts['facebook'], 1):
            status = '✅' if post['status'] == 'success' else '❌' if post['status'] == 'failed' else '⏳'
            print(f"\n{i}. {status} {post['timestamp']}")
            print(f"   {post['caption']}")
            if post['post_id']:
                print(f"   ID: {post['post_id']}")

    def post_to_instagram(self):
        """Post to Instagram"""
        caption = input("\n📝 Caption: ").strip()
        image_url = input("🖼️  Image URL: ").strip()

        if not caption:
            print("❌ Caption required")
            return

        self.add_post('instagram', caption, 'pending')

        try:
            from mcp_servers.instagram_mcp import InstagramClient
            ig = InstagramClient()
            result = ig.post_feed(caption, image_url if image_url else None)

            if result.get('success'):
                self.add_post('instagram', caption, 'success', result.get('post_id'))
                print(f"✅ Posted to Instagram!")
                print(f"   ID: {result.get('post_id')}")
            else:
                self.add_post('instagram', caption, 'failed')
                print(f"❌ Failed: {result.get('error')}")
        except Exception as e:
            self.add_post('instagram', caption, 'failed')
            print(f"❌ Error: {e}")

    def post_to_facebook(self):
        """Post to Facebook"""
        message = input("\n📝 Message: ").strip()
        link = input("🔗 Link (optional): ").strip()

        if not message:
            print("❌ Message required")
            return

        self.add_post('facebook', message, 'pending')

        try:
            from mcp_servers.facebook_mcp import FacebookClient
            fb = FacebookClient()
            result = fb.post_feed(message, link if link else None)

            if result.get('success'):
                self.add_post('facebook', message, 'success', result.get('post_id'))
                print(f"✅ Posted to Facebook!")
                print(f"   ID: {result.get('post_id')}")
            else:
                self.add_post('facebook', message, 'failed')
                print(f"❌ Failed: {result.get('error')}")
        except Exception as e:
            self.add_post('facebook', message, 'failed')
            print(f"❌ Error: {e}")

    def run(self):
        """Run dashboard"""
        while True:
            self.display_dashboard()

            choice = input("\n👉 Select option (1-8): ").strip()

            if choice == '1':
                self.post_to_instagram()
            elif choice == '2':
                self.post_to_facebook()
            elif choice == '3':
                self.post_to_instagram()
                self.post_to_facebook()
            elif choice == '4':
                self.view_all_posts()
            elif choice == '5':
                confirm = input("\n⚠️  Clear all stats? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.save_posts({'instagram': [], 'facebook': []})
                    print("✅ Stats cleared")
            elif choice == '6':
                os.system('python setup_insta_fb.py')
            elif choice == '7':
                os.system('python test_insta_fb.py')
            elif choice == '8':
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid option")

            input("\nPress Enter to continue...")

if __name__ == '__main__':
    try:
        dashboard = SocialMediaDashboard()
        dashboard.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
