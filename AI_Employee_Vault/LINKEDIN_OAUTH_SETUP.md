# LinkedIn OAuth 2.0 Setup Guide

## Step 1: Register Your App on LinkedIn Developer Portal

1. Go to https://www.linkedin.com/developers/apps
2. Click "Create app"
3. Fill in the form:
   - **App name**: AI Employee Vault
   - **LinkedIn Page**: Select your business page (or create one)
   - **App logo**: Upload a logo
   - **Legal agreement**: Accept terms
4. Click "Create app"

## Step 2: Get Your Credentials

1. Go to your app's "Auth" tab
2. Copy these values:
   - **Client ID**: Found under "Authentication keys"
   - **Client Secret**: Found under "Authentication keys"
3. Under "Authorized redirect URLs", add:
   - `http://localhost:8080/callback`
   - `http://localhost:3000/callback`

## Step 3: Request Access to APIs

1. Go to the "Products" tab
2. Request access to:
   - **Sign In with LinkedIn** (for user authentication)
   - **Share on LinkedIn** (for posting)
3. Wait for approval (usually instant for testing)

## Step 4: Run OAuth Setup

```bash
python linkedin_oauth.py
```

This will:
1. Prompt you for Client ID, Client Secret, and Redirect URI
2. Generate an authorization URL
3. Open the URL in your browser
4. Ask you to authorize the app
5. Save your access token securely

## Step 5: Update Your .env File

Add these to your `.env`:

```
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:8080/callback
```

## Step 6: Use OAuth in Your Code

```python
from linkedin_oauth import LinkedInOAuth

oauth = LinkedInOAuth(
    client_id=os.getenv("LINKEDIN_CLIENT_ID"),
    client_secret=os.getenv("LINKEDIN_CLIENT_SECRET"),
    redirect_uri=os.getenv("LINKEDIN_REDIRECT_URI")
)

# Post to LinkedIn
result = oauth.post_to_linkedin(
    content="Your post content here",
    hashtags=["#AI", "#automation"]
)
```

## Scopes Explained

- **w_member_social**: Permission to post on behalf of the user
- **r_liteprofile**: Permission to read basic profile info

## Token Management

- Access tokens expire after 1 hour
- Refresh tokens are valid for 1 year
- The system automatically refreshes expired tokens
- Tokens are stored securely in `.linkedin_token.json`

## Troubleshooting

**"Invalid redirect URI"**
- Make sure the redirect URI in your app settings matches exactly
- Include the full URL with protocol (http:// or https://)

**"Insufficient permissions"**
- Request the required scopes in the Products tab
- Wait for approval (usually instant)

**"Token expired"**
- The system automatically refreshes tokens
- If manual refresh needed: `oauth.refresh_access_token()`

## Security Notes

- Never commit `.linkedin_token.json` to git (add to .gitignore)
- Never share your Client Secret
- Use environment variables for credentials
- Tokens are stored locally and encrypted when possible

## Next Steps

1. Complete the OAuth setup above
2. Update your `linkedin_poster.py` to use `LinkedInOAuth` instead of Playwright
3. Test posting through the API
4. Remove Playwright dependency for LinkedIn posting
