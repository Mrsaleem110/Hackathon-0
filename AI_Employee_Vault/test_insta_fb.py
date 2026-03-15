#!/usr/bin/env python3
"""
Test Instagram + Facebook Integration
Verify ke credentials sahi hain aur posting kaam kar rahi hai
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_section(title):
    print(f"\n📌 {title}")
    print("-"*70)

def print_success(msg):
    print(f"✅ {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def print_warning(msg):
    print(f"⚠️  {msg}")

def print_info(msg):
    print(f"ℹ️  {msg}")

class SocialMediaTester:
    def __init__(self):
        self.results = {
            'instagram': {},
            'facebook': {},
            'timestamp': datetime.utcnow().isoformat()
        }

    def test_instagram_credentials(self):
        """Test Instagram credentials"""
        print_section("INSTAGRAM CREDENTIALS TEST")

        token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')

        print(f"Access Token: {token[:20] if token else 'NOT SET'}...")
        print(f"Account ID: {account_id if account_id else 'NOT SET'}")

        if not token or not account_id:
            print_error("Instagram credentials missing!")
            self.results['instagram']['credentials'] = False
            return False

        if token.startswith('IGAB_demo') or token.startswith('demo_'):
            print_warning("Demo token detected - replace with real token")
            self.results['instagram']['credentials'] = 'demo'
            return False

        print_success("Instagram credentials found")
        self.results['instagram']['credentials'] = True
        return True

    def test_facebook_credentials(self):
        """Test Facebook credentials"""
        print_section("FACEBOOK CREDENTIALS TEST")

        token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        page_id = os.getenv('FACEBOOK_PAGE_ID')

        print(f"Access Token: {token[:20] if token else 'NOT SET'}...")
        print(f"Page ID: {page_id if page_id else 'NOT SET'}")

        if not token or not page_id:
            print_error("Facebook credentials missing!")
            self.results['facebook']['credentials'] = False
            return False

        if token.startswith('EAAB_demo') or token.startswith('demo_'):
            print_warning("Demo token detected - replace with real token")
            self.results['facebook']['credentials'] = 'demo'
            return False

        print_success("Facebook credentials found")
        self.results['facebook']['credentials'] = True
        return True

    def test_instagram_client(self):
        """Test Instagram client initialization"""
        print_section("INSTAGRAM CLIENT TEST")

        try:
            from mcp_servers.instagram_mcp import InstagramClient

            # Test with dry_run=True first
            ig = InstagramClient(dry_run=True)
            print_success("Instagram client initialized (dry-run mode)")

            # Test dry-run post
            result = ig.post_feed(
                caption="Test post from AI Employee Vault",
                image_url="https://via.placeholder.com/1080x1080"
            )

            if result.get('success'):
                print_success("Dry-run post successful")
                print_info(f"Post ID: {result.get('post_id')}")
                self.results['instagram']['client'] = True
                return True
            else:
                print_error(f"Dry-run failed: {result.get('error')}")
                self.results['instagram']['client'] = False
                return False

        except Exception as e:
            print_error(f"Instagram client error: {e}")
            self.results['instagram']['client'] = False
            return False

    def test_facebook_client(self):
        """Test Facebook client initialization"""
        print_section("FACEBOOK CLIENT TEST")

        try:
            from mcp_servers.facebook_mcp import FacebookClient

            # Test with dry_run=True first
            fb = FacebookClient(dry_run=True)
            print_success("Facebook client initialized (dry-run mode)")

            # Test dry-run post
            result = fb.post_feed(
                message="Test post from AI Employee Vault",
                link="https://example.com"
            )

            if result.get('success'):
                print_success("Dry-run post successful")
                print_info(f"Post ID: {result.get('post_id')}")
                self.results['facebook']['client'] = True
                return True
            else:
                print_error(f"Dry-run failed: {result.get('error')}")
                self.results['facebook']['client'] = False
                return False

        except Exception as e:
            print_error(f"Facebook client error: {e}")
            self.results['facebook']['client'] = False
            return False

    def test_instagram_live(self):
        """Test live Instagram posting (if credentials are real)"""
        print_section("INSTAGRAM LIVE TEST")

        token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        if token.startswith('IGAB_demo') or token.startswith('demo_'):
            print_warning("Skipping live test - demo token detected")
            print_info("Replace token with real credentials to test live posting")
            self.results['instagram']['live'] = 'skipped'
            return None

        try:
            from mcp_servers.instagram_mcp import InstagramClient

            ig = InstagramClient(dry_run=False)
            result = ig.post_feed(
                caption="🤖 Test post from AI Employee Vault - Instagram",
                image_url="https://via.placeholder.com/1080x1080"
            )

            if result.get('success'):
                print_success("Live Instagram post successful!")
                print_info(f"Post ID: {result.get('post_id')}")
                self.results['instagram']['live'] = True
                return True
            else:
                print_error(f"Live post failed: {result.get('error')}")
                self.results['instagram']['live'] = False
                return False

        except Exception as e:
            print_error(f"Live test error: {e}")
            self.results['instagram']['live'] = False
            return False

    def test_facebook_live(self):
        """Test live Facebook posting (if credentials are real)"""
        print_section("FACEBOOK LIVE TEST")

        token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        if token.startswith('EAAB_demo') or token.startswith('demo_'):
            print_warning("Skipping live test - demo token detected")
            print_info("Replace token with real credentials to test live posting")
            self.results['facebook']['live'] = 'skipped'
            return None

        try:
            from mcp_servers.facebook_mcp import FacebookClient

            fb = FacebookClient(dry_run=False)
            result = fb.post_feed(
                message="🤖 Test post from AI Employee Vault - Facebook",
                link="https://example.com"
            )

            if result.get('success'):
                print_success("Live Facebook post successful!")
                print_info(f"Post ID: {result.get('post_id')}")
                self.results['facebook']['live'] = True
                return True
            else:
                print_error(f"Live post failed: {result.get('error')}")
                self.results['facebook']['live'] = False
                return False

        except Exception as e:
            print_error(f"Live test error: {e}")
            self.results['facebook']['live'] = False
            return False

    def save_results(self):
        """Save test results to file"""
        results_file = Path(__file__).parent / 'Logs' / 'test_results.json'
        results_file.parent.mkdir(parents=True, exist_ok=True)

        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print_info(f"Results saved to {results_file}")

    def print_summary(self):
        """Print test summary"""
        print_section("TEST SUMMARY")

        instagram_ok = self.results['instagram'].get('credentials') and self.results['instagram'].get('client')
        facebook_ok = self.results['facebook'].get('credentials') and self.results['facebook'].get('client')

        print(f"\n📱 Instagram:")
        print(f"   Credentials: {'✅' if self.results['instagram'].get('credentials') else '❌'}")
        print(f"   Client: {'✅' if self.results['instagram'].get('client') else '❌'}")
        print(f"   Live: {'✅' if self.results['instagram'].get('live') == True else '⏳' if self.results['instagram'].get('live') == 'skipped' else '❌'}")

        print(f"\n📘 Facebook:")
        print(f"   Credentials: {'✅' if self.results['facebook'].get('credentials') else '❌'}")
        print(f"   Client: {'✅' if self.results['facebook'].get('client') else '❌'}")
        print(f"   Live: {'✅' if self.results['facebook'].get('live') == True else '⏳' if self.results['facebook'].get('live') == 'skipped' else '❌'}")

        if instagram_ok and facebook_ok:
            print_success("\n✅ All tests passed! Ready to post!")
        else:
            print_warning("\n⚠️  Some tests failed - check credentials")

def main():
    print_header("INSTAGRAM + FACEBOOK TEST SUITE")

    tester = SocialMediaTester()

    # Test credentials
    ig_creds = tester.test_instagram_credentials()
    fb_creds = tester.test_facebook_credentials()

    # Test clients
    if ig_creds:
        tester.test_instagram_client()

    if fb_creds:
        tester.test_facebook_client()

    # Test live (optional)
    print_section("LIVE POSTING TEST")
    print("Yeh optional hai - demo tokens ke saath skip hoga")

    response = input("\nLive posting test karo? (y/n): ").strip().lower()
    if response == 'y':
        if ig_creds:
            tester.test_instagram_live()
        if fb_creds:
            tester.test_facebook_live()

    # Save and print results
    tester.save_results()
    tester.print_summary()

    # Next steps
    print_section("NEXT STEPS")
    if ig_creds and fb_creds:
        print("""
✅ Credentials sahi hain!

Ab ye kar sakte ho:
1. python auto_post_social.py - Interactive posting
2. python orchestrator.py - Automated posting
3. Check logs: tail -f Logs/2026-03-15.json
        """)
    else:
        print("""
❌ Credentials update karo:
1. python setup_insta_fb.py
2. Real tokens add karo (demo tokens nahi)
3. Phir se test karo: python test_insta_fb.py
        """)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Test cancelled")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
