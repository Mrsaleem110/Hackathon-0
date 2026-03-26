#!/usr/bin/env python3
"""
Simple LinkedIn Post Creator - Creates post file for manual posting
"""

from pathlib import Path
from datetime import datetime
import json

def create_linkedin_post(content, title="LinkedIn Post"):
    """Create a LinkedIn post file"""

    # Create posts directory
    posts_dir = Path('Done')
    posts_dir.mkdir(exist_ok=True)

    # Create filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"LINKEDIN_POST_{title.replace(' ', '_')}_{timestamp}.md"
    filepath = posts_dir / filename

    # Create post file
    post_content = f"""# LinkedIn Post - {title}

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status:** Ready to Post
**Platform:** LinkedIn
**Page:** Agentic Sphere

## Post Content

{content}

## How to Post Manually

1. Go to https://www.linkedin.com/
2. Click "Start a post" button
3. Copy the content above
4. Paste it in the text editor
5. Click "Post"

## Post Details
- Word Count: {len(content.split())}
- Characters: {len(content)}
- Hashtags: {content.count('#')}

---
**Posted:** Not yet
**Message ID:** Pending
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(post_content)

    print(f"\nPost file created: {filepath}")
    print(f"Ready for manual posting on LinkedIn")

    return filepath

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        content = ' '.join(sys.argv[1:])
        title = "automation_topic"
    else:
        content = "Default post content"
        title = "default"

    create_linkedin_post(content, title)
