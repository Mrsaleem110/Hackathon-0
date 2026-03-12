# Twitter/X MCP Integration - Setup Guide

**Status**: Gold Tier #4
**Date**: 2026-03-12
**Port**: 8071

## Quick Start (5 minutes)

### 1. Get Twitter/X API Credentials

**Option A: Bearer Token (Recommended - Read-only)**
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Go to **Keys and tokens** tab
3. Copy **Bearer Token**
4. Add to `.env`:
   ```
   TWITTER_BEARER_TOKEN=your_bearer_token_here
   ```

**Option B: OAuth 1.0a (For posting)**
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Go to **Keys and tokens** tab
3. Generate/copy:
   - API Key (Consumer Key)
   - API Secret (Consumer Secret)
   - Access Token
   - Access Token Secret
4. Add to `.env`:
   ```
   TWITTER_API_KEY=your_api_key_here
   TWITTER_API_SECRET=your_api_secret_here
   TWITTER_ACCESS_TOKEN=your_access_token_here
   TWITTER_ACCESS_SECRET=your_access_token_secret_here
   ```

### 2. Update .env

Edit `.env` in the project root with either Bearer Token or OAuth 1.0a credentials:

```bash
# Bearer Token (Recommended)
TWITTER_BEARER_TOKEN=your_bearer_token_here

# OR OAuth 1.0a (optional fallback)
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_SECRET=your_access_token_secret_here

TWITTER_MCP_PORT=8071
```

### 3. Install Dependencies

```bash
cd mcp_servers/twitter_mcp
pip install -r requirements.txt
```

### 4. Test the Server

```bash
# Dry-run mode (no actual posts)
DRY_RUN=true python test_twitter_mcp.py

# Or start the server
python server.py
```

Expected output:
```
✓ PASS: Post Tweet
✓ PASS: Post Thread
✓ PASS: Get Mentions
✓ PASS: Get Engagement
✓ PASS: Get Timeline
✓ PASS: Length Validation
Results: 6/6 tests passed
```

## API Credentials Explained

### Bearer Token (Recommended)
- **What it is**: A single token for read-only access to X API v2
- **Use case**: Querying mentions, engagement metrics, timeline data
- **Advantages**: Simple, single credential, no user context needed
- **Limitations**: Read-only (cannot post tweets)
- **Where to get**: Dashboard → Keys and tokens → Bearer Token

### OAuth 1.0a (For Posting)
- **What it is**: User-context authentication for posting tweets
- **Use case**: Posting tweets, threads, replying to mentions
- **Advantages**: Full posting capabilities, user-specific actions
- **Limitations**: More complex, requires 4 credentials
- **Where to get**: Dashboard → Keys and tokens → API Key, Secret, Access Token, Access Secret

### Why Bearer Token First?
- Simpler setup (1 credential vs 4)
- Sufficient for querying engagement data
- Can add OAuth 1.0a later for posting
- Better security (fewer credentials to manage)

## MCP Tools Available

### 1. post_tweet
Post a single tweet (max 280 chars)

```json
{
  "text": "Hello Twitter! 🚀",
  "in_reply_to": null,
  "media_ids": null
}
```

**HITL Approval Required If:**
- Contains URLs (http://, https://, bit.ly, t.co)
- Contains prices ($, €, £, ₹, ¥)
- Is a reply to another tweet

### 2. post_thread
Post a thread of sequential tweets

```json
{
  "tweets": [
    "Thread: AI Employee Vault 🧵",
    "Part 1: Multi-channel detection",
    "Part 2: Intelligent planning",
    "Part 3: Autonomous execution"
  ]
}
```

**Note:** Each tweet in thread is checked for approval triggers

### 3. get_mentions
Get recent @mentions (last 7-30 days)

```json
{
  "since_days": 7
}
```

Returns:
- Tweet ID, text, author
- Likes, retweets, replies
- Created timestamp

### 4. get_engagement_summary
Get metrics for specific tweet or recent tweets

```json
{
  "tweet_id": null
}
```

Returns:
- Likes, retweets, replies, impressions
- Average engagement per tweet
- Top performing tweet

### 5. get_user_timeline_summary
Get weekly engagement stats

```json
{
  "days": 7
}
```

Returns:
- Total tweets, likes, retweets, replies
- Average likes per tweet
- Top tweet of the period

## Logging

All actions logged to `/Logs/YYYY-MM-DD.json`:

```json
{
  "timestamp": "2026-03-12T12:00:00.000Z",
  "action_type": "TWITTER_POST_TWEET",
  "params": {
    "text": "Hello Twitter!",
    "in_reply_to": null
  },
  "result": {
    "success": true,
    "tweet_id": "1234567890",
    "created_at": "2026-03-12T12:00:00.000Z"
  }
}
```

## Approval Workflow

Sensitive posts require human approval:

1. **Detection**: Server detects links, prices, or replies
2. **Request**: Creates `/Pending_Approval/X_POST_*.md`
3. **Review**: Human reviews and approves/rejects
4. **Execution**: Post sent only after approval

Example approval request:

```markdown
# Twitter/X Post - Pending Approval

**Timestamp**: 2026-03-12T12:00:00.000Z
**Action**: SINGLE
**Status**: PENDING_APPROVAL

## Content

Check out our new AI Employee Vault: https://github.com/...

## Parameters

{...}

## Approval

- [ ] Approved
- [ ] Rejected

**Reviewer**: [name]
**Review Date**: [date]
**Notes**: [comments]
```

## Dry-Run Mode

Test without posting:

```bash
# Via environment variable
DRY_RUN=true python server.py

# Or in code
client = TwitterClient(dry_run=True)
```

Dry-run responses include `"dry_run": true` flag.

## Rate Limits

**X API v2 Free Tier:**
- Posts: ~500/month (depends on account age)
- Search: 300 requests/15 min
- Metrics: Included in tweet lookup

**Backoff Strategy:**
- Exponential backoff on 429 errors
- 2s → 4s → 8s → 16s
- Automatic retry with tweepy

## Troubleshooting

### "Missing Twitter credentials in .env"
- Check all four keys are set in `.env`
- No spaces around `=` sign
- Credentials are not expired

### "Failed to authenticate"
- Verify API keys are correct
- Check app has OAuth 1.0a enabled
- Ensure access tokens are generated
- Try regenerating tokens in developer portal

### "Tweet too long"
- Max 280 characters
- Emojis count as 2 characters
- URLs count as 23 characters

### "Rate limit exceeded"
- Wait 15 minutes for search quota reset
- Reduce request frequency
- Check `/Logs/` for error details

## Integration with CEO Briefing

The social briefing generator queries Twitter MCP for weekly engagement:

```python
# In briefing_generator.py
twitter_summary = query_twitter_mcp(days=7)
briefing += f"\n## Social Media (Twitter/X)\n{twitter_summary}"
```

Output in `/Briefings/CEO_Weekly_*.md`:

```markdown
## Social Media (Twitter/X)

**Period**: Last 7 days
**Tweets**: 12
**Total Engagement**: 145 likes, 23 retweets, 8 replies
**Avg Likes/Tweet**: 12.1
**Top Tweet**: "AI Employee Vault reaches 1000 stars! 🚀" (45 likes)
**Mentions**: 8 new mentions from followers
```

## Security Best Practices

1. **Never commit credentials**
   - `.env` is in `.gitignore`
   - Use environment variables in production

2. **Rotate tokens regularly**
   - Regenerate in developer portal every 90 days
   - Update `.env` immediately

3. **Sanitize logs**
   - Tokens truncated in logs
   - Sensitive data redacted

4. **HITL for external links**
   - Prevents accidental spam
   - Requires human review for URLs

5. **Monitor approval queue**
   - Check `/Pending_Approval/` regularly
   - Review before posts go live

## Next Steps

1. ✅ Get Twitter API credentials
2. ✅ Update `.env`
3. ✅ Install dependencies
4. ✅ Run tests
5. ✅ Start server: `python server.py`
6. ✅ Integrate with orchestrator
7. ✅ Add to CEO Briefing
8. ✅ Monitor `/Logs/` and `/Pending_Approval/`

## Support

- Twitter API Docs: https://developer.twitter.com/en/docs/twitter-api
- Tweepy Docs: https://docs.tweepy.org/
- X API v2 Rate Limits: https://developer.twitter.com/en/docs/twitter-api/rate-limits
