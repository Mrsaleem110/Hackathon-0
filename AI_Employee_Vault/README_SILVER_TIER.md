# AI Employee - Silver Tier Implementation Guide

**Status**: Silver Tier Complete ✅
**Date**: February 25, 2026
**Version**: 0.2

---

## 🎯 What is Silver Tier?

Silver Tier transforms your AI Employee from a basic foundation into a **Functional Assistant** that:
- Monitors multiple communication channels (Gmail, WhatsApp, LinkedIn)
- Generates intelligent plans for complex tasks
- Manages approval workflows for sensitive actions
- Automatically schedules and executes tasks
- Posts business updates to LinkedIn
- Maintains comprehensive audit logs

---

## 📋 Silver Tier Requirements - All Complete ✅

| Requirement | Status | Component |
|------------|--------|-----------|
| Two or more Watchers | ✅ | Gmail, WhatsApp, LinkedIn |
| LinkedIn auto-posting | ✅ | LinkedIn Poster |
| Claude reasoning loop | ✅ | Reasoning Engine |
| MCP server for actions | ✅ | Email MCP Server |
| Human-in-the-loop approval | ✅ | Approval Handler |
| Basic scheduling | ✅ | Task Scheduler |
| Agent Skills | ✅ | 7 Skills implemented |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL SOURCES                         │
│  Gmail │ WhatsApp │ LinkedIn │ Files │ Banking              │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              PERCEPTION LAYER (Watchers)                    │
│  Gmail Watcher │ WhatsApp Watcher │ LinkedIn Watcher        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│           OBSIDIAN VAULT (Local Knowledge Base)             │
│  /Needs_Action/ │ /Plans/ │ /Pending_Approval/ │ /Done/    │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│            REASONING LAYER (Claude Code)                    │
│  Reasoning Engine │ Plan Generation │ Task Analysis         │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────────┐    ┌────────▼──────────┐
│ HUMAN-IN-LOOP    │    │  ACTION LAYER     │
│ Approval Handler │    │  MCP Servers      │
│ /Pending_Approval│    │  Email, LinkedIn  │
└──────────────────┘    └───────────────────┘
```

---

## 📁 Folder Structure

```
AI_Employee_Vault/
│
├── 📄 Dashboard.md                 # Silver Tier status dashboard
├── 📄 Company_Handbook.md          # Rules of engagement
├── 📄 Business_Goals.md            # Business objectives
│
├── 📂 Needs_Action/                # Incoming tasks from watchers
│   ├── GMAIL_*.md
│   ├── WHATSAPP_*.md
│   └── LINKEDIN_*.md
│
├── 📂 Plans/                       # Claude-generated plans
│   ├── PLAN_*.md
│   └── Archive/
│
├── 📂 Pending_Approval/            # Approval workflow
│   ├── EMAIL_*.md
│   ├── PAYMENT_*.md
│   ├── LINKEDIN_POST_*.md
│   ├── Approved/                   # Move here to execute
│   ├── Rejected/                   # Move here to cancel
│   └── Archive/
│
├── 📂 Done/                        # Completed tasks
│   └── (moved from Needs_Action)
│
├── 📂 Business_Updates/            # LinkedIn content
│   ├── draft_*.md
│   └── scheduled_*.md
│
├── 📂 Logs/                        # Audit trail
│   ├── 2026-02-25.json
│   └── Archive/
│
├── 📂 Watchers/                    # Watcher scripts
│   ├── base_watcher.py
│   ├── gmail_watcher.py
│   ├── whatsapp_watcher.py
│   ├── linkedin_watcher.py
│   └── linkedin_poster.py
│
├── 📂 MCP/                         # MCP servers
│   ├── email_mcp_server.py
│   └── email_mcp_config.json
│
├── 📂 Skills/                      # Agent Skills
│   ├── email_processor.py
│   ├── whatsapp_processor.py
│   ├── linkedin_poster.py
│   ├── plan_generator.py
│   ├── approval_manager.py
│   └── __init__.py
│
├── 🐍 orchestrator.py              # Master coordinator
├── 🐍 reasoning_engine.py          # Claude reasoning
├── 🐍 approval_handler.py          # Approval workflow
├── 🐍 scheduler.py                 # Task scheduling
└── 📄 README.md                    # This file
```

---

## 🚀 Quick Start

### 1. Installation

```bash
# Install required dependencies
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
pip install playwright
pip install apscheduler

# Install Playwright browsers
playwright install chromium
```

### 2. Run Demo Mode

```bash
# Test all components in demo mode
cd AI_Employee_Vault
python orchestrator.py demo
```

This will:
- Create sample Gmail action files
- Create sample WhatsApp messages
- Create sample LinkedIn opportunities
- Generate sample plans
- Create sample approval requests
- Generate sample briefings

### 3. Run Processing Cycle

```bash
# Run one processing cycle
python orchestrator.py

# Run continuous processing (every 5 minutes)
python orchestrator.py continuous

# Run continuous with custom interval (in seconds)
python orchestrator.py continuous 300
```

---

## 🔧 Component Details

### Gmail Watcher
**File**: `Watchers/gmail_watcher.py`

Monitors Gmail for urgent messages and creates action files.

```python
from Watchers.gmail_watcher import GmailWatcher

watcher = GmailWatcher(vault_path=".")
watcher.demo_run()  # Create sample files
watcher.run()       # Start monitoring
```

**Keywords monitored**: urgent, asap, help, payment, invoice

### WhatsApp Watcher
**File**: `Watchers/whatsapp_watcher.py`

Monitors WhatsApp Web for urgent messages using Playwright.

```python
from Watchers.whatsapp_watcher import WhatsAppWatcher

watcher = WhatsAppWatcher(vault_path=".")
watcher.demo_run()  # Create sample files
watcher.run()       # Start monitoring
```

**Keywords monitored**: urgent, asap, help, invoice, payment, emergency, important

### LinkedIn Integration
**File**: `Watchers/linkedin_watcher.py` + `Watchers/linkedin_poster.py`

Monitors LinkedIn for opportunities and auto-posts business updates.

```python
from Watchers.linkedin_watcher import LinkedInWatcher
from Watchers.linkedin_poster import LinkedInPoster

watcher = LinkedInWatcher(vault_path=".")
poster = LinkedInPoster(vault_path=".")

watcher.demo_run()  # Create sample opportunities
poster.demo_run()   # Create sample posts for approval
```

### Claude Reasoning Engine
**File**: `reasoning_engine.py`

Analyzes tasks and creates structured plans.

```python
from reasoning_engine import ClaudeReasoningEngine

engine = ClaudeReasoningEngine(vault_path=".")
engine.demo_run()      # Create sample plans
engine.process_tasks() # Process pending tasks
```

### Email MCP Server
**File**: `MCP/email_mcp_server.py`

Sends emails via Gmail API through MCP interface.

```python
from MCP.email_mcp_server import EmailMCPServer

server = EmailMCPServer(vault_path=".")
result = server.send_email(
    to="client@example.com",
    subject="Invoice #1234",
    body="Please find attached your invoice."
)
```

### Approval Handler
**File**: `approval_handler.py`

Manages human-in-the-loop approval workflow.

```python
from approval_handler import ApprovalHandler

handler = ApprovalHandler(vault_path=".")

# Create approval request
handler.create_approval_request(
    action_type='email_send',
    details={
        'id': 'client_a_invoice',
        'to': 'client@example.com',
        'subject': 'Invoice #1234',
        'body': 'Please find attached...'
    }
)

# Process approvals
handler.process_approved_actions()
handler.process_rejected_actions()
handler.handle_expired_approvals()
```

### Task Scheduler
**File**: `scheduler.py`

Schedules automated tasks like daily briefings and weekly audits.

```python
from scheduler import TaskScheduler

scheduler = TaskScheduler(vault_path=".")
scheduler.start_scheduler()

# Scheduled jobs:
# - Daily briefing at 8:00 AM
# - Weekly audit on Sunday at 8:00 PM
# - Process posts daily at 9:00 AM
# - Cleanup logs monthly on 1st at 2:00 AM
```

### Master Orchestrator
**File**: `orchestrator.py`

Coordinates all components and implements Ralph Wiggum loop.

```python
from orchestrator import VaultOrchestrator

orchestrator = VaultOrchestrator(vault_path=".")

# Run one cycle
orchestrator.run_once()

# Run continuously
orchestrator.run_continuous(interval=300)

# Get status
status = orchestrator.get_system_status()
```

---

## 🔐 Security & Privacy

### Credential Management

**Never store credentials in plain text!**

```bash
# Use environment variables
export GMAIL_CLIENT_ID="your_client_id"
export GMAIL_CLIENT_SECRET="your_client_secret"
export LINKEDIN_TOKEN="your_token"

# Or use .env file (add to .gitignore)
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
```

### Approval Workflow

All sensitive actions require human approval:

1. **Email sends** to new contacts
2. **Payments** over $100
3. **LinkedIn posts** (all)
4. **New vendor interactions**

Move files to `/Pending_Approval/Approved/` to execute.

### Audit Logging

All actions are logged to `/Logs/YYYY-MM-DD.json`:

```json
{
  "timestamp": "2026-02-25T20:34:59Z",
  "action": "email_send",
  "status": "success",
  "component": "email_mcp"
}
```

---

## 📊 Workflow Examples

### Example 1: Invoice Request via WhatsApp

1. **Trigger**: Client sends "urgent: can you send the invoice asap?"
2. **Watcher**: WhatsApp Watcher detects keyword "urgent" + "invoice"
3. **Action File**: Creates `WHATSAPP_client_a_urgent.md` in `/Needs_Action/`
4. **Reasoning**: Claude Reasoning Engine analyzes and creates `PLAN_client_a_urgent.md`
5. **Plan**: Includes steps to generate invoice, send email, log transaction
6. **Approval**: Creates `EMAIL_invoice_client_a.md` in `/Pending_Approval/`
7. **Human Review**: You review and move to `/Pending_Approval/Approved/`
8. **Execution**: Email MCP Server sends invoice
9. **Logging**: Action logged to audit trail
10. **Completion**: Files moved to `/Done/`

### Example 2: LinkedIn Post Scheduling

1. **Trigger**: You create `Business_Updates/draft_q1_update.md`
2. **Scheduler**: Daily at 9:00 AM, moves to `/Pending_Approval/`
3. **LinkedIn Poster**: Creates approval request with post preview
4. **Human Review**: You review and move to `/Pending_Approval/Approved/`
5. **Execution**: LinkedIn Poster publishes to LinkedIn
6. **Logging**: Post action logged
7. **Completion**: Moved to `/Done/`

### Example 3: Daily Briefing

1. **Trigger**: Scheduler runs at 8:00 AM
2. **Generation**: Task Scheduler generates daily briefing
3. **Content**: Includes pending tasks, completed items, metrics
4. **Location**: Saved to `/Briefings/2026-02-25_briefing.md`
5. **Dashboard**: Dashboard updated with briefing link

---

## 🧪 Testing

### Run Demo Mode

```bash
python orchestrator.py demo
```

Creates sample files for all components without requiring real credentials.

### Test Individual Components

```python
# Test Gmail Watcher
from Watchers.gmail_watcher import GmailWatcher
watcher = GmailWatcher(".")
watcher.demo_run()

# Test WhatsApp Watcher
from Watchers.whatsapp_watcher import WhatsAppWatcher
watcher = WhatsAppWatcher(".")
watcher.demo_run()

# Test Approval Handler
from approval_handler import ApprovalHandler
handler = ApprovalHandler(".")
handler.demo_run()
```

### Check Logs

```bash
# View today's logs
cat Logs/2026-02-25.json | python -m json.tool

# View all actions
grep "action" Logs/*.json
```

---

## 🔄 Workflow: How It All Works Together

```
┌─────────────────────────────────────────────────────────────┐
│ 1. PERCEPTION: Watchers detect events                       │
│    Gmail → WhatsApp → LinkedIn → Files                      │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│ 2. STORAGE: Create action files in /Needs_Action/           │
│    GMAIL_*.md │ WHATSAPP_*.md │ LINKEDIN_*.md               │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│ 3. REASONING: Claude analyzes and creates plans             │
│    PLAN_*.md with steps, approvals, estimates               │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│ 4. APPROVAL: Create approval requests if needed             │
│    Move to /Pending_Approval/ for human review              │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│ 5. HUMAN REVIEW: You approve or reject                      │
│    Move to /Approved/ or /Rejected/                         │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│ 6. EXECUTION: MCP servers execute approved actions          │
│    Send emails, post to LinkedIn, etc.                      │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│ 7. LOGGING: All actions logged to audit trail               │
│    /Logs/YYYY-MM-DD.json                                    │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│ 8. COMPLETION: Move to /Done/ and update Dashboard          │
│    Task complete, ready for next cycle                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 Next Steps: Gold Tier

After mastering Silver Tier, upgrade to **Gold Tier** for:

- Full cross-domain integration (Personal + Business)
- Odoo Community integration for accounting
- Facebook and Instagram integration
- Twitter/X integration
- Multiple MCP servers for different action types
- Weekly Business and Accounting Audit with CEO Briefing
- Error recovery and graceful degradation
- Ralph Wiggum loop for autonomous multi-step completion

---

## 🆘 Troubleshooting

### Watchers not detecting messages

1. Check credentials are set up correctly
2. Run in demo mode first: `python orchestrator.py demo`
3. Check logs: `cat Logs/2026-02-25.json`

### Approval requests not processing

1. Ensure files are in `/Pending_Approval/Approved/`
2. Check file format matches expected structure
3. Check logs for errors

### Scheduler not running

1. Install APScheduler: `pip install apscheduler`
2. Check system time is correct
3. Verify scheduler started: `scheduler.get_scheduled_jobs()`

### Email MCP not sending

1. Set up Gmail API credentials
2. Run in demo mode first
3. Check Gmail API is enabled in Google Cloud Console

---

## 📚 Resources

- [Claude Code Documentation](https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows)
- [Obsidian Help](https://help.obsidian.md/)
- [Gmail API](https://developers.google.com/gmail/api)
- [Playwright Documentation](https://playwright.dev/python/)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)

---

## 📝 License

This project is part of the Personal AI Employee Hackathon 0.

---

*AI Employee v0.2 - Silver Tier*
*Functional Assistant Implementation*
*February 25, 2026*
