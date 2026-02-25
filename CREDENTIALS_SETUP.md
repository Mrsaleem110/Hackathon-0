# Real Credentials Setup Guide - Silver Tier

**Complete guide to set up real credentials for production use**

---

## ⚠️ IMPORTANT SECURITY NOTES

- **NEVER commit `.env` file to git**
- **NEVER share credentials publicly**
- **Use environment variables for sensitive data**
- **Rotate credentials monthly**
- **Keep `.env` in `.gitignore`**

---

## Step 1: Gmail API Setup

### 1.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a Project" → "New Project"
3. Enter project name: `AI-Employee-Vault`
4. Click "Create"

### 1.2 Enable Gmail API

1. In Google Cloud Console, search for "Gmail API"
2. Click on "Gmail API"
3. Click "Enable"

### 1.3 Create OAuth 2.0 Credentials

1. Go to "Credentials" in left sidebar
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External
   - App name: AI Employee Vault
   - User support email: your-email@gmail.com
   - Developer contact: your-email@gmail.com
4. For Application type, select "Desktop application"
5. Click "Create"
6. Download JSON file as `gmail_credentials.json`

### 1.4 Place Credentials File

```bash
# Copy to vault directory
cp ~/Downloads/gmail_credentials.json AI_Employee_Vault/

# Verify
ls -la AI_Employee_Vault/gmail_credentials.json
```

### 1.5 Test Gmail Connection

```bash
cd AI_Employee_Vault

# Run authentication
python << 'EOF'
from Watchers.gmail_watcher import GmailWatcher

watcher = GmailWatcher(".")
if watcher.service:
    print("✅ Gmail API authenticated successfully!")
else:
    print("❌ Gmail API authentication failed")
EOF
```

---

## Step 2: WhatsApp Setup

### 2.1 First Run - QR Code Login

```bash
cd AI_Employee_Vault

# Run WhatsApp watcher for first time
python << 'EOF'
from Watchers.whatsapp_watcher import WhatsAppWatcher

watcher = WhatsAppWatcher(".")
print("Opening WhatsApp Web...")
print("Scan QR code with your phone")
print("Session will be saved to .whatsapp_session/")

# This will open browser and wait for QR scan
# watcher.run()  # Uncomment to start monitoring
EOF
```

### 2.2 What Happens

1. Browser opens to https://web.whatsapp.com
2. QR code appears on screen
3. Scan with your phone's WhatsApp
4. Session automatically saved to `.whatsapp_session/`
5. Watcher starts monitoring

### 2.3 Verify Session

```bash
# Check if session was created
ls -la AI_Employee_Vault/.whatsapp_session/

# Should see browser profile files
```

---

## Step 3: LinkedIn Setup

### 3.1 Create LinkedIn App

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Click "Create app"
3. Fill in details:
   - App name: AI Employee Vault
   - LinkedIn Page: (create or select existing)
   - App logo: (upload)
   - Legal agreement: Accept
4. Click "Create app"

### 3.2 Get Credentials

1. Go to "Auth" tab
2. Copy:
   - Client ID
   - Client Secret
3. Add to `.env` file:
   ```
   LINKEDIN_CLIENT_ID=your_client_id
   LINKEDIN_CLIENT_SECRET=your_client_secret
   ```

### 3.3 First Run - LinkedIn Login

```bash
cd AI_Employee_Vault

# Run LinkedIn watcher for first time
python << 'EOF'
from Watchers.linkedin_watcher import LinkedInWatcher

watcher = LinkedInWatcher(".")
print("Opening LinkedIn...")
print("Log in with your account")
print("Session will be saved to .linkedin_session/")

# This will open browser and wait for login
# watcher.run()  # Uncomment to start monitoring
EOF
```

### 3.4 Verify Session

```bash
# Check if session was created
ls -la AI_Employee_Vault/.linkedin_session/

# Should see browser profile files
```

---

## Step 4: Create .env File

### 4.1 Copy Template

```bash
cd AI_Employee_Vault
cp .env.example .env
```

### 4.2 Edit .env File

```bash
# Open .env in your editor
nano .env
# or
code .env
```

### 4.3 Fill in Credentials

```env
# Gmail API Credentials (from Step 1)
GMAIL_CLIENT_ID=your_actual_client_id
GMAIL_CLIENT_SECRET=your_actual_client_secret
GMAIL_REDIRECT_URI=http://localhost:8080/

# LinkedIn Credentials (from Step 3)
LINKEDIN_CLIENT_ID=your_actual_client_id
LINKEDIN_CLIENT_SECRET=your_actual_client_secret
LINKEDIN_ACCESS_TOKEN=your_actual_token

# Session Paths (auto-created)
WHATSAPP_SESSION_PATH=.whatsapp_session
LINKEDIN_SESSION_PATH=.linkedin_session

# System Settings
VAULT_PATH=.
LOG_LEVEL=INFO
DRY_RUN=false
APPROVAL_EXPIRY_HOURS=24
ENABLE_SCHEDULER=true
TIMEZONE=UTC
```

---

## Step 5: Add to .gitignore

### 5.1 Create/Update .gitignore

```bash
cd AI_Employee_Vault

# Add to .gitignore
cat >> .gitignore << 'EOF'

# Credentials and secrets
.env
.env.local
gmail_credentials.json
token.json

# Sessions
.whatsapp_session/
.linkedin_session/

# Temporary files
*.pyc
__pycache__/
.DS_Store

# IDE
.vscode/
.idea/

# Logs (optional - keep for audit)
# Logs/

EOF

# Verify
cat .gitignore
```

### 5.2 Remove Accidentally Committed Files

```bash
# If you accidentally committed .env
git rm --cached .env
git commit -m "Remove .env from tracking"
```

---

## Step 6: Load Environment Variables

### 6.1 Create Config Loader

```bash
cat > AI_Employee_Vault/config.py << 'EOF'
"""
Configuration loader for AI Employee Vault
Loads credentials from .env file
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Gmail Configuration
GMAIL_CLIENT_ID = os.getenv('GMAIL_CLIENT_ID')
GMAIL_CLIENT_SECRET = os.getenv('GMAIL_CLIENT_SECRET')
GMAIL_REDIRECT_URI = os.getenv('GMAIL_REDIRECT_URI', 'http://localhost:8080/')

# LinkedIn Configuration
LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')

# Session Paths
WHATSAPP_SESSION_PATH = os.getenv('WHATSAPP_SESSION_PATH', '.whatsapp_session')
LINKEDIN_SESSION_PATH = os.getenv('LINKEDIN_SESSION_PATH', '.linkedin_session')

# System Configuration
VAULT_PATH = os.getenv('VAULT_PATH', '.')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
DRY_RUN = os.getenv('DRY_RUN', 'false').lower() == 'true'

# Approval Settings
APPROVAL_EXPIRY_HOURS = int(os.getenv('APPROVAL_EXPIRY_HOURS', '24'))
AUTO_APPROVE_THRESHOLD = int(os.getenv('AUTO_APPROVE_THRESHOLD', '50'))

# Scheduling
ENABLE_SCHEDULER = os.getenv('ENABLE_SCHEDULER', 'true').lower() == 'true'
TIMEZONE = os.getenv('TIMEZONE', 'UTC')

def validate_credentials():
    """Validate that all required credentials are set"""
    required = {
        'GMAIL_CLIENT_ID': GMAIL_CLIENT_ID,
        'GMAIL_CLIENT_SECRET': GMAIL_CLIENT_SECRET,
        'LINKEDIN_CLIENT_ID': LINKEDIN_CLIENT_ID,
        'LINKEDIN_CLIENT_SECRET': LINKEDIN_CLIENT_SECRET,
    }

    missing = [key for key, value in required.items() if not value]

    if missing:
        print(f"⚠️  Missing credentials: {', '.join(missing)}")
        print("Please set up .env file with real credentials")
        return False

    return True

if __name__ == '__main__':
    if validate_credentials():
        print("✅ All credentials configured")
    else:
        print("❌ Some credentials missing")
EOF
```

### 6.2 Install python-dotenv

```bash
pip install python-dotenv
```

---

## Step 7: Test All Credentials

### 7.1 Test Gmail

```bash
cd AI_Employee_Vault

python << 'EOF'
from config import validate_credentials, GMAIL_CLIENT_ID
from Watchers.gmail_watcher import GmailWatcher

if validate_credentials():
    print("✅ Credentials loaded")
    watcher = GmailWatcher(".")
    if watcher.service:
        print("✅ Gmail API connected")
    else:
        print("❌ Gmail API connection failed")
else:
    print("❌ Credentials validation failed")
EOF
```

### 7.2 Test WhatsApp

```bash
cd AI_Employee_Vault

python << 'EOF'
from Watchers.whatsapp_watcher import WhatsAppWatcher
import os

watcher = WhatsAppWatcher(".")
session_exists = os.path.exists(".whatsapp_session")

if session_exists:
    print("✅ WhatsApp session found")
else:
    print("⚠️  WhatsApp session not found - run first login")
EOF
```

### 7.3 Test LinkedIn

```bash
cd AI_Employee_Vault

python << 'EOF'
from Watchers.linkedin_watcher import LinkedInWatcher
import os

watcher = LinkedInWatcher(".")
session_exists = os.path.exists(".linkedin_session")

if session_exists:
    print("✅ LinkedIn session found")
else:
    print("⚠️  LinkedIn session not found - run first login")
EOF
```

---

## Step 8: Run with Real Credentials

### 8.1 Run Demo Mode (Still Works)

```bash
cd AI_Employee_Vault
python orchestrator.py demo
```

### 8.2 Run One Cycle

```bash
cd AI_Employee_Vault
python orchestrator.py
```

### 8.3 Run Continuous

```bash
cd AI_Employee_Vault
python orchestrator.py continuous
```

---

## Step 9: Credential Rotation

### 9.1 Rotate Gmail Credentials (Monthly)

1. Go to Google Cloud Console
2. Delete old credentials
3. Create new OAuth credentials
4. Update `.env` file
5. Test connection

### 9.2 Rotate LinkedIn Credentials (Monthly)

1. Go to LinkedIn Developers
2. Regenerate Client Secret
3. Update `.env` file
4. Test connection

### 9.3 Rotate WhatsApp Session (As Needed)

```bash
# If session expires, delete and re-login
rm -rf AI_Employee_Vault/.whatsapp_session

# Run first login again
python << 'EOF'
from Watchers.whatsapp_watcher import WhatsAppWatcher
watcher = WhatsAppWatcher(".")
# Scan QR code when prompted
EOF
```

---

## Troubleshooting

### Issue: "Gmail credentials not found"

```bash
# Check if file exists
ls -la AI_Employee_Vault/gmail_credentials.json

# Check if .env is loaded
python -c "from config import GMAIL_CLIENT_ID; print(GMAIL_CLIENT_ID)"
```

### Issue: "WhatsApp session expired"

```bash
# Delete old session
rm -rf AI_Employee_Vault/.whatsapp_session

# Re-login
python << 'EOF'
from Watchers.whatsapp_watcher import WhatsAppWatcher
watcher = WhatsAppWatcher(".")
EOF
```

### Issue: "LinkedIn authentication failed"

```bash
# Check credentials in .env
cat AI_Employee_Vault/.env | grep LINKEDIN

# Regenerate token from LinkedIn Developers
```

### Issue: "DRY_RUN mode enabled"

```bash
# Check .env
grep DRY_RUN AI_Employee_Vault/.env

# Should be: DRY_RUN=false
```

---

## Security Best Practices

✅ **DO:**
- Store credentials in `.env` file
- Add `.env` to `.gitignore`
- Rotate credentials monthly
- Use environment variables
- Keep sessions secure
- Monitor audit logs

❌ **DON'T:**
- Commit `.env` to git
- Share credentials in messages
- Use same credentials for multiple services
- Store credentials in code
- Leave sessions unattended
- Ignore security warnings

---

## Next Steps

1. ✅ Set up Gmail API credentials
2. ✅ Set up WhatsApp session
3. ✅ Set up LinkedIn credentials
4. ✅ Create `.env` file
5. ✅ Test all connections
6. ✅ Run with real credentials
7. 🔄 Monitor logs and dashboard
8. 📈 Upgrade to Gold Tier

---

*Real Credentials Setup Guide*
*February 25, 2026*
