# Instagram + Facebook Auto-Posting Setup

## 🚀 Quick Start

### Step 1: Get Your Credentials

**Instagram:**
1. Go to https://business.facebook.com/
2. Settings → Apps and Websites
3. Add Instagram Business Account
4. Copy: Business Account ID and Access Token

**Facebook:**
1. Go to https://developers.facebook.com/tools/explorer/
2. Click "Get Token" → Select "Page Access Token"
3. Copy: Access Token and Page ID

### Step 2: Setup

```bash
python setup_insta_fb_cli.py \
  --instagram-token YOUR_INSTAGRAM_TOKEN \
  --instagram-id YOUR_INSTAGRAM_ID \
  --facebook-token YOUR_FACEBOOK_TOKEN \
  --facebook-id YOUR_FACEBOOK_ID
```

### Step 3: Verify

```bash
python setup_insta_fb_cli.py --verify
```

### Step 4: Post

```bash
python auto_post_social.py
```

---

## 📱 Instagram Setup (Detailed)

### Option A: Business Manager (Recommended)

1. **Open Business Manager**
   - https://business.facebook.com/

2. **Add Instagram Account**
   - Settings → Apps and Websites
   - Click "Add Apps"
   - Select Instagram Business Account
   - Connect your Instagram account

3. **Get Credentials**
   - Go to Settings → Instagram Accounts
   - Find your account
   - Copy Business Account ID (looks like: 17841400000000)
   - Generate Access Token

### Option B: Facebook Developers

1. **Create App**
   - https://developers.facebook.com/
   - My Apps → Create App
   - App Type: Business
   - App Name: (anything, e.g., "My Social Bot")

2. **Add Instagram Basic Display**
   - Products → Add Products
   - Search "Instagram Basic Display"
   - Click "Set Up"

3. **Get Token**
   - Settings → Basic (copy App ID and App Secret)
   - Tools → Access Token Generator
   - Select Instagram account
   - Copy token

---

## 📘 Facebook Setup (Detailed)

### Option A: Graph API Explorer (Fastest)

1. **Open Explorer**
   - https://developers.facebook.com/tools/explorer/

2. **Get Token**
   - Click "Get Token" button
   - Select "Page Access Token"
   - Choose your page
   - Copy token

3. **Get Page ID**
   - In Graph API, run: `/me`
   - Look for "id" field in response
   - That's your Page ID

### Option B: Facebook Developers

1. **Create App**
   - https://developers.facebook.com/
   - My Apps → Create App
   - App Type: Business
   - App Name: (anything)

2. **Add Facebook Login**
   - Products → Add Products
   - Search "Facebook Login"
   - Click "Set Up"

3. **Configure**
   - Settings → Basic
   - Copy App ID and App Secret
   - Settings → Facebook Login
   - Add your domain

4. **Get Token**
   - Tools → Access Token Generator
   - Select your page
   - Copy token

5. **Get Page ID**
   - Page Settings → Page ID
   - Copy it

---

## 💻 Commands

### Setup Guide
```bash
python setup_insta_fb_cli.py --show-guide
```

### Setup with Credentials
```bash
python setup_insta_fb_cli.py \
  --instagram-token IGABxxxxxxxx \
  --instagram-id 17841400000000 \
  --facebook-token EAACxxxxxxxx \
  --facebook-id 1048264368365205
```

### Verify Setup
```bash
python setup_insta_fb_cli.py --verify
```

### Test Credentials
```bash
python test_insta_fb.py
```

### Post to Social Media
```bash
python auto_post_social.py
```

### View Dashboard
```bash
python social_dashboard.py
```

---

## 📝 Example: Complete Setup

```bash
# 1. Show guide
python setup_insta_fb_cli.py --show-guide

# 2. Get your tokens from Facebook/Instagram

# 3. Setup
python setup_insta_fb_cli.py \
  --instagram-token "IGABxxxxxxxxxxxxxxxx" \
  --instagram-id "17841400000000" \
  --facebook-token "EAACxxxxxxxxxxxxxxxx" \
  --facebook-id "1048264368365205"

# 4. Verify
python setup_insta_fb_cli.py --verify

# 5. Test
python test_insta_fb.py

# 6. Post
python auto_post_social.py
```

---

## 🎯 Posting Examples

### Interactive Mode
```bash
python auto_post_social.py
```

Then enter:
- Instagram caption
- Image URL (optional)
- Facebook message
- Link (optional)

### Batch Mode
```bash
# Create posts.txt
echo "Hello Instagram!" > posts.txt
echo "Second post" >> posts.txt

# Post all
python auto_post_social.py posts.txt
```

### Python Code
```python
from mcp_servers.instagram_mcp import InstagramClient
from mcp_servers.facebook_mcp import FacebookClient

# Instagram
ig = InstagramClient()
result = ig.post_feed(
    caption="Hello Instagram!",
    image_url="https://example.com/image.jpg"
)
print(result)

# Facebook
fb = FacebookClient()
result = fb.post_feed(
    message="Hello Facebook!",
    link="https://example.com"
)
print(result)
```

---

## 🐛 Troubleshooting

### "Invalid credentials"
- Check token format
- Verify token is not expired
- Run: `python setup_insta_fb_cli.py --verify`

### "Access Denied"
- Token needs correct scopes
- Instagram: `instagram_basic` scope
- Facebook: `pages_manage_posts` scope
- Regenerate token with correct scopes

### "Rate Limited"
- Wait 5-10 minutes
- Don't post more than 5 times per day
- Space posts 5-10 minutes apart

### "Invalid Image URL"
- Must be HTTPS (not HTTP)
- Must be publicly accessible
- Supported formats: JPG, PNG, GIF

---

## 📊 Monitoring

### View Logs
```bash
tail -f Logs/2026-03-15.json
```

### Check Specific Posts
```bash
tail -f Logs/2026-03-15.json | grep -i instagram
tail -f Logs/2026-03-15.json | grep -i facebook
```

### View Dashboard
```bash
python social_dashboard.py
```

---

## 🔐 Security

- Tokens stored in .env (not in git)
- Never commit .env file
- Rotate tokens monthly
- Use environment variables in production
- Keep tokens private

---

## ✅ Checklist

- [ ] Instagram Business Account created
- [ ] Facebook Page created
- [ ] Instagram token generated
- [ ] Instagram Account ID copied
- [ ] Facebook token generated
- [ ] Facebook Page ID copied
- [ ] Setup command run
- [ ] Credentials verified
- [ ] Test passed
- [ ] First post successful

---

## 📞 Support

### Quick Help
```bash
python setup_insta_fb_cli.py --show-guide
```

### Verify Setup
```bash
python setup_insta_fb_cli.py --verify
```

### Test Everything
```bash
python test_insta_fb.py
```

---

## 🎉 You're Ready!

Once setup is complete, you can:

1. **Post manually**
   ```bash
   python auto_post_social.py
   ```

2. **Monitor dashboard**
   ```bash
   python social_dashboard.py
   ```

3. **Automate with orchestrator**
   ```bash
   python orchestrator.py
   ```

---

**Happy posting!** 🚀
