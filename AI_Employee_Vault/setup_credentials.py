"""
Real Credentials Setup - Master Script
Sets up WhatsApp and LinkedIn with real credentials
"""

import sys
import subprocess
from pathlib import Path

def run_setup():
    """Run complete setup for WhatsApp and LinkedIn"""

    print("\n" + "="*70)
    print("AI EMPLOYEE VAULT - REAL CREDENTIALS SETUP")
    print("="*70)
    print("\nThis script will help you set up real credentials for:")
    print("  1. WhatsApp Web (scan QR code)")
    print("  2. LinkedIn (enter your credentials)")
    print("\n" + "="*70 + "\n")

    vault_path = Path(".")

    # Step 1: WhatsApp Setup
    print("\n[STEP 1/2] WhatsApp Web Setup")
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
    print("\n[STEP 2/2] LinkedIn Setup")
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
            print("LinkedIn login failed.")
    except Exception as e:
        print(f"Error running LinkedIn login: {e}")

    # Verify setup
    print("\n" + "="*70)
    print("SETUP VERIFICATION")
    print("="*70)

    whatsapp_session = (vault_path / ".whatsapp_session").exists()
    linkedin_session = (vault_path / ".linkedin_session").exists()

    print(f"\nWhatsApp Session: {'OK' if whatsapp_session else 'NOT FOUND'}")
    print(f"LinkedIn Session: {'OK' if linkedin_session else 'NOT FOUND'}")

    if whatsapp_session and linkedin_session:
        print("\n" + "="*70)
        print("SUCCESS! All credentials set up!")
        print("="*70)
        print("\nYour AI Employee Vault is now ready to use with real credentials.")
        print("\nNext steps:")
        print("  1. Update .env file with LinkedIn API credentials (if needed)")
        print("  2. Run: python orchestrator.py")
        print("  3. Monitor your WhatsApp and LinkedIn messages!")
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
