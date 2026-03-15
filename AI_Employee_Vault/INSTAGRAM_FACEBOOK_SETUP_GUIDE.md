# Instagram + Facebook Auto-Posting Guide

## 🚀 Quick Start

### Step 1: Setup Credentials
```bash
python setup_insta_fb.py
```

Yeh script tumse poochega:
- **Instagram Access Token** - Business account ka token
- **Instagram Business Account ID** - Account ka ID
- **Facebook Access Token** - Page ka token
- **Facebook Page ID** - Page ka ID

### Step 2: Verify Setup
```bash
python test_mcp_servers.py
```

### Step 3: Post Content
```bash
python auto_post_social.py
```

---

## 📱 Instagram Credentials Kaise Milenge

### Option A: Business Account (Recommended)

1. **Facebook Business Manager par jao**
   - https://business.facebook.com/

2. **Settings → Apps and Websites**
   - Click "Add Apps"

3. **Instagram Business Account add karo**
   - Apna Instagram account connect karo

4. **Credentials nikalo**
   - Settings → Instagram Accounts
   - Business Account ID copy karo
   - Access Token generate karo

### Option B: Facebook Developers

1. **Developers portal par jao**
   - https://developers.facebook.com/

2. **App create karo**
   - Type: Business
   - Name: Kuch bhi (e.g., "My Social Bot")

3. **Instagram Basic Display add karo**
   - Products → Add Products
   - Instagram Basic Display select karo

4. **Token generate karo**
   - Settings → Basic
   - App ID aur App Secret dekho
   - Tools → Access Token Generator
   - Instagram select karo
   - Token copy karo

### Option C: Graph API Explorer

1. **https://developers.facebook.com/tools/explorer/**

2. **Get Token button click karo**

3. **Instagram Business Account select karo**

4. **Token copy karo**

---

## 📘 Facebook Credentials Kaise Milenge

### Option A: Facebook Developers (Recommended)

1. **https://developers.facebook.com/ par jao**

2. **App create karo**
   - Type: Business
   - Name: Kuch bhi (e.g., "My Social Bot")

3. **Facebook Login product add karo**
   - Products → Add Products
   - Facebook Login select karo

4. **Scopes set karo**
   - Settings → Basic
   - Required scopes:
     - `pages_manage_posts` - Posts create karne ke liye
     - `pages_read_engagement` - Analytics dekh sakte ho

5. **Token generate karo**
   - Tools → Access Token Generator
   - Apna page select karo
   - Token copy karo

6. **Page ID nikalo**
   - Page Settings → Page ID copy karo

### Option B: Graph API Explorer

1. **https://developers.facebook.com/tools/explorer/**

2. **Get Token button click karo**

3. **Page Access Token select karo**

4. **Token copy karo**

5. **Page ID nikalo**
   - Graph API mein `/me` query karo
   - Response mein `id` field dekho

---

## 🔧 Setup Process

### 1. Credentials Add Karo
```bash
python setup_insta_fb.py
```

Script poochega:
```
🔑 INSTAGRAM_ACCESS_TOKEN: [paste karo]
🔑 INSTAGRAM_BUSINESS_ACCOUNT_ID: [paste karo]
🔑 FACEBOOK_ACCESS_TOKEN: [paste karo]
🔑 FACEBOOK_PAGE_ID: [paste karo]
```

### 2. .env File Check Karo
```bash
cat .env | grep -E "INSTAGRAM|FACEBOOK"
```

Output hona chahiye:
```
INSTAGRAM_ACCESS_TOKEN=IGABxxxxxxxx...
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000
FACEBOOK_ACCESS_TOKEN=EAACxxxxxxxx...
FACEBOOK_PAGE_ID=1048264368365205
```

### 3. Test Karo
```bash
python test_mcp_servers.py
```

---

## 📝 Posts Kaise Karo

### Interactive Mode
```bash
python auto_post_social.py
```

Script poochega:
```
📝 Instagram caption enter karo: Hello Instagram!
🖼️  Image URL (optional): https://example.com/image.jpg
📝 Facebook message enter karo: Hello Facebook!
🔗 Facebook link (optional): https://example.com
✅ Post karo? (y/n): y
```

### Batch Mode (File se)
```bash
python auto_post_social.py posts.txt
```

`posts.txt` format:
```
Hello Instagram! #first
Second post here
Third post with hashtags #awesome
```

### Python Code se
```python
from mcp_servers.instagram_mcp import InstagramClient
from mcp_servers.facebook_mcp import FacebookClient

# Instagram post
ig = InstagramClient()
result = ig.post_feed(
    caption="Hello Instagram!",
    image_url="https://example.com/image.jpg"
)
print(result)

# Facebook post
fb = FacebookClient()
result = fb.post_feed(
    message="Hello Facebook!",
    link="https://example.com"
)
print(result)
```

---

## 🐛 Troubleshooting

### "Invalid credentials" Error
- Token expire ho gaya? → Naya token generate karo
- Account ID galat? → Verify karo Facebook Business Manager se
- Scopes missing? → Token mein required scopes add karo

### "Access Denied" Error
- Token ko required permissions nahi hain
- Instagram: `instagram_basic` scope chahiye
- Facebook: `pages_manage_posts` scope chahiye

### "Rate Limited" Error
- Bohot jaldi posts kar rahe ho
- 5-10 seconds wait karo posts ke beech

### "Invalid Image URL" Error
- Image URL publicly accessible hona chahiye
- HTTPS use karo (HTTP nahi)
- Image format: JPG, PNG, GIF

---

## 📊 Advanced Usage

### Orchestrator ke saath
```bash
python orchestrator.py
```

Yeh automatically:
- Emails monitor karega
- WhatsApp messages check karega
- LinkedIn opportunities dekha
- Automatically Instagram + Facebook par post karega

### Scheduling
```python
from apscheduler.schedulers.background import BackgroundScheduler
from auto_post_social import SocialMediaPoster

scheduler = BackgroundScheduler()
poster = SocialMediaPoster()

# Har din 9 AM par post karo
scheduler.add_job(
    poster.post_to_both,
    'cron',
    hour=9,
    args=["Good morning!", "Good morning!"]
)

scheduler.start()
```

### Logging
```bash
tail -f Logs/2026-03-15.json | grep -i "instagram\|facebook"
```

---

## ✅ Checklist

- [ ] Instagram Business Account setup kiya
- [ ] Facebook Page setup kiya
- [ ] Credentials generate kiye
- [ ] `python setup_insta_fb.py` run kiya
- [ ] `python test_mcp_servers.py` se verify kiya
- [ ] `python auto_post_social.py` se test post kiya
- [ ] Orchestrator start kiya

---

## 🎯 Next Steps

1. **Credentials add karo** → `python setup_insta_fb.py`
2. **Test karo** → `python test_mcp_servers.py`
3. **Post karo** → `python auto_post_social.py`
4. **Automate karo** → `python orchestrator.py`

---

## 📞 Support

Agar koi issue ho:
1. Logs check karo: `tail -f Logs/2026-03-15.json`
2. Credentials verify karo: `cat .env | grep -E "INSTAGRAM|FACEBOOK"`
3. Test karo: `python test_mcp_servers.py`

---

**Happy Posting! 🚀**
