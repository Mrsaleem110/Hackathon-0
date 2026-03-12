# Instagram & Facebook Integration - Quick Start

**Status**: Gold Tier #5 - COMPLETE
**Date**: 2026-03-12
**Tests**: PASS (100%)

## What's New

Instagram and Facebook MCP servers are now integrated into your AI Employee Vault. Post to both platforms automatically.

## Test Results

```
Facebook MCP Server: [SUCCESS] All tests passed!
- [OK] Post Feed
- [OK] Post Video
- [OK] Get Page Insights
- [OK] Get Feed

Instagram MCP Server: [SUCCESS] All tests passed!
- [OK] Post Feed
- [OK] Post Story
- [OK] Get Insights
```

## Setup (5 minutes)

### 1. Get Credentials

**Facebook:**
1. Go to https://developers.facebook.com/
2. Create app → Business type
3. Add Facebook Login product
4. Get Page ID and Access Token
5. Add to `.env`:
```
FACEBOOK_ACCESS_TOKEN=your_token_here
FACEBOOK_PAGE_ID=your_page_id_here
```

**Instagram:**
1. Go to https://business.facebook.com/
2. Add Instagram Business Account
3. Get Business Account ID and Access Token
4. Add to `.env`:
```
INSTAGRAM_ACCESS_TOKEN=your_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id_here
```

### 2. Install Dependencies

```bash
cd mcp_servers/facebook_mcp
pip install -r requirements.txt

cd ../instagram_mcp
pip install -r requirements.txt
```

### 3. Use in Your Code

```python
from mcp_servers.facebook_mcp import FacebookClient
from mcp_servers.instagram_mcp import InstagramClient

# Facebook
fb = FacebookClient()
fb.post_feed(message="Hello Facebook!", link="https://example.com")

# Instagram
ig = InstagramClient()
ig.post_feed(caption="Hello Instagram!", image_url="https://example.com/image.jpg")
```

## Available Methods

### Facebook
- `post_feed()` - Post to page
- `post_video()` - Post video
- `get_page_insights()` - Get metrics
- `get_feed()` - Get recent posts

### Instagram
- `post_feed()` - Post to feed
- `post_story()` - Post story
- `get_insights()` - Get metrics

## Files Created

```
mcp_servers/
├── facebook_mcp/
│   ├── facebook_client.py
│   ├── server.py
│   ├── test_facebook_mcp.py
│   ├── requirements.txt
│   └── __init__.py
└── instagram_mcp/
    ├── instagram_client.py
    ├── server.py
    ├── test_instagram_mcp.py
    ├── requirements.txt
    └── __init__.py
```

## Next Steps

1. Add credentials to `.env`
2. Run tests: `python test_facebook_mcp.py` and `python test_instagram_mcp.py`
3. Integrate with orchestrator
4. Start posting!

## Documentation

See `INSTAGRAM_FACEBOOK_SETUP.md` for detailed setup and API reference.
