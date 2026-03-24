# Gold Tier Implementation Plan - Phase 1
**Date**: 2026-03-24
**Phase**: Foundation (Odoo, Cross-Domain, Error Recovery)
**Estimated Duration**: 1 week

---

## Phase 1: Foundation Requirements

### 1. Odoo Community Integration (Requirement #7)

#### 1.1 Odoo MCP Server Architecture

**File**: `mcp_servers/odoo_mcp/server.py` (~400 lines)

```
Odoo MCP Server (Port 8074)
├── JSON-RPC Client
├── Authentication (API Key)
├── Accounting Module
│   ├── Invoice Management
│   ├── Expense Tracking
│   ├── Payment Recording
│   └── Financial Reports
├── Business Module
│   ├── Customer Management
│   ├── Vendor Management
│   ├── Order Tracking
│   └── Sales Pipeline
└── Tools
    ├── create_invoice()
    ├── record_expense()
    ├── get_financial_summary()
    ├── get_sales_pipeline()
    └── generate_accounting_report()
```

**Key Features**:
- JSON-RPC 2.0 protocol for Odoo 19+
- API key authentication
- Dry-run mode for testing
- HITL approval for financial transactions
- Comprehensive error handling
- Rate limiting

**Dependencies**:
```
requests>=2.28.0
fastapi>=0.95.0
uvicorn>=0.21.0
pydantic>=1.10.0
python-dotenv>=0.21.0
```

#### 1.2 Odoo Setup Requirements

**Local Installation**:
1. Odoo 19 Community Edition (self-hosted)
2. PostgreSQL database
3. Python 3.10+
4. API key generation

**Configuration**:
```env
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_vault
ODOO_API_KEY=your_api_key
ODOO_MCP_PORT=8074
```

#### 1.3 Implementation Steps

1. **Setup Odoo Locally**
   - Install Odoo 19 Community
   - Configure PostgreSQL
   - Create database
   - Generate API key

2. **Create Odoo MCP Server**
   - JSON-RPC client
   - Authentication handler
   - Tool implementations
   - Error handling

3. **Integration Points**
   - Orchestrator integration
   - CEO briefing integration
   - Logging integration

---

### 2. Cross-Domain Integration (Requirement #8)

#### 2.1 Domain Detection & Routing

**File**: `domain_router.py` (~250 lines)

```python
class DomainRouter:
    """Route tasks to personal or business domain"""

    def __init__(self):
        self.personal_domains = ['gmail.com', 'personal.com']
        self.business_domains = ['company.com', 'business.com']

    def detect_domain(self, email: str) -> str:
        """Detect if email is personal or business"""
        # Returns: 'personal' or 'business'

    def route_task(self, task: Task) -> str:
        """Route task to appropriate domain"""
        # Returns: domain identifier

    def get_domain_config(self, domain: str) -> Dict:
        """Get configuration for domain"""
        # Returns: domain-specific config
```

**Configuration Structure**:
```yaml
domains:
  personal:
    email_domains: ['gmail.com', 'yahoo.com']
    approval_threshold: 30
    auto_approve: false
    channels: ['gmail', 'whatsapp']

  business:
    email_domains: ['company.com']
    approval_threshold: 70
    auto_approve: true
    channels: ['gmail', 'linkedin', 'odoo']
```

#### 2.2 Orchestrator Updates

**File**: `orchestrator.py` (updates ~150 lines)

```python
class VaultOrchestrator:
    def __init__(self, vault_path: str):
        # ... existing code ...
        self.domain_router = DomainRouter()
        self.personal_vault = vault_path / 'Personal'
        self.business_vault = vault_path / 'Business'

    def process_needs_action(self):
        """Process tasks by domain"""
        for domain in ['personal', 'business']:
            self._process_domain_tasks(domain)

    def _process_domain_tasks(self, domain: str):
        """Process tasks for specific domain"""
        vault_path = self.personal_vault if domain == 'personal' else self.business_vault
        # Process domain-specific tasks
```

#### 2.3 Vault Structure

```
ai_employee_vault/
├── Personal/
│   ├── Inbox/
│   ├── Needs_Action/
│   ├── Pending_Approval/
│   ├── Done/
│   └── Logs/
├── Business/
│   ├── Inbox/
│   ├── Needs_Action/
│   ├── Pending_Approval/
│   ├── Done/
│   └── Logs/
└── Shared/
    ├── Dashboard.md
    └── Briefings/
```

---

### 3. Error Recovery & Graceful Degradation (Requirement #10)

#### 3.1 Error Handler Module

**File**: `error_handler.py` (~300 lines)

```python
class ErrorHandler:
    """Centralized error handling with recovery strategies"""

    def __init__(self):
        self.max_retries = 3
        self.backoff_factor = 2
        self.circuit_breakers = {}

    def handle_error(self, error: Exception, context: Dict) -> Dict:
        """Handle error with recovery strategy"""
        # Determine error type
        # Apply recovery strategy
        # Log error
        # Return recovery action

    def retry_with_backoff(self, func, *args, **kwargs):
        """Retry function with exponential backoff"""
        # Implement exponential backoff
        # Max retries: 3
        # Delays: 2s, 4s, 8s

    def circuit_breaker(self, service_name: str):
        """Circuit breaker pattern for service calls"""
        # Track failures
        # Open circuit after threshold
        # Half-open state for recovery
        # Close circuit on success
```

**Recovery Strategies**:
```
Error Type              | Recovery Strategy
-----------------------|------------------
Network Timeout        | Retry with backoff
API Rate Limit         | Queue and retry later
Authentication Failed  | Re-authenticate
Service Unavailable    | Use fallback service
Invalid Data           | Log and skip
Database Error         | Retry transaction
```

#### 3.2 Health Check System

**File**: `health_checker.py` (~200 lines)

```python
class HealthChecker:
    """Monitor health of all services"""

    def __init__(self):
        self.services = {
            'gmail': 'http://localhost:8070/health',
            'twitter': 'http://localhost:8071/health',
            'instagram': 'http://localhost:8072/health',
            'facebook': 'http://localhost:8073/health',
            'odoo': 'http://localhost:8074/health',
        }

    def check_all_services(self) -> Dict[str, bool]:
        """Check health of all services"""
        # Ping each service
        # Return status dict

    def get_service_status(self, service: str) -> Dict:
        """Get detailed status for service"""
        # Response time
        # Error rate
        # Last check time
        # Status: healthy/degraded/down
```

#### 3.3 Graceful Degradation

**File**: `degradation_manager.py` (~250 lines)

```python
class DegradationManager:
    """Manage graceful service degradation"""

    def __init__(self):
        self.degraded_services = set()
        self.fallback_services = {
            'twitter': 'linkedin',
            'instagram': 'facebook',
            'odoo': 'local_cache',
        }

    def mark_service_degraded(self, service: str):
        """Mark service as degraded"""
        self.degraded_services.add(service)

    def get_available_service(self, primary: str) -> str:
        """Get available service (primary or fallback)"""
        if primary not in self.degraded_services:
            return primary
        return self.fallback_services.get(primary, primary)

    def execute_with_fallback(self, action: Dict) -> Dict:
        """Execute action with fallback if primary fails"""
        # Try primary service
        # If fails, try fallback
        # If both fail, queue for retry
```

---

## Implementation Sequence

### Week 1: Foundation

**Day 1-2: Odoo Setup**
- [ ] Install Odoo 19 Community locally
- [ ] Configure PostgreSQL
- [ ] Generate API key
- [ ] Test JSON-RPC connection

**Day 2-3: Odoo MCP Server**
- [ ] Create `mcp_servers/odoo_mcp/` directory
- [ ] Implement JSON-RPC client
- [ ] Implement accounting tools
- [ ] Add HITL approval workflow
- [ ] Write tests

**Day 3-4: Cross-Domain Support**
- [ ] Create `domain_router.py`
- [ ] Update `orchestrator.py`
- [ ] Create vault structure
- [ ] Update configuration

**Day 4-5: Error Recovery**
- [ ] Create `error_handler.py`
- [ ] Create `health_checker.py`
- [ ] Create `degradation_manager.py`
- [ ] Integrate with orchestrator

**Day 5: Testing & Documentation**
- [ ] End-to-end testing
- [ ] Documentation
- [ ] Git commit

---

## Files to Create

### Odoo Integration
- `mcp_servers/odoo_mcp/__init__.py`
- `mcp_servers/odoo_mcp/server.py` (400 lines)
- `mcp_servers/odoo_mcp/odoo_client.py` (300 lines)
- `mcp_servers/odoo_mcp/test_odoo_mcp.py` (250 lines)
- `mcp_servers/odoo_mcp/requirements.txt`

### Cross-Domain
- `domain_router.py` (250 lines)
- `domain_config.yaml` (50 lines)
- Updated `orchestrator.py` (150 lines)

### Error Recovery
- `error_handler.py` (300 lines)
- `health_checker.py` (200 lines)
- `degradation_manager.py` (250 lines)

### Documentation
- `ODOO_SETUP.md` (300 lines)
- `CROSS_DOMAIN_GUIDE.md` (200 lines)
- `ERROR_RECOVERY_GUIDE.md` (200 lines)

---

## Success Criteria

### Odoo Integration
- [ ] Odoo MCP server starts on port 8074
- [ ] Can create invoices via JSON-RPC
- [ ] Can record expenses
- [ ] Can generate financial reports
- [ ] HITL approval works
- [ ] All tests pass

### Cross-Domain
- [ ] Personal and business tasks separated
- [ ] Domain detection works correctly
- [ ] Separate approval workflows
- [ ] Separate logging
- [ ] Dashboard shows both domains

### Error Recovery
- [ ] Retry logic works with backoff
- [ ] Circuit breaker prevents cascading failures
- [ ] Health checks run every 5 minutes
- [ ] Graceful degradation activates
- [ ] Fallback services work

---

## Questions Before Implementation

1. **Odoo Hosting**: Local installation or cloud?
2. **Domain Config**: Should domains be in config file or database?
3. **Approval Thresholds**: Different thresholds per domain?
4. **Fallback Services**: Which services should have fallbacks?
5. **Health Check Interval**: How often to check service health?

---

**Status**: Ready for Phase 1 implementation
**Next**: Confirm requirements and start Odoo setup
