# Complete Credentials Management Guide

Comprehensive guide for managing real credentials in AI Employee Vault.

## Overview

The system supports 6 platforms with different authentication methods:

| Platform | Auth Type | Expiry | Setup Time |
|----------|-----------|--------|-----------|
| Gmail | OAuth 2.0 | 1 hour (refresh token) | 5 min |
| LinkedIn | OAuth 2.0 | 60 days | 5 min |
| Instagram | Access Token | 60 days | 2 min |
| Facebook | Access Token | 60 days | 2 min |
| Twitter/X | Bearer Token | Indefinite | 5 min |
| WhatsApp | Session | 30 days (inactive) | 2 min |

---

## Step-by-Step Setup

### Step 1: Run Interactive Setup

```bash
python setup_real_credentials.py
```

This will:
1. Show you which platforms to configure
2. Provide links and instructions for each
3. Prompt for credentials
4. Validate format
5. Update `.env` file
6. Verify credentials

### Step 2: Verify Configuration

```bash
python config.py
```

Check that all platforms show `[OK]`:
```
[OK] Gmail API configured
[OK] LinkedIn API configured
[OK] Instagram API configured
[OK] Facebook API configured
[OK] Twitter API configured
```

### Step 3: Test Credentials

```bash
python test_mcp_servers.py
```

This tests all MCP servers with real credentials.

### Step 4: Start System

```bash
python orchestrator.py
```

System is now ready to use real credentials.

---

## Platform-Specific Setup

### Gmail

**Time: 5 minutes**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable Gmail API (search "Gmail API" → Enable)
4. Create OAuth 2.0 credentials:
   - Credentials → Create Credentials → OAuth 2.0 Client ID
   - Choose "Desktop application"
   - Download JSON
5. Extract:
   - `client_id` → `GMAIL_CLIENT_ID`
   - `client_secret` → `GMAIL_CLIENT_SECRET`

**Scopes:**
- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/gmail.send`

**Token Refresh:**
- Access token: 1 hour
- Refresh token: Indefinite (auto-refreshed)

---

### LinkedIn

**Time: 5 minutes**

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Create new app:
   - App name: "AI Employee Vault"
   - LinkedIn Page: Select or create
   - Accept legal agreement
3. Go to "Auth" tab:
   - Copy `Client ID` → `LINKEDIN_CLIENT_ID`
   - Copy `Client secret` → `LINKEDIN_CLIENT_SECRET`
4. Generate access token:
   - Add redirect URL: `http://localhost:8080/callback`
   - Use OAuth flow to get `LINKEDIN_ACCESS_TOKEN`

**Scopes:**
- `r_liteprofile`
- `r_emailaddress`
- `w_member_social`

**Token Expiry:**
- 60 days (regenerate before expiry)

---

### Instagram

**Time: 2 minutes**

**Option A: Business Account (Recommended)**

1. Go to [Facebook Business Manager](https://business.facebook.com/)
2. Settings → Apps and Websites
3. Add Instagram Business Account
4. Get:
   - `INSTAGRAM_BUSINESS_ACCOUNT_ID`: Business account ID
   - `INSTAGRAM_ACCESS_TOKEN`: Generate from Business Manager

**Option B: Personal Account**

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create app (type: Business)
3. Add "Instagram Basic Display" product
4. Generate access token with scopes:
   - `instagram_basic`
   - `pages_read_engagement`

**Fastest Method:**

1. Open [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your app (top-right dropdown)
3. Click "Generate Access Token"
4. Choose scopes: `instagram_basic`, `pages_manage_posts`
5. Copy token (starts with `IGAB_`)
6. Run query: `GET /me/instagram_business_accounts`
7. Copy the `id` field (17 digits)

**Token Expiry:**
- 60 days (regenerate before expiry)

---

### Facebook

**Time: 2 minutes**

1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your app (top-right dropdown)
3. Click "Generate Access Token"
4. Choose scopes: `pages_manage_posts`, `pages_read_engagement`
5. Copy token (starts with `EAAB_`)
6. Run query: `GET /me/accounts`
7. Copy the `id` field of your page

**Scopes:**
- `pages_manage_posts`
- `pages_read_engagement`
- `pages_manage_metadata`

**Token Expiry:**
- 60 days (regenerate before expiry)

---

### Twitter/X

**Time: 5 minutes**

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create app (if not exists)
3. Go to "Keys and tokens" tab
4. Copy:
   - `Bearer Token` → `TWITTER_BEARER_TOKEN`
   - `API Key` → `TWITTER_API_KEY`
   - `API Secret` → `TWITTER_API_SECRET`
   - `Access Token` → `TWITTER_ACCESS_TOKEN`
   - `Access Token Secret` → `TWITTER_ACCESS_SECRET`
5. Ensure app has "Read and Write" permissions

**Permissions:**
- Read and Write
- Tweet.write
- Tweet.read
- Users.read

**Token Expiry:**
- Indefinite (no expiry)

---

### WhatsApp

**Time: 2 minutes (First run)**

WhatsApp uses session-based authentication (no API key needed).

1. Start orchestrator: `python orchestrator.py`
2. A QR code will appear in terminal
3. Scan with WhatsApp mobile app
4. Session saved to `.whatsapp_session`

**Important:**
- Keep `.whatsapp_session` file safe
- Don't share or commit to git
- Session expires after 30 days of inactivity
- Backup session file for recovery

---

## Environment Variables

All credentials are stored in `.env` file:

```bash
# Gmail
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
GMAIL_REDIRECT_URI=http://localhost:8080/callback

# LinkedIn
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_ACCESS_TOKEN=your_access_token

# Instagram
INSTAGRAM_ACCESS_TOKEN=your_access_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id
INSTAGRAM_USERNAME=your_username

# Facebook
FACEBOOK_ACCESS_TOKEN=your_access_token
FACEBOOK_PAGE_ID=your_page_id

# Twitter
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret

# WhatsApp
WHATSAPP_SESSION_PATH=.whatsapp_session

# System
VAULT_PATH=.
LOG_LEVEL=INFO
DRY_RUN=false
DEMO_MODE=false
```

---

## Token Rotation Schedule

| Platform | Expiry | Action | Frequency |
|----------|--------|--------|-----------|
| Gmail | 1 hour | Auto-refresh | Automatic |
| LinkedIn | 60 days | Regenerate | Every 50 days |
| Instagram | 60 days | Regenerate | Every 50 days |
| Facebook | 60 days | Regenerate | Every 50 days |
| Twitter | Indefinite | Monitor | Quarterly |
| WhatsApp | 30 days | Re-scan QR | If inactive |

---

## Security Best Practices

### 1. Never Commit Credentials
- `.env` is in `.gitignore`
- Never push credentials to git
- Use environment variables in production

### 2. Keep Tokens Secret
- Treat like passwords
- Don't share in messages or emails
- Don't log or print tokens

### 3. Rotate Regularly
- LinkedIn: Every 50 days
- Instagram: Every 50 days
- Facebook: Every 50 days
- Twitter: Quarterly
- WhatsApp: If inactive 30 days

### 4. Monitor Usage
- Check API dashboards regularly
- Look for unusual activity
- Set up alerts for suspicious access

### 5. Limit Scopes
- Only request needed permissions
- Remove unused scopes
- Review scopes quarterly

### 6. Backup Sessions
- Keep `.whatsapp_session` safe
- Backup to secure location
- Don't commit to git

---

## Troubleshooting

### "Invalid credentials" Error

**Cause:** Token format incorrect or expired

**Solution:**
1. Check token format (no extra spaces)
2. Verify token hasn't expired
3. Regenerate from platform dashboard
4. Update `.env` file

### "Insufficient permissions" Error

**Cause:** Token doesn't have required scopes

**Solution:**
1. Add required scopes to token
2. Regenerate token with correct scopes
3. Check app permissions in platform settings
4. Update `.env` file

### "Rate limit exceeded" Error

**Cause:** Too many API requests

**Solution:**
1. Wait before retrying (usually 15 minutes)
2. Check API quota in platform dashboard
3. Consider upgrading API tier
4. Implement request throttling

### WhatsApp QR Code Not Appearing

**Cause:** Terminal output issue or WhatsApp not installed

**Solution:**
1. Ensure WhatsApp is installed on phone
2. Check terminal output for QR code
3. Try scanning again
4. Restart orchestrator

### "Token expired" Error

**Cause:** Token has expired

**Solution:**
1. Regenerate token from platform dashboard
2. Update `.env` file
3. Restart orchestrator
4. Set reminder for next rotation

---

## Verification Commands

### Check Configuration Status
```bash
python config.py
```

### Test All MCP Servers
```bash
python test_mcp_servers.py
```

### Test Individual Platforms
```bash
# Gmail
python mcp_servers/email_mcp/test_email_mcp.py

# LinkedIn
python mcp_servers/linkedin_mcp/test_linkedin_mcp.py

# Instagram
python mcp_servers/instagram_mcp/test_instagram_mcp.py

# Facebook
python mcp_servers/facebook_mcp/test_facebook_mcp.py

# Twitter
python mcp_servers/twitter_mcp/test_twitter_mcp.py
```

### View Logs
```bash
tail -f Logs/YYYY-MM-DD.json
```

---

## Production Deployment

### Before Going Live

1. ✅ All credentials configured
2. ✅ All MCP servers tested
3. ✅ Credentials rotated (if needed)
4. ✅ Logs monitored
5. ✅ Backup created
6. ✅ Security review completed

### Deployment Steps

1. Update `.env` with production credentials
2. Run verification: `python config.py`
3. Test all servers: `python test_mcp_servers.py`
4. Start orchestrator: `python orchestrator.py`
5. Monitor logs: `tail -f Logs/YYYY-MM-DD.json`
6. Set up alerts for errors

### Monitoring

- Check logs daily
- Monitor API usage
- Verify token expiry dates
- Test credentials weekly
- Rotate tokens on schedule

---

## Support

For issues:
1. Check platform-specific documentation
2. Review error messages in logs
3. Verify token scopes and permissions
4. Test individual MCP servers
5. Check `.env` file format

