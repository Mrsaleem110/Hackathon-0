# Instagram & Facebook Integration - Setup Guide

**Status**: Gold Tier #5
**Date**: 2026-03-12
**Platforms**: Instagram + Facebook

## Quick Start (10 minutes)

### 1. Get Instagram Credentials

**Option A: Business Account (Recommended)**
1. Go to https://business.facebook.com/
2. Click **Settings** → **Apps and Websites**
3. Add your Instagram Business Account
4. Go to **Roles** → **Assign Users**
5. Get your **Business Account ID** and **Access Token**

**Option B: Personal Account**
1. Go to https://developers.facebook.com/
2. Create an app (type: Business)
3. Add Instagram Basic Display product
4. Generate access token with `instagram_basic` scope

### 2. Get Facebook Credentials

1. Go to https://developers.facebook.com/
2. Create an app (type: Business)
3. Add Facebook Login product
4. Get your **Page ID** and **Access Token**
5. Token needs `pages_manage_posts` and `pages_read_engagement` scopes

### 3. Update .env

Add to your `.env` file:

```bash
# Instagram Configuration
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_business_account_id_here

# Facebook Configuration
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token_here
FACEBOOK_PAGE_ID=your_facebook_page_id_here
```

### 4. Install Dependencies

```bash
cd mcp_servers/instagram_mcp
pip install -r requirements.txt

cd ../facebook_mcp
pip install -r requirements.txt
```

### 5. Test the Servers

```bash
# Test Instagram
python test_instagram_mcp.py

# Test Facebook
python test_facebook_mcp.py
```

## API Credentials Explained

### Instagram Business Account
- **What it is**: Access to Instagram Business features via Graph API
- **Use case**: Posting to feed, stories, getting insights
- **Advantages**: Full posting capabilities, analytics
- **Where to get**: Facebook Business Manager → Instagram Settings

### Facebook Page
- **What it is**: Access to Facebook Page via Graph API
- **Use case**: Posting to page, videos, getting engagement metrics
- **Advantages**: Full page management, video support
- **Where to get**: Facebook Developers → App Dashboard

## MCP Tools Available

### Instagram

#### 1. post_feed
Post to Instagram feed

```json
{
  "caption": "Check out Agentic Sphere! 🚀",
  "image_url": "https://example.com/image.jpg",
  "media_type": "IMAGE"
}
```

#### 2. post_story
Post to Instagram story

```json
{
  "image_url": "https://example.com/story.jpg"
}
```

#### 3. get_insights
Get account insights

```json
{}
```

Returns: impressions, reach, profile_views, follower_count

### Facebook

#### 1. post_feed
Post to Facebook page

```json
{
  "message": "Agentic Sphere is live! 🎉",
  "link": "https://github.com/...",
  "picture": "https://example.com/image.jpg",
  "name": "AI Employee Vault",
  "description": "Multi-channel automation"
}
```

#### 2. post_video
Post video to Facebook

```json
{
  "video_url": "https://example.com/video.mp4",
  "title": "Agentic Sphere Demo",
  "description": "See it in action"
}
```

#### 3. get_page_insights
Get page metrics

```json
{}
```

Returns: impressions, reach, engaged_users, page_fans

#### 4. get_feed
Get recent posts

```json
{
  "limit": 10
}
```

## Integration with Orchestrator

Add to `orchestrator.py`:

```python
from mcp_servers.instagram_mcp.server import InstagramMCPServer
from mcp_servers.facebook_mcp.server import FacebookMCPServer

# Initialize servers
instagram_server = InstagramMCPServer()
facebook_server = FacebookMCPServer()

# Use in action executor
def execute_social_action(action_type, params):
    if action_type == "INSTAGRAM_POST":
        return instagram_server.post_feed(**params)
    elif action_type == "FACEBOOK_POST":
        return facebook_server.post_feed(**params)
```

## Logging

All actions logged to `/Logs/YYYY-MM-DD.json`:

```json
{
  "timestamp": "2026-03-12T21:40:00.000Z",
  "action_type": "INSTAGRAM_POST_FEED",
  "params": {
    "caption": "Agentic Sphere...",
    "image_url": "..."
  },
  "result": {
    "success": true,
    "post_id": "123456789",
    "created_at": "2026-03-12T21:40:00.000Z"
  }
}
```

## Rate Limits

**Instagram Graph API:**
- Posts: 200/hour
- Stories: 200/hour
- Insights: 200/hour

**Facebook Graph API:**
- Posts: 500/hour
- Videos: 100/hour
- Insights: 200/hour

## Troubleshooting

### "Invalid access token"
- Check token is not expired
- Regenerate in developer portal
- Verify scopes are correct

### "Page/Account not found"
- Verify Page ID and Business Account ID
- Check token has access to page/account
- Try regenerating token

### "Rate limit exceeded"
- Wait 1 hour for quota reset
- Reduce posting frequency
- Check logs for error details

## Next Steps

1. ✅ Get Instagram credentials
2. ✅ Get Facebook credentials
3. ✅ Update .env
4. ✅ Install dependencies
5. ✅ Run tests
6. ✅ Integrate with orchestrator
7. ✅ Monitor /Logs/ for activity

## Support

- Instagram Graph API: https://developers.facebook.com/docs/instagram-api
- Facebook Graph API: https://developers.facebook.com/docs/graph-api
- Rate Limits: https://developers.facebook.com/docs/graph-api/overview/rate-limiting
