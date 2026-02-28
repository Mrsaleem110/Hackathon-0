# WhatsApp & LinkedIn Real Credentials Setup Guide

## Quick Start

### Option 1: Automated Setup (Recommended)
```bash
cd AI_Employee_Vault
python setup_credentials.py
```

This will guide you through:
1. WhatsApp Web login (scan QR code)
2. LinkedIn login (enter credentials)

---

### Option 2: Manual Setup

#### WhatsApp Setup
```bash
cd AI_Employee_Vault
python whatsapp_login.py
```

**What to do:**
1. Browser opens to https://web.whatsapp.com
2. On your phone: Settings → Linked Devices → Link a Device
3. Scan the QR code with your phone camera
4. Wait for login to complete
5. Session saves automatically to `.whatsapp_session/`

#### LinkedIn Setup
```bash
cd AI_Employee_Vault
python linkedin_login.py
```

**What to do:**
1. Browser opens to https://www.linkedin.com
2. Enter your LinkedIn email
3. Enter your LinkedIn password
4. Complete 2FA if prompted
5. Wait for login to complete
6. Session saves automatically to `.linkedin_session/`

---

## Verify Setup

Check if sessions were created:
```bash
cd AI_Employee_Vault

# Check WhatsApp session
ls -la .whatsapp_session/

# Check LinkedIn session
ls -la .linkedin_session/
```

Both should show files/folders inside them.

---

## Update .env File (Optional)

If you want to use LinkedIn API features, update your `.env`:

```bash
cd AI_Employee_Vault
nano .env
```

Replace these lines with your actual LinkedIn credentials from https://www.linkedin.com/developers/apps:

```env
LINKEDIN_CLIENT_ID=YOUR_ACTUAL_CLIENT_ID
LINKEDIN_CLIENT_SECRET=YOUR_ACTUAL_CLIENT_SECRET
LINKEDIN_ACCESS_TOKEN=YOUR_ACTUAL_TOKEN
```

---

## Test Everything

```bash
cd AI_Employee_Vault
python config.py
```

Should show:
- [OK] WhatsApp session found
- [OK] LinkedIn session found

---

## Run the Vault

Once setup is complete:

```bash
cd AI_Employee_Vault
python orchestrator.py
```

Your AI Employee Vault will now monitor:
- WhatsApp messages (urgent keywords)
- LinkedIn messages (business opportunities)
- Gmail (already configured)

---

## Troubleshooting

### WhatsApp QR Code Not Appearing
- Make sure WhatsApp is installed on your phone
- Try closing and reopening the browser
- Check your internet connection

### LinkedIn Login Fails
- Verify your email and password are correct
- If 2FA is enabled, complete the verification
- Try logging in manually first to ensure account is active

### Sessions Not Saving
- Make sure you have write permissions in the folder
- Check that the browser window stayed open long enough
- Try deleting the session folder and running again

---

## Security Notes

✅ DO:
- Keep `.whatsapp_session/` and `.linkedin_session/` private
- Don't share these folders
- Rotate credentials monthly
- Monitor your account activity

❌ DON'T:
- Commit session folders to git
- Share session files with others
- Leave sessions unattended
- Use weak passwords

---

## Next Steps

1. Run `python setup_credentials.py`
2. Follow the on-screen instructions
3. Verify sessions were created
4. Run `python orchestrator.py`
5. Check the dashboard for monitored messages

Enjoy your AI Employee Vault!
