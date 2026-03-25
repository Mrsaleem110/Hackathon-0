# 🚀 QUICK START GUIDE - USE BEFORE DEPLOYMENT

**Date**: 2026-03-26
**Purpose**: Test and use the Gold Tier system locally
**Time to Setup**: 15-30 minutes

---

## STEP 1: INSTALL DEPENDENCIES

```bash
cd "C:\Users\Agentic Sphere\Documents\GitHub\Hackathon-0\ai_employee_vault"

# Install all MCP server dependencies
pip install -r mcp_servers/email_mcp/requirements.txt
pip install -r mcp_servers/vault_mcp/requirements.txt
pip install -r mcp_servers/whatsapp_mcp/requirements.txt
pip install -r mcp_servers/linkedin_mcp/requirements.txt

# Install additional dependencies
pip install apscheduler requests
```

---

## STEP 2: START MCP SERVERS (Open 4 terminals)

### Terminal 1: Email MCP Server
```bash
cd mcp_servers/email_mcp
python server.py
# Output: INFO:     Uvicorn running on http://0.0.0.0:8070
```

### Terminal 2: Vault MCP Server
```bash
cd mcp_servers/vault_mcp
python server.py
# Output: INFO:     Uvicorn running on http://0.0.0.0:8072
```

### Terminal 3: WhatsApp MCP Server
```bash
cd mcp_servers/whatsapp_mcp
python server.py
# Output: INFO:     Uvicorn running on http://0.0.0.0:8073
```

### Terminal 4: LinkedIn MCP Server
```bash
cd mcp_servers/linkedin_mcp
python server.py
# Output: INFO:     Uvicorn running on http://0.0.0.0:8075
```

---

## STEP 3: TEST MCP SERVERS (New terminal)

```bash
# Test Email MCP
python mcp_servers/email_mcp/test_email_mcp.py

# Test Vault MCP
python mcp_servers/vault_mcp/test_vault_mcp.py

# Test WhatsApp MCP
python mcp_servers/whatsapp_mcp/test_whatsapp_mcp.py

# Test LinkedIn MCP
python mcp_servers/linkedin_mcp/test_linkedin_mcp.py
```

Expected output: ✅ All tests passing

---

## STEP 4: USE AGENT SKILLS

### Example 1: Send WhatsApp Message

```python
from agent_skills.whatsapp_skill import WhatsAppSkill

wa = WhatsAppSkill()
result = wa.send_whatsapp_message(
    phone="+1234567890",
    message="Hello from AI Employee Vault!"
)
print(result)
# Output: {'success': True, 'message_id': '...', 'phone': '+1234567890'}
```

### Example 2: Post to LinkedIn

```python
from agent_skills.linkedin_skill import LinkedInSkill

li = LinkedInSkill()
result = li.post_to_linkedin(
    text="Excited to announce the Gold Tier completion!",
    visibility="PUBLIC"
)
print(result)
# Output: {'success': True, 'post_id': '...'}
```

### Example 3: Generate Report

```python
from agent_skills.reporting_skill import ReportingSkill

rep = ReportingSkill()
daily = rep.generate_daily_report()
print(daily)
# Output: {'success': True, 'report': {...}}
```

### Example 4: Log Action

```python
from agent_skills.audit_skill import AuditSkill

audit = AuditSkill()
result = audit.log_action(
    action_type="email_sent",
    details={"to": "user@example.com", "subject": "Test"},
    status="success"
)
print(result)
# Output: {'success': True, 'log_id': '...'}
```

---

## STEP 5: USE DOMAIN ROUTER

```python
from domain_router_enhanced import DomainRouter

router = DomainRouter()

# Route personal email
domain, config = router.route_email("personal@gmail.com")
print(f"Domain: {domain.value}")  # Output: personal

# Route business email
domain, config = router.route_email("business@company.com")
print(f"Domain: {domain.value}")  # Output: business

# Route WhatsApp
domain, config = router.route_whatsapp("+1234567890")
print(f"Domain: {domain.value}")  # Output: personal or business
```

---

## STEP 6: USE CEO BRIEFING SCHEDULER

```python
from ceo_briefing_scheduler import CEOBriefingScheduler

scheduler = CEOBriefingScheduler(ceo_email="ceo@company.com")

# Schedule weekly briefing (Monday 9 AM)
scheduler.schedule_weekly_briefing(day_of_week='mon', hour=9, minute=0)

# Start scheduler
scheduler.start()
print("CEO Briefing Scheduler started!")

# Send briefing immediately (for testing)
scheduler.send_briefing()
print("Briefing sent!")

# Stop scheduler when done
# scheduler.stop()
```

---

## STEP 7: USE ERROR RECOVERY

```python
from error_recovery_manager import ErrorRecoveryManager, Platform

recovery = ErrorRecoveryManager()

# Execute with fallback methods
result = recovery.execute_with_fallback(
    action="send_email",
    platform=Platform.EMAIL,
    to="user@example.com",
    subject="Test Email",
    body="This is a test"
)
print(result)
# Output: {'success': True, 'method': 'gmail_api', ...}

# Get recovery statistics
stats = recovery.get_recovery_stats()
print(stats)
# Output: {'total_errors': 0, 'errors_by_platform': {}, 'recovery_rate': 100}
```

---

## STEP 8: USE ENHANCED ORCHESTRATOR

```python
from orchestrator_enhanced import EnhancedOrchestrator, Task

orchestrator = EnhancedOrchestrator()

# Create a task with steps
task = Task(
    task_id="task_001",
    title="Send Email Campaign",
    steps=[
        {
            'name': 'Validate Recipients',
            'type': 'validation',
            'action': 'validate_email_list',
            'expected_output': 'validation passed',
            'has_rollback': False
        },
        {
            'name': 'Generate Email Content',
            'type': 'generation',
            'action': 'generate_email_content',
            'expected_output': 'content generated',
            'has_rollback': False
        },
        {
            'name': 'Send Emails',
            'type': 'action',
            'action': 'send_emails',
            'expected_output': 'emails sent',
            'has_rollback': True,
            'rollback_action': 'recall_emails'
        },
        {
            'name': 'Log Results',
            'type': 'logging',
            'action': 'log_campaign_results',
            'expected_output': 'results logged',
            'has_rollback': False
        }
    ]
)

# Execute task with verification (Ralph Wiggum Loop)
success = orchestrator.execute_task_with_verification(task)
print(f"Task execution: {'SUCCESS' if success else 'FAILED'}")

# Get execution statistics
stats = orchestrator.get_execution_stats()
print(stats)
```

---

## STEP 9: TEST COMPLETE WORKFLOW

```python
# Complete workflow example
from agent_skills.whatsapp_skill import WhatsAppSkill
from agent_skills.linkedin_skill import LinkedInSkill
from agent_skills.audit_skill import AuditSkill
from domain_router_enhanced import DomainRouter

# 1. Route incoming message
router = DomainRouter()
domain, config = router.route_whatsapp("+1234567890")
print(f"Message routed to: {domain.value}")

# 2. Send WhatsApp response
wa = WhatsAppSkill()
wa.send_whatsapp_message("+1234567890", "Thanks for your message!")

# 3. Post update to LinkedIn
li = LinkedInSkill()
li.post_to_linkedin("Just processed a customer inquiry!")

# 4. Log the action
audit = AuditSkill()
audit.log_action(
    action_type="whatsapp_processed",
    details={"phone": "+1234567890", "domain": domain.value},
    status="success"
)

print("✅ Complete workflow executed successfully!")
```

---

## STEP 10: CHECK LOGS

```bash
# View audit logs
ls -la Logs/

# View latest log file
cat Logs/2026-03-26.json

# View briefings
ls -la Briefings/

# View tasks
ls -la Tasks/
```

---

## TROUBLESHOOTING

### Issue: Port already in use
```bash
# Find process using port 8070
lsof -i :8070

# Kill process
kill -9 <PID>
```

### Issue: Gmail authentication fails
```bash
# Make sure credentials.json exists in email_mcp directory
# Or set GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET environment variables
```

### Issue: MCP server won't start
```bash
# Check if all dependencies are installed
pip list | grep fastapi
pip list | grep uvicorn

# Reinstall if needed
pip install --upgrade fastapi uvicorn
```

---

## NEXT: DEPLOYMENT

Once you've tested everything locally and it's working:

1. **Verify all tests pass**
   ```bash
   python mcp_servers/*/test_*.py
   ```

2. **Check logs for errors**
   ```bash
   cat Logs/*.json
   ```

3. **Review audit trail**
   ```bash
   cat Logs/audit_*.json
   ```

4. **Then proceed to deployment** (Docker, cloud, etc.)

---

## QUICK REFERENCE

| Component | Port | Start Command |
|---|---|---|
| Email MCP | 8070 | `cd mcp_servers/email_mcp && python server.py` |
| Vault MCP | 8072 | `cd mcp_servers/vault_mcp && python server.py` |
| WhatsApp MCP | 8073 | `cd mcp_servers/whatsapp_mcp && python server.py` |
| LinkedIn MCP | 8075 | `cd mcp_servers/linkedin_mcp && python server.py` |

---

## SUPPORT

For issues or questions:
1. Check the logs in `Logs/` directory
2. Review the documentation in `GOLD_TIER_COMPLETION_SUMMARY.md`
3. Check the verification report in `VERIFICATION_REPORT.md`

---

**Status**: Ready to use locally ✅
**Next Step**: Test all components, then deploy

