# Real Credentials Setup Guide

Complete guide to adding real credentials for all platforms in AI Employee Vault.

## Quick Start

```bash
python setup_real_credentials.py
```

This interactive script will guide you through getting and adding credentials for:
- ✅ Gmail
- ✅ LinkedIn
- ✅ Instagram
- ✅ Facebook
- ✅ Twitter/X
- ✅ WhatsApp

---

## Platform-by-Platform Setup

### 1. Gmail API

**Time: 5-10 minutes**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable Gmail API:
   - Search "Gmail API"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
   - Choose "Desktop application"
   - Download JSON file
5. Extract from JSON:
   - `GMAIL_CLIENT_ID`: client_id field
   - `GMAIL_CLIENT_SECRET`: client_secret field

**Scopes needed:**
- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/gmail.send`

---

### 2. LinkedIn

**Time: 5-10 minutes**

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Create new app:
   - App name: "AI Employee Vault"
   - LinkedIn Page: Select or create
   - App logo: Upload
   - Legal agreement: Accept
3. Go to "Auth" tab:
   - Copy `Client ID` → `LINKEDIN_CLIENT_ID`
   - Copy `Client secret` → `LINKEDIN_CLIENT_SECRET`
4. Generate access token:
   - Go to "Auth" → "Authorized redirect URLs"
   - Add: `http://localhost:8080/callback`
   - Use OAuth flow to get `LINKEDIN_ACCESS_TOKEN`

**Scopes needed:**
- `r_liteprofile`
- `r_emailaddress`
- `w_member_social`

---

### 3. Instagram

**Time: 10-15 minutes**

**Option A: Business Account (Recommended)**

1. Go to [Facebook Business Manager](https://business.facebook.com/)
2. Settings → Apps and Websites
3. Add your Instagram Business Account
4. Get credentials:
   - `INSTAGRAM_BUSINESS_ACCOUNT_ID`: Your business account ID
   - `INSTAGRAM_ACCESS_TOKEN`: Generate from Business Manager

**Option B: Personal Account**

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create app (type: Business)
3. Add "Instagram Basic Display" product
4. Create access token with scopes:
   - `instagram_basic`
   - `instagram_graph_user_profile`

**Scopes needed:**
- `instagram_basic`
- `pages_read_engagement`
- `pages_manage_metadata`

---

### 4. Facebook

**Time: 5-10 minutes**

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create app (type: Business)
3. Add "Facebook Login" product
4. Get credentials:
   - `FACEBOOK_PAGE_ID`: Your Facebook page ID
   - `FACEBOOK_ACCESS_TOKEN`: Generate with scopes below

**Scopes needed:**
- `pages_manage_posts`
- `pages_read_engagement`
- `pages_manage_metadata`

---

### 5. Twitter/X API

**Time: 10-15 minutes**

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create app (if not exists)
3. Go to "Keys and tokens" tab
4. Get credentials:
   - `TWITTER_BEARER_TOKEN`: Copy Bearer Token
   - `TWITTER_API_KEY`: Copy API Key
   - `TWITTER_API_SECRET`: Copy API Secret
   - `TWITTER_ACCESS_TOKEN`: Copy Access Token
   - `TWITTER_ACCESS_SECRET`: Copy Access Token Secret

**Permissions needed:**
- Read and Write
- Tweet.write
- Tweet.read
- Users.read

---

### 6. WhatsApp

**Time: 2-5 minutes**

WhatsApp uses session-based authentication (no API key needed).

1. First run will prompt for QR code scan
2. Scan with WhatsApp mobile app
3. Session saved to `.whatsapp_session`

**Note:** Keep `.whatsapp_session` file safe - it contains your session.

---

## Setup Script Usage

### Interactive Setup

```bash
python setup_real_credentials.py
```

The script will:
1. Ask which platforms to configure
2. Provide links and instructions for each
3. Prompt for credentials
4. Validate format
5. Update `.env` file
6. Test credentials

### Manual Setup

Edit `.env` file directly:

```bash
# Gmail
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret

# LinkedIn
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_ACCESS_TOKEN=your_access_token

# Instagram
INSTAGRAM_ACCESS_TOKEN=your_access_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id

# Facebook
FACEBOOK_ACCESS_TOKEN=your_access_token
FACEBOOK_PAGE_ID=your_page_id

# Twitter
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
```

---

## Verification

### Check Configuration Status

```bash
python config.py
```

Output shows which platforms are configured:
```
[OK] Gmail API configured
[OK] LinkedIn API configured
[OK] Instagram API configured
[OK] Facebook API configured
[NO] WhatsApp session not found
```

### Test Credentials

```bash
python test_mcp_servers.py
```

Tests all MCP servers with real credentials.

---

## Security Best Practices

1. **Never commit credentials** - `.env` is in `.gitignore`
2. **Rotate tokens regularly** - Set reminders to refresh
3. **Use environment variables** - Don't hardcode in code
4. **Limit scopes** - Only request needed permissions
5. **Monitor usage** - Check API dashboards for suspicious activity
6. **Backup session files** - Keep `.whatsapp_session` safe

---

## Troubleshooting

### "Invalid credentials" error

- Check token format (no extra spaces)
- Verify token hasn't expired
- Regenerate token from platform dashboard

### "Insufficient permissions" error

- Add required scopes to token
- Regenerate token with correct scopes
- Check app permissions in platform settings

### "Rate limit exceeded" error

- Wait before retrying
- Check API quota in platform dashboard
- Consider upgrading API tier

### WhatsApp QR code not appearing

- Ensure WhatsApp is installed on phone
- Check terminal output for QR code
- Try scanning again

---

## Next Steps

1. Run setup script: `python setup_real_credentials.py`
2. Verify credentials: `python config.py`
3. Test MCP servers: `python test_mcp_servers.py`
4. Start orchestrator: `python orchestrator.py`
5. Monitor logs: `tail -f Logs/YYYY-MM-DD.json`

---

## Support

For issues:
1. Check platform-specific documentation
2. Review error messages in logs
3. Verify token scopes and permissions
4. Test individual MCP servers
5. Check `.env` file format

