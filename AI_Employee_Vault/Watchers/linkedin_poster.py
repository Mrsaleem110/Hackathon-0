"""
LinkedIn Poster for AI Employee Vault
Automatically posts business updates to LinkedIn to generate sales
Supports scheduling and approval workflow
"""

import time
import logging
from pathlib import Path
from datetime import datetime
import json

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logging.warning("Playwright not installed. Install with: pip install playwright")


class LinkedInPoster:
    """Post business updates to LinkedIn"""

    def __init__(self, vault_path: str, session_path: str = None):
        self.vault_path = Path(vault_path)
        self.session_path = Path(session_path) if session_path else Path(vault_path) / '.linkedin_session'
        self.business_updates = self.vault_path / 'Business_Updates'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.logs = self.vault_path / 'Logs'

        # Create directories
        self.business_updates.mkdir(exist_ok=True)
        self.pending_approval.mkdir(exist_ok=True)
        self.logs.mkdir(exist_ok=True)
        self.session_path.mkdir(exist_ok=True)

        # Set up logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        if not PLAYWRIGHT_AVAILABLE:
            self.logger.warning("Playwright not available - running in demo mode only")

    def check_for_approved_posts(self) -> list:
        """Check Pending_Approval folder for approved LinkedIn posts"""
        approved_folder = self.pending_approval / 'Approved'
        approved_folder.mkdir(exist_ok=True)

        approved_posts = []
        for file in approved_folder.glob('LINKEDIN_POST_*.md'):
            try:
                content = file.read_text(encoding='utf-8')
                approved_posts.append({
                    'file': file,
                    'content': content
                })
            except Exception as e:
                self.logger.error(f"Error reading approved post: {e}")

        return approved_posts

    def extract_post_content(self, markdown_content: str) -> dict:
        """Extract post content from markdown file"""
        lines = markdown_content.split('\n')
        post_data = {
            'title': '',
            'content': '',
            'hashtags': [],
            'image_url': None
        }

        in_content = False
        for line in lines:
            if line.startswith('## Title'):
                in_content = True
                continue
            if line.startswith('## Content'):
                in_content = True
                continue
            if line.startswith('## Hashtags'):
                in_content = False
                continue
            if line.startswith('## Image'):
                in_content = False
                continue

            if in_content and line.strip():
                if not post_data['title'] and not line.startswith('#'):
                    post_data['title'] = line.strip()
                elif post_data['title']:
                    post_data['content'] += line + '\n'

            if 'hashtag' in line.lower():
                hashtag = line.strip().lstrip('- ').strip()
                if hashtag.startswith('#'):
                    post_data['hashtags'].append(hashtag)

        return post_data

    def post_to_linkedin(self, post_content: str) -> bool:
        """Post content to LinkedIn using Playwright"""
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.warning("Playwright not available - skipping actual post")
            return False

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    viewport={'width': 1280, 'height': 720}
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                try:
                    page.goto('https://www.linkedin.com/feed/', timeout=10000)
                    page.wait_for_selector('[data-testid="share-box"]', timeout=5000)

                    # Click on share box
                    share_box = page.query_selector('[data-testid="share-box"]')
                    if share_box:
                        share_box.click()
                        page.wait_for_selector('[data-testid="post-editor"]', timeout=5000)

                        # Type content
                        editor = page.query_selector('[data-testid="post-editor"]')
                        if editor:
                            editor.fill(post_content)

                            # Click post button
                            post_button = page.query_selector('[data-testid="post-button"]')
                            if post_button:
                                post_button.click()
                                page.wait_for_timeout(2000)

                                self.logger.info("Post published successfully to LinkedIn")
                                return True

                except Exception as e:
                    self.logger.error(f"Error posting to LinkedIn: {e}")
                    return False
                finally:
                    browser.close()

        except Exception as e:
            self.logger.error(f"Error in post_to_linkedin: {e}")
            return False

    def create_approval_request(self, post_content: str, filename: str) -> Path:
        """Create approval request file for LinkedIn post"""
        approval_file = self.pending_approval / f"LINKEDIN_POST_{filename}.md"

        content = f"""---
type: linkedin_post_approval
created: {datetime.now().isoformat()}
status: pending_approval
expires: {datetime.now().isoformat()}
---

## LinkedIn Post for Approval

{post_content}

## To Approve
Move this file to `/Pending_Approval/Approved/` folder to publish.

## To Reject
Move this file to `/Pending_Approval/Rejected/` folder to cancel.

## Post Metadata
- Created: {datetime.now().isoformat()}
- Type: Business Update
- Platform: LinkedIn
"""

        try:
            approval_file.write_text(content, encoding='utf-8')
            self.logger.info(f"Created approval request: {approval_file}")
        except Exception as e:
            self.logger.error(f"Error creating approval request: {e}")

        return approval_file

    def log_post_action(self, action: str, post_title: str, status: str):
        """Log post action to audit trail"""
        log_file = self.logs / f"{datetime.now().strftime('%Y-%m-%d')}.json"

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'post_title': post_title,
            'status': status,
            'platform': 'linkedin'
        }

        try:
            if log_file.exists():
                logs = json.loads(log_file.read_text())
            else:
                logs = []

            logs.append(log_entry)
            log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Error logging action: {e}")

    def process_approved_posts(self):
        """Process and post approved LinkedIn posts"""
        approved_posts = self.check_for_approved_posts()

        for post in approved_posts:
            try:
                post_data = self.extract_post_content(post['content'])
                full_content = f"{post_data['title']}\n\n{post_data['content']}"

                if post_data['hashtags']:
                    full_content += '\n\n' + ' '.join(post_data['hashtags'])

                # Post to LinkedIn
                success = self.post_to_linkedin(full_content)

                if success:
                    self.log_post_action('post_published', post_data['title'], 'success')
                    # Move to Done
                    done_folder = self.vault_path / 'Done'
                    done_folder.mkdir(exist_ok=True)
                    post['file'].rename(done_folder / post['file'].name)
                else:
                    self.log_post_action('post_failed', post_data['title'], 'failed')

            except Exception as e:
                self.logger.error(f"Error processing approved post: {e}")

    def demo_run(self):
        """Demo run that creates sample LinkedIn posts"""
        self.logger.info("Running LinkedIn Poster in demo mode")

        sample_posts = [
            {
                'title': 'Q1 2026 Business Update',
                'content': 'Excited to share our progress this quarter. We\'ve achieved 45% growth and expanded our team.',
                'hashtags': ['#business', '#growth', '#2026']
            },
            {
                'title': 'New Service Launch',
                'content': 'Launching our new AI-powered automation service. This will help businesses save 20+ hours per week.',
                'hashtags': ['#innovation', '#automation', '#AI']
            },
            {
                'title': 'Industry Insights',
                'content': 'The future of work is autonomous. Here\'s how we\'re building it.',
                'hashtags': ['#futureofwork', '#automation', '#AI']
            }
        ]

        for i, post in enumerate(sample_posts):
            content = f"""---
type: linkedin_post
title: {post['title']}
created: {datetime.now().isoformat()}
---

## Title
{post['title']}

## Content
{post['content']}

## Hashtags
{chr(10).join([f"- {tag}" for tag in post['hashtags']])}
"""
            self.create_approval_request(content, f"demo_{i+1}")

        self.logger.info(f"Created {len(sample_posts)} demo LinkedIn posts for approval")


if __name__ == "__main__":
    # Initialize the poster
    VAULT_PATH = Path(".")

    poster = LinkedInPoster(vault_path=VAULT_PATH)

    # For demo purposes, create sample posts
    poster.demo_run()

    print(f"\nLinkedIn Poster setup complete!")
    print(f"Approval requests created in: {poster.pending_approval}")
    print(f"\nTo process approved posts:")
    print(f"  poster.process_approved_posts()")
