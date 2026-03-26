"""
LinkedIn OAuth 2.0 Authentication
Secure API-based authentication for LinkedIn posting
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
import requests
from urllib.parse import urlencode, parse_qs, urlparse

logger = logging.getLogger(__name__)


class LinkedInOAuth:
    """Handle LinkedIn OAuth 2.0 authentication flow"""

    LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
    LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
    LINKEDIN_API_URL = "https://api.linkedin.com/v2"

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, vault_path: str = "."):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.vault_path = Path(vault_path)
        self.token_file = self.vault_path / ".linkedin_token.json"
        self.logger = logger

    def get_authorization_url(self, state: str = "random_state") -> str:
        """Generate LinkedIn authorization URL for user to visit"""
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "state": state,
            "scope": "w_member_social,r_liteprofile"
        }
        return f"{self.LINKEDIN_AUTH_URL}?{urlencode(params)}"

    def exchange_code_for_token(self, code: str) -> dict:
        """Exchange authorization code for access token"""
        try:
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri
            }

            response = requests.post(self.LINKEDIN_TOKEN_URL, data=data, timeout=10)
            response.raise_for_status()

            token_data = response.json()
            token_data["expires_at"] = (
                datetime.now() + timedelta(seconds=token_data.get("expires_in", 3600))
            ).isoformat()

            self._save_token(token_data)
            self.logger.info("Access token obtained successfully")
            return token_data

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error exchanging code for token: {e}")
            raise

    def refresh_access_token(self) -> dict:
        """Refresh expired access token using refresh token"""
        token_data = self._load_token()
        if not token_data or "refresh_token" not in token_data:
            raise ValueError("No refresh token available")

        try:
            data = {
                "grant_type": "refresh_token",
                "refresh_token": token_data["refresh_token"],
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }

            response = requests.post(self.LINKEDIN_TOKEN_URL, data=data, timeout=10)
            response.raise_for_status()

            new_token_data = response.json()
            new_token_data["expires_at"] = (
                datetime.now() + timedelta(seconds=new_token_data.get("expires_in", 3600))
            ).isoformat()

            self._save_token(new_token_data)
            self.logger.info("Access token refreshed successfully")
            return new_token_data

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error refreshing token: {e}")
            raise

    def get_valid_access_token(self) -> str:
        """Get a valid access token, refreshing if necessary"""
        token_data = self._load_token()

        if not token_data:
            raise ValueError("No token available. Please authenticate first.")

        # Check if token is expired
        expires_at = datetime.fromisoformat(token_data.get("expires_at", ""))
        if datetime.now() >= expires_at:
            self.logger.info("Token expired, refreshing...")
            token_data = self.refresh_access_token()

        return token_data["access_token"]

    def post_to_linkedin(self, content: str, hashtags: list = None) -> dict:
        """Post content to LinkedIn using API"""
        try:
            access_token = self.get_valid_access_token()

            # Get user ID first
            user_id = self._get_user_id(access_token)

            # Prepare post data
            post_data = {
                "author": f"urn:li:person:{user_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "LinkedIn-Version": "202401"
            }

            response = requests.post(
                f"{self.LINKEDIN_API_URL}/ugcPosts",
                json=post_data,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()

            result = response.json()
            self.logger.info(f"Post published successfully: {result.get('id')}")
            return result

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error posting to LinkedIn: {e}")
            raise

    def _get_user_id(self, access_token: str) -> str:
        """Get authenticated user's LinkedIn ID"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "LinkedIn-Version": "202401"
        }

        response = requests.get(
            f"{self.LINKEDIN_API_URL}/me",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        user_data = response.json()
        return user_data["id"]

    def _save_token(self, token_data: dict):
        """Save token to file"""
        try:
            self.token_file.write_text(json.dumps(token_data, indent=2))
            self.logger.info(f"Token saved to {self.token_file}")
        except Exception as e:
            self.logger.error(f"Error saving token: {e}")

    def _load_token(self) -> dict:
        """Load token from file"""
        try:
            if self.token_file.exists():
                return json.loads(self.token_file.read_text())
        except Exception as e:
            self.logger.error(f"Error loading token: {e}")
        return None


def setup_oauth_flow():
    """Interactive setup for LinkedIn OAuth"""
    print("\n" + "="*60)
    print("LinkedIn OAuth 2.0 Setup")
    print("="*60)

    print("\n1. Go to https://www.linkedin.com/developers/apps")
    print("2. Create a new app or select existing one")
    print("3. Get your credentials from the 'Auth' tab\n")

    client_id = input("Enter your LinkedIn Client ID: ").strip()
    client_secret = input("Enter your LinkedIn Client Secret: ").strip()
    redirect_uri = input("Enter your Redirect URI (e.g., http://localhost:8080/callback): ").strip()

    oauth = LinkedInOAuth(client_id, client_secret, redirect_uri)

    # Step 1: Get authorization URL
    auth_url = oauth.get_authorization_url()
    print(f"\n2. Visit this URL to authorize:\n{auth_url}\n")

    # Step 2: Get authorization code
    auth_code = input("After authorizing, paste the 'code' parameter from the redirect URL: ").strip()

    # Step 3: Exchange code for token
    try:
        token_data = oauth.exchange_code_for_token(auth_code)
        print("\n✓ Authentication successful!")
        print(f"Token saved to: {oauth.token_file}")
        print(f"Token expires at: {token_data.get('expires_at')}")
    except Exception as e:
        print(f"\n✗ Authentication failed: {e}")
        return False

    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_oauth_flow()
