# Real Odoo Setup Guide - Quick Start

## Fastest Way: Docker (Recommended)

### Step 1: Install Docker Desktop
- Download: https://www.docker.com/products/docker-desktop
- Install and restart your computer

### Step 2: Start Odoo in Docker
Open PowerShell and run:

```powershell
docker run -d -p 8069:8069 --name odoo19 `
  -e POSTGRES_PASSWORD=odoo `
  -e POSTGRES_USER=odoo `
  -e POSTGRES_DB=odoo `
  odoo:19
```

Wait 2-3 minutes for it to start.

### Step 3: Access Odoo
1. Open browser: http://localhost:8069
2. Create admin account (email/password)
3. Create a new database
4. Login

### Step 4: Get API Key
1. Click your profile icon (top right)
2. Go to Settings
3. Click "Users"
4. Click on your user
5. Scroll down to "API Keys" section
6. Click "Generate API Key"
7. Copy the key

### Step 5: Configure AI Employee Vault
Edit `.env` file and add:

```
ODOO_URL=http://localhost:8069
ODOO_DB=odoo
ODOO_API_KEY=your_api_key_here
```

### Step 6: Test It
```bash
python test_all_fixes.py
```

---

## Alternative: Windows Installer

1. Download: https://www.odoo.com/en_US/download
2. Run installer (PostgreSQL included)
3. Odoo starts automatically on http://localhost:8069
4. Follow Steps 3-6 above

---

## Check if Odoo is Running

```bash
python -c "import requests; print('Odoo running!' if requests.get('http://localhost:8069', timeout=2).status_code else 'Not running')"
```

---

## Troubleshooting

**Docker not found?**
- Install Docker Desktop first
- Restart computer
- Run docker command again

**Can't access http://localhost:8069?**
- Wait 2-3 minutes for Odoo to start
- Check: `docker ps` (should show odoo19 container)
- Check logs: `docker logs odoo19`

**API Key not working?**
- Make sure you copied the full key
- Try generating a new one
- Check database name matches

---

## Once Odoo is Running

Your AI Employee Vault will automatically:
- Connect to real Odoo
- Pull real financial data
- Track real sales pipeline
- Generate real accounting reports

Run this to verify:
```bash
python test_all_fixes.py
```

You should see:
```
ODOO                 [OK] PASS (real mode)
```

Instead of mock mode!
