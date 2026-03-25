# 🚀 DEPLOYMENT GUIDE - AFTER LOCAL TESTING

**Date**: 2026-03-26
**Purpose**: Deploy Gold Tier system to production
**Prerequisites**: All local testing completed and verified

---

## PRE-DEPLOYMENT CHECKLIST

Before deploying, verify:

- [ ] All 4 MCP servers tested locally and working
- [ ] All 7 agent skills tested and functional
- [ ] Domain router tested with personal/business separation
- [ ] CEO briefing scheduler tested
- [ ] Error recovery tested with fallback methods
- [ ] Enhanced orchestrator tested with sample tasks
- [ ] All logs reviewed for errors
- [ ] Audit trail verified
- [ ] No sensitive data in code
- [ ] All environment variables configured

---

## DEPLOYMENT OPTIONS

### Option 1: DOCKER DEPLOYMENT (Recommended)

#### Step 1: Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY mcp_servers/email_mcp/requirements.txt ./email_requirements.txt
COPY mcp_servers/vault_mcp/requirements.txt ./vault_requirements.txt
COPY mcp_servers/whatsapp_mcp/requirements.txt ./whatsapp_requirements.txt
COPY mcp_servers/linkedin_mcp/requirements.txt ./linkedin_requirements.txt

# Install dependencies
RUN pip install -r email_requirements.txt && \
    pip install -r vault_requirements.txt && \
    pip install -r whatsapp_requirements.txt && \
    pip install -r linkedin_requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 8070 8072 8073 8075

# Start all servers
CMD ["python", "start_all_servers.py"]
```

#### Step 2: Create docker-compose.yml

```yaml
version: '3.8'

services:
  email-mcp:
    build: .
    ports:
      - "8070:8070"
    environment:
      - EMAIL_MCP_PORT=8070
      - GMAIL_CLIENT_ID=${GMAIL_CLIENT_ID}
      - GMAIL_CLIENT_SECRET=${GMAIL_CLIENT_SECRET}
    volumes:
      - ./Logs:/app/Logs
      - ./token.json:/app/token.json

  vault-mcp:
    build: .
    ports:
      - "8072:8072"
    environment:
      - VAULT_MCP_PORT=8072
      - VAULT_PATH=/app
    volumes:
      - ./Logs:/app/Logs

  whatsapp-mcp:
    build: .
    ports:
      - "8073:8073"
    environment:
      - WHATSAPP_MCP_PORT=8073
      - WHATSAPP_PHONE_NUMBER_ID=${WHATSAPP_PHONE_NUMBER_ID}
      - WHATSAPP_ACCESS_TOKEN=${WHATSAPP_ACCESS_TOKEN}
    volumes:
      - ./Logs:/app/Logs

  linkedin-mcp:
    build: .
    ports:
      - "8075:8075"
    environment:
      - LINKEDIN_MCP_PORT=8075
      - LINKEDIN_ACCESS_TOKEN=${LINKEDIN_ACCESS_TOKEN}
    volumes:
      - ./Logs:/app/Logs
```

#### Step 3: Build and Run

```bash
# Build Docker image
docker-compose build

# Run containers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

---

### Option 2: CLOUD DEPLOYMENT (AWS/GCP/Azure)

#### AWS Deployment

```bash
# 1. Create EC2 instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.medium \
  --key-name your-key-pair

# 2. SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# 3. Install dependencies
sudo yum update -y
sudo yum install python3 python3-pip -y

# 4. Clone repository
git clone https://github.com/your-repo/ai-employee-vault.git
cd ai-employee-vault

# 5. Install Python dependencies
pip3 install -r requirements.txt

# 6. Set environment variables
export GMAIL_CLIENT_ID=your_id
export GMAIL_CLIENT_SECRET=your_secret
# ... set all other variables

# 7. Start services
python3 orchestrator.py
```

#### GCP Deployment

```bash
# 1. Create Cloud Run service
gcloud run deploy ai-employee-vault \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# 2. Set environment variables
gcloud run services update ai-employee-vault \
  --set-env-vars GMAIL_CLIENT_ID=your_id,GMAIL_CLIENT_SECRET=your_secret
```

---

### Option 3: KUBERNETES DEPLOYMENT

#### Step 1: Create Kubernetes manifests

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-employee-vault
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-employee-vault
  template:
    metadata:
      labels:
        app: ai-employee-vault
    spec:
      containers:
      - name: email-mcp
        image: ai-employee-vault:latest
        ports:
        - containerPort: 8070
        env:
        - name: EMAIL_MCP_PORT
          value: "8070"
        - name: GMAIL_CLIENT_ID
          valueFrom:
            secretKeyRef:
              name: gmail-credentials
              key: client-id

      - name: vault-mcp
        image: ai-employee-vault:latest
        ports:
        - containerPort: 8072
        env:
        - name: VAULT_MCP_PORT
          value: "8072"

      - name: whatsapp-mcp
        image: ai-employee-vault:latest
        ports:
        - containerPort: 8073
        env:
        - name: WHATSAPP_MCP_PORT
          value: "8073"

      - name: linkedin-mcp
        image: ai-employee-vault:latest
        ports:
        - containerPort: 8075
        env:
        - name: LINKEDIN_MCP_PORT
          value: "8075"
```

#### Step 2: Deploy to Kubernetes

```bash
# Create secrets
kubectl create secret generic gmail-credentials \
  --from-literal=client-id=your_id \
  --from-literal=client-secret=your_secret

# Deploy
kubectl apply -f deployment.yaml

# Check status
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/ai-employee-vault
```

---

## ENVIRONMENT VARIABLES SETUP

Create `.env` file with all credentials:

```bash
# Gmail Configuration
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret
GMAIL_REDIRECT_URI=http://localhost:8080/

# LinkedIn Configuration
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_ACCESS_TOKEN=your_linkedin_token

# Instagram Configuration
INSTAGRAM_APP_ID=your_instagram_app_id
INSTAGRAM_APP_SECRET=your_instagram_app_secret
INSTAGRAM_ACCESS_TOKEN=your_instagram_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_business_account_id

# Facebook Configuration
FACEBOOK_ACCESS_TOKEN=your_facebook_token
FACEBOOK_PAGE_ID=your_facebook_page_id

# WhatsApp Configuration
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_ACCESS_TOKEN=your_whatsapp_token

# Odoo Configuration
ODOO_URL=http://your-odoo-instance:8069
ODOO_DB=your_database
ODOO_API_KEY=your_api_key

# CEO Email
CEO_EMAIL=ceo@company.com

# System Configuration
VAULT_PATH=/app
LOG_LEVEL=INFO
DEMO_MODE=false
TIMEZONE=UTC
```

---

## MONITORING & LOGGING

### Setup Monitoring

```bash
# Install monitoring tools
pip install prometheus-client
pip install python-json-logger

# Configure logging
export LOG_LEVEL=INFO
export LOG_FORMAT=json
```

### View Logs

```bash
# Docker logs
docker-compose logs -f email-mcp

# Kubernetes logs
kubectl logs -f deployment/ai-employee-vault

# Local logs
tail -f Logs/2026-03-26.json
```

### Health Checks

```bash
# Check Email MCP
curl http://localhost:8070/health

# Check Vault MCP
curl http://localhost:8072/health

# Check WhatsApp MCP
curl http://localhost:8073/health

# Check LinkedIn MCP
curl http://localhost:8075/health
```

---

## SECURITY CHECKLIST

- [ ] All credentials in environment variables (not in code)
- [ ] HTTPS enabled for all endpoints
- [ ] API authentication configured
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Secrets encrypted at rest
- [ ] Audit logging enabled
- [ ] Error messages don't leak sensitive data
- [ ] Database credentials secured
- [ ] API keys rotated regularly

---

## POST-DEPLOYMENT VERIFICATION

```bash
# 1. Verify all services running
curl http://localhost:8070/health
curl http://localhost:8072/health
curl http://localhost:8073/health
curl http://localhost:8075/health

# 2. Test MCP endpoints
curl -X GET http://localhost:8070/tools
curl -X GET http://localhost:8072/tools
curl -X GET http://localhost:8073/tools
curl -X GET http://localhost:8075/tools

# 3. Check logs for errors
grep ERROR Logs/*.json

# 4. Verify audit trail
grep "action_type" Logs/*.json | head -20

# 5. Test complete workflow
python test_complete_workflow.py
```

---

## ROLLBACK PROCEDURE

If issues occur:

```bash
# Docker rollback
docker-compose down
docker-compose up -d --build

# Kubernetes rollback
kubectl rollout undo deployment/ai-employee-vault

# Check previous version
kubectl rollout history deployment/ai-employee-vault
```

---

## SCALING

### Horizontal Scaling

```bash
# Docker Compose
docker-compose up -d --scale email-mcp=3

# Kubernetes
kubectl scale deployment ai-employee-vault --replicas=5
```

### Load Balancing

```yaml
# nginx.conf
upstream mcp_servers {
    server email-mcp:8070;
    server vault-mcp:8072;
    server whatsapp-mcp:8073;
    server linkedin-mcp:8075;
}

server {
    listen 80;
    location / {
        proxy_pass http://mcp_servers;
    }
}
```

---

## MAINTENANCE

### Regular Tasks

- [ ] Monitor disk space
- [ ] Rotate logs weekly
- [ ] Update dependencies monthly
- [ ] Review audit logs weekly
- [ ] Test disaster recovery monthly
- [ ] Update credentials quarterly

### Backup Strategy

```bash
# Backup logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz Logs/

# Backup configuration
tar -czf config_backup_$(date +%Y%m%d).tar.gz .env

# Backup database
pg_dump your_database > backup_$(date +%Y%m%d).sql
```

---

## SUPPORT & TROUBLESHOOTING

### Common Issues

**Issue**: Port already in use
```bash
lsof -i :8070
kill -9 <PID>
```

**Issue**: Out of memory
```bash
# Increase memory limit
docker-compose.yml: mem_limit: 2g
```

**Issue**: Slow response times
```bash
# Check logs for bottlenecks
grep "duration" Logs/*.json
```

---

## NEXT STEPS AFTER DEPLOYMENT

1. **Monitor system** - Watch logs and metrics
2. **Gather feedback** - Get user feedback
3. **Optimize** - Improve performance based on usage
4. **Scale** - Add more resources if needed
5. **Enhance** - Add new features based on requirements

---

**Status**: Ready for deployment ✅
**Next**: Choose deployment option and follow steps

