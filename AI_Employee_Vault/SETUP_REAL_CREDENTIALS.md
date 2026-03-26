# Setup Real Instagram & Facebook Credentials - Complete Guide

**Last Updated**: 2026-03-26
**Status**: Ready to Use

## 🚀 Quick Start (5 minutes)

```bash
python setup_real_credentials.py
```

This interactive script will guide you through adding real credentials step-by-step.

---

## 📋 What You Need

Before starting, gather:
- ✅ Instagram Business Account (or create one)
- ✅ Facebook Page (or create one)
- ✅ Facebook Developer Account (free)
- ✅ 5 minutes of your time

---

## 🎯 Step-by-Step Setup

### Part 1: Get Instagram Credentials (2 minutes)

**Option A: Fastest Way (Recommended)**

1. **Open Graph API Explorer**
   ```
   https://developers.facebook.com/tools/explorer/
   ```

2. **Select Your App**
   - Click dropdown in top-right
   - Choose your app (or create one if needed)

3. **Generate Access Token**
   - Click "Generate Access Token"
   - Select scopes:
     - ✓ `instagram_basic`
     - ✓ `pages_manage_posts`
   - Click "Generate"
   - **Copy the token** (starts with `IGAB_`)

4. **Get Account ID**
   - In the query box, paste:
     ```
     GET /me/instagram_business_accounts
     ```
   - Click "Submit"
   - Find the response with `"id": "17841400000000"`
   - **Copy this ID** (17 digits)

**Result:**
```
INSTAGRAM_ACCESS_TOKEN=IGAB_1234567890abcdefghijklmnopqrstuvwxyz...
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000
```

---

### Part 2: Get Facebook Credentials (2 minutes)

**Option A: Fastest Way (Recommended)**

1. **Open Graph API Explorer**
   ```
   https://developers.facebook.com/tools/explorer/
   ```

2. **Select Your App**
   - Click dropdown in top-right
   - Choose your app (same as Instagram)

3. **Generate Access Token**
   - Click "Generate Access Token"
   - Select scopes:
     - ✓ `pages_manage_posts`
     - ✓ `pages_read_engagement`
   - Click "Generate"
   - **Copy the token** (starts with `EAAB_`)

4. **Get Page ID**
   - In the query box, paste:
     ```
     GET /me/accounts
     ```
   - Click "Submit"
   - Find your page in the response
   - **Copy the `id` field** (numeric)

**Result:**
```
FACEBOOK_ACCESS_TOKEN=EAAB_1234567890abcdefghijklmnopqrstuvwxyz...
FACEBOOK_PAGE_ID=1048264368365205
```

---

## 🔧 Running the Setup Script

### Interactive Setup

```bash
python setup_real_credentials.py
```

**What happens:**
1. Shows Instagram setup guide
2. Prompts for Instagram token and account ID
3. Shows Facebook setup guide
4. Prompts for Facebook token and page ID
5. Shows summary for confirmation
6. Updates .env file
7. Verifies credentials
8. Shows next steps

### Manual Setup (Alternative)

If you prefer to edit directly:

```bash
# Open .env file
code .env
# or
nano .env
```

Find and update these lines:

```env
# Instagram Configuration
INSTAGRAM_ACCESS_TOKEN=IGAB_your_real_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000

# Facebook Configuration
FACEBOOK_ACCESS_TOKEN=EAAB_your_real_token_here
FACEBOOK_PAGE_ID=1048264368365205
```

Save and close.

---

## ✅ Verify Your Setup

### Check Configuration

```bash
python config.py
```

Should show:
```
[OK] Instagram API configured
[OK] Facebook API configured
```

### Validate Credentials

```bash
python validate_credentials.py
```

Should show:
```
✓ Access Token: Token format valid
✓ Business Account ID: Account ID format valid
✓ Instagram API connection successful
✓ Facebook API connection successful
```

---

## 🧪 Test Your Credentials

### Test Instagram Posting

```bash
python auto_post_social.py --platform instagram --caption "Test post!" --image-url "https://example.com/image.jpg"
```

### Test Facebook Posting

```bash
python auto_post_social.py --platform facebook --message "Test post!" --link "https://example.com"
```

### View Dashboard

```bash
python social_dashboard.py
```

---

## 🔐 Security Best Practices

### ✅ DO:
- Keep .env in `.gitignore` (never commit)
- Treat tokens like passwords
- Rotate tokens every 90 days
- Use environment variables in production
- Monitor token usage
- Limit token permissions to minimum needed

### ❌ DON'T:
- Share tokens in messages/emails
- Commit .env to git
- Use same token for multiple apps
- Store tokens in code
- Log tokens to console
- Use tokens in URLs

### Token Rotation (Every 90 Days)

```bash
# 1. Generate new tokens from Graph API Explorer
# 2. Update .env file
# 3. Test with: python validate_credentials.py
# 4. Delete old tokens from developer console
```

---

## 🆘 Troubleshooting

### "Invalid Access Token"
**Solution:**
- Token may have expired (valid for 60 days)
- Generate new token from Graph API Explorer
- Verify token has correct scopes

### "Invalid Business Account ID"
**Solution:**
- Check ID is 17 digits
- Verify it's Instagram Business Account ID (not personal)
- Run: `GET /me/instagram_business_accounts` in Graph API Explorer

### "Invalid Page ID"
**Solution:**
- Check ID is numeric
- Verify it's your page's ID (not your personal ID)
- Run: `GET /me/accounts` in Graph API Explorer

### "Permission Denied"
**Solution:**
- Token may not have required scopes
- Generate new token with all required permissions
- Check token hasn't been revoked

### "Rate Limited"
**Solution:**
- Too many requests in short time
- Wait a few minutes before retrying
- Implement exponential backoff in code

### Credentials Not Loading
**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check .env has correct format
cat .env | grep INSTAGRAM
cat .env | grep FACEBOOK

# Reload config
python config.py
```

---

## 📚 Token Formats

### Instagram Token
- **Starts with:** `IGAB_`
- **Length:** 100+ characters
- **Example:** `IGAB_1234567890abcdefghijklmnopqrstuvwxyz...`
- **Expires:** 60 days

### Facebook Token
- **Starts with:** `EAAB_`
- **Length:** 100+ characters
- **Example:** `EAAB_1234567890abcdefghijklmnopqrstuvwxyz...`
- **Expires:** 60 days

### Account IDs
- **Instagram:** 17 digits (e.g., `17841400000000`)
- **Facebook:** 10-15 digits (e.g., `1048264368365205`)

---

## 🎯 Next Steps After Setup

### 1. Validate Credentials (1 minute)
```bash
python validate_credentials.py
```

### 2. Test Posting (2 minutes)
```bash
python auto_post_social.py --platform instagram --caption "Hello!"
python auto_post_social.py --platform facebook --message "Hello!"
```

### 3. View Dashboard (ongoing)
```bash
python social_dashboard.py
```

### 4. Start Orchestrator (production)
```bash
python orchestrator.py
```

---

## 📖 Useful Resources

| Resource | URL |
|----------|-----|
| Graph API Explorer | https://developers.facebook.com/tools/explorer/ |
| Developer Console | https://developers.facebook.com/ |
| Business Manager | https://business.facebook.com/ |
| Token Debugger | https://developers.facebook.com/tools/debug/token/ |
| Instagram API Docs | https://developers.facebook.com/docs/instagram-api |
| Facebook API Docs | https://developers.facebook.com/docs/graph-api |
| Permissions Reference | https://developers.facebook.com/docs/permissions |

---

## 🔗 API Endpoints

### Instagram Endpoints
```
POST /v18.0/{business_account_id}/media
GET /v18.0/{business_account_id}/media
GET /v18.0/{business_account_id}/insights
```

### Facebook Endpoints
```
POST /v18.0/{page_id}/feed
GET /v18.0/{page_id}/feed
GET /v18.0/{page_id}/insights
```

---

## 📝 Checklist

- [ ] Created Facebook Developer Account
- [ ] Created/Selected Instagram Business Account
- [ ] Created/Selected Facebook Page
- [ ] Generated Instagram Access Token
- [ ] Got Instagram Business Account ID
- [ ] Generated Facebook Access Token
- [ ] Got Facebook Page ID
- [ ] Ran `python setup_real_credentials.py`
- [ ] Ran `python validate_credentials.py`
- [ ] Tested posting with `python auto_post_social.py`
- [ ] Verified in dashboard with `python social_dashboard.py`
- [ ] Ready for production!

---

## 💡 Tips

1. **Use Graph API Explorer** - Easiest way to get tokens and test API calls
2. **Keep tokens safe** - Treat them like passwords
3. **Test before production** - Always validate credentials first
4. **Monitor usage** - Check token usage in developer console
5. **Rotate regularly** - Generate new tokens every 90 days

---

## 🆘 Need Help?

1. Check troubleshooting section above
2. Review .env file format
3. Run `python config.py` to check status
4. Run `python validate_credentials.py` to test
5. Check token scopes in developer console
6. Verify token hasn't expired

---

**You're all set! Your Instagram and Facebook credentials are now configured and ready to use.** 🎉
