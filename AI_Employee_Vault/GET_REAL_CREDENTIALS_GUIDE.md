# Get Real Instagram & Facebook Credentials - Complete Guide

## Overview

This guide will help you get real credentials for Instagram and Facebook to replace the demo tokens.

---

## Instagram Credentials Setup

### Step 1: Create a Facebook Business Account

1. Go to https://business.facebook.com/
2. Click "Create Account"
3. Fill in your business details
4. Verify your email

### Step 2: Create an Instagram Business Account

1. In Facebook Business Manager, go to **Settings** → **Instagram Accounts**
2. Click **Add**
3. Connect your existing Instagram account or create a new one
4. Make sure it's set to **Business Account** (not Personal)

### Step 3: Get Instagram Access Token

1. Go to https://developers.facebook.com/
2. Create an App (if you don't have one):
   - Click **My Apps** → **Create App**
   - Choose **Business** type
   - Fill in app details
3. Add **Instagram Basic Display** product:
   - Go to **Products** → **Add Products**
   - Search for "Instagram Basic Display"
   - Click **Set Up**
4. Generate Access Token:
   - Go to **Tools** → **Graph API Explorer**
   - Select your app from dropdown
   - Select your Instagram Business Account
   - Click **Generate Access Token**
   - Copy the token (it will look like: `IGABxxxxxxxxxxxxxx...`)

### Step 4: Get Instagram Business Account ID

1. In Graph API Explorer, run this query:
   ```
   GET /me?fields=id,name
   ```
2. Copy the `id` field (it will look like: `17841400000000`)

### Instagram Credentials Summary

You need:
- **INSTAGRAM_ACCESS_TOKEN**: `IGABxxxxxxxxxxxxxx...`
- **INSTAGRAM_BUSINESS_ACCOUNT_ID**: `17841400000000`
- **INSTAGRAM_USERNAME**: Your Instagram handle (optional)

---

## Facebook Credentials Setup

### Step 1: Create a Facebook App

1. Go to https://developers.facebook.com/
2. Click **My Apps** → **Create App**
3. Choose **Business** type
4. Fill in app details:
   - App Name: "AI Employee Vault"
   - App Purpose: "Business"
5. Click **Create App**

### Step 2: Add Facebook Login Product

1. In your app dashboard, go to **Products**
2. Search for "Facebook Login"
3. Click **Set Up**
4. Choose **Web** as your platform

### Step 3: Get Facebook Page Access Token

1. Go to **Settings** → **Basic**
2. Copy your **App ID** and **App Secret**
3. Go to **Tools** → **Graph API Explorer**
4. Select your app from dropdown
5. In the dropdown next to your app, select your Facebook Page
6. Click **Generate Access Token**
7. Copy the token (it will look like: `EAABxxxxxxxxxxxxxx...`)

### Step 4: Get Facebook Page ID

1. Go to your Facebook Page
2. Click **Settings** → **Page Info**
3. Copy the **Page ID** (it will look like: `123456789`)

Alternatively, in Graph API Explorer:
```
GET /me?fields=id,name
```

### Facebook Credentials Summary

You need:
- **FACEBOOK_ACCESS_TOKEN**: `EAABxxxxxxxxxxxxxx...`
- **FACEBOOK_PAGE_ID**: `123456789`

---

## Add Credentials to Your System

### Option 1: Interactive Script (Recommended)

```bash
python add_real_insta_fb_credentials.py
```

This will:
1. Ask for Instagram credentials
2. Ask for Facebook credentials
3. Validate the input
4. Save to .env file
5. Verify everything is working

### Option 2: Manual Edit

Edit `.env` file and replace:

```env
# Instagram Configuration
INSTAGRAM_ACCESS_TOKEN=your_real_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id_here
INSTAGRAM_USERNAME=your_instagram_handle

# Facebook Configuration
FACEBOOK_ACCESS_TOKEN=your_real_token_here
FACEBOOK_PAGE_ID=your_page_id_here
```

### Option 3: Environment Variables

```bash
export INSTAGRAM_ACCESS_TOKEN="your_real_token_here"
export INSTAGRAM_BUSINESS_ACCOUNT_ID="your_account_id_here"
export FACEBOOK_ACCESS_TOKEN="your_real_token_here"
export FACEBOOK_PAGE_ID="your_page_id_here"
```

---

## Verify Credentials

### Check Configuration Status

```bash
python config.py
```

This will show:
- [OK] Instagram API configured
- [OK] Facebook API configured

### Test Credentials

```bash
python test_insta_fb.py
```

This will:
- Test Instagram connection
- Test Facebook connection
- Show any errors

---

## Security Best Practices

### DO:
- ✅ Keep .env file secure
- ✅ Never commit .env to git
- ✅ Use strong, unique tokens
- ✅ Rotate tokens regularly
- ✅ Use environment variables in production
- ✅ Add .env to .gitignore

### DON'T:
- ❌ Share your tokens
- ❌ Commit .env to git
- ❌ Use demo tokens in production
- ❌ Hardcode credentials in code
- ❌ Post tokens in public forums
- ❌ Use the same token for multiple apps

---

## Troubleshooting

### "Invalid Access Token"
- Check token is correct and not expired
- Regenerate token from Facebook Developer Console
- Verify token has correct permissions

### "Account ID not found"
- Verify Instagram account is Business Account (not Personal)
- Check account ID is correct
- Regenerate token with correct account selected

### "Permission Denied"
- Check token has required permissions
- Verify app has Instagram Basic Display product added
- Check Facebook Page is connected to app

### "Connection Failed"
- Verify internet connection
- Check API endpoints are accessible
- Try regenerating token

---

## Next Steps

1. **Get Credentials**
   - Follow steps above to get real tokens

2. **Add to System**
   ```bash
   python add_real_insta_fb_credentials.py
   ```

3. **Verify Setup**
   ```bash
   python config.py
   python test_insta_fb.py
   ```

4. **Start Using**
   ```bash
   python auto_post_social.py
   python audit_dashboard.py dashboard
   ```

---

## Support

For issues:
1. Check troubleshooting section above
2. Review Facebook Developer Documentation
3. Check .env file is properly formatted
4. Verify tokens are not expired

---

**Generated**: 2026-03-28T11:28:11.532Z
**Status**: Ready to add real credentials
