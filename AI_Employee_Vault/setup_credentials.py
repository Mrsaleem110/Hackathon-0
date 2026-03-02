"""
Real Credentials Setup - Master Script
Sets up WhatsApp, LinkedIn, and Gmail with real credentials
"""

import sys
import subprocess
from pathlib import Path

def run_setup():
    """Run complete setup for WhatsApp, LinkedIn, and Gmail"""

    print("\n" + "="*70)
    print("AI EMPLOYEE VAULT - REAL CREDENTIALS SETUP")
    print("="*70)
    print("\nThis script will help you set up real credentials for:")
    print("  1. WhatsApp Web (scan QR code)")
    print("  2. LinkedIn (enter your credentials)")
    print("  3. Gmail (OAuth approval)")
    print("\n" + "="*70 + "\n")

    vault_path = Path(".")

    # Step 1: WhatsApp Setup
    print("\n[STEP 1/3] WhatsApp Web Setup")
    print("-" * 70)
    print("You will need to:")
    print("  - Have WhatsApp installed on your phone")
    print("  - Be ready to scan a QR code")
    print("\nReady? Press Enter to continue...")
    input()

    try:
        print("\nStarting WhatsApp login...")
        result = subprocess.run([sys.executable, "whatsapp_login.py"], cwd=vault_path)
        if result.returncode != 0:
            print("WhatsApp login failed. Continuing to LinkedIn...")
    except Exception as e:
        print(f"Error running WhatsApp login: {e}")

    # Step 2: LinkedIn Setup
    print("\n[STEP 2/3] LinkedIn Setup")
    print("-" * 70)
    print("You will need to:")
    print("  - Have your LinkedIn email/password ready")
    print("  - Be ready to complete 2FA if enabled")
    print("\nReady? Press Enter to continue...")
    input()

    try:
        print("\nStarting LinkedIn login...")
        result = subprocess.run([sys.executable, "linkedin_login.py"], cwd=vault_path)
        if result.returncode != 0:
            print("LinkedIn login failed. Continuing to Gmail...")
    except Exception as e:
        print(f"Error running LinkedIn login: {e}")

    # Step 3: Gmail Setup
    print("\n[STEP 3/3] Gmail Setup")
    print("-" * 70)
    print("You will need to:")
    print("  - Have your Gmail account ready")
    print("  - Approve OAuth access when browser opens")
    print("\nReady? Press Enter to continue...")
    input()

    try:
        print("\nStarting Gmail login...")
        result = subprocess.run([sys.executable, "gmail_login.py"], cwd=vault_path)
        if result.returncode != 0:
            print("Gmail login may have issues. Continuing...")
    except Exception as e:
        print(f"Error running Gmail login: {e}")

    # Verify setup
    print("\n" + "="*70)
    print("SETUP VERIFICATION")
    print("="*70)

    whatsapp_session = (vault_path / ".whatsapp_session").exists()
    linkedin_session = (vault_path / ".linkedin_session").exists()
    gmail_token = (vault_path / "gmail_token.json").exists()

    print(f"\nWhatsApp Session: {'✓ OK' if whatsapp_session else '✗ NOT FOUND'}")
    print(f"LinkedIn Session: {'✓ OK' if linkedin_session else '✗ NOT FOUND'}")
    print(f"Gmail Token: {'✓ OK' if gmail_token else '✗ NOT FOUND'}")

    if whatsapp_session and linkedin_session and gmail_token:
        print("\n" + "="*70)
        print("SUCCESS! All credentials set up!")
        print("="*70)
        print("\nYour AI Employee Vault is now ready to use with real credentials.")
        print("\nNext steps:")
        print("  1. Run: python orchestrator.py")
        print("  2. Monitor your WhatsApp, LinkedIn, and Gmail!")
        print("  3. Gemini AI will generate intelligent plans for all tasks")
        print("\n" + "="*70 + "\n")
        return True
    else:
        print("\n" + "="*70)
        print("SETUP INCOMPLETE")
        print("="*70)
        print("\nSome sessions were not created. Please try again.")
        print("\n" + "="*70 + "\n")
        return False

if __name__ == "__main__":
    success = run_setup()
    sys.exit(0 if success else 1)
