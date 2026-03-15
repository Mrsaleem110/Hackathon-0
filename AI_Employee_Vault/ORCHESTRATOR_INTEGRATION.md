# Instagram + Facebook Integration with Orchestrator

## 🎯 Complete Workflow

```
Email/WhatsApp/LinkedIn Detection
         ↓
    Orchestrator
         ↓
    Claude API (Planning)
         ↓
    Human Approval
         ↓
Instagram + Facebook Auto-Post
         ↓
    Logging & Tracking
```

---

## 📋 Setup Steps

### 1. Credentials Setup
```bash
python setup_insta_fb.py
```

### 2. Verify Setup
```bash
python test_insta_fb.py
```

### 3. Start Orchestrator
```bash
python orchestrator.py
```

---

## 🤖 How It Works

### Detection Phase
- Gmail watcher detects emails
- WhatsApp watcher detects messages
- LinkedIn watcher detects opportunities

### Planning Phase
- Claude API analyzes content
- Generates Instagram + Facebook posts
- Creates approval request

### Approval Phase
- Human reviews posts
- Approves or rejects
- Stored in Pending_Approval/

### Execution Phase
- Posts to Instagram
- Posts to Facebook
- Logs results

### Logging Phase
- Records in Logs/YYYY-MM-DD.json
- Tracks success/failure
- Maintains audit trail

---

## 📝 Example Workflow

### Scenario: Email Detection

```
1. Email arrives: "Check out our new product!"
   ↓
2. Orchestrator detects it
   ↓
3. Claude generates:
   - Instagram: "🚀 New product launch! Check it out..."
   - Facebook: "Exciting news! We just launched..."
   ↓
4. Saved to: Pending_Approval/INSTAGRAM_POST_xxx.md
   ↓
5. Human reviews and approves
   ↓
6. Auto-posts to both platforms
   ↓
7. Logged in: Logs/2026-03-15.json
```

---

## 🔧 Configuration

### .env Settings
```bash
# Instagram
INSTAGRAM_ACCESS_TOKEN=your_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id

# Facebook
FACEBOOK_ACCESS_TOKEN=your_token_here
FACEBOOK_PAGE_ID=your_page_id

# Orchestrator
ENABLE_SCHEDULER=true
AUTO_APPROVE_THRESHOLD=50
APPROVAL_EXPIRY_HOURS=24
```

### Orchestrator Config
```python
# config.py
SOCIAL_MEDIA_PLATFORMS = {
    'instagram': {
        'enabled': True,
        'auto_approve': False,
        'max_posts_per_day': 5
    },
    'facebook': {
        'enabled': True,
        'auto_approve': False,
        'max_posts_per_day': 5
    }
}
```

---

## 📊 Monitoring

### View Logs
```bash
# Real-time logs
tail -f Logs/2026-03-15.json

# Instagram posts only
tail -f Logs/2026-03-15.json | grep -i instagram

# Facebook posts only
tail -f Logs/2026-03-15.json | grep -i facebook

# Failed posts
tail -f Logs/2026-03-15.json | grep -i "failed\|error"
```

### Dashboard
```bash
python social_dashboard.py
```

---

## 🎮 Manual Commands

### Post Immediately
```bash
python auto_post_social.py
```

### Batch Post
```bash
python auto_post_social.py posts.txt
```

### Test Credentials
```bash
python test_insta_fb.py
```

### View Dashboard
```bash
python social_dashboard.py
```

---

## 📁 File Structure

```
ai_employee_vault/
├── orchestrator.py                    # Main orchestrator
├── setup_insta_fb.py                 # Setup script
├── test_insta_fb.py                  # Test script
├── auto_post_social.py               # Manual posting
├── social_dashboard.py               # Dashboard
├── mcp_servers/
│   ├── instagram_mcp/
│   │   ├── instagram_client.py
│   │   └── test_instagram_mcp.py
│   └── facebook_mcp/
│       ├── facebook_client.py
│       └── test_facebook_mcp.py
├── Pending_Approval/                 # Posts awaiting approval
│   ├── INSTAGRAM_POST_xxx.md
│   └── FACEBOOK_POST_xxx.md
├── Done/                             # Executed posts
│   ├── EXECUTED_INSTAGRAM_xxx.md
│   └── EXECUTED_FACEBOOK_xxx.md
└── Logs/                             # Audit trail
    └── 2026-03-15.json
```

---

## 🚀 Quick Start

```bash
# 1. Setup
python setup_insta_fb.py

# 2. Test
python test_insta_fb.py

# 3. Start orchestrator
python orchestrator.py

# 4. In another terminal, monitor
tail -f Logs/2026-03-15.json

# 5. Or use dashboard
python social_dashboard.py
```

---

## 🔐 Security

### Token Management
- Tokens stored in .env (not in git)
- Never commit .env file
- Rotate tokens regularly
- Use environment variables in production

### Approval Workflow
- All posts require human approval
- Prevents accidental posts
- Maintains brand safety
- Audit trail for compliance

### Rate Limiting
- Max 5 posts per day per platform
- 5-10 second delay between posts
- Prevents API rate limiting
- Respects platform guidelines

---

## 🐛 Troubleshooting

### Posts Not Posting
```bash
# Check credentials
cat .env | grep -E "INSTAGRAM|FACEBOOK"

# Test credentials
python test_insta_fb.py

# Check logs
tail -f Logs/2026-03-15.json | grep -i error
```

### Orchestrator Not Running
```bash
# Check if running
ps aux | grep orchestrator

# Start with debug
python orchestrator.py --debug

# Check logs
tail -f Logs/2026-03-15.json
```

### Approval Not Working
```bash
# Check Pending_Approval folder
ls -la Pending_Approval/

# Check approval settings
grep -i "approval" .env

# Check orchestrator logs
tail -f Logs/2026-03-15.json | grep -i approval
```

---

## 📈 Analytics

### View Statistics
```bash
python social_dashboard.py
# Select option 4 to view all posts
```

### Export Data
```bash
# Export to CSV
python -c "
import json
from pathlib import Path

posts = json.load(open('social_posts.json'))
print('Platform,Date,Status,Caption')
for p in posts['instagram']:
    print(f'Instagram,{p[\"timestamp\"]},{p[\"status\"]},{p[\"caption\"]}')
for p in posts['facebook']:
    print(f'Facebook,{p[\"timestamp\"]},{p[\"status\"]},{p[\"caption\"]}')
" > posts.csv
```

---

## 🎯 Best Practices

1. **Always Test First**
   - Run `python test_insta_fb.py` before going live
   - Use dry-run mode for testing

2. **Monitor Logs**
   - Keep logs open while posting
   - Check for errors immediately
   - Review audit trail regularly

3. **Approval Workflow**
   - Review all posts before approval
   - Check for brand consistency
   - Verify links and images

4. **Rate Limiting**
   - Don't post more than 5 times per day
   - Space posts 5-10 minutes apart
   - Respect platform guidelines

5. **Credential Management**
   - Rotate tokens monthly
   - Never share tokens
   - Use environment variables
   - Keep .env secure

---

## 📞 Support

### Common Issues

| Issue | Solution |
|-------|----------|
| "Invalid credentials" | Run `python setup_insta_fb.py` |
| "Access Denied" | Check token scopes in Facebook/Instagram |
| "Rate Limited" | Wait 5-10 minutes before posting again |
| "Post not appearing" | Check approval folder, approve manually |
| "Orchestrator not running" | Check logs: `tail -f Logs/2026-03-15.json` |

### Debug Mode
```bash
# Run with debug logging
python orchestrator.py --debug

# Run with verbose output
python auto_post_social.py --verbose

# Test with dry-run
python test_insta_fb.py --dry-run
```

---

## ✅ Checklist

- [ ] Instagram credentials setup
- [ ] Facebook credentials setup
- [ ] Credentials tested
- [ ] Orchestrator running
- [ ] Logs being monitored
- [ ] First post successful
- [ ] Approval workflow working
- [ ] Dashboard accessible

---

**Ready to automate your social media? Start with: `python setup_insta_fb.py`** 🚀
