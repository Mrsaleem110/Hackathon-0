# Add Real Instagram & Facebook Credentials - Quick Start

## Status: Ready to Add Real Credentials ✅

**Date**: 2026-03-28T11:29:14.655Z
**System**: AI Employee Vault - Credential Setup
**Status**: READY FOR REAL CREDENTIALS

---

## What You Need

### Instagram Credentials
- **Access Token**: `IGABxxxxxxxxxxxxxx...` (from Facebook Developer Console)
- **Business Account ID**: `17841400000000` (your Instagram Business Account ID)
- **Username**: Your Instagram handle (optional)

### Facebook Credentials
- **Page Access Token**: `EAABxxxxxxxxxxxxxx...` (from Facebook Developer Console)
- **Page ID**: `123456789` (your Facebook Page ID)

---

## How to Get Credentials

### Quick Steps:

1. **Go to Facebook Developer Console**
   - https://developers.facebook.com/

2. **Create an App** (if you don't have one)
   - My Apps → Create App → Business type

3. **Add Instagram Basic Display Product**
   - Products → Add Products → Instagram Basic Display

4. **Generate Access Tokens**
   - Tools → Graph API Explorer
   - Select your app and Instagram/Facebook account
   - Click "Generate Access Token"

5. **Get Account IDs**
   - Instagram: Business Account ID from settings
   - Facebook: Page ID from page settings

---

## Add Credentials to Your System

### Option 1: Interactive Script (Easiest)

```bash
python add_real_insta_fb_credentials.py
```

This will:
1. Ask for Instagram credentials
2. Ask for Facebook credentials
3. Validate the input
4. Save to .env file
5. Verify everything works

### Option 2: Manual Edit

Edit `.env` file:

```env
INSTAGRAM_ACCESS_TOKEN=your_real_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id_here
INSTAGRAM_USERNAME=your_handle
FACEBOOK_ACCESS_TOKEN=your_real_token_here
FACEBOOK_PAGE_ID=your_page_id_here
```

---

## Verify Setup

### Check Configuration

```bash
python config.py
```

Expected output:
```
[OK] Instagram API configured
[OK] Facebook API configured
```

### Test Credentials

```bash
python test_insta_fb.py
```

This will test:
- Instagram connection
- Facebook connection
- Token validity

---

## Start Using

### Post to Instagram

```bash
python auto_post_social.py
# Select Instagram
# Enter caption and image URL
```

### Post to Facebook

```bash
python auto_post_social.py
# Select Facebook
# Enter message and link
```

### Monitor Dashboard

```bash
python audit_dashboard.py dashboard
```

### View Social Media Metrics

```bash
python social_dashboard.py
```

---

## Files Created

### Setup Script
- `add_real_insta_fb_credentials.py` - Interactive credential setup

### Documentation
- `GET_REAL_CREDENTIALS_GUIDE.md` - Complete step-by-step guide

### Existing Tools
- `config.py` - Check configuration status
- `test_insta_fb.py` - Test credentials
- `auto_post_social.py` - Post to social media
- `social_dashboard.py` - Monitor social media

---

## Security Checklist

- ✅ Keep .env file secure
- ✅ Never commit .env to git
- ✅ Use strong, unique tokens
- ✅ Rotate tokens regularly
- ✅ Add .env to .gitignore
- ✅ Don't share tokens

---

## Next Steps

1. **Get Real Credentials**
   - Follow GET_REAL_CREDENTIALS_GUIDE.md

2. **Add to System**
   ```bash
   python add_real_insta_fb_credentials.py
   ```

3. **Verify Setup**
   ```bash
   python config.py
   python test_insta_fb.py
   ```

4. **Start Posting**
   ```bash
   python auto_post_social.py
   ```

5. **Monitor**
   ```bash
   python audit_dashboard.py dashboard
   ```

---

## Troubleshooting

### Invalid Token
- Regenerate from Facebook Developer Console
- Check token is not expired
- Verify correct permissions

### Account Not Found
- Verify Instagram account is Business Account
- Check account ID is correct
- Regenerate token with correct account

### Permission Denied
- Check token has required permissions
- Verify app has Instagram Basic Display product
- Check Facebook Page is connected

---

## Support Resources

- **Setup Guide**: GET_REAL_CREDENTIALS_GUIDE.md
- **Configuration**: config.py
- **Testing**: test_insta_fb.py
- **Posting**: auto_post_social.py
- **Monitoring**: social_dashboard.py

---

## Summary

You now have:
✅ Interactive credential setup script
✅ Complete step-by-step guide
✅ Validation and verification tools
✅ Security best practices
✅ Testing capabilities
✅ Posting functionality
✅ Monitoring dashboard

**Ready to add real Instagram and Facebook credentials!**

---

**Generated**: 2026-03-28T11:29:14.655Z
**Status**: READY FOR REAL CREDENTIALS
**Next**: Run `python add_real_insta_fb_credentials.py`
