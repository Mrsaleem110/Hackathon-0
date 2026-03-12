# Twitter/X MCP - Command Reference

**Quick Reference for all Twitter integration commands**

## Installation

### Install Dependencies
```bash
cd mcp_servers/twitter_mcp
pip install -r requirements.txt
cd ../..
```

### Configure Credentials
```bash
# Edit .env and add:
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_SECRET=your_access_token_secret_here
TWITTER_MCP_PORT=8071
```

## Running the Server

### Start Twitter MCP Server
```bash
cd mcp_servers/twitter_mcp
python server.py
# Output: Starting Twitter MCP Server on port 8071
```

### Start with Custom Port
```bash
TWITTER_MCP_PORT=8072 python server.py
```

### Start in Dry-Run Mode (No Actual Posts)
```bash
DRY_RUN=true python server.py
```

## Testing

### Run Full Test Suite
```bash
cd mcp_servers/twitter_mcp
python test_twitter_mcp.py
```

### Run Tests in Dry-Run Mode
```bash
cd mcp_servers/twitter_mcp
DRY_RUN=true python test_twitter_mcp.py
```

### Quick Start Wizard
```bash
python twitter_quick_start.py
```

## Server Health & Status

### Check Server Status
```bash
curl http://localhost:8071/health
```

### List Available Tools
```bash
curl http://localhost:8071/mcp/tools
```

### Check if Server is Running
```bash
lsof -i :8071
```

## API Calls (Direct HTTP)

### Post a Tweet
```bash
curl -X POST http://localhost:8071/tools/post_tweet \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello Twitter! 🚀",
    "in_reply_to": null,
    "media_ids": null
  }'
```

### Post a Thread
```bash
curl -X POST http://localhost:8071/tools/post_thread \
  -H "Content-Type: application/json" \
  -d '{
    "tweets": [
      "Thread: AI Employee Vault 🧵",
      "Part 1: Multi-channel detection",
      "Part 2: Intelligent planning",
      "Part 3: Autonomous execution"
    ]
  }'
```

### Get Mentions (Last 7 Days)
```bash
curl -X POST http://localhost:8071/tools/get_mentions \
  -H "Content-Type: application/json" \
  -d '{"since_days": 7}'
```

### Get Engagement Summary
```bash
curl -X POST http://localhost:8071/tools/get_engagement_summary \
  -H "Content-Type: application/json" \
  -d '{"tweet_id": null}'
```

### Get Timeline Summary (Last 7 Days)
```bash
curl -X POST http://localhost:8071/tools/get_user_timeline_summary \
  -H "Content-Type: application/json" \
  -d '{"days": 7}'
```

## Python API Calls

### Import and Use Client
```python
from mcp_servers.twitter_mcp.twitter_client import TwitterClient

# Initialize client
client = TwitterClient(dry_run=False)

# Post tweet
result = client.post_tweet("Hello Twitter! 🚀")
print(result)

# Post thread
tweets = ["Part 1", "Part 2", "Part 3"]
result = client.post_thread(tweets)
print(result)

# Get mentions
mentions = client.get_mentions(since_days=7)
print(f"Found {mentions['count']} mentions")

# Get engagement
engagement = client.get_engagement_summary()
print(engagement)

# Get timeline summary
summary = client.get_user_timeline_summary(days=7)
print(f"This week: {summary['tweets_count']} tweets")
```

### Query via Requests
```python
import requests

# Post tweet
response = requests.post(
    "http://localhost:8071/tools/post_tweet",
    json={"text": "Hello Twitter!"}
)
print(response.json())

# Get mentions
response = requests.post(
    "http://localhost:8071/tools/get_mentions",
    json={"since_days": 7}
)
mentions = response.json()
print(f"Found {mentions['count']} mentions")
```

## Vault Operations

### Create Test Post
```bash
cat > Needs_Action/X_POST_test.md << 'EOF'
# Twitter/X Post

**Status**: PENDING

## Content

Testing Twitter integration! 🚀 #AI #Automation
EOF
```

### Create Test Thread
```bash
cat > Needs_Action/X_POST_thread.md << 'EOF'
# Twitter/X Thread

**Status**: PENDING

## Thread

- Thread: AI Employee Vault 🧵
- Part 1: Multi-channel detection
- Part 2: Intelligent planning
- Part 3: Autonomous execution
EOF
```

### View Pending Posts
```bash
ls -la Needs_Action/X_POST_*
```

### View Approval Queue
```bash
ls -la Pending_Approval/X_POST_*
```

### View Completed Posts
```bash
ls -la Done/X_POST_*
```

### View Recent Logs
```bash
tail -f Logs/2026-03-12.json
```

## Briefing Generation

### Generate Social Briefing
```bash
python social_briefing_generator.py
```

### View Social Briefing
```bash
cat Briefings/Social_X_Weekly_*.md
```

### View CEO Briefing with Social Section
```bash
cat Briefings/CEO_Weekly_*.md | grep -A 50 "Social Media"
```

## Orchestrator Integration

### Run Orchestrator (Processes Posts)
```bash
python orchestrator.py
```

### Run Orchestrator in Dry-Run Mode
```bash
DRY_RUN=true python orchestrator.py
```

### Monitor Orchestrator Logs
```bash
tail -f Logs/2026-03-12.json | grep TWITTER
```

## Troubleshooting

### Check Dependencies
```bash
python -c "import tweepy; import fastapi; import uvicorn; print('All dependencies OK')"
```

### Verify Credentials
```bash
grep TWITTER_ .env
```

### Test Authentication
```bash
python -c "
from mcp_servers.twitter_mcp.twitter_client import TwitterClient
try:
    client = TwitterClient()
    print(f'✓ Authenticated as @{client.user.data.username}')
except Exception as e:
    print(f'✗ Auth failed: {e}')
"
```

### Check Port Availability
```bash
# Check if port 8071 is in use
lsof -i :8071

# Kill process on port 8071
kill -9 $(lsof -t -i :8071)
```

### View Server Logs
```bash
# Start server with verbose logging
python -u mcp_servers/twitter_mcp/server.py 2>&1 | tee twitter_server.log
```

### Test Rate Limits
```bash
# Check X API rate limits
curl -H "Authorization: Bearer $TWITTER_ACCESS_TOKEN" \
  "https://api.twitter.com/2/tweets/search/recent?query=test&max_results=10"
```

## Environment Variables

### Required
```bash
TWITTER_API_KEY              # X API v2 API Key
TWITTER_API_SECRET           # X API v2 API Secret
TWITTER_ACCESS_TOKEN         # OAuth 1.0a Access Token
TWITTER_ACCESS_SECRET        # OAuth 1.0a Access Token Secret
```

### Optional
```bash
TWITTER_MCP_PORT=8071        # Server port (default: 8071)
DRY_RUN=false                # Dry-run mode (default: false)
LOG_LEVEL=INFO               # Logging level (default: INFO)
```

## File Locations

```
mcp_servers/twitter_mcp/
├── __init__.py               # Package init
├── requirements.txt          # Dependencies
├── twitter_client.py         # Core client (350 lines)
├── server.py                 # FastAPI server (400 lines)
└── test_twitter_mcp.py       # Test suite (300 lines)

Root directory:
├── social_briefing_generator.py    # Briefing generator (350 lines)
├── twitter_quick_start.py          # Quick start wizard (250 lines)
├── TWITTER_SETUP.md                # Setup guide
├── TWITTER_INTEGRATION_GUIDE.md    # Integration guide
├── TWITTER_COMMANDS.md             # This file
├── TWITTER_IMPLEMENTATION_COMPLETE.md  # Summary
└── Plans/TWITTER_INTEGRATION_PLAN.md   # Plan

Vault directories:
├── Logs/YYYY-MM-DD.json            # Action logs
├── Pending_Approval/X_POST_*.md    # Approval requests
├── Needs_Action/X_POST_*.md        # Posts to process
├── Done/X_POST_*.md                # Completed posts
└── Briefings/
    ├── CEO_Weekly_*.md             # CEO briefings
    └── Social_X_Weekly_*.md        # Social briefings
```

## Common Workflows

### Workflow 1: Post a Tweet
```bash
# 1. Create post file
cat > Needs_Action/X_POST_hello.md << 'EOF'
# Twitter/X Post
## Content
Hello Twitter! 🚀
EOF

# 2. Run orchestrator
python orchestrator.py

# 3. Check logs
tail -f Logs/2026-03-12.json

# 4. Verify in Done/
ls Done/X_POST_hello.md
```

### Workflow 2: Post a Thread
```bash
# 1. Create thread file
cat > Needs_Action/X_POST_thread.md << 'EOF'
# Twitter/X Thread
## Thread
- Part 1: Introduction
- Part 2: Details
- Part 3: Conclusion
EOF

# 2. Run orchestrator
python orchestrator.py

# 3. Check completion
ls Done/X_POST_thread.md
```

### Workflow 3: Get Engagement Data
```bash
# 1. Query mentions
curl -X POST http://localhost:8071/tools/get_mentions \
  -H "Content-Type: application/json" \
  -d '{"since_days": 7}'

# 2. Query engagement
curl -X POST http://localhost:8071/tools/get_engagement_summary \
  -H "Content-Type: application/json" \
  -d '{"tweet_id": null}'

# 3. Generate briefing
python social_briefing_generator.py

# 4. View results
cat Briefings/Social_X_Weekly_*.md
```

### Workflow 4: Approve Sensitive Post
```bash
# 1. Post with link (requires approval)
cat > Needs_Action/X_POST_link.md << 'EOF'
# Twitter/X Post
## Content
Check out: https://github.com/agentic-sphere/ai-employee-vault
EOF

# 2. Run orchestrator (creates approval request)
python orchestrator.py

# 3. Review approval request
cat Pending_Approval/X_POST_SINGLE_*.md

# 4. Approve (edit file)
# Change: - [ ] Approved
# To:     - [x] Approved

# 5. Run orchestrator again (posts after approval)
python orchestrator.py

# 6. Verify in Done/
ls Done/X_POST_link.md
```

## Performance Tips

### Optimize Posting
- Post during off-peak hours (less rate limiting)
- Space out thread posts (1s delay between tweets)
- Batch mentions queries (search 7-30 days at once)

### Optimize Queries
- Cache engagement data (don't query every minute)
- Use timeline summary instead of individual tweets
- Limit mention search to 7 days (faster)

### Monitor Resources
- Check server memory: `ps aux | grep server.py`
- Monitor API calls: `tail -f Logs/2026-03-12.json | wc -l`
- Check rate limits: `curl https://api.twitter.com/2/tweets/search/recent`

## Support & Resources

- **Twitter API Docs**: https://developer.twitter.com/en/docs/twitter-api
- **Tweepy Docs**: https://docs.tweepy.org/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **X API Rate Limits**: https://developer.twitter.com/en/docs/twitter-api/rate-limits

---

**Last Updated**: 2026-03-12
**Status**: Production Ready
