# Add Real Instagram & Facebook Credentials - Complete Guide

**Last Updated**: 2026-03-26
**Status**: Production Ready

## Quick Start

```bash
python add_real_credentials.py
```

This interactive script will guide you through adding real credentials step-by-step.

---

## Instagram Setup - Step by Step

### Method 1: Facebook Business Manager (Recommended)

**Best for**: Existing Instagram Business Accounts

1. **Go to Facebook Business Manager**
   - URL: https://business.facebook.com/
   - Login with your Facebook account

2. **Find Your Instagram Account**
   - Click "Settings" in the left menu
   - Select "Apps and Websites"
   - Look for your Instagram Business Account

3. **Get Business Account ID**
   - Click on your Instagram account
   - Look for "Instagram Business Account ID" (17-digit number)
   - Example: `17841400000000`
   - Copy this value

4. **Generate Access Token**
   - In the same section, find "Access Tokens"
   - Click "Generate Token"
   - Select scopes:
     - `instagram_basic`
     - `instagram_manage_insights`
     - `pages_read_engagement`
   - Copy the token (starts with `IGAB_`)

5. **Update .env**
   ```
   INSTAGRAM_ACCESS_TOKEN=IGAB_your_real_token_here
   INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000
   ```

### Method 2: Facebook Developers Console

**Best for**: New setup or testing

1. **Create/Select App**
   - URL: https://developers.facebook.com/
   - Go to "My Apps"
   - Create new app or select existing

2. **Add Instagram Basic Display**
   - Click "Add Product"
   - Search for "Instagram Basic Display"
   - Click "Set Up"

3. **Configure Settings**
   - Go to Settings → Basic
   - Copy your App ID
   - Generate App Secret

4. **Get Access Token**
   - Go to Tools → Graph API Explorer
   - Select your app from dropdown
   - Select "Get User Access Token"
   - Choose scopes:
     - `instagram_basic`
     - `pages_manage_posts`
   - Click "Generate Access Token"
   - Copy the token

5. **Get Instagram Business Account ID**
   - In Graph API Explorer, run:
     ```
     GET /me/instagram_business_accounts
     ```
   - Copy the `id` from response

### Method 3: Graph API Explorer (Quickest)

**Best for**: Quick testing

1. **Open Graph API Explorer**
   - URL: https://developers.facebook.com/tools/explorer/

2. **Select Your App**
   - Choose your app from top-right dropdown

3. **Generate Token**
   - Click "Generate Access Token"
   - Select required permissions
   - Copy the token

4. **Get Account ID**
   - Run query: `GET /me/instagram_business_accounts`
   - Copy the ID from response

---

## Facebook Setup - Step by Step

### Method 1: Facebook Developers (Recommended)

**Best for**: Production use

1. **Create/Select App**
   - URL: https://developers.facebook.com/
   - Go to "My Apps"
   - Create new app (type: Business)

2. **Add Facebook Login Product**
   - Click "Add Product"
   - Search for "Facebook Login"
   - Click "Set Up"

3. **Configure App**
   - Go to Settings → Basic
   - Copy App ID and App Secret
   - Add your domain to "App Domains"

4. **Get Page Access Token**
   - Go to Tools → Graph API Explorer
   - Select your app
   - Run: `GET /me/accounts`
   - Find your page in the response
   - Copy the `access_token` value

5. **Get Page ID**
   - In the same response, copy the `id` field
   - This is your Page ID

6. **Verify Permissions**
   - Token should have scopes:
     - `pages_manage_posts`
     - `pages_read_engagement`
     - `pages_manage_metadata`

### Method 2: Graph API Explorer (Quick)

**Best for**: Testing

1. **Open Graph API Explorer**
   - URL: https://developers.facebook.com/tools/explorer/

2. **Select Your App**
   - Choose from top-right dropdown

3. **Generate Page Token**
   - Click "Generate Access Token"
   - Select your page
   - Choose required permissions
   - Copy the token

4. **Get Page ID**
   - Run: `GET /me/accounts`
   - Copy the `id` of your page

### Method 3: Facebook Business Manager

**Best for**: Existing business accounts

1. **Go to Business Manager**
   - URL: https://business.facebook.com/

2. **Select Your Page**
   - Click on your page
   - Go to Settings → Access Tokens

3. **Generate Token**
   - Click "Generate New Token"
   - Select required permissions
   - Copy the token

4. **Get Page ID**
   - Go to page settings
   - Copy the Page ID (numeric)

---

## Token Scopes Explained

### Instagram Scopes
- `instagram_basic` - Read basic profile info
- `instagram_manage_insights` - Read analytics
- `pages_manage_posts` - Create/edit posts
- `pages_read_engagement` - Read comments/likes

### Facebook Scopes
- `pages_manage_posts` - Create/edit/delete posts
- `pages_read_engagement` - Read comments/likes/shares
- `pages_manage_metadata` - Manage page settings
- `pages_read_user_content` - Read user comments

---

## Using the Setup Script

### Run Interactive Setup

```bash
python add_real_credentials.py
```

**What it does:**
1. Shows setup guides for both platforms
2. Prompts you to enter credentials
3. Validates the input
4. Updates .env file
5. Verifies credentials are set
6. Shows next steps

### Manual Setup

If you prefer to edit .env directly:

```bash
# Open .env file
nano .env
# or
code .env
```

Find these lines and update:

```env
# Instagram Configuration
INSTAGRAM_ACCESS_TOKEN=IGAB_your_real_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000

# Facebook Configuration
FACEBOOK_ACCESS_TOKEN=EAAB_your_real_token_here
FACEBOOK_PAGE_ID=1048264368365205
```

---

## Verify Credentials

### Check Configuration Status

```bash
python config.py
```

Output should show:
```
[OK] Instagram API configured
[OK] Facebook API configured
```

### Test Credentials

```bash
python test_insta_fb.py
```

This will:
- Load credentials from .env
- Test Instagram connection
- Test Facebook connection
- Show any errors

---

## Security Best Practices

### ✅ DO:
- Keep .env file in `.gitignore`
- Rotate tokens regularly (every 90 days)
- Use environment variables in production
- Store tokens securely (use secrets manager)
- Limit token permissions to minimum needed
- Monitor token usage

### ❌ DON'T:
- Commit .env to git
- Share tokens in messages/emails
- Use same token for multiple apps
- Store tokens in code
- Log tokens to console
- Use tokens in URLs

### Token Rotation

```bash
# Every 90 days, generate new tokens:
1. Go to https://developers.facebook.com/tools/explorer/
2. Generate new access token
3. Update .env file
4. Test with: python test_insta_fb.py
5. Delete old token from developer console
```

---

## Troubleshooting

### "Invalid Access Token"
- Token may have expired (valid for 60 days)
- Generate new token from developer console
- Verify token has correct scopes

### "Invalid Business Account ID"
- Check ID is 17 digits
- Verify it's the Instagram Business Account ID (not personal)
- Run: `GET /me/instagram_business_accounts` in Graph API Explorer

### "Invalid Page ID"
- Check ID is numeric
- Verify it's your page's ID (not your personal ID)
- Run: `GET /me/accounts` in Graph API Explorer

### "Permission Denied"
- Token may not have required scopes
- Generate new token with all required permissions
- Check token hasn't been revoked

### "Rate Limited"
- Too many requests in short time
- Wait a few minutes before retrying
- Implement exponential backoff in code

---

## Next Steps

After adding credentials:

### 1. Test Everything
```bash
python test_insta_fb.py
```

### 2. Post to Instagram
```bash
python auto_post_social.py --platform instagram --caption "Hello!" --image-url "https://..."
```

### 3. Post to Facebook
```bash
python auto_post_social.py --platform facebook --message "Hello!" --link "https://..."
```

### 4. View Dashboard
```bash
python social_dashboard.py
```

### 5. Start Orchestrator
```bash
python orchestrator.py
```

---

## API Endpoints Used

### Instagram
- `POST /v18.0/{business_account_id}/media` - Create post
- `GET /v18.0/{business_account_id}/media` - Get posts
- `GET /v18.0/{business_account_id}/insights` - Get analytics

### Facebook
- `POST /v18.0/{page_id}/feed` - Create post
- `GET /v18.0/{page_id}/feed` - Get posts
- `GET /v18.0/{page_id}/insights` - Get analytics

---

## Support

For issues:
1. Check troubleshooting section above
2. Review .env file for correct format
3. Run `python config.py` to check status
4. Check token scopes in developer console
5. Verify token hasn't expired

---

## References

- [Facebook Developers](https://developers.facebook.com/)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)
- [Access Tokens](https://developers.facebook.com/docs/facebook-login/access-tokens)
- [Permissions](https://developers.facebook.com/docs/permissions)
