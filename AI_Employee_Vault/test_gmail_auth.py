"""
Test Gmail Authentication
Run this to authenticate with Gmail API
"""

import os
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate():
    """Authenticate with Gmail API"""
    creds = None
    token_path = Path('token.json')

    # Check if we have valid credentials
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow...")
            print("You'll need to create credentials.json from Google Cloud Console")
            print("1. Go to: https://console.cloud.google.com/")
            print("2. Enable Gmail API")
            print("3. Create OAuth 2.0 credentials")
            print("4. Download as credentials.json")

            if not Path('credentials.json').exists():
                print("\n❌ credentials.json not found!")
                print("Please create it first from Google Cloud Console")
                return False

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        print("✅ Authentication successful! token.json created")
    else:
        print("✅ Already authenticated!")

    return True

if __name__ == '__main__':
    authenticate()
