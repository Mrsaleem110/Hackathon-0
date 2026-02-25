# Silver Tier Setup Guide

**Complete step-by-step guide to set up and run Silver Tier**

---

## Prerequisites

Before starting, ensure you have:

- Python 3.13+
- Node.js v24+ LTS
- Obsidian v1.10.6+
- Claude Code (Pro subscription or Free with Gemini API)
- Git

---

## Step 1: Install Dependencies

```bash
# Navigate to vault directory
cd AI_Employee_Vault

# Install Python dependencies
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
pip install playwright
pip install apscheduler
pip install watchdog

# Install Playwright browsers
playwright install chromium
```

---

## Step 2: Set Up Gmail API (Optional for Demo)

### For Production Use:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download credentials as `gmail_credentials.json`
6. Place in `AI_Employee_Vault/` folder

```bash
# Test Gmail connection
python -c "from Watchers.gmail_watcher import GmailWatcher; w = GmailWatcher('.'); print('Gmail ready')"
```

---

## Step 3: Set Up WhatsApp (Optional for Demo)

### For Production Use:

WhatsApp Watcher uses Playwright to automate WhatsApp Web.

1. First run will open browser for login
2. Scan QR code with your phone
3. Session saved to `.whatsapp_session/`

```bash
# Test WhatsApp connection
python -c "from Watchers.whatsapp_watcher import WhatsAppWatcher; w = WhatsAppWatcher('.'); print('WhatsApp ready')"
```

---

## Step 4: Set Up LinkedIn (Optional for Demo)

### For Production Use:

LinkedIn integration uses Playwright for automation.

1. First run will open browser for login
2. Log in with your LinkedIn account
3. Session saved to `.linkedin_session/`

```bash
# Test LinkedIn connection
python -c "from Watchers.linkedin_watcher import LinkedInWatcher; w = LinkedInWatcher('.'); print('LinkedIn ready')"
```

---

## Step 5: Run Demo Mode

**Start here!** Demo mode creates sample files without requiring real credentials.

```bash
# Run all components in demo mode
python orchestrator.py demo
```

This will:
- ✅ Create sample Gmail messages in `/Needs_Action/`
- ✅ Create sample WhatsApp messages in `/Needs_Action/`
- ✅ Create sample LinkedIn opportunities in `/Needs_Action/`
- ✅ Generate sample plans in `/Plans/`
- ✅ Create sample approval requests in `/Pending_Approval/`
- ✅ Generate sample briefings in `/Briefings/`

**Expected output:**
```
--- Gmail Watcher Demo ---
Created demo action file: ./Needs_Action/GMAIL_demo_1_demo.md
Created demo action file: ./Gmail_demo_2_demo.md

--- WhatsApp Watcher Demo ---
Created demo action file: ./Needs_Action/WHATSAPP_client_a_urgent.md
...

--- LinkedIn Watcher Demo ---
Created demo action file: ./Needs_Action/LINKEDIN_john_smith_partnership.md
...

DEMO COMPLETE
```

---

## Step 6: Verify Folder Structure

After demo run, check that all folders are created:

```bash
# List vault structure
ls -la AI_Employee_Vault/

# Should see:
# Needs_Action/      (with sample files)
# Plans/             (with sample plans)
# Pending_Approval/  (with sample approvals)
# Done/              (empty initially)
# Logs/              (with 2026-02-25.json)
# Watchers/          (all watcher scripts)
# MCP/               (email MCP server)
# Skills/            (agent skills)
```

---

## Step 7: Run One Processing Cycle

```bash
# Process all pending tasks once
python orchestrator.py

# Expected output:
# ============================================================
# Starting processing cycle...
# ============================================================
# Found X files to process
# Processing: GMAIL_demo_1_demo.md
# Created plan: PLAN_GMAIL_demo_1_demo.md
# Dashboard updated
# Processing cycle completed
```

---

## Step 8: Run Continuous Mode

```bash
# Run continuous processing (checks every 5 minutes)
python orchestrator.py continuous

# Or with custom interval (in seconds)
python orchestrator.py continuous 300

# Press Ctrl+C to stop
```

---

## Step 9: Test Approval Workflow

1. Check `/Pending_Approval/` folder for approval requests
2. Review the approval file content
3. Move file to `/Pending_Approval/Approved/` to approve
4. Run orchestrator again to process approved actions
5. Check `/Done/` for completed actions

```bash
# Example: Approve an email
mv Pending_Approval/EMAIL_*.md Pending_Approval/Approved/

# Run orchestrator to execute
python orchestrator.py
```

---

## Step 10: Check Logs

```bash
# View today's audit log
cat Logs/2026-02-25.json | python -m json.tool

# View specific action
grep "email_send" Logs/2026-02-25.json

# View all logs
ls -la Logs/
```

---

## Step 11: Test Individual Components

### Test Gmail Watcher

```python
from Watchers.gmail_watcher import GmailWatcher

watcher = GmailWatcher(".")
watcher.demo_run()  # Creates sample files
# watcher.run()     # Uncomment for production
```

### Test WhatsApp Watcher

```python
from Watchers.whatsapp_watcher import WhatsAppWatcher

watcher = WhatsAppWatcher(".")
watcher.demo_run()  # Creates sample files
# watcher.run()     # Uncomment for production
```

### Test LinkedIn Integration

```python
from Watchers.linkedin_watcher import LinkedInWatcher
from Watchers.linkedin_poster import LinkedInPoster

watcher = LinkedInWatcher(".")
watcher.demo_run()  # Creates sample opportunities

poster = LinkedInPoster(".")
poster.demo_run()   # Creates sample posts for approval
```

### Test Reasoning Engine

```python
from reasoning_engine import ClaudeReasoningEngine

engine = ClaudeReasoningEngine(".")
engine.demo_run()      # Creates sample plans
# engine.process_tasks()  # Uncomment for production
```

### Test Approval Handler

```python
from approval_handler import ApprovalHandler

handler = ApprovalHandler(".")
handler.demo_run()  # Creates sample approval requests
# handler.process_approved_actions()  # Uncomment for production
```

### Test Task Scheduler

```python
from scheduler import TaskScheduler

scheduler = TaskScheduler(".")
scheduler.demo_run()  # Creates sample briefings
# scheduler.start_scheduler()  # Uncomment for production
```

---

## Step 12: Set Up Real Credentials (Production)

### Gmail API Setup

```bash
# Set environment variables
export GMAIL_CLIENT_ID="your_client_id"
export GMAIL_CLIENT_SECRET="your_client_secret"

# Or create .env file
echo "GMAIL_CLIENT_ID=your_client_id" > .env
echo "GMAIL_CLIENT_SECRET=your_client_secret" >> .env

# Add to .gitignore
echo ".env" >> .gitignore
```

### WhatsApp Session

```bash
# First run will prompt for QR code scan
python -c "from Watchers.whatsapp_watcher import WhatsAppWatcher; w = WhatsAppWatcher('.'); w.run()"

# Session saved to .whatsapp_session/
```

### LinkedIn Session

```bash
# First run will prompt for login
python -c "from Watchers.linkedin_watcher import LinkedInWatcher; w = LinkedInWatcher('.'); w.run()"

# Session saved to .linkedin_session/
```

---

## Step 13: Configure Scheduling

### On Windows (Task Scheduler)

```bash
# Create scheduled task for daily briefing
# Open Task Scheduler and create new task:
# - Trigger: Daily at 8:00 AM
# - Action: Run python orchestrator.py
# - Location: C:\Users\YourName\Documents\GitHub\Hackathon-0\AI_Employee_Vault
```

### On Mac/Linux (Cron)

```bash
# Edit crontab
crontab -e

# Add daily briefing at 8:00 AM
0 8 * * * cd /path/to/AI_Employee_Vault && python orchestrator.py

# Add weekly audit on Sunday at 8:00 PM
0 20 * * 0 cd /path/to/AI_Employee_Vault && python orchestrator.py
```

---

## Step 14: Integrate with Claude Code

### Create Claude Code Skill

```bash
# Create skill file
mkdir -p ~/.claude/skills
cat > ~/.claude/skills/ai_employee.md << 'EOF'
# AI Employee Skill

Process tasks from AI Employee vault.

## Usage
```
claude ai-employee process
```

## What it does
- Reads from /Needs_Action/
- Creates plans in /Plans/
- Manages approvals in /Pending_Approval/
- Logs all actions to /Logs/
EOF
```

---

## Troubleshooting

### Issue: "No module named 'playwright'"

```bash
pip install playwright
playwright install chromium
```

### Issue: "Gmail service not available"

```bash
# Check credentials
ls -la gmail_credentials.json

# If missing, set up Gmail API (see Step 2)
```

### Issue: "WhatsApp session not found"

```bash
# First run needs QR code scan
python -c "from Watchers.whatsapp_watcher import WhatsAppWatcher; w = WhatsAppWatcher('.'); w.run()"
```

### Issue: "Scheduler not running"

```bash
# Install APScheduler
pip install apscheduler

# Check if running
python -c "from scheduler import TaskScheduler; s = TaskScheduler('.'); print(s.get_scheduled_jobs())"
```

### Issue: "Approval files not processing"

```bash
# Check file location
ls -la Pending_Approval/Approved/

# Check logs for errors
cat Logs/2026-02-25.json | grep "approval"
```

---

## Next Steps

1. ✅ Run demo mode
2. ✅ Test individual components
3. ✅ Set up real credentials
4. ✅ Run continuous processing
5. ✅ Test approval workflow
6. ✅ Configure scheduling
7. 🔄 Monitor logs and dashboard
8. 📈 Upgrade to Gold Tier

---

## Support

For issues or questions:
- Check logs: `Logs/2026-02-25.json`
- Review Company_Handbook.md for rules
- Check Dashboard.md for status
- Run demo mode to verify setup

---

*Silver Tier Setup Guide*
*February 25, 2026*
