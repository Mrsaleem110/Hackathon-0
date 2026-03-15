# Instagram + Facebook Quick Reference

## 🚀 30-Second Setup

```bash
# Step 1: Setup credentials
python setup_insta_fb.py

# Step 2: Test
python test_insta_fb.py

# Step 3: Post
python auto_post_social.py
```

---

## 📱 Instagram Token Kaise Nikalo

### Fastest Way (5 minutes)

1. **https://business.facebook.com/** par jao
2. **Settings → Apps and Websites**
3. **Add Apps → Instagram Business Account**
4. **Business Account ID copy karo**
5. **Access Token generate karo**

**Done!** ✅

---

## 📘 Facebook Token Kaise Nikalo

### Fastest Way (5 minutes)

1. **https://developers.facebook.com/tools/explorer/** par jao
2. **Get Token button click karo**
3. **Page Access Token select karo**
4. **Token copy karo**
5. **Page ID nikalo** (Settings → Page ID)

**Done!** ✅

---

## 💻 Commands

| Command | Purpose |
|---------|---------|
| `python setup_insta_fb.py` | Credentials add karo |
| `python test_insta_fb.py` | Test karo |
| `python auto_post_social.py` | Interactive post karo |
| `python auto_post_social.py posts.txt` | Batch post karo |
| `python orchestrator.py` | Auto-post karo |

---

## 📝 Post Karne Ke Tarike

### Interactive
```bash
python auto_post_social.py
# Phir caption, image, message enter karo
```

### Batch (File se)
```bash
# posts.txt banao:
# Hello Instagram!
# Second post
# Third post

python auto_post_social.py posts.txt
```

### Python Code
```python
from mcp_servers.instagram_mcp import InstagramClient
from mcp_servers.facebook_mcp import FacebookClient

ig = InstagramClient()
ig.post_feed("Hello!", "https://example.com/image.jpg")

fb = FacebookClient()
fb.post_feed("Hello!", "https://example.com")
```

---

## 🔑 Credentials Format

```
INSTAGRAM_ACCESS_TOKEN=IGABxxxxxxxxxxxxxxxx
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000
FACEBOOK_ACCESS_TOKEN=EAACxxxxxxxxxxxxxxxx
FACEBOOK_PAGE_ID=1048264368365205
```

---

## ✅ Checklist

- [ ] Instagram Business Account setup kiya
- [ ] Facebook Page setup kiya
- [ ] Tokens generate kiye
- [ ] `python setup_insta_fb.py` run kiya
- [ ] `python test_insta_fb.py` se verify kiya
- [ ] `python auto_post_social.py` se test post kiya

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| "Invalid credentials" | Token expire ho gaya - naya generate karo |
| "Access Denied" | Scopes missing - token regenerate karo |
| "Rate Limited" | 5-10 sec wait karo posts ke beech |
| "Invalid Image URL" | HTTPS use karo, publicly accessible hona chahiye |

---

## 📊 Logs

```bash
# Latest logs dekho
tail -f Logs/2026-03-15.json

# Instagram posts dekho
tail -f Logs/2026-03-15.json | grep -i instagram

# Facebook posts dekho
tail -f Logs/2026-03-15.json | grep -i facebook
```

---

## 🎯 Full Workflow

```
1. Credentials setup
   ↓
2. Test credentials
   ↓
3. Post content
   ↓
4. Monitor logs
   ↓
5. Automate with orchestrator
```

---

**Ready to post? Start with: `python setup_insta_fb.py`** 🚀
