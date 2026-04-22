# Real Credentials Setup - Complete Implementation

## Overview

You now have a complete system for adding real credentials to AI Employee Vault. The system supports 6 platforms with multiple setup methods.

## Files Created

### 1. Documentation
- **CREDENTIALS_SETUP_GUIDE.md** - Comprehensive platform-by-platform setup guide
- **REAL_CREDENTIALS_QUICK_START.md** - Quick reference for fast setup
- **CREDENTIALS_MANAGEMENT_GUIDE.md** - Complete management and troubleshooting guide

### 2. Setup Scripts
- **setup_real_credentials.py** - Interactive setup for all platforms
- **setup_credentials.py** - Non-interactive setup with CLI arguments

## Supported Platforms

| Platform | Setup Time | Auth Type | Expiry |
|----------|-----------|-----------|--------|
| Gmail | 5 min | OAuth 2.0 | 1 hour (auto-refresh) |
| LinkedIn | 5 min | OAuth 2.0 | 60 days |
| Instagram | 2 min | Access Token | 60 days |
| Facebook | 2 min | Access Token | 60 days |
| Twitter/X | 5 min | Bearer Token | Indefinite |
| WhatsApp | 2 min | Session | 30 days (inactive) |

## Quick Start

### Option 1: Interactive Setup
```bash
python setup_real_credentials.py
```
Guides you through each platform with instructions and links.

### Option 2: Command-Line Setup
```bash
python setup_credentials.py --guides
python setup_credentials.py --verify
python setup_credentials.py --from-env
```

### Option 3: Environment Variables
```bash
export GMAIL_CLIENT_ID="your_id"
export GMAIL_CLIENT_SECRET="your_secret"
export INSTAGRAM_ACCESS_TOKEN="your_token"
export INSTAGRAM_BUSINESS_ACCOUNT_ID="your_account_id"
python setup_credentials.py --from-env
```

## Setup Instructions by Platform

### Gmail (5 minutes)
1. Go to https://console.cloud.google.com/
2. Create project → Enable Gmail API
3. Create OAuth 2.0 credentials (Desktop app)
4. Download JSON and extract client_id and client_secret

### LinkedIn (5 minutes)
1. Go to https://www.linkedin.com/developers/apps
2. Create app → Go to Auth tab
3. Copy Client ID and Client Secret
4. Generate access token with OAuth flow

### Instagram (2 minutes)
1. Go to https://developers.facebook.com/tools/explorer/
2. Select your app → Generate Access Token
3. Choose scopes: instagram_basic, pages_manage_posts
4. Query: GET /me/instagram_business_accounts
5. Copy token and account ID

### Facebook (2 minutes)
1. Go to https://developers.facebook.com/tools/explorer/
2. Select your app → Generate Access Token
3. Choose scopes: pages_manage_posts, pages_read_engagement
4. Query: GET /me/accounts
5. Copy token and page ID

### Twitter/X (5 minutes)
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Go to Keys and tokens tab
3. Copy: Bearer Token, API Key, API Secret, Access Token, Access Token Secret

### WhatsApp (2 minutes)
1. Start orchestrator: python orchestrator.py
2. Scan QR code with WhatsApp mobile app
3. Session saved to .whatsapp_session

## Verification

After setup, verify credentials are configured:

```bash
# Check configuration status
python config.py

# Test all MCP servers
python test_mcp_servers.py

# Verify specific credentials
python setup_credentials.py --verify
```

## Environment Variables

All credentials are stored in `.env`:

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

## Security Best Practices

1. **Never commit .env** - It's in .gitignore
2. **Keep tokens secret** - Treat like passwords
3. **Rotate regularly** - Every 50-90 days
4. **Monitor usage** - Check API dashboards
5. **Limit scopes** - Only request needed permissions
6. **Backup sessions** - Keep .whatsapp_session safe

## Token Rotation Schedule

| Platform | Expiry | Action | Frequency |
|----------|--------|--------|-----------|
| Gmail | 1 hour | Auto-refresh | Automatic |
| LinkedIn | 60 days | Regenerate | Every 50 days |
| Instagram | 60 days | Regenerate | Every 50 days |
| Facebook | 60 days | Regenerate | Every 50 days |
| Twitter | Indefinite | Monitor | Quarterly |
| WhatsApp | 30 days | Re-scan QR | If inactive |

## Next Steps

1. **Get credentials** - Follow platform-specific instructions above
2. **Run setup** - Use interactive or CLI setup
3. **Verify** - Run `python config.py`
4. **Test** - Run `python test_mcp_servers.py`
5. **Start** - Run `python orchestrator.py`
6. **Monitor** - Check logs: `tail -f Logs/YYYY-MM-DD.json`

## Troubleshooting

### "Invalid credentials" error
- Check token format (no extra spaces)
- Verify token hasn't expired
- Regenerate from platform dashboard

### "Insufficient permissions" error
- Add required scopes to token
- Regenerate with correct scopes
- Check app permissions in settings

### "Rate limit exceeded" error
- Wait before retrying (usually 15 minutes)
- Check API quota in dashboard
- Consider upgrading API tier

### WhatsApp QR code not appearing
- Ensure WhatsApp is installed on phone
- Check terminal output
- Try scanning again

## Documentation Files

- **CREDENTIALS_SETUP_GUIDE.md** - Complete setup guide with all details
- **REAL_CREDENTIALS_QUICK_START.md** - Quick reference card
- **CREDENTIALS_MANAGEMENT_GUIDE.md** - Management, rotation, and troubleshooting

## Support

For issues:
1. Check platform-specific documentation
2. Review error messages in logs
3. Verify token scopes and permissions
4. Test individual MCP servers
5. Check .env file format

