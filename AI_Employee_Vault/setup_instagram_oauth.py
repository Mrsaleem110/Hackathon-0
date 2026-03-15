"""
Instagram OAuth Setup - Secure credential acquisition
Uses OAuth flow to get access token without storing passwords
"""

import os
import json
import webbrowser
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import requests
from dotenv import load_dotenv, set_key

# Load existing .env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Instagram OAuth Configuration
INSTAGRAM_APP_ID = os.getenv('INSTAGRAM_APP_ID', 'YOUR_APP_ID')
INSTAGRAM_APP_SECRET = os.getenv('INSTAGRAM_APP_SECRET', 'YOUR_APP_SECRET')
REDIRECT_URI = 'http://localhost:8888/callback'

# Global variable to store the code
auth_code = None
server_instance = None


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback from Instagram"""

    def do_GET(self):
        global auth_code

        # Parse the callback URL
        parsed_url = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_url.query)

        if 'code' in params:
            auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <head><title>Instagram OAuth Success</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>✅ Success!</h1>
                <p>Instagram authentication successful!</p>
                <p>You can close this window and return to the terminal.</p>
            </body>
            </html>
            """)
        elif 'error' in params:
            error = params['error'][0]
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"""
            <html>
            <head><title>Instagram OAuth Error</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>❌ Error</h1>
                <p>Authentication failed: {error}</p>
                <p>Please try again.</p>
            </body>
            </html>
            """.encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Invalid callback")

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def start_oauth_server():
    """Start local server for OAuth callback"""
    global server_instance
    server = HTTPServer(('localhost', 8888), OAuthCallbackHandler)
    server_instance = server
    print("🔄 OAuth callback server started on http://localhost:8888")
    return server


def get_instagram_auth_url():
    """Generate Instagram OAuth authorization URL"""
    params = {
        'client_id': INSTAGRAM_APP_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'instagram_business_basic,instagram_business_content_publish,instagram_business_manage_messages',
        'response_type': 'code'
    }

    base_url = 'https://api.instagram.com/oauth/authorize'
    auth_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return auth_url


def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    url = 'https://graph.instagram.com/v18.0/oauth/access_token'

    data = {
        'client_id': INSTAGRAM_APP_ID,
        'client_secret': INSTAGRAM_APP_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': code
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error exchanging code for token: {e}")
        return None


def get_business_account_id(access_token):
    """Get Instagram Business Account ID"""
    url = 'https://graph.instagram.com/v18.0/me'
    params = {'access_token': access_token, 'fields': 'id,username'}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting account info: {e}")
        return None


def save_credentials(access_token, business_account_id, username):
    """Save credentials to .env file"""
    try:
        set_key(env_path, 'INSTAGRAM_ACCESS_TOKEN', access_token)
        set_key(env_path, 'INSTAGRAM_BUSINESS_ACCOUNT_ID', business_account_id)
        set_key(env_path, 'INSTAGRAM_USERNAME', username)
        print(f"✅ Credentials saved to .env")
        return True
    except Exception as e:
        print(f"❌ Error saving credentials: {e}")
        return False


def setup_instagram_oauth():
    """Main OAuth setup flow"""
    print("\n" + "=" * 60)
    print("INSTAGRAM OAUTH SETUP")
    print("=" * 60)

    # Check if app credentials are configured
    if INSTAGRAM_APP_ID == 'YOUR_APP_ID' or INSTAGRAM_APP_SECRET == 'YOUR_APP_SECRET':
        print("\n❌ Instagram App credentials not configured!")
        print("\nTo set up Instagram OAuth:")
        print("1. Go to https://developers.facebook.com/")
        print("2. Create an app or use existing one")
        print("3. Add Instagram Basic Display product")
        print("4. Get your App ID and App Secret")
        print("5. Add to .env file:")
        print("   INSTAGRAM_APP_ID=your_app_id")
        print("   INSTAGRAM_APP_SECRET=your_app_secret")
        return False

    print("\n📱 Starting Instagram OAuth flow...")
    print("A browser window will open for you to login to Instagram.\n")

    # Start OAuth server
    server = start_oauth_server()

    # Generate auth URL
    auth_url = get_instagram_auth_url()
    print(f"🔗 Opening: {auth_url}\n")

    # Open browser
    webbrowser.open(auth_url)
    print("⏳ Waiting for authorization...")

    # Handle one request
    server.handle_request()
    server.server_close()

    global auth_code
    if not auth_code:
        print("❌ No authorization code received")
        return False

    print(f"✅ Authorization code received")

    # Exchange code for token
    print("🔄 Exchanging code for access token...")
    token_response = exchange_code_for_token(auth_code)

    if not token_response or 'access_token' not in token_response:
        print("❌ Failed to get access token")
        return False

    access_token = token_response['access_token']
    print(f"✅ Access token obtained")

    # Get business account info
    print("📊 Fetching account information...")
    account_info = get_business_account_id(access_token)

    if not account_info or 'id' not in account_info:
        print("❌ Failed to get account information")
        return False

    business_account_id = account_info['id']
    username = account_info.get('username', 'unknown')

    print(f"✅ Account: @{username} (ID: {business_account_id})")

    # Save credentials
    if save_credentials(access_token, business_account_id, username):
        print("\n" + "=" * 60)
        print("✅ INSTAGRAM OAUTH SETUP COMPLETE!")
        print("=" * 60)
        print(f"\nCredentials saved:")
        print(f"  Username: @{username}")
        print(f"  Account ID: {business_account_id}")
        print(f"  Access Token: {access_token[:20]}...")
        print("\nYou can now use Instagram features in the system!")
        return True

    return False


if __name__ == '__main__':
    setup_instagram_oauth()
