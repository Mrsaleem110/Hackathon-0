# 🚀 LOCAL PRODUCTION - QUICK START GUIDE

**Date**: 2026-03-26
**Status**: All 4 MCP servers running and healthy
**Mode**: Local Production (Development/Testing)

---

## CURRENT STATUS

All MCP servers are running:
- ✅ Vault MCP (8072) - HEALTHY
- ✅ Email MCP (8070) - HEALTHY
- ✅ WhatsApp MCP (8073) - HEALTHY
- ✅ LinkedIn MCP (8075) - HEALTHY

---

## HOW TO USE THE SYSTEM

### 1. Test MCP Servers

```bash
# Test all servers
curl http://localhost:8070/health
curl http://localhost:8072/health
curl http://localhost:8073/health
curl http://localhost:8075/health
```

### 2. Use Agent Skills

```python
from agent_skills.whatsapp_skill import WhatsAppSkill
from agent_skills.linkedin_skill import LinkedInSkill
from agent_skills.audit_skill import AuditSkill

# Send WhatsApp message
wa = WhatsAppSkill()
wa.send_whatsapp_message("+1234567890", "Hello!")

# Post to LinkedIn
li = LinkedInSkill()
li.post_to_linkedin("Great news!")

# Log action
audit = AuditSkill()
audit.log_action("test_action", {"data": "test"}, "success")
```

### 3. Use Domain Router

```python
from domain_router_enhanced import DomainRouter

router = DomainRouter()

# Route personal email
domain, config = router.route_email("personal@gmail.com")
print(f"Domain: {domain.value}")  # Output: personal

# Route business email
domain, config = router.route_email("business@company.com")
print(f"Domain: {domain.value}")  # Output: business
```

### 4. Use CEO Briefing Scheduler

```python
from ceo_briefing_scheduler import CEOBriefingScheduler

scheduler = CEOBriefingScheduler(ceo_email="ceo@company.com")

# Schedule weekly briefing (Monday 9 AM)
scheduler.schedule_weekly_briefing(day_of_week='mon', hour=9, minute=0)

# Start scheduler
scheduler.start()

# Send briefing immediately (for testing)
scheduler.send_briefing()
```

### 5. Use Error Recovery Manager

```python
from error_recovery_manager import ErrorRecoveryManager, Platform

recovery = ErrorRecoveryManager()

# Execute with fallback methods
result = recovery.execute_with_fallback(
    action="send_email",
    platform=Platform.EMAIL,
    to="user@example.com",
    subject="Test",
    body="Test email"
)

# Get recovery statistics
stats = recovery.get_recovery_stats()
print(stats)
```

### 6. Use Enhanced Orchestrator

```python
from orchestrator_enhanced import EnhancedOrchestrator, Task

orchestrator = EnhancedOrchestrator()

# Create a task
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
            'name': 'Send Emails',
            'type': 'action',
            'action': 'send_emails',
            'expected_output': 'emails sent',
            'has_rollback': True,
            'rollback_action': 'recall_emails'
        }
    ]
)

# Execute task with verification
success = orchestrator.execute_task_with_verification(task)
print(f"Task execution: {'SUCCESS' if success else 'FAILED'}")
```

---

## COMPLETE WORKFLOW EXAMPLE

```python
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

## CHECK LOGS

```bash
# View audit logs
cat Logs/2026-03-26.json

# View briefings
ls -la Briefings/

# View tasks
ls -la Tasks/
```

---

## STOP SERVERS (When Done)

To stop the MCP servers, go to each terminal and press `Ctrl+C`:

```bash
# Terminal 1: Vault MCP
Ctrl+C

# Terminal 2: Email MCP
Ctrl+C

# Terminal 3: WhatsApp MCP
Ctrl+C

# Terminal 4: LinkedIn MCP
Ctrl+C
```

---

## TROUBLESHOOTING

### Port Already in Use
```bash
lsof -i :8070
kill -9 <PID>
```

### Server Not Responding
```bash
# Check if server is running
curl http://localhost:8070/health

# If not, restart the server
cd mcp_servers/email_mcp && python server.py
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r mcp_servers/email_mcp/requirements.txt
pip install -r mcp_servers/vault_mcp/requirements.txt
pip install -r mcp_servers/whatsapp_mcp/requirements.txt
pip install -r mcp_servers/linkedin_mcp/requirements.txt
```

---

## NEXT STEPS

### Option 1: Continue Testing Locally
- Use the examples above to test different components
- Experiment with agent skills
- Test complete workflows

### Option 2: Add Real Credentials (Optional)
- Gmail OAuth for real email sending
- LinkedIn API token for real posts
- WhatsApp Business API token for real messages

### Option 3: Deploy to Production
- Choose Docker, Cloud, or Kubernetes
- Follow DEPLOYMENT_ACTION_PLAN.md
- Monitor system metrics

---

## SUPPORT

For issues:
1. Check LOCAL_TESTING_COMPLETE.md
2. Review logs in Logs/ directory
3. Check health endpoints
4. Review DEPLOYMENT_GUIDE.md

---

**Status**: ✅ LOCAL PRODUCTION READY
**All Servers**: ✅ RUNNING
**Ready to Use**: ✅ YES

---

*Created: 2026-03-26*
*By: Claude Code*
*Status: READY FOR USE*
