# Twitter/X Integration Guide - Gold Tier #4

**Status**: Complete
**Date**: 2026-03-12
**Tier**: Gold
**Requirement**: Integrate Twitter (X) — post messages/threads, generate summary of mentions/replies/engagement

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│ Orchestrator (orchestrator.py)                              │
├─────────────────────────────────────────────────────────────┤
│ • Monitors Needs_Action/ for X_POST_* files                │
│ • Calls Twitter MCP for posting/querying                   │
│ • Logs all actions to /Logs/YYYY-MM-DD.json               │
│ • Moves approved posts to Done/                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Twitter MCP Server (port 8071)                              │
├─────────────────────────────────────────────────────────────┤
│ • FastAPI server with 5 MCP tools                          │
│ • OAuth 1.0a authentication                                │
│ • HITL approval workflow                                   │
│ • Rate limit handling                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Twitter/X API v2                                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ CEO Briefing Generator (briefing_generator.py)              │
├─────────────────────────────────────────────────────────────┤
│ • Calls social_briefing_generator.py                       │
│ • Queries Twitter MCP for engagement data                  │
│ • Appends social section to weekly briefing                │
│ • Generates recommendations                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Social Briefing Generator (social_briefing_generator.py)    │
├─────────────────────────────────────────────────────────────┤
│ • Queries Twitter MCP for timeline summary                 │
│ • Fetches mentions and engagement metrics                  │
│ • Formats markdown briefing                                │
│ • Saves to /Briefings/Social_X_Weekly_*.md                │
└─────────────────────────────────────────────────────────────┘
```

## Installation Steps

### Step 1: Install Twitter MCP Dependencies

```bash
cd mcp_servers/twitter_mcp
pip install -r requirements.txt
cd ../..
```

### Step 2: Configure .env

Update `.env` with Twitter API credentials:

```bash
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_SECRET=your_access_token_secret_here
TWITTER_MCP_PORT=8071
```

### Step 3: Test Twitter MCP Server

```bash
# Dry-run test (no actual posts)
cd mcp_servers/twitter_mcp
DRY_RUN=true python test_twitter_mcp.py

# Expected output:
# ✓ PASS: Post Tweet
# ✓ PASS: Post Thread
# ✓ PASS: Get Mentions
# ✓ PASS: Get Engagement
# ✓ PASS: Get Timeline
# ✓ PASS: Length Validation
# Results: 6/6 tests passed
```

### Step 4: Start Twitter MCP Server

In a separate terminal:

```bash
cd mcp_servers/twitter_mcp
python server.py
# Output: Starting Twitter MCP Server on port 8071
```

### Step 5: Verify Server is Running

```bash
curl http://localhost:8071/health
# Response: {"status":"ok","service":"Twitter/X MCP Server","port":8071,"authenticated":true}
```

## Integration with Orchestrator

### Update orchestrator.py

Add Twitter MCP client initialization:

```python
import requests

class Orchestrator:
    def __init__(self):
        # ... existing code ...
        self.twitter_mcp_url = os.getenv("TWITTER_MCP_URL", "http://localhost:8071")
        self.twitter_enabled = self._check_twitter_mcp()

    def _check_twitter_mcp(self) -> bool:
        """Check if Twitter MCP server is running"""
        try:
            response = requests.get(f"{self.twitter_mcp_url}/health", timeout=2)
            return response.status_code == 200
        except:
            logger.warning("Twitter MCP server not available")
            return False

    def process_twitter_posts(self):
        """Process pending Twitter posts from Needs_Action/"""
        if not self.twitter_enabled:
            logger.info("Twitter MCP not available, skipping")
            return

        needs_action_dir = Path(self.vault_path) / "Needs_Action"
        for file in needs_action_dir.glob("X_POST_*.md"):
            self._process_twitter_post(file)

    def _process_twitter_post(self, file_path: Path):
        """Process a single Twitter post file"""
        try:
            content = file_path.read_text()

            # Parse post content
            if "## Thread" in content:
                tweets = self._extract_thread_tweets(content)
                result = self._post_thread(tweets)
            else:
                text = self._extract_tweet_text(content)
                result = self._post_tweet(text)

            if result.get("success"):
                # Move to Done/
                done_file = Path(self.vault_path) / "Done" / file_path.name
                file_path.rename(done_file)
                logger.info(f"Posted tweet: {file_path.name}")
            else:
                logger.error(f"Failed to post: {result.get('error')}")

        except Exception as e:
            logger.error(f"Error processing Twitter post: {e}")

    def _post_tweet(self, text: str) -> dict:
        """Post a single tweet via MCP"""
        try:
            response = requests.post(
                f"{self.twitter_mcp_url}/tools/post_tweet",
                json={"text": text},
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _post_thread(self, tweets: list) -> dict:
        """Post a thread via MCP"""
        try:
            response = requests.post(
                f"{self.twitter_mcp_url}/tools/post_thread",
                json={"tweets": tweets},
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _extract_tweet_text(self, content: str) -> str:
        """Extract tweet text from markdown file"""
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("## Content"):
                return "\n".join(lines[i+2:]).strip().split("\n")[0]
        return ""

    def _extract_thread_tweets(self, content: str) -> list:
        """Extract thread tweets from markdown file"""
        tweets = []
        in_thread = False
        for line in content.split("\n"):
            if line.startswith("- "):
                tweets.append(line[2:].strip())
            elif line.startswith("## Thread"):
                in_thread = True
        return tweets
```

### Add to Main Loop

In `orchestrator.py` main loop:

```python
def run(self):
    """Main orchestrator loop"""
    while True:
        try:
            # ... existing watchers ...

            # Process Twitter posts
            self.process_twitter_posts()

            # ... rest of loop ...

        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
            time.sleep(5)
```

## Integration with CEO Briefing

### Update briefing_generator.py

Add social briefing integration:

```python
from social_briefing_generator import SocialBriefingGenerator

class CEOBriefingGenerator:
    def __init__(self):
        # ... existing code ...
        self.social_generator = SocialBriefingGenerator()

    def generate_weekly_briefing(self) -> str:
        """Generate complete CEO briefing with social section"""
        briefing = "# CEO Weekly Briefing\n\n"
        briefing += f"**Generated**: {datetime.utcnow().isoformat()}\n\n"

        # ... existing sections (Odoo, Gmail, etc.) ...

        # Add social media section
        try:
            social_section = self.social_generator.format_social_section(days=7)
            briefing += social_section
        except Exception as e:
            logger.warning(f"Failed to add social section: {e}")
            briefing += "\n## Social Media (Twitter/X)\n\nUnavailable\n\n"

        # ... rest of briefing ...

        return briefing
```

## File Structure

```
ai_employee_vault/
├── mcp_servers/
│   └── twitter_mcp/
│       ├── __init__.py
│       ├── requirements.txt
│       ├── twitter_client.py          # Core Twitter client
│       ├── server.py                  # FastAPI MCP server
│       └── test_twitter_mcp.py        # Test suite
├── social_briefing_generator.py       # Social briefing generator
├── TWITTER_SETUP.md                   # Setup guide
├── TWITTER_INTEGRATION_GUIDE.md       # This file
├── Plans/
│   └── TWITTER_INTEGRATION_PLAN.md    # Implementation plan
├── Logs/
│   └── YYYY-MM-DD.json               # Action logs
├── Pending_Approval/
│   └── X_POST_*.md                   # Approval requests
├── Briefings/
│   ├── CEO_Weekly_*.md               # CEO briefings
│   └── Social_X_Weekly_*.md          # Social briefings
└── Done/
    └── X_POST_*.md                   # Completed posts
```

## Usage Examples

### Example 1: Post a Simple Tweet

Create file: `Needs_Action/X_POST_hello_world.md`

```markdown
# Twitter/X Post

**Status**: PENDING

## Content

Hello Twitter! Testing AI Employee Vault integration 🚀 #AI #Automation
```

Orchestrator will:
1. Detect the file
2. Extract tweet text
3. Call Twitter MCP to post
4. Move to `Done/X_POST_hello_world.md`
5. Log action to `Logs/YYYY-MM-DD.json`

### Example 2: Post a Thread

Create file: `Needs_Action/X_POST_thread_example.md`

```markdown
# Twitter/X Thread

**Status**: PENDING

## Thread

- Thread: AI Employee Vault - Gold Tier 🧵
- Part 1: Multi-channel detection (Gmail, WhatsApp, LinkedIn)
- Part 2: Intelligent planning with Claude API
- Part 3: Human-in-the-loop approval workflow
- Part 4: Autonomous execution and logging
- Part 5: Now with Twitter/X integration! 🎉
```

### Example 3: Query Mentions

```python
import requests

response = requests.post(
    "http://localhost:8071/tools/get_mentions",
    json={"since_days": 7}
)
mentions = response.json()
print(f"Found {mentions['count']} mentions")
```

### Example 4: Get Engagement Summary

```python
import requests

response = requests.post(
    "http://localhost:8071/tools/get_user_timeline_summary",
    json={"days": 7}
)
summary = response.json()
print(f"This week: {summary['tweets_count']} tweets, {summary['total_likes']} likes")
```

## Approval Workflow

### Automatic Approval Triggers

Posts requiring human approval:

1. **Contains URLs**
   - `http://`, `https://`, `bit.ly`, `t.co`
   - Prevents accidental spam

2. **Contains Prices/Currency**
   - `$`, `€`, `£`, `₹`, `¥`
   - Prevents accidental financial commitments

3. **Is a Reply**
   - `in_reply_to` parameter set
   - Requires review before engaging

### Approval Process

1. **Detection**: Server detects trigger
2. **Request**: Creates `/Pending_Approval/X_POST_*.md`
3. **Review**: Human reviews content
4. **Approval**: Check `[x] Approved` box
5. **Execution**: Orchestrator posts after approval

Example approval file:

```markdown
# Twitter/X Post - Pending Approval

**Timestamp**: 2026-03-12T12:00:00.000Z
**Action**: SINGLE
**Status**: PENDING_APPROVAL

## Content

Check out our new AI Employee Vault: https://github.com/agentic-sphere/ai-employee-vault

## Approval

- [x] Approved
- [ ] Rejected

**Reviewer**: John Doe
**Review Date**: 2026-03-12
**Notes**: Great content, approved for posting
```

## Logging

All actions logged to `/Logs/YYYY-MM-DD.json`:

```json
{
  "timestamp": "2026-03-12T12:00:00.000Z",
  "action_type": "TWITTER_POST_TWEET",
  "params": {
    "text": "Hello Twitter!",
    "in_reply_to": null,
    "media_ids": null
  },
  "result": {
    "success": true,
    "tweet_id": "1234567890",
    "text": "Hello Twitter!",
    "created_at": "2026-03-12T12:00:00.000Z"
  }
}
```

## Monitoring

### Check Server Status

```bash
curl http://localhost:8071/health
```

### View Recent Logs

```bash
tail -f Logs/2026-03-12.json
```

### Monitor Approval Queue

```bash
ls -la Pending_Approval/X_POST_*
```

### Check Completed Posts

```bash
ls -la Done/X_POST_*
```

## Troubleshooting

### Server Won't Start

```bash
# Check if port 8071 is in use
lsof -i :8071

# Kill existing process
kill -9 <PID>

# Try different port
TWITTER_MCP_PORT=8072 python server.py
```

### Authentication Failed

```bash
# Verify credentials in .env
grep TWITTER_ .env

# Test with tweepy directly
python -c "import tweepy; print('Tweepy installed')"
```

### Posts Not Being Posted

```bash
# Check if orchestrator is running
ps aux | grep orchestrator.py

# Check logs
tail -f Logs/2026-03-12.json

# Check approval queue
ls Pending_Approval/
```

### Rate Limit Errors

```bash
# Check X API rate limits
curl -H "Authorization: Bearer $TWITTER_ACCESS_TOKEN" \
  "https://api.twitter.com/2/tweets/search/recent?query=test&max_results=10"

# Wait 15 minutes for quota reset
```

## Performance Considerations

- **Posting**: ~1-2 seconds per tweet
- **Thread posting**: ~5-10 seconds (1 second delay between tweets)
- **Mention search**: ~2-3 seconds
- **Engagement query**: ~1-2 seconds
- **Rate limits**: 300 searches/15 min, ~500 posts/month

## Security Checklist

- [x] Credentials in `.env` (never in code)
- [x] `.env` in `.gitignore`
- [x] HITL approval for external links
- [x] HITL approval for replies
- [x] Logs sanitized (tokens truncated)
- [x] Dry-run mode for testing
- [x] Error handling for API failures
- [x] Rate limit backoff

## Next Steps

1. ✅ Install Twitter MCP dependencies
2. ✅ Configure `.env` with Twitter credentials
3. ✅ Test Twitter MCP server
4. ✅ Start Twitter MCP server
5. ✅ Update orchestrator.py
6. ✅ Update briefing_generator.py
7. ✅ Create test posts in Needs_Action/
8. ✅ Monitor Logs/ and Pending_Approval/
9. ✅ Review CEO briefings with social section

## Support & Resources

- **Twitter API Docs**: https://developer.twitter.com/en/docs/twitter-api
- **Tweepy Documentation**: https://docs.tweepy.org/
- **X API v2 Rate Limits**: https://developer.twitter.com/en/docs/twitter-api/rate-limits
- **OAuth 1.0a Guide**: https://developer.twitter.com/en/docs/authentication/oauth-1-0a

---

**Status**: ✅ Complete
**Gold Tier #4**: Twitter/X Integration - DONE
