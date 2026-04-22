# Real Credentials Quick Reference

Fast setup guide for adding real credentials to AI Employee Vault.

## Quick Start

```bash
python setup_real_credentials.py
```

The script will guide you through getting credentials for each platform.

---

## Platform Credentials Needed

### 1. Gmail (5 min)
- **Where**: https://console.cloud.google.com/
- **Get**: Client ID, Client Secret
- **Steps**: Create project → Enable Gmail API → Create OAuth 2.0 credentials

### 2. LinkedIn (5 min)
- **Where**: https://www.linkedin.com/developers/apps
- **Get**: Client ID, Client Secret, Access Token
- **Steps**: Create app → Go to Auth tab → Generate token

### 3. Instagram (2 min)
- **Where**: https://developers.facebook.com/tools/explorer/
- **Get**: Access Token (IGAB_...), Business Account ID
- **Steps**: Select app → Generate token → Query `/me/instagram_business_accounts`

### 4. Facebook (2 min)
- **Where**: https://developers.facebook.com/tools/explorer/
- **Get**: Access Token (EAAB_...), Page ID
- **Steps**: Select app → Generate token → Query `/me/accounts`

### 5. Twitter/X (5 min)
- **Where**: https://developer.twitter.com/en/portal/dashboard
- **Get**: Bearer Token, API Key, API Secret, Access Token, Access Token Secret
- **Steps**: Go to Keys and tokens tab → Copy all credentials

### 6. WhatsApp (Session-based)
- **No setup needed** - QR code scan on first run
- Session saved to `.whatsapp_session`

---

## Environment Variables

After setup, your `.env` file will contain:

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

After setup, verify credentials are configured:

```bash
python config.py
```

Output will show which platforms are ready:
```
[OK] Gmail API configured
[OK] LinkedIn API configured
[OK] Instagram API configured
[OK] Facebook API configured
[OK] Twitter API configured
```

---

## Testing

Test all MCP servers with real credentials:

```bash
python test_mcp_servers.py
```

Test individual platforms:

```bash
python mcp_servers/instagram_mcp/test_instagram_mcp.py
python mcp_servers/facebook_mcp/test_facebook_mcp.py
python mcp_servers/twitter_mcp/test_twitter_mcp.py
```

---

## Security Best Practices

1. **Never commit .env** - It's in `.gitignore`
2. **Keep tokens secret** - Treat like passwords
3. **Rotate regularly** - Every 90 days
4. **Monitor usage** - Check API dashboards
5. **Limit scopes** - Only request needed permissions
6. **Backup sessions** - Keep `.whatsapp_session` safe

---

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
- Wait before retrying
- Check API quota in dashboard
- Consider upgrading API tier

### WhatsApp QR code not appearing
- Ensure WhatsApp is installed on phone
- Check terminal output
- Try scanning again

---

## Next Steps

1. Run setup: `python setup_real_credentials.py`
2. Verify: `python config.py`
3. Test: `python test_mcp_servers.py`
4. Start: `python orchestrator.py`
5. Monitor: `tail -f Logs/YYYY-MM-DD.json`

