# Get Real Instagram & Facebook Credentials - Visual Guide

**Time Required**: 5 minutes
**Difficulty**: Easy

---

## 🎯 What You'll Get

```
INSTAGRAM_ACCESS_TOKEN = IGAB_1234567890abcdefghijklmnopqrstuvwxyz...
INSTAGRAM_BUSINESS_ACCOUNT_ID = 17841400000000

FACEBOOK_ACCESS_TOKEN = EAAB_1234567890abcdefghijklmnopqrstuvwxyz...
FACEBOOK_PAGE_ID = 1048264368365205
```

---

## 📱 Getting Instagram Credentials (2 minutes)

### Step 1: Open Graph API Explorer
```
https://developers.facebook.com/tools/explorer/
```

### Step 2: Select Your App
- Look at top-right corner
- Click the dropdown menu
- Select your app (or create one if needed)

### Step 3: Generate Instagram Token
- Click blue button: **"Generate Access Token"**
- A popup will appear
- Select these scopes:
  - ✓ `instagram_basic`
  - ✓ `pages_manage_posts`
- Click "Generate"
- **Copy the token** (long string starting with `IGAB_`)

### Step 4: Get Account ID
- In the query box at top, paste:
  ```
  GET /me/instagram_business_accounts
  ```
- Click "Submit" button
- Look at the response (right side)
- Find: `"id": "17841400000000"`
- **Copy this ID** (17 digits)

### Result
```
INSTAGRAM_ACCESS_TOKEN = IGAB_xxxxxxxxxxxxx...
INSTAGRAM_BUSINESS_ACCOUNT_ID = 17841400000000
```

---

## 📘 Getting Facebook Credentials (2 minutes)

### Step 1: Open Graph API Explorer
```
https://developers.facebook.com/tools/explorer/
```

### Step 2: Select Your App
- Look at top-right corner
- Click the dropdown menu
- Select your app (same one as Instagram)

### Step 3: Generate Facebook Token
- Click blue button: **"Generate Access Token"**
- A popup will appear
- Select these scopes:
  - ✓ `pages_manage_posts`
  - ✓ `pages_read_engagement`
- Click "Generate"
- **Copy the token** (long string starting with `EAAB_`)

### Step 4: Get Page ID
- In the query box at top, paste:
  ```
  GET /me/accounts
  ```
- Click "Submit" button
- Look at the response (right side)
- Find your page in the list
- Copy the `"id"` field (numeric)

### Result
```
FACEBOOK_ACCESS_TOKEN = EAAB_xxxxxxxxxxxxx...
FACEBOOK_PAGE_ID = 1048264368365205
```

---

## 🔧 Adding Credentials to Your Project

### Option 1: Using the Manual Script (Easiest)

1. **Edit the file:**
   ```bash
   code add_credentials_manual.py
   # or
   nano add_credentials_manual.py
   ```

2. **Find STEP 1 section** (around line 10-15)

3. **Replace the values:**
   ```python
   INSTAGRAM_ACCESS_TOKEN = "IGAB_your_real_token_here"
   INSTAGRAM_BUSINESS_ACCOUNT_ID = "17841400000000"

   FACEBOOK_ACCESS_TOKEN = "EAAB_your_real_token_here"
   FACEBOOK_PAGE_ID = "1048264368365205"
   ```

4. **Save the file** (Ctrl+S)

5. **Run the script:**
   ```bash
   python add_credentials_manual.py
   ```

### Option 2: Edit .env Directly

1. **Open .env file:**
   ```bash
   code .env
   # or
   nano .env
   ```

2. **Find these lines:**
   ```env
   INSTAGRAM_ACCESS_TOKEN=IGAB_demo_token_123456789
   INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000
   FACEBOOK_ACCESS_TOKEN=EAAB_demo_token_987654321
   FACEBOOK_PAGE_ID=1048264368365205
   ```

3. **Replace with your real values:**
   ```env
   INSTAGRAM_ACCESS_TOKEN=IGAB_your_real_token_here
   INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000
   FACEBOOK_ACCESS_TOKEN=EAAB_your_real_token_here
   FACEBOOK_PAGE_ID=1048264368365205
   ```

4. **Save the file** (Ctrl+S)

---

## ✅ Verify Your Setup

After adding credentials, run:

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
python auto_post_social.py --platform instagram --caption "Hello World!"
```

### Test Facebook Posting
```bash
python auto_post_social.py --platform facebook --message "Hello World!"
```

### View Dashboard
```bash
python social_dashboard.py
```

---

## 📋 Checklist

- [ ] Opened https://developers.facebook.com/tools/explorer/
- [ ] Selected my app
- [ ] Generated Instagram Access Token (IGAB_...)
- [ ] Got Instagram Business Account ID (17 digits)
- [ ] Generated Facebook Access Token (EAAB_...)
- [ ] Got Facebook Page ID (numeric)
- [ ] Edited add_credentials_manual.py with my values
- [ ] Ran: python add_credentials_manual.py
- [ ] Ran: python validate_credentials.py
- [ ] All checks passed ✓

---

## 🆘 Troubleshooting

### "I can't find the Generate Access Token button"
- Make sure you're at: https://developers.facebook.com/tools/explorer/
- Look for the blue button in the top area
- If you don't see it, try refreshing the page

### "The token I copied is too short"
- Tokens should be 100+ characters
- Make sure you copied the entire token
- Try again and copy more carefully

### "I don't see my Instagram account in the response"
- Make sure your account is a Business Account (not Personal)
- Try running: `GET /me/instagram_business_accounts`
- If still not showing, create a new Business Account

### "I don't see my Facebook page in the response"
- Make sure you're the admin of the page
- Try running: `GET /me/accounts`
- If still not showing, check you have the right permissions

### "Validation says credentials are invalid"
- Check tokens start with IGAB_ and EAAB_
- Check account IDs are numeric
- Make sure you didn't accidentally add extra spaces
- Try regenerating the tokens

---

## 🔐 Security Reminders

✅ **DO:**
- Keep tokens secret (like passwords)
- Never share tokens in messages
- Rotate tokens every 90 days
- Use .env file (never commit to git)

❌ **DON'T:**
- Commit .env to git
- Share tokens publicly
- Use same token for multiple apps
- Store tokens in code

---

## 📚 Quick Links

| Resource | URL |
|----------|-----|
| Graph API Explorer | https://developers.facebook.com/tools/explorer/ |
| Developer Console | https://developers.facebook.com/ |
| Business Manager | https://business.facebook.com/ |
| Instagram API Docs | https://developers.facebook.com/docs/instagram-api |
| Facebook API Docs | https://developers.facebook.com/docs/graph-api |

---

## 🚀 You're Ready!

Once you've added your credentials and verified them, you can:

1. **Post to Instagram:**
   ```bash
   python auto_post_social.py --platform instagram --caption "My post!"
   ```

2. **Post to Facebook:**
   ```bash
   python auto_post_social.py --platform facebook --message "My post!"
   ```

3. **Monitor everything:**
   ```bash
   python social_dashboard.py
   ```

4. **Start the full system:**
   ```bash
   python orchestrator.py
   ```

**Total time: ~10 minutes from start to production ready!** 🎉
