"""
Instagram Setup Instructions and Quick Start Guide
"""

# INSTAGRAM SETUP - QUICK START GUIDE

## Step 1: Run Setup Script

```bash
cd "C:\Users\Agentic Sphere\Documents\GitHub\Hackathon-0\ai_employee_vault"
python setup_instagram_selenium.py
```

**What happens:**
- Chrome browser khul jayega
- Instagram login page open hoga
- Tum apna username aur password enter karo (already configured)
- Agar 2FA hai to complete karo
- Session automatically save ho jayega
- Credentials .env mein save honge

## Step 2: Verify Setup

```bash
python -c "from config import get_config_status; import json; print(json.dumps(get_config_status(), indent=2))"
```

Expected output:
```
{
  "instagram_configured": true,
  "instagram_session": true
}
```

## Step 3: Test Instagram Posting

```bash
python instagram_poster.py
```

**What happens:**
- Browser khul jayega
- Saved session load hoga
- Test post share hoga
- Browser close hoga

## Step 4: Use in Your Code

```python
from instagram_poster import post_instagram

# Post with caption only
post_instagram(caption="Hello from AI Employee Vault! 🚀")

# Post with image URL
post_instagram(
    caption="Check this out! 📸",
    image_url="https://example.com/image.jpg"
)

# Post with local image
post_instagram(
    caption="Local image post",
    image_path="/path/to/image.jpg"
)
```

## Troubleshooting

### Issue: "Session file not found"
**Solution:** Run setup script again
```bash
python setup_instagram_selenium.py
```

### Issue: "Not logged in"
**Solution:**
- Check internet connection
- Try setup script again
- Make sure 2FA is completed

### Issue: "Create button not found"
**Solution:**
- Instagram UI might have changed
- Try manual post first
- Update selectors if needed

### Issue: Browser closes immediately
**Solution:**
- Check Chrome is installed
- Update ChromeDriver: `pip install --upgrade webdriver-manager`

## Files Created

1. **setup_instagram_selenium.py** - Setup script (run once)
2. **instagram_poster.py** - Posting script (use in code)
3. **.instagram_session/** - Session folder (auto-created)
4. **.env** - Updated with credentials

## Security Notes

✅ **Safe:**
- Session cookies stored locally
- Password not stored anywhere
- Only used for Instagram automation

⚠️ **Important:**
- Don't share .instagram_session folder
- Don't commit .env to git
- Keep credentials private

## Next Steps

1. ✅ Run setup script
2. ✅ Test posting
3. ✅ Integrate with orchestrator
4. ✅ Set up automated posts

## Integration with Orchestrator

```python
# In action_executor.py
from instagram_poster import post_instagram

def execute_instagram_post(action):
    caption = action.get('caption')
    image_url = action.get('image_url')

    result = post_instagram(caption, image_url=image_url)
    return {
        'status': 'success' if result else 'failed',
        'platform': 'instagram',
        'timestamp': datetime.now().isoformat()
    }
```

## Support

For issues:
1. Check browser console (F12)
2. Check terminal output
3. Verify credentials in .env
4. Try setup script again

---

**Ready to post to Instagram! 🚀**
