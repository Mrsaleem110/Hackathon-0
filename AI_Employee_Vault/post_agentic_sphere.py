"""
Post Agentic Sphere summary to LinkedIn - Enhanced version
"""
import time
import logging
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not installed. Install with: pip install playwright")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def post_to_linkedin():
    """Post Agentic Sphere summary to LinkedIn"""

    post_content = """🤖 Introducing Agentic Sphere - Your Personal AI Employee

What it does:
✅ Monitors Gmail, WhatsApp & LinkedIn for opportunities
✅ Generates intelligent plans using Claude AI
✅ Executes actions with human approval
✅ Maintains complete audit trail

Built with a 5-layer architecture:
1. Detection Layer - Multi-channel monitoring
2. Planning Layer - AI-powered task planning
3. Approval Layer - Human-in-the-loop control
4. Execution Layer - Automated action execution
5. Logging Layer - Complete transparency

This is the future of personal productivity - AI that works FOR you, not just WITH you.

#AgenticSphere #AI #Automation #PersonalAssistant #FutureOfWork #Innovation #ProductivityTech"""

    if not PLAYWRIGHT_AVAILABLE:
        logger.error("Playwright not available. Install with: pip install playwright")
        return False

    try:
        session_path = Path(".linkedin_session_fresh")
        session_path.mkdir(exist_ok=True)

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                viewport={'width': 1280, 'height': 720}
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            try:
                logger.info("Opening LinkedIn feed...")
                page.goto('https://www.linkedin.com/feed/', timeout=15000)
                page.wait_for_timeout(3000)

                # Method 1: Try clicking "Start a post" button
                logger.info("Looking for 'Start a post' button...")
                try:
                    start_post_btn = page.locator('text=Start a post').first
                    if start_post_btn.is_visible():
                        start_post_btn.click()
                        page.wait_for_timeout(2000)
                        logger.info("Clicked 'Start a post' button")
                except:
                    logger.info("'Start a post' button not found, trying alternative...")

                # Method 2: Try clicking on the share box area
                logger.info("Looking for share box...")
                try:
                    share_box = page.locator('[data-testid="share-box"]').first
                    if share_box.is_visible():
                        share_box.click()
                        page.wait_for_timeout(2000)
                        logger.info("Clicked share box")
                except:
                    logger.info("Share box not found, trying alternative...")

                # Wait for modal/editor to appear
                page.wait_for_timeout(2000)

                # Method 3: Find any contenteditable div
                logger.info("Looking for text input area...")
                contenteditable = page.locator('[contenteditable="true"]').first

                if contenteditable.is_visible():
                    logger.info("Found contenteditable area, typing post...")
                    contenteditable.click()
                    page.wait_for_timeout(500)
                    contenteditable.type(post_content, delay=5)
                    page.wait_for_timeout(1000)
                    logger.info("Post content typed")

                    # Find and click post button
                    logger.info("Looking for post/publish button...")
                    page.wait_for_timeout(1000)

                    # Try different button selectors
                    post_btn = page.locator('button:has-text("Post")').first
                    if post_btn.is_visible():
                        logger.info("Found 'Post' button, clicking...")
                        post_btn.click()
                        page.wait_for_timeout(3000)
                        logger.info("✅ Post published successfully!")
                        return True
                    else:
                        # Try alternative button text
                        publish_btn = page.locator('button:has-text("Publish")').first
                        if publish_btn.is_visible():
                            logger.info("Found 'Publish' button, clicking...")
                            publish_btn.click()
                            page.wait_for_timeout(3000)
                            logger.info("✅ Post published successfully!")
                            return True
                        else:
                            logger.error("Could not find Post/Publish button")
                            logger.info("Keeping browser open for manual posting...")
                            page.wait_for_timeout(30000)  # Keep open for 30 seconds
                            return False
                else:
                    logger.error("Could not find text input area")
                    logger.info("Keeping browser open for manual inspection...")
                    page.wait_for_timeout(30000)
                    return False

            except Exception as e:
                logger.error(f"Error posting: {e}")
                logger.info("Keeping browser open for manual inspection...")
                page.wait_for_timeout(30000)
                return False
            finally:
                browser.close()

    except Exception as e:
        logger.error(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Starting LinkedIn post...")
    print("A browser window will open - please authenticate if needed")
    print("=" * 60)

    success = post_to_linkedin()

    if success:
        print("\n✅ Post published successfully to LinkedIn!")
    else:
        print("\n⚠️  Could not auto-post. Browser was kept open for manual posting.")
        print("Please manually post the content or check the browser window.")
