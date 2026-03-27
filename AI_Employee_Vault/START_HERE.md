# 🚀 REAL CREDENTIALS - START HERE

**Time**: 5 minutes | **Difficulty**: Easy | **Status**: Ready

---

## 📋 What You Need

- Instagram Business Account
- Facebook Page
- Facebook Developer Account (free)
- 5 minutes

---

## ⚡ Quick Start

### 1️⃣ Get Credentials (2 min)

Go to: https://developers.facebook.com/tools/explorer/

**Instagram:**
- Generate Token → scopes: `instagram_basic`, `pages_manage_posts`
- Copy token (IGAB_...)
- Run: `GET /me/instagram_business_accounts`
- Copy account ID (17 digits)

**Facebook:**
- Generate Token → scopes: `pages_manage_posts`, `pages_read_engagement`
- Copy token (EAAB_...)
- Run: `GET /me/accounts`
- Copy page ID (numeric)

### 2️⃣ Add to Project (2 min)

```bash
# Edit this file
code add_credentials_manual.py

# Replace lines 10-15 with your credentials:
INSTAGRAM_ACCESS_TOKEN = "IGAB_your_token_here"
INSTAGRAM_BUSINESS_ACCOUNT_ID = "17841400000000"
FACEBOOK_ACCESS_TOKEN = "EAAB_your_token_here"
FACEBOOK_PAGE_ID = "1048264368365205"

# Save and run
python add_credentials_manual.py
```

### 3️⃣ Verify (1 min)

```bash
python validate_credentials.py
```

---

## ✅ Done!

Your credentials are now configured. Test with:

```bash
# Test Instagram
python auto_post_social.py --platform instagram --caption "Test!"

# Test Facebook
python auto_post_social.py --platform facebook --message "Test!"

# View dashboard
python social_dashboard.py

# Start system
python orchestrator.py
```

---

## 📚 Need Help?

| Question | File |
|----------|------|
| Step-by-step guide? | `GET_CREDENTIALS_VISUAL_GUIDE.md` |
| Quick reference? | `CREDENTIALS_QUICK_REFERENCE.md` |
| Complete guide? | `SETUP_REAL_CREDENTIALS.md` |
| Full package? | `REAL_CREDENTIALS_COMPLETE_PACKAGE.md` |

---

## 🔐 Security

✅ Keep .env secret (never commit to git)
✅ Treat tokens like passwords
✅ Rotate every 90 days

---

## 🆘 Issues?

**Token invalid?** → Regenerate from Graph API Explorer
**Account ID not found?** → Run `GET /me/instagram_business_accounts`
**Page ID not found?** → Run `GET /me/accounts`
**Validation fails?** → Check token format (IGAB_ or EAAB_)

---

**Ready? Start with:** `python add_credentials_manual.py`
