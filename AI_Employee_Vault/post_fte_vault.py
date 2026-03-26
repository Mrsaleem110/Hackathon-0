#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post to Agentic Sphere LinkedIn via Vault Workflow
Creates a post in Needs_Action for approval
"""
from pathlib import Path
from datetime import datetime

def create_linkedin_post():
    vault_path = Path(".")
    needs_action = vault_path / "Needs_Action"
    needs_action.mkdir(exist_ok=True)

    post_content = """---
type: linkedin_post
title: Agentic Sphere FTE Announcement
created: 2026-03-07T00:04:56Z
status: needs_action
platform: linkedin
target: agentic_sphere_company_page
---

## Post Content

hello from Agentic Sphere FTE

## Hashtags
- #AgenticSphere
- #AI
- #Automation

## Instructions
1. Review the post content above
2. Move to Pending_Approval/Approved/ to publish
3. The system will automatically post to LinkedIn
"""

    filename = "LINKEDIN_POST_agentic_sphere_fte.md"
    filepath = needs_action / filename

    filepath.write_text(post_content, encoding='utf-8')

    print("=" * 70)
    print("LINKEDIN POST CREATED")
    print("=" * 70)
    print(f"\nPost: hello from Agentic Sphere FTE")
    print(f"File: {filename}")
    print(f"Location: Needs_Action/")
    print("\nNext steps:")
    print("1. Review the post in Needs_Action/")
    print("2. Move to Pending_Approval/Approved/ to publish")
    print("3. System will post to LinkedIn automatically")
    print("\n" + "=" * 70)

if __name__ == '__main__':
    create_linkedin_post()
