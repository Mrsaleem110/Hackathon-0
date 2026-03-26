# Real Credentials Setup - Summary

**Created**: 2026-03-26
**Status**: Ready to Use

## 📦 What Was Created

### 1. Interactive Setup Script
**File:** `setup_real_credentials.py`
- Interactive prompts for Instagram & Facebook credentials
- Built-in validation
- Automatic .env file updates
- Verification after setup

### 2. Credential Validator
**File:** `validate_credentials.py`
- Validates credential format
- Tests API connections
- Provides detailed feedback
- Helps troubleshoot issues

### 3. Documentation
**Files:**
- `SETUP_REAL_CREDENTIALS.md` - Complete setup guide
- `REAL_CREDENTIALS_GUIDE.md` - Detailed reference
- `CREDENTIALS_QUICK_REFERENCE.md` - Quick cheat sheet

---

## 🚀 Quick Start

### Step 1: Get Your Credentials (5 minutes)

Go to: https://developers.facebook.com/tools/explorer/

**For Instagram:**
1. Generate Access Token (scopes: `instagram_basic`, `pages_manage_posts`)
2. Run: `GET /me/instagram_business_accounts`
3. Copy token and account ID

**For Facebook:**
1. Generate Access Token (scopes: `pages_manage_posts`, `pages_read_engagement`)
2. Run: `GET /me/accounts`
3. Copy token and page ID

### Step 2: Run Setup Script (1 minute)

```bash
python setup_real_credentials.py
```

The script will:
- Show setup guides
- Prompt for credentials
- Validate input
- Update .env file
- Verify setup

### Step 3: Validate (1 minute)

```bash
python validate_credentials.py
```

Should show all credentials as valid and API connections working.

---

## 📋 What You Need

- ✅ Instagram Business Account
- ✅ Facebook Page
- ✅ Facebook Developer Account (free)
- ✅ 5 minutes

---

## 🔐 Security

**Important:**
- Never commit .env to git
- Keep tokens secret (like passwords)
- Tokens expire after 60 days
- Rotate every 90 days
- Use environment variables in production

---

## ✅ Verification

After setup, verify with:

```bash
# Check configuration
python config.py

# Validate credentials
python validate_credentials.py

# Test posting
python auto_post_social.py --platform instagram --caption "Test!"
python auto_post_social.py --platform facebook --message "Test!"

# View dashboard
python social_dashboard.py
```

---

## 📚 Files Reference

| File | Purpose |
|------|---------|
| `setup_real_credentials.py` | Interactive setup script |
| `validate_credentials.py` | Credential validator & tester |
| `SETUP_REAL_CREDENTIALS.md` | Complete setup guide |
| `REAL_CREDENTIALS_GUIDE.md` | Detailed reference |
| `CREDENTIALS_QUICK_REFERENCE.md` | Quick cheat sheet |

---

## 🎯 Next Steps

1. ✅ Run `python setup_real_credentials.py`
2. ✅ Run `python validate_credentials.py`
3. ✅ Test with `python auto_post_social.py`
4. ✅ Monitor with `python social_dashboard.py`
5. ✅ Start with `python orchestrator.py`

---

## 🆘 Troubleshooting

**Invalid Token?**
- Generate new token from Graph API Explorer
- Verify scopes are correct

**Account ID not found?**
- Run: `GET /me/instagram_business_accounts`
- Copy the `id` field

**Page ID not found?**
- Run: `GET /me/accounts`
- Copy the `id` field of your page

**API Connection Failed?**
- Check token hasn't expired (60 days)
- Verify token has correct scopes
- Try regenerating token

---

## 💡 Pro Tips

1. **Use Graph API Explorer** - Easiest way to get tokens
2. **Test before production** - Always validate first
3. **Keep tokens safe** - Treat like passwords
4. **Monitor usage** - Check in developer console
5. **Rotate regularly** - Every 90 days

---

**Ready to add real credentials? Run: `python setup_real_credentials.py`** 🚀
