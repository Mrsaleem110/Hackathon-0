"""
Email Response Agent Skill
This skill demonstrates how an AI Employee can process and respond to emails
"""

import os
import sys
from pathlib import Path
import json

def process_email_request(needs_action_file):
    """
    Process an email request from the Needs_Action folder
    """
    # Read the email file
    with open(needs_action_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse the frontmatter and content
    lines = content.split('\n')
    frontmatter = []
    content_lines = []
    in_frontmatter = False

    for line in lines:
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                in_frontmatter = False
                continue
        elif in_frontmatter:
            frontmatter.append(line)
        else:
            content_lines.append(line)

    # Extract email details
    email_content = '\n'.join(content_lines)
    subject = extract_frontmatter_value(frontmatter, 'subject')
    sender = extract_frontmatter_value(frontmatter, 'from')

    # Generate response based on content
    response = generate_email_response(sender, subject, email_content)

    return response

def extract_frontmatter_value(frontmatter, key):
    """Extract a value from frontmatter"""
    for line in frontmatter:
        if line.startswith(f'{key}:'):
            return line.split(':', 1)[1].strip().strip('"').strip("'")
    return "Unknown"

def generate_email_response(sender, subject, content):
    """Generate an appropriate email response"""
    # This is a simplified response generator
    # In a real implementation, this would use Claude Code for more sophisticated responses

    response = f"""
Subject: RE: {subject}

Dear {sender.split('<')[0].strip()},  # Extract name from email header

Thank you for your message regarding: {subject}

I am your AI Employee, handling communications on behalf of [Your Name].
I have received your request and will process it accordingly.

Current status: This is an automated response from your AI Employee.
For urgent matters, I will flag this for immediate attention.
For routine matters, expect a response within 24 hours.

Best regards,
[Your Name]'s AI Employee System

---
This response was automatically generated on {get_current_datetime()}
Request ID: {hash(content) % 10000}
    """.strip()

    return response

def get_current_datetime():
    """Get current datetime as string"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    # This would normally be called by Claude Code as an agent skill
    print("Email Processing Agent Skill v0.1")
    print("This skill demonstrates email processing capabilities")

    # Find a sample email in Needs_Action (if available)
    vault_path = Path(".")
    needs_action_path = vault_path / "Needs_Action"

    if needs_action_path.exists():
        email_files = list(needs_action_path.glob("*.md"))
        if email_files:
            sample_file = email_files[0]
            print(f"Processing sample file: {sample_file}")
            response = process_email_request(sample_file)
            print("Generated response:")
            print(response)
        else:
            print("No email files found in Needs_Action folder")
    else:
        print("Needs_Action folder not found")

if __name__ == "__main__":
    main()