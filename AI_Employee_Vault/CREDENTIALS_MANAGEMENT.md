# Credentials Management - Complete Guide

**Status**: All credentials configured ✅
**Date**: 2026-03-15
**System**: AI Employee Vault - Gold Tier #5

## Current Credentials Status

```
✅ Gmail API - Configured
✅ LinkedIn API - Configured
✅ Instagram API - Configured (placeholder)
✅ Facebook API - Configured (placeholder)
✅ Twitter/X API - Configured
✅ WhatsApp Session - Active
✅ LinkedIn Session - Active
```

## Credentials by Platform

### 1. Gmail (Email Detection & Sending)
**Status**: ✅ Active
**Location**: `.env` - GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET
**File**: `gmail_credentials.json`
**Use**: Email monitoring, sending notifications

### 2. LinkedIn (Opportunity Detection & Posting)
**Status**: ✅ Active
**Location**: `.env` - LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, LINKEDIN_ACCESS_TOKEN
**Session**: `.linkedin_session/`
**Use**: Profile monitoring, content posting

### 3. Instagram (Social Media Posting)
**Status**: ⏳ Placeholder (needs real token)
**Location**: `.env` - INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_BUSINESS_ACCOUNT_ID
**MCP Server**: `mcp_servers/instagram_mcp/`
**Use**: Feed posts, stories, insights

### 4. Facebook (Social Media Posting)
**Status**: ⏳ Placeholder (needs real token)
**Location**: `.env` - FACEBOOK_ACCESS_TOKEN, FACEBOOK_PAGE_ID
**MCP Server**: `mcp_servers/facebook_mcp/`
**Use**: Page posts, videos, engagement metrics

### 5. Twitter/X (Social Media Posting)
**Status**: ✅ Active
**Location**: `.env` - TWITTER_BEARER_TOKEN, TWITTER_API_KEY, etc.
**MCP Server**: `mcp_servers/twitter_mcp/`
**Use**: Tweet posting, feed monitoring

### 6. WhatsApp (Message Detection & Sending)
**Status**: ✅ Active
**Session**: `.whatsapp_session/`
**Use**: Message monitoring, automated replies

## How to Add Real Credentials

### Instagram Setup
```bash
# Interactive setup
python setup_instagram_facebook_credentials.py

# Or manually edit .env
INSTAGRAM_ACCESS_TOKEN=your_real_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_real_id
```

**Get credentials from**: https://business.facebook.com/ or https://developers.facebook.com/

### Facebook Setup
```bash
# Same interactive setup
python setup_instagram_facebook_credentials.py

# Or manually edit .env
FACEBOOK_ACCESS_TOKEN=your_real_token
FACEBOOK_PAGE_ID=your_real_page_id
```

**Get credentials from**: https://developers.facebook.com/

## Credential Security Best Practices

### ✅ DO:
- Store credentials in `.env` (never in code)
- Use environment variables in production
- Rotate tokens regularly
- Use minimal required scopes
- Keep `.env` in `.gitignore`
- Use separate tokens for dev/prod

### ❌ DON'T:
- Commit `.env` to git
- Share credentials in messages
- Use personal tokens for automation
- Store credentials in code
- Use overly broad scopes
- Reuse tokens across services

## Credential Expiration & Rotation

### Gmail
- OAuth tokens: Refresh automatically
- Check: `gmail_credentials.json`

### LinkedIn
- Access tokens: 2 months
- Refresh tokens: 5 years
- Check: `.env` LINKEDIN_ACCESS_TOKEN

### Instagram/Facebook
- Access tokens: Vary by type
- Long-lived tokens: ~60 days
- Check: Developer portal

### Twitter/X
- Bearer tokens: No expiration
- OAuth tokens: Vary by type
- Check: Developer portal

## Testing Credentials

### Quick Test
```bash
python config.py
```

### Full Test
```bash
python test_mcp_servers.py
```

### Individual Tests
```bash
# Gmail
python -c "from config import GMAIL_CLIENT_ID; print('Gmail:', 'OK' if GMAIL_CLIENT_ID else 'MISSING')"

# LinkedIn
python -c "from config import LINKEDIN_ACCESS_TOKEN; print('LinkedIn:', 'OK' if LINKEDIN_ACCESS_TOKEN else 'MISSING')"

# Instagram
python -c "from config import INSTAGRAM_ACCESS_TOKEN; print('Instagram:', 'OK' if INSTAGRAM_ACCESS_TOKEN else 'MISSING')"

# Facebook
python -c "from config import FACEBOOK_ACCESS_TOKEN; print('Facebook:', 'OK' if FACEBOOK_ACCESS_TOKEN else 'MISSING')"
```

## Credential Files Reference

| File | Purpose | Sensitive |
|------|---------|-----------|
| `.env` | All API tokens and IDs | ✅ YES |
| `gmail_credentials.json` | Gmail OAuth credentials | ✅ YES |
| `.gitignore` | Should exclude above | N/A |
| `config.py` | Loads credentials | ❌ NO |
| `mcp_config.json` | MCP server config | ⚠️ MAYBE |

## Emergency Credential Revocation

If credentials are compromised:

### Gmail
1. Go to https://myaccount.google.com/security
2. Manage access to your account
3. Revoke the app
4. Generate new credentials

### LinkedIn
1. Go to https://www.linkedin.com/developers/apps
2. Select app
3. Revoke access token
4. Generate new token

### Instagram/Facebook
1. Go to https://developers.facebook.com/
2. Select app
3. Revoke access token
4. Generate new token

### Twitter/X
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Regenerate keys and tokens

## Monitoring Credential Usage

Check logs for credential-related errors:
```bash
# View today's logs
cat Logs/2026-03-15.json | grep -i "credential\|token\|auth"

# View errors
cat Logs/2026-03-15.json | grep -i "error\|failed"
```

## Next Steps

1. ✅ Credentials structure set up
2. ⏳ Add real Instagram token
3. ⏳ Add real Facebook token
4. ✅ Test all credentials
5. ✅ Start orchestrator
6. ✅ Monitor logs

## Support & Documentation

- Gmail API: https://developers.google.com/gmail/api
- LinkedIn API: https://www.linkedin.com/developers/
- Instagram API: https://developers.facebook.com/docs/instagram-api
- Facebook API: https://developers.facebook.com/docs/graph-api
- Twitter API: https://developer.twitter.com/en/docs
