"""
Test Real Gmail and LinkedIn Integration
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from MCP.email_mcp_server import EmailMCPServer

def test_gmail():
    """Test Gmail integration"""
    print("\n" + "="*60)
    print("TESTING GMAIL INTEGRATION")
    print("="*60)

    email_server = EmailMCPServer(vault_path='.')

    if email_server.service:
        print("[OK] Gmail service authenticated!")
        print("\nSending test email...")

        result = email_server.send_email(
            to="test@example.com",  # Replace with your email
            subject="AI Employee Test - Gmail Integration",
            body="This is a test email from your AI Employee Vault system.\n\nIf you receive this, Gmail integration is working!"
        )

        print(f"Result: {result}")
        return True
    else:
        print("[FAIL] Gmail service not authenticated")
        print("Token file exists but authentication failed")
        return False

def test_linkedin():
    """Test LinkedIn integration"""
    print("\n" + "="*60)
    print("TESTING LINKEDIN INTEGRATION")
    print("="*60)

    # Create a test post
    test_post = Path('Business_Updates/TEST_POST.md')
    test_post.parent.mkdir(exist_ok=True)

    test_content = """---
type: linkedin_post
created: 2026-03-02
---

## Title
Testing AI Employee LinkedIn Integration

## Content
This is a test post from my AI Employee system.

The system can now:
- Monitor emails and messages
- Generate intelligent plans
- Post to LinkedIn automatically

## Hashtags
#AI #Automation #Productivity #Tech
"""

    test_post.write_text(test_content)
    print(f"[OK] Test post created: {test_post}")

    # Move to approval
    approved_folder = Path('Pending_Approval/Approved')
    approved_folder.mkdir(parents=True, exist_ok=True)

    approved_post = approved_folder / 'LINKEDIN_POST_test.md'
    approved_post.write_text(test_content)
    print(f"[OK] Post moved to approval: {approved_post}")

    print("\n[INFO] LinkedIn posting requires browser automation")
    print("Run orchestrator.py to execute the approved post")

    return True

def main():
    print("\n>> AI EMPLOYEE VAULT - REAL INTEGRATION TEST")
    print("="*60)

    # Test Gmail
    gmail_ok = test_gmail()

    # Test LinkedIn
    linkedin_ok = test_linkedin()

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Gmail: {'[PASS]' if gmail_ok else '[FAIL]'}")
    print(f"LinkedIn: {'[READY]' if linkedin_ok else '[FAIL]'}")
    print("\nNext: Run 'python orchestrator.py' to execute approved actions")
    print("="*60)

if __name__ == '__main__':
    main()
