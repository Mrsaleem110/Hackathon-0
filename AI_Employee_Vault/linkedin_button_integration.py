#!/usr/bin/env python3
"""
LinkedIn Create Post Button - Integration with Agentic Sphere
Monitors for new posts and triggers the posting workflow
"""
import time
import json
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

class LinkedInButtonIntegration:
    """Integrate the Create Post button with Agentic Sphere workflow"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.plans = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'

    def open_agentic_sphere_page(self):
        """Open Agentic Sphere page with Create Post button ready"""
        print("=" * 70)
        print("LINKEDIN AGENTIC SPHERE - CREATE POST BUTTON")
        print("=" * 70)
        print("\n✨ Opening Agentic Sphere page with Create Post button...\n")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            # Navigate to Agentic Sphere page
            page.goto('https://www.linkedin.com/company/agentic-sphere/', timeout=30000)
            print("✓ Page loaded")
            print("✓ Create Post button should be visible (if Tampermonkey is installed)")
            print("\nInstructions:")
            print("1. Click the '✨ Create Post' button")
            print("2. Write your post content")
            print("3. Click 'Post' to publish")
            print("\nThe post will be automatically logged to your vault.\n")

            # Keep browser open
            input("Press Enter when you're done posting...")
            browser.close()

    def create_post_from_template(self, title: str, content: str, hashtags: list = None):
        """Create a post template in Needs_Action for approval"""
        if hashtags is None:
            hashtags = []

        filename = f"LINKEDIN_POST_{title.replace(' ', '_')}.md"
        filepath = self.needs_action / filename

        hashtag_text = '\n'.join([f"- {tag}" for tag in hashtags])

        post_content = f"""---
type: linkedin_post
title: {title}
created: {datetime.now().isoformat()}
status: needs_action
---

## Title
{title}

## Content
{content}

## Hashtags
{hashtag_text}

## Instructions
1. Review the content above
2. Move to Pending_Approval/Approved/ to publish
3. Or move to Pending_Approval/Rejected/ to discard
"""

        filepath.write_text(post_content, encoding='utf-8')
        print(f"✓ Created post template: {filename}")
        return filepath

    def list_pending_posts(self):
        """List all pending posts waiting for action"""
        pending_files = list(self.needs_action.glob('LINKEDIN_POST_*.md'))

        if not pending_files:
            print("No pending posts")
            return []

        print(f"\n📋 Pending LinkedIn Posts ({len(pending_files)}):")
        print("-" * 70)

        posts = []
        for i, file in enumerate(pending_files, 1):
            content = file.read_text(encoding='utf-8')
            # Extract title
            title = "Untitled"
            for line in content.split('\n'):
                if line.startswith('## Title'):
                    idx = content.find('## Title')
                    title_section = content[idx:].split('\n')[1]
                    title = title_section.strip()
                    break

            posts.append({'file': file, 'title': title})
            print(f"{i}. {title}")
            print(f"   File: {file.name}\n")

        return posts


def main():
    """Main entry point"""
    vault_path = Path(".")
    integration = LinkedInButtonIntegration(vault_path=vault_path)

    print("\n🚀 LinkedIn Agentic Sphere Integration\n")
    print("Options:")
    print("1. Open Agentic Sphere page (with Create Post button)")
    print("2. Create a post from template")
    print("3. List pending posts")
    print("4. Exit\n")

    choice = input("Select option (1-4): ").strip()

    if choice == "1":
        integration.open_agentic_sphere_page()

    elif choice == "2":
        title = input("Post title: ").strip()
        content = input("Post content: ").strip()
        hashtags_input = input("Hashtags (comma-separated, e.g., #AI,#Automation): ").strip()
        hashtags = [tag.strip() for tag in hashtags_input.split(',') if tag.strip()]

        integration.create_post_from_template(title, content, hashtags)
        print("\n✓ Post template created in Needs_Action/")

    elif choice == "3":
        integration.list_pending_posts()

    elif choice == "4":
        print("Goodbye!")

    else:
        print("Invalid option")


if __name__ == "__main__":
    main()
