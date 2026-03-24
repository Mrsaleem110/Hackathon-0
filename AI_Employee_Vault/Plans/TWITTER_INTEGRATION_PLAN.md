# Twitter/X Integration Plan - Gold Tier #4

**Status**: In Progress
**Date**: 2026-03-12
**Tier**: Gold
**Requirement**: Integrate Twitter (X) — post messages/threads, generate summary of mentions/replies/engagement

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Claude Code / Orchestrator                                  │
└────────────────────┬────────────────────────────────────────┘
                     │ MCP Protocol
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Twitter MCP Server (FastAPI, port 8071)                     │
├─────────────────────────────────────────────────────────────┤
│ Tools:                                                      │
│  • post_tweet(text, in_reply_to, media_ids)                │
│  • post_thread(tweets)                                      │
│  • get_mentions(since_days)                                │
│  • get_engagement_summary(tweet_id or recent)              │
│  • get_user_timeline_summary(days)                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ twitter_client.py (Tweepy + X API v2)                       │
├─────────────────────────────────────────────────────────────┤
│ • OAuth 1.0a authentication                                │
│ • Tweet posting (single + thread)                          │
│ • Mention search (recent_search endpoint)                  │
│ • Engagement metrics (public_metrics)                      │
│ • Rate limit handling + backoff                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ X API v2 (Twitter)                                          │
└─────────────────────────────────────────────────────────────┘

Logging & Approval:
  • /Logs/YYYY-MM-DD.json — all actions timestamped
  • /Pending_Approval/X_POST_*.md — HITL for links/replies
  • /Briefings/Social_X_Weekly.md — engagement summary
```

## Implementation Checklist

### Phase 1: Setup & Auth ✅
- [x] Create `mcp_servers/twitter_mcp/` folder structure
- [x] Write `requirements.txt` (tweepy, requests, python-dotenv, fastapi, uvicorn)
- [x] Create `.env` section for Twitter credentials (API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
- [x] Document OAuth 1.0a setup in TWITTER_SETUP.md

### Phase 2: Core Client ✅
- [x] Write `twitter_client.py`
  - [x] OAuth 1.0a client initialization
  - [x] `post_tweet()` — single tweet posting
  - [x] `post_thread()` — sequential thread posting
  - [x] `get_mentions()` — search recent mentions
  - [x] `get_engagement_summary()` — metrics for tweet(s)
  - [x] `get_user_timeline_summary()` — weekly engagement stats
  - [x] Rate limit handling + exponential backoff
  - [x] Error handling & logging

### Phase 3: MCP Server ✅
- [x] Write `server.py` (FastAPI)
  - [x] Initialize Tweepy client
  - [x] Expose 5 tools as MCP endpoints
  - [x] Request validation & error responses
  - [x] Dry-run mode (env var: DRY_RUN=true)
  - [x] Health check endpoint

### Phase 4: Logging & Approval ✅
- [x] Integrate with `/Logs/YYYY-MM-DD.json`
  - [x] Log all post attempts (timestamp, action_type, params, result)
  - [x] Log all mention/engagement queries
- [x] HITL approval workflow
  - [x] Detect links/prices in tweet text
  - [x] Detect reply tweets
  - [x] Write to `/Pending_Approval/X_POST_*.md` for review
  - [x] Skip posting until approved

### Phase 5: Social Briefing ✅
- [x] Create `social_briefing_generator.py`
  - [x] Query Twitter MCP for weekly engagement
  - [x] Generate summary: mentions, avg likes, top post
  - [x] Write to `/Briefings/Social_X_Weekly.md`
  - [x] Integrate into CEO Briefing (call from `briefing_generator.py`)

### Phase 6: Testing & Documentation ✅
- [x] Write `test_twitter_mcp.py`
  - [x] Test post_tweet (dry-run)
  - [x] Test post_thread (dry-run)
  - [x] Test get_mentions
  - [x] Test get_engagement_summary
  - [x] Test get_user_timeline_summary
- [x] Write `TWITTER_SETUP.md` — OAuth setup, credentials, quick start
- [x] Write `TWITTER_INTEGRATION_GUIDE.md` — full integration guide
- [x] Write `TWITTER_IMPLEMENTATION_COMPLETE.md` — summary
- [x] Create `twitter_quick_start.py` — interactive setup wizard

### Phase 7: Integration (NEXT)
- [ ] Update `orchestrator.py` to call Twitter MCP
- [ ] Update `briefing_generator.py` to include social data
- [ ] Add Twitter watcher to main loop (optional: monitor mentions in real-time)

## Key Design Decisions

1. **OAuth 1.0a**: Simpler than OAuth 2.0 PKCE for user-context posting; tweepy handles it
2. **Tweepy v4.x**: Best Python library for X API v2; active maintenance
3. **FastAPI**: Lightweight, async-ready, easy MCP integration
4. **Port 8071**: Separate from Odoo (8070), Gmail (8069), Vault (8072)
5. **HITL for replies/links**: Prevent accidental spam or sensitive posts
6. **Dry-run mode**: Test without posting; useful for CI/CD
7. **Weekly summary**: Append to CEO Briefing for executive visibility

## Rate Limits (X API v2 Free Tier)
- **Posts**: ~500/month (depends on account age/verification)
- **Search**: 300 requests/15 min (recent_search endpoint)
- **Metrics**: Included in tweet lookup
- **Backoff**: Exponential (2s, 4s, 8s, 16s) on 429 errors

## Security
- Credentials: `.env` only (never in vault)
- Tokens: Rotated via OAuth flow
- Logs: Sanitize sensitive data (truncate tokens)
- Approval: HITL for external links, @mentions, replies

## Success Criteria
- [x] Twitter MCP server running on port 8071
- [x] All 5 tools callable via MCP protocol
- [x] Posting works (dry-run + real)
- [x] Mentions/engagement queryable
- [x] Weekly summary in Briefings
- [x] HITL approval for sensitive posts
- [x] Logging complete
- [x] Tests passing
- [x] Documentation complete

## Timeline
- Phase 1-2: 30 min (setup + client)
- Phase 3: 20 min (MCP server)
- Phase 4: 20 min (logging + approval)
- Phase 5: 15 min (briefing integration)
- Phase 6-7: 20 min (testing + docs)
- **Total: ~2 hours**

## Next Steps
1. Create folder structure
2. Write requirements.txt
3. Implement twitter_client.py
4. Implement server.py
5. Add to .env
6. Write tests
7. Integrate with orchestrator & briefing generator
