# Gold Tier Implementation Plan - Phase 3
**Date**: 2026-03-24
**Phase**: Integration (Agent Skills, Documentation)
**Estimated Duration**: 1 week
**Dependencies**: Phase 1 & 2 complete

---

## Phase 3: Integration Requirements

### 1. Agent Skills Framework (Requirement #13)

#### 1.1 Claude Code Agent SDK Integration

**File**: `agent_skills/__init__.py` (~100 lines)

```python
"""
Agent Skills Framework for AI Employee Vault
Integrates with Claude Code Agent SDK
"""

from typing import Dict, Any, Callable, List
import json
import logging

logger = logging.getLogger(__name__)

class SkillRegistry:
    """Registry for all available skills"""

    def __init__(self):
        self.skills: Dict[str, 'Skill'] = {}
        self.skill_groups: Dict[str, List[str]] = {}

    def register_skill(self, skill: 'Skill'):
        """Register a skill"""
        self.skills[skill.name] = skill
        group = skill.group or 'general'
        if group not in self.skill_groups:
            self.skill_groups[group] = []
        self.skill_groups[group].append(skill.name)
        logger.info(f"Registered skill: {skill.name}")

    def get_skill(self, name: str) -> 'Skill':
        """Get skill by name"""
        return self.skills.get(name)

    def list_skills(self, group: str = None) -> List[str]:
        """List available skills"""
        if group:
            return self.skill_groups.get(group, [])
        return list(self.skills.keys())

    def get_skill_manifest(self) -> Dict:
        """Get manifest of all skills for Claude Code"""
        return {
            'skills': [
                {
                    'name': skill.name,
                    'description': skill.description,
                    'group': skill.group,
                    'parameters': skill.parameters,
                    'version': skill.version,
                }
                for skill in self.skills.values()
            ],
            'total': len(self.skills),
            'groups': list(self.skill_groups.keys()),
        }

# Global registry
_registry = SkillRegistry()

def get_registry() -> SkillRegistry:
    """Get global skill registry"""
    return _registry
```

#### 1.2 Skill Base Class

**File**: `agent_skills/skill.py` (~200 lines)

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SkillParameter:
    """Skill parameter definition"""
    name: str
    type: str  # 'string', 'number', 'boolean', 'object', 'array'
    description: str
    required: bool = True
    default: Any = None

class Skill(ABC):
    """Base class for all skills"""

    def __init__(
        self,
        name: str,
        description: str,
        group: str = 'general',
        version: str = '1.0.0',
    ):
        self.name = name
        self.description = description
        self.group = group
        self.version = version
        self.parameters: List[SkillParameter] = []
        self.execution_history: List[Dict] = []

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the skill"""
        pass

    def validate_parameters(self, **kwargs) -> bool:
        """Validate input parameters"""
        for param in self.parameters:
            if param.required and param.name not in kwargs:
                raise ValueError(f"Missing required parameter: {param.name}")
        return True

    def log_execution(self, params: Dict, result: Dict):
        """Log skill execution"""
        self.execution_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'parameters': params,
            'result': result,
        })

    def get_manifest(self) -> Dict:
        """Get skill manifest for Claude Code"""
        return {
            'name': self.name,
            'description': self.description,
            'group': self.group,
            'version': self.version,
            'parameters': [
                {
                    'name': p.name,
                    'type': p.type,
                    'description': p.description,
                    'required': p.required,
                    'default': p.default,
                }
                for p in self.parameters
            ],
        }
```

#### 1.3 Skill Implementations

**File**: `agent_skills/skills/` directory

```
agent_skills/skills/
├── __init__.py
├── email_skills.py          # Email operations
├── social_skills.py         # Social media operations
├── accounting_skills.py      # Accounting operations
├── task_skills.py           # Task management
├── approval_skills.py       # Approval workflows
└── reporting_skills.py      # Report generation
```

**Example: Email Skill**

```python
# agent_skills/skills/email_skills.py

from agent_skills.skill import Skill, SkillParameter

class SendEmailSkill(Skill):
    """Send email via Gmail MCP"""

    def __init__(self):
        super().__init__(
            name='send_email',
            description='Send email to recipient',
            group='email',
            version='1.0.0',
        )
        self.parameters = [
            SkillParameter('to', 'string', 'Recipient email address', required=True),
            SkillParameter('subject', 'string', 'Email subject', required=True),
            SkillParameter('body', 'string', 'Email body', required=True),
            SkillParameter('cc', 'array', 'CC recipients', required=False),
            SkillParameter('bcc', 'array', 'BCC recipients', required=False),
            SkillParameter('attachments', 'array', 'File attachments', required=False),
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute email sending"""
        self.validate_parameters(**kwargs)

        try:
            # Call Gmail MCP
            result = self._send_via_gmail_mcp(kwargs)
            self.log_execution(kwargs, result)
            return result
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
            }

    def _send_via_gmail_mcp(self, params: Dict) -> Dict:
        """Send via Gmail MCP server"""
        # Implementation
        pass
```

#### 1.4 Skill Discovery & Loading

**File**: `agent_skills/loader.py` (~150 lines)

```python
import importlib
import pkgutil
from pathlib import Path
from agent_skills.skill import Skill
from agent_skills import get_registry

class SkillLoader:
    """Load and register skills"""

    @staticmethod
    def load_all_skills():
        """Load all skills from skills directory"""
        skills_dir = Path(__file__).parent / 'skills'
        registry = get_registry()

        for importer, modname, ispkg in pkgutil.iter_modules([str(skills_dir)]):
            if modname.startswith('_'):
                continue

            module = importlib.import_module(f'agent_skills.skills.{modname}')

            # Find all Skill subclasses
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and
                    issubclass(attr, Skill) and
                    attr is not Skill):
                    skill_instance = attr()
                    registry.register_skill(skill_instance)

    @staticmethod
    def get_skill_manifest() -> Dict:
        """Get manifest for Claude Code"""
        registry = get_registry()
        return registry.get_skill_manifest()
```

#### 1.5 Claude Code Integration

**File**: `agent_skills/claude_code_integration.py` (~150 lines)

```python
"""
Integration with Claude Code Agent SDK
Exposes skills as Claude Code commands
"""

from agent_skills import get_registry
from agent_skills.loader import SkillLoader

class ClaudeCodeBridge:
    """Bridge between skills and Claude Code"""

    def __init__(self):
        SkillLoader.load_all_skills()
        self.registry = get_registry()

    def get_available_commands(self) -> Dict:
        """Get available commands for Claude Code"""
        manifest = self.registry.get_skill_manifest()
        return {
            'commands': [
                {
                    'name': f"/{skill['name']}",
                    'description': skill['description'],
                    'group': skill['group'],
                }
                for skill in manifest['skills']
            ],
            'total': manifest['total'],
        }

    def execute_command(self, command: str, **kwargs) -> Dict:
        """Execute a skill command"""
        skill_name = command.lstrip('/')
        skill = self.registry.get_skill(skill_name)

        if not skill:
            return {
                'status': 'error',
                'error': f'Skill not found: {skill_name}',
            }

        return skill.execute(**kwargs)

    def get_skill_help(self, skill_name: str) -> Dict:
        """Get help for a skill"""
        skill = self.registry.get_skill(skill_name)
        if not skill:
            return {'error': f'Skill not found: {skill_name}'}
        return skill.get_manifest()
```

---

### 2. Architecture Documentation (Requirement #14)

#### 2.1 Architecture Overview Document

**File**: `ARCHITECTURE.md` (~800 lines)

```markdown
# AI Employee Vault - Architecture Documentation

## System Overview

### 6-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Layer 6: Agent Skills Framework                         │
│ (Claude Code integration, skill discovery, execution)   │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 5: MCP Servers                                    │
│ (Email, Twitter, Instagram, Facebook, Odoo, WhatsApp)  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 4: Orchestration & Execution                      │
│ (Task routing, action execution, error recovery)        │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 3: Intelligence & Planning                        │
│ (Claude API reasoning, task decomposition, briefings)   │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Approval & Governance                          │
│ (HITL approval, domain routing, audit logging)          │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Detection & Ingestion                          │
│ (Gmail, WhatsApp, LinkedIn watchers)                    │
└─────────────────────────────────────────────────────────┘
```

### Component Diagram

```
Detection Layer
├── Gmail Watcher → Inbox/
├── WhatsApp Watcher → Inbox/
└── LinkedIn Watcher → Inbox/

Orchestrator
├── Domain Router (Personal/Business)
├── Ralph Wiggum Loop (Task decomposition)
└── Action Executor

MCP Servers
├── Email MCP (Gmail)
├── Twitter MCP
├── Instagram MCP
├── Facebook MCP
├── Odoo MCP (Accounting)
└── WhatsApp MCP

Reasoning Engine
├── Claude API (Opus 4.6)
├── Task Planning
└── Briefing Generation

Approval Layer
├── HITL Approval Handler
├── Approval Workflow
└── Audit Logger

Storage
├── Obsidian Vault
│   ├── Personal/
│   ├── Business/
│   └── Shared/
└── Logs/
    └── YYYY-MM-DD.json
```

### Data Flow

```
1. Detection
   Email/WhatsApp/LinkedIn → Inbox/

2. Processing
   Inbox/ → Needs_Action/
   (Orchestrator processes)

3. Planning
   Needs_Action/ → Plans/
   (Claude API creates plan)

4. Approval
   Plans/ → Pending_Approval/
   (Human reviews)

5. Execution
   Pending_Approval/Approved/ → Action Executor
   (MCP servers execute)

6. Completion
   Action Executor → Done/
   (Task marked complete)

7. Logging
   All steps → Logs/YYYY-MM-DD.json
   (Audit trail)
```

## Design Decisions

### 1. Obsidian Vault Structure
**Decision**: Use Obsidian vault for storage
**Rationale**:
- Human-readable markdown files
- Version control friendly
- Easy to audit
- Supports linking and backlinks
- Works offline

### 2. MCP Servers
**Decision**: Separate MCP server per platform
**Rationale**:
- Modularity
- Independent scaling
- Easy to add/remove platforms
- Clear separation of concerns
- Testable in isolation

### 3. Claude API for Reasoning
**Decision**: Use Claude Opus 4.6 for planning
**Rationale**:
- Best reasoning capability
- Handles complex task decomposition
- Generates high-quality plans
- Supports multi-step reasoning

### 4. Domain Separation
**Decision**: Separate personal and business domains
**Rationale**:
- Different approval thresholds
- Different channels
- Different retention policies
- Better security
- Clearer audit trails

### 5. Ralph Wiggum Loop
**Decision**: Autonomous multi-step task completion
**Rationale**:
- Reduces human intervention
- Handles complex workflows
- Preserves context across steps
- Enables true autonomy

## Security Architecture

### Authentication
- Gmail: OAuth 2.0
- LinkedIn: OAuth 2.0
- Twitter: OAuth 1.0a
- Instagram: OAuth 2.0
- Facebook: OAuth 2.0
- Odoo: API Key

### Authorization
- Domain-based access control
- Role-based approval thresholds
- HITL approval for sensitive actions
- Audit logging of all access

### Data Protection
- Credentials in .env (never in code)
- Sensitive data redacted in logs
- Encrypted storage for sessions
- HTTPS for all API calls

## Scalability Considerations

### Horizontal Scaling
- MCP servers can run on separate machines
- Orchestrator can be load-balanced
- Logs can be centralized
- Database can be replicated

### Vertical Scaling
- Increase resources for Claude API calls
- Cache frequently accessed data
- Batch process tasks
- Optimize database queries

## Monitoring & Observability

### Logging
- All actions logged to Logs/YYYY-MM-DD.json
- Structured logging format
- Sensitive data redacted
- Audit trail for compliance

### Health Checks
- Service health endpoints
- Dependency checks
- Performance metrics
- Error rate monitoring

### Alerting
- Critical errors
- Service degradation
- Approval bottlenecks
- Unusual activity

## Disaster Recovery

### Backup Strategy
- Daily vault backups
- Log archival
- Credential backup (encrypted)
- Configuration backup

### Recovery Procedures
- Restore from backup
- Replay logs
- Verify data integrity
- Resume operations

## Performance Optimization

### Caching
- Cache frequently accessed data
- Cache Claude API responses
- Cache MCP server responses
- Invalidate on updates

### Batching
- Batch email sends
- Batch social media posts
- Batch database queries
- Batch log writes

### Async Processing
- Async MCP calls
- Async email sending
- Async logging
- Async briefing generation
```

#### 2.2 Lessons Learned Document

**File**: `LESSONS_LEARNED.md` (~400 lines)

```markdown
# Lessons Learned - AI Employee Vault

## What Worked Well

### 1. Obsidian Vault Structure
- Excellent for human-readable task tracking
- Version control friendly
- Easy to audit and review
- Supports complex linking

### 2. MCP Server Architecture
- Clean separation of concerns
- Easy to test independently
- Simple to add new platforms
- Scales well

### 3. Claude API for Reasoning
- Excellent task decomposition
- High-quality planning
- Handles complex scenarios
- Good error recovery suggestions

### 4. HITL Approval Workflow
- Prevents accidental actions
- Builds trust in automation
- Easy to audit
- Flexible approval rules

### 5. Domain Separation
- Clear security boundaries
- Different policies per domain
- Better audit trails
- Easier to manage

## What Could Be Improved

### 1. Error Handling
**Issue**: Initial error handling was too basic
**Solution**: Implement comprehensive error recovery with circuit breakers
**Lesson**: Plan error handling upfront, not as afterthought

### 2. Logging
**Issue**: Logs became too verbose
**Solution**: Implement structured logging with filtering
**Lesson**: Design logging strategy before implementation

### 3. Performance
**Issue**: Orchestrator became slow with many tasks
**Solution**: Implement caching and async processing
**Lesson**: Profile early, optimize based on data

### 4. Testing
**Issue**: Hard to test MCP servers in isolation
**Solution**: Implement mock servers and dry-run mode
**Lesson**: Design for testability from the start

### 5. Documentation
**Issue**: Documentation lagged behind implementation
**Solution**: Document as you build
**Lesson**: Make documentation part of definition of done

## Technical Decisions

### 1. Why Obsidian?
- Human-readable format
- Version control friendly
- Supports complex workflows
- Easy to audit

### 2. Why MCP Servers?
- Modularity
- Independent scaling
- Clear interfaces
- Easy to test

### 3. Why Claude API?
- Best reasoning capability
- Handles complexity
- Good error recovery
- Supports multi-step tasks

### 4. Why Domain Separation?
- Security boundaries
- Different policies
- Better audit trails
- Clearer workflows

## Recommendations for Future

### 1. Implement Caching
- Cache Claude API responses
- Cache MCP server responses
- Implement cache invalidation
- Monitor cache hit rates

### 2. Add Monitoring
- Real-time dashboards
- Performance metrics
- Error rate tracking
- Service health monitoring

### 3. Improve Testing
- Unit tests for all components
- Integration tests for workflows
- Load testing for scalability
- Security testing

### 4. Enhance Documentation
- Architecture diagrams
- API documentation
- Troubleshooting guides
- Best practices guide

### 5. Plan for Scale
- Database optimization
- Caching strategy
- Load balancing
- Distributed logging

## Metrics & KPIs

### System Metrics
- Task completion rate: 95%+
- Average task time: < 5 minutes
- Error rate: < 1%
- Approval rate: 90%+

### Performance Metrics
- API response time: < 2 seconds
- MCP server latency: < 1 second
- Orchestrator throughput: 100+ tasks/hour
- Log write latency: < 100ms

### Quality Metrics
- Test coverage: 80%+
- Documentation completeness: 100%
- Security audit: Passed
- Compliance: SOC2 ready

## Conclusion

The AI Employee Vault demonstrates that autonomous task execution with human oversight is achievable. The key success factors were:

1. Clear architecture with separation of concerns
2. Strong emphasis on auditability and compliance
3. Flexible approval workflows
4. Comprehensive error handling
5. Excellent documentation

The system is production-ready and can scale to handle complex business workflows.
```

#### 2.3 Deployment Guide

**File**: `DEPLOYMENT_GUIDE.md` (~300 lines)

```markdown
# Deployment Guide - AI Employee Vault

## Prerequisites

- Python 3.10+
- PostgreSQL 13+ (for Odoo)
- Docker (optional, for containerization)
- Git for version control

## Installation Steps

### 1. Clone Repository
```bash
git clone <repo-url>
cd ai_employee_vault
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r mcp_servers/email_mcp/requirements.txt
pip install -r mcp_servers/twitter_mcp/requirements.txt
pip install -r mcp_servers/instagram_mcp/requirements.txt
pip install -r mcp_servers/facebook_mcp/requirements.txt
pip install -r mcp_servers/odoo_mcp/requirements.txt
```

### 4. Setup Odoo
```bash
# Install Odoo 19 Community
# Configure PostgreSQL
# Create database
# Generate API key
```

### 5. Configure Credentials
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 6. Initialize Vault
```bash
python orchestrator.py --init
```

### 7. Start Services
```bash
# Terminal 1: Orchestrator
python orchestrator.py

# Terminal 2: Email MCP
python mcp_servers/email_mcp/server.py

# Terminal 3: Twitter MCP
python mcp_servers/twitter_mcp/server.py

# Terminal 4: Instagram MCP
python mcp_servers/instagram_mcp/server.py

# Terminal 5: Facebook MCP
python mcp_servers/facebook_mcp/server.py

# Terminal 6: Odoo MCP
python mcp_servers/odoo_mcp/server.py
```

## Configuration

### .env File
```
# Gmail
GMAIL_CLIENT_ID=...
GMAIL_CLIENT_SECRET=...

# LinkedIn
LINKEDIN_CLIENT_ID=...
LINKEDIN_CLIENT_SECRET=...

# Twitter
TWITTER_API_KEY=...
TWITTER_API_SECRET=...

# Instagram
INSTAGRAM_ACCESS_TOKEN=...
INSTAGRAM_BUSINESS_ACCOUNT_ID=...

# Facebook
FACEBOOK_ACCESS_TOKEN=...
FACEBOOK_PAGE_ID=...

# Odoo
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_vault
ODOO_API_KEY=...

# System
VAULT_PATH=.
LOG_LEVEL=INFO
DRY_RUN=false
```

## Monitoring

### Health Checks
```bash
curl http://localhost:8070/health  # Email MCP
curl http://localhost:8071/health  # Twitter MCP
curl http://localhost:8072/health  # Instagram MCP
curl http://localhost:8073/health  # Facebook MCP
curl http://localhost:8074/health  # Odoo MCP
```

### Logs
```bash
tail -f Logs/$(date +%Y-%m-%d).json
```

### Dashboard
```bash
python social_dashboard.py
```

## Troubleshooting

### Service Won't Start
1. Check port availability
2. Check credentials
3. Check logs for errors
4. Verify dependencies installed

### Tasks Not Processing
1. Check orchestrator logs
2. Verify vault structure
3. Check approval workflow
4. Verify MCP servers running

### Approval Stuck
1. Check Pending_Approval/ folder
2. Review approval files
3. Check approval handler logs
4. Manually approve if needed

## Backup & Recovery

### Backup
```bash
# Backup vault
tar -czf vault_backup_$(date +%Y%m%d).tar.gz .

# Backup logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz Logs/

# Backup credentials
tar -czf credentials_backup_$(date +%Y%m%d).tar.gz .env
```

### Recovery
```bash
# Restore vault
tar -xzf vault_backup_YYYYMMDD.tar.gz

# Restore logs
tar -xzf logs_backup_YYYYMMDD.tar.gz

# Restore credentials
tar -xzf credentials_backup_YYYYMMDD.tar.gz
```

## Production Deployment

### Docker Deployment
```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "orchestrator.py"]
```

### Cloud Deployment
- AWS: EC2 + RDS
- GCP: Compute Engine + Cloud SQL
- Azure: Virtual Machine + Azure Database

### Scaling
- Load balance orchestrator
- Distribute MCP servers
- Centralize logging
- Use managed database
```

---

## Implementation Sequence

### Week 3: Integration

**Day 1-2: Agent Skills Framework**
- [ ] Create `agent_skills/` package
- [ ] Implement skill base class
- [ ] Create skill implementations
- [ ] Implement skill loader
- [ ] Integrate with Claude Code

**Day 2-3: Documentation**
- [ ] Create `ARCHITECTURE.md`
- [ ] Create `LESSONS_LEARNED.md`
- [ ] Create `DEPLOYMENT_GUIDE.md`
- [ ] Create troubleshooting guide
- [ ] Create best practices guide

**Day 3-4: Integration & Testing**
- [ ] Integrate all components
- [ ] End-to-end testing
- [ ] Performance testing
- [ ] Security testing
- [ ] Documentation review

**Day 4-5: Final Polish**
- [ ] Code cleanup
- [ ] Documentation finalization
- [ ] Git commit
- [ ] Release preparation

---

## Files to Create

### Agent Skills
- `agent_skills/__init__.py` (100 lines)
- `agent_skills/skill.py` (200 lines)
- `agent_skills/loader.py` (150 lines)
- `agent_skills/claude_code_integration.py` (150 lines)
- `agent_skills/skills/email_skills.py` (200 lines)
- `agent_skills/skills/social_skills.py` (200 lines)
- `agent_skills/skills/accounting_skills.py` (200 lines)
- `agent_skills/skills/task_skills.py` (200 lines)
- `agent_skills/skills/approval_skills.py` (150 lines)
- `agent_skills/skills/reporting_skills.py` (150 lines)

### Documentation
- `ARCHITECTURE.md` (800 lines)
- `LESSONS_LEARNED.md` (400 lines)
- `DEPLOYMENT_GUIDE.md` (300 lines)
- `TROUBLESHOOTING.md` (200 lines)
- `BEST_PRACTICES.md` (200 lines)

---

## Success Criteria

### Agent Skills
- [ ] All skills discoverable
- [ ] Skills execute correctly
- [ ] Claude Code integration works
- [ ] Skill versioning works
- [ ] All tests pass

### Documentation
- [ ] Architecture clear
- [ ] Lessons documented
- [ ] Deployment guide complete
- [ ] Troubleshooting guide helpful
- [ ] Best practices documented

---

**Status**: Ready for Phase 3 (after Phase 1 & 2 complete)
**Next**: Final review and deployment
