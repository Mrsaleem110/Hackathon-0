# Quick Reference - Instagram & Facebook Credentials

## 🚀 Quick Start (2 minutes)

```bash
python add_real_credentials.py
```

---

## 📱 Instagram - Get Credentials in 3 Steps

### Step 1: Go to Facebook Developers
https://developers.facebook.com/tools/explorer/

### Step 2: Generate Token
- Select your app (top-right)
- Click "Generate Access Token"
- Choose scopes: `instagram_basic`, `pages_manage_posts`
- Copy token (starts with `IGAB_`)

### Step 3: Get Account ID
- Run query: `GET /me/instagram_business_accounts`
- Copy the `id` field (17 digits)

**Result:**
```
INSTAGRAM_ACCESS_TOKEN=IGAB_xxxxx...
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000
```

---

## 📘 Facebook - Get Credentials in 3 Steps

### Step 1: Go to Facebook Developers
https://developers.facebook.com/tools/explorer/

### Step 2: Generate Token
- Select your app (top-right)
- Click "Generate Access Token"
- Choose scopes: `pages_manage_posts`, `pages_read_engagement`
- Copy token (starts with `EAAB_`)

### Step 3: Get Page ID
- Run query: `GET /me/accounts`
- Copy the `id` field of your page

**Result:**
```
FACEBOOK_ACCESS_TOKEN=EAAB_xxxxx...
FACEBOOK_PAGE_ID=1048264368365205
```

---

## ✅ Verify Setup

```bash
# Check configuration
python config.py

# Test credentials
python test_insta_fb.py

# View dashboard
python social_dashboard.py
```

---

## 🔗 Useful Links

| Task | URL |
|------|-----|
| Graph API Explorer | https://developers.facebook.com/tools/explorer/ |
| Developer Console | https://developers.facebook.com/ |
| Business Manager | https://business.facebook.com/ |
| Token Debugger | https://developers.facebook.com/tools/debug/token/ |
| API Reference | https://developers.facebook.com/docs/graph-api |

---

## ⚠️ Important

- **Never commit .env to git**
- **Keep tokens secret** (treat like passwords)
- **Tokens expire** (generate new ones every 60 days)
- **Rotate regularly** (every 90 days recommended)

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Invalid token | Generate new token from Graph API Explorer |
| Permission denied | Add required scopes when generating token |
| Account ID not found | Run `GET /me/instagram_business_accounts` |
| Page ID not found | Run `GET /me/accounts` |
| Token expired | Generate new token (valid for 60 days) |

---

## 📝 Token Format

**Instagram Token:**
- Starts with: `IGAB_`
- Length: 100+ characters
- Example: `IGAB_1234567890abcdefghijklmnopqrstuvwxyz...`

**Facebook Token:**
- Starts with: `EAAB_`
- Length: 100+ characters
- Example: `EAAB_1234567890abcdefghijklmnopqrstuvwxyz...`

**Account IDs:**
- Instagram: 17 digits (e.g., `17841400000000`)
- Facebook: 10-15 digits (e.g., `1048264368365205`)

---

## 🎯 Next Steps

1. ✅ Get credentials (3 minutes)
2. ✅ Run setup script (1 minute)
3. ✅ Test credentials (1 minute)
4. ✅ Post to social media (2 minutes)
5. ✅ Monitor dashboard (ongoing)

**Total time: ~7 minutes to production ready!**
