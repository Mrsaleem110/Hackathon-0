# 📋 DEPLOYMENT ACTION PLAN

**Date**: 2026-03-26
**Status**: READY TO EXECUTE
**Estimated Time**: 15-30 minutes (depending on option chosen)

---

## DECISION MATRIX

Choose your deployment option based on your needs:

| Factor | Docker | Cloud | Kubernetes | Local |
|--------|--------|-------|------------|-------|
| Complexity | Low | Medium | High | Very Low |
| Scalability | Good | Excellent | Excellent | Limited |
| Cost | Low | Medium | Medium | Free |
| Time | 10-15m | 20-30m | 30-45m | 5m |
| Best For | Production | Enterprise | Large Scale | Dev/Test |

---

## OPTION 1: DOCKER DEPLOYMENT (Recommended)

### Prerequisites
- Docker installed
- Docker Compose installed
- 2GB RAM available
- 5GB disk space

### Steps

**Step 1: Verify Docker Installation**
```bash
docker --version
docker-compose --version
```

**Step 2: Build Docker Image**
```bash
cd "C:\Users\Agentic Sphere\Documents\GitHub\Hackathon-0\ai_employee_vault"
docker-compose build
```

**Step 3: Start Containers**
```bash
docker-compose up -d
```

**Step 4: Verify Services**
```bash
docker-compose ps
curl http://localhost:8070/health
curl http://localhost:8072/health
curl http://localhost:8073/health
curl http://localhost:8075/health
```

**Step 5: Monitor Logs**
```bash
docker-compose logs -f
```

### Rollback
```bash
docker-compose down
docker-compose up -d --build
```

---

## OPTION 2: CLOUD DEPLOYMENT (AWS Example)

### Prerequisites
- AWS account
- AWS CLI installed
- EC2 key pair created
- Security group configured

### Steps

**Step 1: Create EC2 Instance**
```bash
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.medium \
  --key-name your-key-pair \
  --security-groups default
```

**Step 2: SSH into Instance**
```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

**Step 3: Install Dependencies**
```bash
sudo yum update -y
sudo yum install python3 python3-pip git -y
```

**Step 4: Clone Repository**
```bash
git clone https://github.com/your-repo/ai-employee-vault.git
cd ai-employee-vault
```

**Step 5: Install Python Dependencies**
```bash
pip3 install -r mcp_servers/email_mcp/requirements.txt
pip3 install -r mcp_servers/vault_mcp/requirements.txt
pip3 install -r mcp_servers/whatsapp_mcp/requirements.txt
pip3 install -r mcp_servers/linkedin_mcp/requirements.txt
```

**Step 6: Set Environment Variables**
```bash
export GMAIL_CLIENT_ID=your_id
export GMAIL_CLIENT_SECRET=your_secret
# ... set all other variables
```

**Step 7: Start Services**
```bash
# Terminal 1
cd mcp_servers/vault_mcp && python server.py

# Terminal 2
cd mcp_servers/email_mcp && python server.py

# Terminal 3
cd mcp_servers/whatsapp_mcp && python server.py

# Terminal 4
cd mcp_servers/linkedin_mcp && python server.py
```

---

## OPTION 3: KUBERNETES DEPLOYMENT

### Prerequisites
- Kubernetes cluster (local or cloud)
- kubectl installed
- Docker images built and pushed to registry

### Steps

**Step 1: Create Namespace**
```bash
kubectl create namespace ai-vault
```

**Step 2: Create Secrets**
```bash
kubectl create secret generic gmail-credentials \
  --from-literal=client-id=your_id \
  --from-literal=client-secret=your_secret \
  -n ai-vault
```

**Step 3: Apply Deployment**
```bash
kubectl apply -f deployment.yaml -n ai-vault
```

**Step 4: Verify Deployment**
```bash
kubectl get pods -n ai-vault
kubectl get services -n ai-vault
```

**Step 5: Check Logs**
```bash
kubectl logs -f deployment/ai-employee-vault -n ai-vault
```

---

## OPTION 4: LOCAL PRODUCTION (Development/Testing)

### Prerequisites
- Python 3.8+
- 2GB RAM
- 5GB disk space

### Steps

**Step 1: Install Dependencies**
```bash
cd "C:\Users\Agentic Sphere\Documents\GitHub\Hackathon-0\ai_employee_vault"
pip install -r mcp_servers/email_mcp/requirements.txt
pip install -r mcp_servers/vault_mcp/requirements.txt
pip install -r mcp_servers/whatsapp_mcp/requirements.txt
pip install -r mcp_servers/linkedin_mcp/requirements.txt
```

**Step 2: Start Servers (4 terminals)**

Terminal 1:
```bash
cd mcp_servers/vault_mcp && python server.py
```

Terminal 2:
```bash
cd mcp_servers/email_mcp && python server.py
```

Terminal 3:
```bash
cd mcp_servers/whatsapp_mcp && python server.py
```

Terminal 4:
```bash
cd mcp_servers/linkedin_mcp && python server.py
```

**Step 3: Verify All Running**
```bash
curl http://localhost:8070/health
curl http://localhost:8072/health
curl http://localhost:8073/health
curl http://localhost:8075/health
```

---

## POST-DEPLOYMENT VERIFICATION

### Health Checks
```bash
# All should return {"status":"healthy",...}
curl http://localhost:8070/health
curl http://localhost:8072/health
curl http://localhost:8073/health
curl http://localhost:8075/health
```

### Tool Listing
```bash
curl http://localhost:8070/tools
curl http://localhost:8072/tools
curl http://localhost:8073/tools
curl http://localhost:8075/tools
```

### Complete Workflow Test
```bash
python -c "
from agent_skills.whatsapp_skill import WhatsAppSkill
from agent_skills.linkedin_skill import LinkedInSkill
from agent_skills.audit_skill import AuditSkill

wa = WhatsAppSkill()
print('WhatsApp Skill:', wa.validate_phone_number('+1234567890'))

li = LinkedInSkill()
print('LinkedIn Skill:', len(li.get_linkedin_feed(limit=5)), 'posts')

audit = AuditSkill()
result = audit.log_action('test', {'test': 'data'}, 'success')
print('Audit Skill:', result['success'])
"
```

---

## MONITORING SETUP

### Log Monitoring
```bash
# Docker
docker-compose logs -f email-mcp

# Kubernetes
kubectl logs -f deployment/ai-employee-vault

# Local
tail -f Logs/2026-03-26.json
```

### Metrics to Monitor
- Server uptime
- Request latency
- Error rates
- API usage
- Storage usage

### Alert Thresholds
- Error rate > 5%
- Latency > 2 seconds
- Disk usage > 80%
- Memory usage > 80%

---

## TROUBLESHOOTING

### Port Already in Use
```bash
# Find process
lsof -i :8070

# Kill process
kill -9 <PID>
```

### Out of Memory
```bash
# Docker: Increase memory in docker-compose.yml
mem_limit: 2g

# Kubernetes: Update resource limits
resources:
  limits:
    memory: "2Gi"
```

### Slow Response Times
```bash
# Check logs for bottlenecks
grep "duration" Logs/*.json

# Check system resources
top
df -h
```

### Connection Refused
```bash
# Verify servers are running
docker-compose ps
kubectl get pods

# Check firewall
sudo ufw status
```

---

## ROLLBACK PROCEDURE

### Docker Rollback
```bash
docker-compose down
docker-compose up -d --build
```

### Kubernetes Rollback
```bash
kubectl rollout undo deployment/ai-employee-vault
kubectl rollout history deployment/ai-employee-vault
```

### Local Rollback
```bash
# Stop all servers
# Check git status
git status

# Revert if needed
git checkout .
```

---

## MAINTENANCE SCHEDULE

### Daily
- [ ] Check server health
- [ ] Review error logs
- [ ] Monitor disk space

### Weekly
- [ ] Review audit logs
- [ ] Check performance metrics
- [ ] Rotate logs

### Monthly
- [ ] Update dependencies
- [ ] Review security logs
- [ ] Test disaster recovery

### Quarterly
- [ ] Rotate credentials
- [ ] Update documentation
- [ ] Performance optimization

---

## DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] All tests passing
- [ ] Documentation reviewed
- [ ] Environment variables prepared
- [ ] Backup strategy planned
- [ ] Monitoring configured

### Deployment
- [ ] Choose deployment option
- [ ] Follow step-by-step instructions
- [ ] Verify all services running
- [ ] Check health endpoints
- [ ] Review logs for errors

### Post-Deployment
- [ ] Monitor system metrics
- [ ] Test complete workflow
- [ ] Verify audit logging
- [ ] Set up monitoring alerts
- [ ] Document any issues

---

## SUPPORT CONTACTS

For issues:
1. Check LOCAL_TESTING_COMPLETE.md
2. Review DEPLOYMENT_GUIDE.md
3. Check health endpoints
4. Review logs in Logs/ directory
5. Check troubleshooting section above

---

## NEXT STEPS

1. **Choose deployment option** (Docker recommended)
2. **Follow step-by-step instructions** for your option
3. **Verify all services running** with health checks
4. **Monitor logs** for any issues
5. **Test complete workflow** after deployment

---

**Status**: READY TO DEPLOY
**Recommendation**: Docker (Option 1)
**Estimated Time**: 15 minutes
**Risk Level**: Low (all tested)

---

*Created: 2026-03-26*
*By: Claude Code*
*Status: APPROVED FOR EXECUTION*
