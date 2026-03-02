"""
Gmail Login Script - Real Credentials Setup
Authenticates with Gmail API and saves token for future use
"""

import sys
import os
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']

def login_gmail():
    """Authenticate with Gmail API and save token"""

    print("\n" + "="*60)
    print("Gmail Login - Real Credentials Setup")
    print("="*60)
    print("\nSetting up Gmail API authentication...\n")

    try:
        # Check if credentials file exists
        credentials_file = Path("gmail_credentials.json")
        if not credentials_file.exists():
            print("Error: gmail_credentials.json not found!")
            print("Please download it from Google Cloud Console:")
            print("1. Go to https://console.cloud.google.com/")
            print("2. Create a project")
            print("3. Enable Gmail API")
            print("4. Create OAuth 2.0 credentials (Desktop app)")
            print("5. Download and save as gmail_credentials.json")
            return False

        # Check if token already exists
        token_file = Path("gmail_token.json")
        creds = None

        if token_file.exists():
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)

        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing Gmail token...")
                creds.refresh(Request())
            else:
                print("Opening browser for Gmail authentication...")
                print("\n" + "-"*60)
                print("INSTRUCTIONS:")
                print("-"*60)
                print("1. A browser window will open")
                print("2. Select your Gmail account")
                print("3. Click 'Allow' to grant access")
                print("4. You'll be redirected to localhost")
                print("5. Copy the authorization code if needed")
                print("-"*60 + "\n")

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_file), SCOPES)
                creds = flow.run_local_server(port=8080)

            # Save the credentials for future use
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
            print("\n✓ Gmail token saved to: gmail_token.json")

        print("\n✓ Success! Gmail authenticated!")
        print("Token saved to: gmail_token.json")

    except Exception as e:
        print(f"\nError during Gmail authentication: {e}")
        return False

    print("\n" + "="*60)
    print("Gmail setup complete!")
    print("="*60)
    print("\nYour Gmail is now authenticated and ready to use.")
    print("The AI Employee Vault can now monitor your Gmail messages.\n")

    return True

if __name__ == "__main__":
    success = login_gmail()
    sys.exit(0 if success else 1)
