# WhatsApp MCP Server - Setup Guide

## Overview
WhatsApp MCP Server provides manual WhatsApp message handling through the MCP protocol. Since WhatsApp Web automation is unreliable, this server enables task creation and reply drafting for manual sending.

## Features

### 1. Create WhatsApp Task
Convert WhatsApp messages into vault tasks:
```python
create_whatsapp_task(
    sender="Client A",
    message="Urgent: Need invoice #1234 ASAP",
    priority="high"  # low, medium, high
)
```

### 2. List WhatsApp Tasks
View all pending WhatsApp tasks in Needs_Action folder.

### 3. Draft Reply
Create reply drafts for manual sending:
```python
send_whatsapp_reply(
    recipient="Client A",
    message="I'll send invoice #1234 right away!"
)
```

## Installation

### 1. Test the Server
```bash
cd "C:\Users\Agentic Sphere\Documents\GitHub\Hackathon-0\ai_employee_vault"
python test_whatsapp_mcp.py
```

### 2. Add to Claude Code
The server is already configured in `mcp_config.json`:
```json
{
  "whatsapp": {
    "command": "python",
    "args": ["whatsapp_mcp_server.py"]
  }
}
```

### 3. Restart Claude Code
Restart Claude Code to load the WhatsApp MCP server.

## Usage in Claude Code

### Create Task from Message
```
Create a WhatsApp task:
- Sender: Client A
- Message: "Urgent: Need invoice #1234 ASAP for records"
- Priority: high
```

### List Pending Tasks
```
List all WhatsApp tasks
```

### Draft Reply
```
Draft a WhatsApp reply to Client A:
"Hi! I'll send invoice #1234 right away. Thanks for your patience!"
```

## Workflow

1. **Receive Message** - You get a WhatsApp message
2. **Create Task** - Use MCP to create task in vault
3. **AI Plans** - Claude creates execution plan
4. **Draft Reply** - MCP creates reply draft
5. **Manual Send** - You copy and send via WhatsApp
6. **Mark Done** - Move to Done folder

## Files Created

### Task File (Needs_Action/)
```markdown
---
type: whatsapp
from: "Client A"
priority: high
status: pending
---

## Message from Client A
Urgent: Need invoice #1234 ASAP

## Suggested Actions
- [ ] Read and understand the message
- [ ] Determine appropriate response
- [ ] Draft reply
- [ ] Send reply manually via WhatsApp
```

### Reply Draft (Pending_Approval/)
```markdown
---
type: whatsapp_reply
to: "Client A"
status: draft
---

## WhatsApp Reply Draft

**To:** Client A

**Message:**
Hi! I'll send invoice #1234 right away.

## Instructions
1. Review the message
2. Copy the message
3. Open WhatsApp and find Client A
4. Paste and send
5. Move to Done/ when sent
```

## Why Manual Sending?

WhatsApp Web automation is unreliable:
- Session expires frequently
- Browser crashes in headless mode
- WhatsApp blocks automation
- QR code re-login required

Manual sending is:
- ✅ More reliable
- ✅ Faster to implement
- ✅ No session management
- ✅ Works every time

## Test Results

```
✅ All tests passed!
- List Tools: PASS
- Create WhatsApp Task: PASS
- List WhatsApp Tasks: PASS
- Draft Reply: PASS
```

## Integration with Vault

The WhatsApp MCP server integrates seamlessly:
- Tasks appear in Needs_Action/
- Drafts go to Pending_Approval/
- Completed items move to Done/
- All logged in Logs/

## Next Steps

1. Test creating a task
2. Test drafting a reply
3. Use in real workflow
4. Integrate with orchestrator

---
**Status:** ✅ Complete and Tested
**Date:** 2026-03-09
**Tests:** 4/4 Passed
