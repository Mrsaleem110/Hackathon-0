"""
Post Automation Topic to Agentic Sphere LinkedIn Page
Generates and posts engaging automation content
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not installed")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("Requests not installed")


class AutomationTopicPoster:
    """Post automation topics to LinkedIn Agentic Sphere page"""

    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path) if vault_path else Path.cwd()
        self.logs_path = self.vault_path / 'Logs'
        self.done_path = self.vault_path / 'Done'
        self.logs_path.mkdir(exist_ok=True)
        self.done_path.mkdir(exist_ok=True)

        # LinkedIn credentials
        self.linkedin_access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.linkedin_org_id = os.getenv('LINKEDIN_ORG_ID', '95234567')  # Agentic Sphere org ID

    def generate_automation_post(self) -> dict:
        """Generate engaging automation topic post"""
        posts = [
            {
                "title": "🤖 Automation: The Future of Business Efficiency",
                "content": """Did you know? Businesses that implement intelligent automation see a 40% increase in productivity.

At Agentic Sphere, we're revolutionizing how companies work by automating repetitive tasks and enabling teams to focus on strategic initiatives.

Key benefits of automation:
✅ 24/7 Operations - Never miss an opportunity
✅ Error Reduction - Eliminate human mistakes
✅ Cost Savings - Reduce operational expenses
✅ Scalability - Grow without proportional headcount increase
✅ Employee Satisfaction - Let AI handle the mundane

The future isn't about replacing humans—it's about empowering them with intelligent systems.

Ready to transform your business? Let's talk automation.

#Automation #AI #BusinessEfficiency #DigitalTransformation #FutureOfWork""",
                "hashtags": ["#Automation", "#AI", "#BusinessEfficiency", "#DigitalTransformation", "#FutureOfWork"]
            },
            {
                "title": "⚡ Why Your Business Needs Intelligent Automation NOW",
                "content": """In 2026, automation isn't a luxury—it's a necessity.

Companies that automate their workflows are:
📈 3x faster at decision-making
💰 50% more cost-efficient
🎯 Better at meeting customer expectations
🚀 More competitive in their markets

The question isn't "Should we automate?"
The question is "How quickly can we automate?"

At Agentic Sphere, we help businesses:
• Identify automation opportunities
• Design intelligent workflows
• Implement AI-powered solutions
• Monitor and optimize continuously

Your competitors are already automating. Don't get left behind.

Let's build the future together.

#Automation #AI #BusinessIntelligence #Innovation #TechLeadership""",
                "hashtags": ["#Automation", "#AI", "#BusinessIntelligence", "#Innovation", "#TechLeadership"]
            },
            {
                "title": "🎯 Automation Success Story: From Manual to Intelligent",
                "content": """Imagine this: Your team spends 40 hours/week on repetitive tasks.

With intelligent automation, that becomes:
✨ 2 hours/week for oversight
✨ 38 hours/week for strategic work
✨ 100% accuracy (no human error)
✨ 24/7 availability

This isn't a dream—it's what our clients are experiencing right now.

The transformation journey:
1️⃣ Audit current processes
2️⃣ Identify automation opportunities
3️⃣ Design intelligent workflows
4️⃣ Implement with AI
5️⃣ Monitor and optimize

Ready to transform your operations?

Agentic Sphere specializes in turning manual processes into intelligent, autonomous systems.

Let's talk about your automation potential.

#ProcessAutomation #AI #OperationalExcellence #DigitalTransformation #SmartBusiness""",
                "hashtags": ["#ProcessAutomation", "#AI", "#OperationalExcellence", "#DigitalTransformation", "#SmartBusiness"]
            }
        ]

        # Return a random post or the first one
        return posts[0]

    def post_via_api(self, post_content: dict) -> bool:
        """Post to LinkedIn using API"""
        if not REQUESTS_AVAILABLE:
            logger.error("Requests library not available")
            return False

        if not self.linkedin_access_token:
            logger.error("LinkedIn access token not configured")
            return False

        try:
            # LinkedIn API endpoint for organization posts
            url = f"https://api.linkedin.com/v2/ugcPosts"

            headers = {
                "Authorization": f"Bearer {self.linkedin_access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }

            # Prepare post payload
            payload = {
                "author": f"urn:li:organization:{self.linkedin_org_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": f"{post_content['title']}\n\n{post_content['content']}"
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)

            if response.status_code in [200, 201]:
                logger.info(f"✅ Post published successfully via API")
                return True
            else:
                logger.error(f"API Error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error posting via API: {e}")
            return False

    def post_via_browser(self, post_content: dict) -> bool:
        """Post to LinkedIn using browser automation"""
        if not PLAYWRIGHT_AVAILABLE:
            logger.error("Playwright not available")
            return False

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                # Navigate to LinkedIn
                page.goto("https://www.linkedin.com/feed/", wait_until="networkidle")
                logger.info("Navigated to LinkedIn feed")

                # Wait for page to load
                page.wait_for_timeout(2000)

                # Click on "Start a post" button
                try:
                    page.click("button:has-text('Start a post')")
                    page.wait_for_timeout(1000)
                except:
                    logger.warning("Could not find 'Start a post' button")

                # Find and fill the post text area
                try:
                    post_text = f"{post_content['title']}\n\n{post_content['content']}"
                    page.fill("div[contenteditable='true']", post_text)
                    logger.info("Filled post content")
                    page.wait_for_timeout(1000)
                except Exception as e:
                    logger.error(f"Error filling post content: {e}")

                # Click Post button
                try:
                    page.click("button:has-text('Post')")
                    page.wait_for_timeout(3000)
                    logger.info("✅ Post published successfully via browser")
                    browser.close()
                    return True
                except Exception as e:
                    logger.error(f"Error clicking post button: {e}")
                    browser.close()
                    return False

        except Exception as e:
            logger.error(f"Browser automation error: {e}")
            return False

    def log_post(self, post_content: dict, success: bool):
        """Log the post to Done folder"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        status = "EXECUTED" if success else "FAILED"

        log_content = f"""# {status} - LinkedIn Automation Topic Post
**Date**: {datetime.now().isoformat()}
**Status**: {status}

## Post Title
{post_content['title']}

## Post Content
{post_content['content']}

## Hashtags
{', '.join(post_content['hashtags'])}

## Execution Details
- Method: LinkedIn API / Browser Automation
- Target: Agentic Sphere Organization Page
- Visibility: PUBLIC
"""

        filename = self.done_path / f"{status}_LINKEDIN_POST_automation_topic_{timestamp}.md"
        filename.write_text(log_content, encoding='utf-8')
        logger.info(f"Logged post to {filename}")

    def post(self, use_api: bool = True) -> bool:
        """Post automation topic to LinkedIn"""
        logger.info("🚀 Starting automation topic post...")

        # Generate post content
        post_content = self.generate_automation_post()
        logger.info(f"Generated post: {post_content['title']}")

        # Try API first, then browser
        success = False
        if use_api:
            success = self.post_via_api(post_content)

        if not success and PLAYWRIGHT_AVAILABLE:
            logger.info("API failed or not available, trying browser automation...")
            success = self.post_via_browser(post_content)

        # Log the result
        self.log_post(post_content, success)

        return success


def main():
    """Main entry point"""
    vault_path = Path.cwd()

    poster = AutomationTopicPoster(vault_path)
    success = poster.post(use_api=True)

    if success:
        logger.info("Automation topic posted successfully!")
    else:
        logger.info("Post may have failed - check logs for details")


if __name__ == "__main__":
    main()
