#!/usr/bin/env python3
"""
LinkedIn OAuth - Generate New Access Token
"""
import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import requests

load_dotenv()

CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
REDIRECT_URI = "http://localhost:8080/callback"

# Store the authorization code
auth_code = None

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query = urlparse(self.path).query
        params = parse_qs(query)

        if 'code' in params:
            auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Success! You can close this window.</h1>')
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress logs

def get_access_token():
    """Generate new LinkedIn access token"""

    print("=" * 60)
    print("LinkedIn OAuth - Generate Access Token")
    print("=" * 60)

    # Step 1: Authorization URL
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope=openid%20profile%20email%20w_member_social"
    )

    print("\nStep 1: Opening browser for authorization...")
    print("Please login and authorize the app.\n")

    webbrowser.open(auth_url)

    # Step 2: Start local server to receive callback
    print("Step 2: Waiting for authorization...")
    server = HTTPServer(('localhost', 8080), CallbackHandler)
    server.handle_request()

    if not auth_code:
        print("Error: No authorization code received")
        return None

    print("Step 3: Authorization received!")

    # Step 3: Exchange code for access token
    print("Step 4: Getting access token...")

    token_url = "https://www.linkedin.com/oauth/v2/accessToken"

    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']

        print("\n" + "=" * 60)
        print("SUCCESS! New Access Token Generated")
        print("=" * 60)
        print(f"\nAccess Token:\n{access_token}\n")
        print("Copy this token and update your .env file:")
        print(f"LINKEDIN_ACCESS_TOKEN={access_token}")
        print("=" * 60)

        return access_token
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == '__main__':
    get_access_token()
