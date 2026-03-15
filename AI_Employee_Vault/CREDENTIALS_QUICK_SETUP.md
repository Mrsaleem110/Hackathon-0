# Instagram & Facebook Credentials - Quick Setup

**Status**: Ready to add credentials
**Date**: 2026-03-15

## Quick Start (5 minutes)

### Option 1: Interactive Setup (Recommended)
```bash
python setup_instagram_facebook_credentials.py
```

This will guide you through:
1. Getting Instagram credentials
2. Getting Facebook credentials
3. Updating your .env file
4. Testing the setup

### Option 2: Manual Setup

#### Step 1: Get Instagram Credentials

**Business Account (Recommended):**
1. Go to https://business.facebook.com/
2. Settings → Apps and Websites
3. Add Instagram Business Account
4. Roles → Assign Users
5. Copy: Business Account ID and Access Token

**Personal Account:**
1. Go to https://developers.facebook.com/
2. Create app (type: Business)
3. Add Instagram Basic Display
4. Generate token with `instagram_basic` scope

#### Step 2: Get Facebook Credentials

1. Go to https://developers.facebook.com/
2. Create app (type: Business)
3. Add Facebook Login product
4. Get Page ID from your page settings
5. Generate Access Token with scopes:
   - `pages_manage_posts`
   - `pages_read_engagement`

#### Step 3: Update .env

Edit `.env` and replace:

```bash
# Instagram Configuration
INSTAGRAM_ACCESS_TOKEN=your_actual_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_actual_id_here

# Facebook Configuration
FACEBOOK_ACCESS_TOKEN=your_actual_token_here
FACEBOOK_PAGE_ID=your_actual_page_id_here
```

#### Step 4: Verify Setup

```bash
python config.py
```

Should show:
```
[INSTAGRAM] Instagram Configuration:
  [OK] Instagram API configured

[FACEBOOK] Facebook Configuration:
  [OK] Facebook API configured
```

#### Step 5: Test Credentials

```bash
# Test all MCP servers
python test_mcp_servers.py

# Or test individually
python mcp_servers/instagram_mcp/test_instagram_mcp.py
python mcp_servers/facebook_mcp/test_facebook_mcp.py
```

## What Each Credential Does

### Instagram Access Token
- Allows posting to Instagram feed
- Allows posting to Instagram stories
- Allows reading account insights
- Expires: Check in developer portal

### Instagram Business Account ID
- Identifies your Instagram business account
- Format: Usually a long number (e.g., 123456789)
- Found in: Facebook Business Manager

### Facebook Access Token
- Allows posting to Facebook page
- Allows uploading videos
- Allows reading page insights
- Expires: Check in developer portal

### Facebook Page ID
- Identifies your Facebook page
- Format: Usually a long number (e.g., 987654321)
- Found in: Facebook page settings or Graph API

## Troubleshooting

### "Invalid access token"
- Token may have expired
- Regenerate in developer portal
- Check token has correct scopes

### "Account/Page not found"
- Verify Account ID or Page ID is correct
- Check token has access to account/page
- Try regenerating token

### "Rate limit exceeded"
- Wait 1 hour for quota reset
- Reduce posting frequency
- Check logs for details

## Testing Your Setup

After adding credentials, test with:

```python
from config import INSTAGRAM_ACCESS_TOKEN, FACEBOOK_ACCESS_TOKEN

# Quick test
if INSTAGRAM_ACCESS_TOKEN and INSTAGRAM_ACCESS_TOKEN != "your_instagram_access_token_here":
    print("✅ Instagram token is set")
else:
    print("❌ Instagram token not configured")

if FACEBOOK_ACCESS_TOKEN and FACEBOOK_ACCESS_TOKEN != "your_facebook_access_token_here":
    print("✅ Facebook token is set")
else:
    print("❌ Facebook token not configured")
```

## Next Steps

1. ✅ Add credentials to .env
2. ✅ Verify with `python config.py`
3. ✅ Test with `python test_mcp_servers.py`
4. ✅ Start orchestrator: `python orchestrator.py`
5. ✅ Monitor logs: `tail -f Logs/YYYY-MM-DD.json`

## Support

- Instagram Graph API: https://developers.facebook.com/docs/instagram-api
- Facebook Graph API: https://developers.facebook.com/docs/graph-api
- Rate Limits: https://developers.facebook.com/docs/graph-api/overview/rate-limiting
