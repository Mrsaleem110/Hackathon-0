"""
Manual Gmail Authentication - Simple approach
"""

import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']

def manual_auth():
    """Manual Gmail authentication with local server"""

    print("\n" + "="*60)
    print("Gmail Authentication")
    print("="*60)

    credentials_file = Path("gmail_credentials.json")
    if not credentials_file.exists():
        print("Error: gmail_credentials.json not found!")
        return False

    try:
        print("\nStarting authentication flow...")
        print("A browser window will open. Please:")
        print("1. Select your Gmail account")
        print("2. Click 'Allow' to grant access")
        print("3. Wait for confirmation\n")

        flow = InstalledAppFlow.from_client_secrets_file(
            str(credentials_file), SCOPES)

        # Run local server on port 8080
        creds = flow.run_local_server(port=8080, open_browser=True)

        # Save token
        token_file = Path("gmail_token.json")
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

        print("\n✓ Success! Gmail authenticated!")
        print("✓ Token saved to: gmail_token.json")
        print("="*60 + "\n")
        return True

    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure gmail_credentials.json is correct")
        print("2. Check that port 8080 is not in use")
        print("3. Try running again\n")
        return False

if __name__ == "__main__":
    manual_auth()
