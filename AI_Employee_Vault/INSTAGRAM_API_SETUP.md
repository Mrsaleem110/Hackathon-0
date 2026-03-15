"""
Instagram API Setup - Complete Guide
"""

# INSTAGRAM API SETUP - STEP BY STEP

## Option 1: Quick Setup (Recommended)

### Step 1: Get Facebook App Credentials

1. Go to: https://developers.facebook.com/
2. Login with your Facebook account
3. Click "My Apps" → "Create App"
4. Choose "Business" type
5. Fill in app details:
   - App Name: "AI Employee Vault"
   - App Contact Email: your email
   - App Purpose: "Business"
6. Click "Create App"

### Step 2: Add Instagram Product

1. In app dashboard, click "Add Product"
2. Search for "Instagram Graph API"
3. Click "Set Up"
4. Choose "Instagram Business Account"

### Step 3: Get Credentials

1. Go to Settings → Basic
2. Copy these values:
   - **App ID** (save as INSTAGRAM_APP_ID)
   - **App Secret** (save as INSTAGRAM_APP_SECRET)

### Step 4: Add to .env File

Create or edit `.env` file:

```
INSTAGRAM_APP_ID=your_app_id_here
INSTAGRAM_APP_SECRET=your_app_secret_here
INSTAGRAM_USERNAME=m.saleem_ai_engineer
```

### Step 5: Get Access Token

Run this command:

```bash
python instagram_api_poster.py
```

Script will:
1. Ask you to go to Facebook Graph Explorer
2. Generate access token
3. Save it to .env automatically

### Step 6: Verify Setup

```bash
python -c "from config import get_config_status; import json; print(json.dumps(get_config_status(), indent=2))"
```

Expected:
```
{
  "instagram_configured": true
}
```

## Option 2: Manual Token Generation

### Using Facebook Graph Explorer

1. Go to: https://developers.facebook.com/tools/explorer/
2. Select your app from dropdown (top right)
3. Click "Generate Access Token"
4. Select scopes:
   - `instagram_business_basic`
   - `instagram_business_content_publish`
   - `instagram_business_manage_messages`
5. Click "Generate"
6. Copy the token
7. Add to .env:
   ```
   INSTAGRAM_ACCESS_TOKEN=your_token_here
   ```

## Testing

### Test 1: Simple Post

```bash
python instagram_api_poster.py
```

### Test 2: Post with Image

```python
from instagram_api_poster import post_to_instagram

post_to_instagram(
    caption="Hello from AI Employee Vault! 🚀",
    image_url="https://via.placeholder.com/1080x1080?text=Test"
)
```

### Test 3: Integration Test

```bash
python -c "
from instagram_api_poster import post_to_instagram
result = post_to_instagram(
    caption='Test post from AI Employee Vault',
    image_url='https://via.placeholder.com/1080x1080?text=AI+Vault'
)
print('Success!' if result else 'Failed!')
"
```

## Troubleshooting

### Error: "Invalid access token"
- Token expired or invalid
- Generate new token from Graph Explorer
- Update .env file

### Error: "Invalid business account"
- Account ID not linked to token
- Make sure token has correct scopes
- Regenerate token

### Error: "Image URL invalid"
- URL must be publicly accessible
- Try with placeholder: `https://via.placeholder.com/1080x1080`

### Error: "Caption too long"
- Instagram limit: 2,200 characters
- Reduce caption length

## Integration with Orchestrator

Add to `action_executor.py`:

```python
from instagram_api_poster import post_to_instagram

def execute_instagram_post(action):
    """Execute Instagram post action"""
    caption = action.get('caption', '')
    image_url = action.get('image_url', '')

    try:
        result = post_to_instagram(caption, image_url)
        return {
            'status': 'success' if result else 'failed',
            'platform': 'instagram',
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'error',
            'platform': 'instagram',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
```

## Files

- `instagram_api_poster.py` - Main posting script
- `.env` - Credentials file (not in git)
- `INSTAGRAM_API_SETUP.md` - This guide

## Security

✅ Safe:
- Credentials stored in .env (local only)
- Token can be revoked anytime
- No password stored

⚠️ Important:
- Don't share .env file
- Don't commit .env to git
- Keep token private

## Next Steps

1. ✅ Get Facebook App credentials
2. ✅ Generate access token
3. ✅ Add to .env
4. ✅ Test posting
5. ✅ Integrate with orchestrator

---

**Ready to post to Instagram! 🚀**
