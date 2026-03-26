"""
Re-authenticate Gmail with full permissions (read, send, modify)
Run this to get new token with all required scopes
"""

from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
import json

# Full Gmail access scope
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main():
    credentials_file = Path('gmail_credentials.json')

    if not credentials_file.exists():
        print("Error: gmail_credentials.json not found!")
        print("Please ensure your OAuth credentials file is in the current directory.")
        return

    print("="*60)
    print("Gmail Re-Authentication")
    print("="*60)
    print("\nThis will open a browser window for you to:")
    print("1. Login to your Google account")
    print("2. Grant permissions to read, send, and modify emails")
    print("\nNew permissions:")
    print("  - Read emails (including unread)")
    print("  - Send emails")
    print("  - Modify emails (mark as read/unread)")
    print("="*60)

    input("\nPress ENTER to continue...")

    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(credentials_file),
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        # Save the credentials
        token_file = Path('token.json')
        token_file.write_text(creds.to_json())

        print("\n" + "="*60)
        print("SUCCESS!")
        print("="*60)
        print("\nNew token saved with full permissions:")
        print("  ✓ Read emails")
        print("  ✓ Send emails")
        print("  ✓ Modify emails (mark as read/unread)")
        print("\nYou can now run auto_reply_emails.py")
        print("="*60)

    except Exception as e:
        print(f"\nError during authentication: {e}")
        print("\nPlease ensure:")
        print("1. gmail_credentials.json is valid")
        print("2. You have internet connection")
        print("3. You allow all permissions in the browser")

if __name__ == "__main__":
    main()
