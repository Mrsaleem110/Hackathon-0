# Real Credentials Setup - Complete Instructions

## What You Need

### For WhatsApp
- WhatsApp installed on your phone
- Internet connection
- 1-2 minutes

### For LinkedIn
- LinkedIn account (email + password)
- Internet connection
- 1-2 minutes
- 2FA device if enabled

---

## Step-by-Step Instructions

### Step 1: Open Terminal/Command Prompt

```bash
cd C:\Users\Agentic Sphere\Documents\GitHub\Hackathon-0\AI_Employee_Vault
```

### Step 2: Run the Setup Script

```bash
python setup_credentials.py
```

### Step 3: Follow the Prompts

The script will guide you through:

**Part 1: WhatsApp Setup**
- Press Enter when ready
- Browser opens to web.whatsapp.com
- On your phone: Settings → Linked Devices → Link a Device
- Scan the QR code
- Wait for login

**Part 2: LinkedIn Setup**
- Press Enter when ready
- Browser opens to linkedin.com
- Enter your email
- Enter your password
- Complete 2FA if needed
- Wait for login

### Step 4: Verify Success

The script will show:
```
WhatsApp Session: OK
LinkedIn Session: OK
```

---

## What Gets Created

After setup, you'll have:

```
AI_Employee_Vault/
├── .whatsapp_session/          (WhatsApp login saved here)
├── .linkedin_session/          (LinkedIn login saved here)
├── .env                        (Your credentials config)
└── [other files...]
```

---

## Run Your AI Employee Vault

Once setup is complete:

```bash
python orchestrator.py
```

This will:
- Monitor WhatsApp for urgent messages
- Monitor LinkedIn for business opportunities
- Monitor Gmail for important emails
- Create action files for you to review

---

## Individual Login Scripts (If Needed)

If you want to login to just one service:

**WhatsApp Only:**
```bash
python whatsapp_login.py
```

**LinkedIn Only:**
```bash
python linkedin_login.py
```

---

## Check Session Status

```bash
# Check if WhatsApp session exists
dir .whatsapp_session

# Check if LinkedIn session exists
dir .linkedin_session

# Check configuration
python config.py
```

---

## Important Notes

⚠️ **Security:**
- Never commit `.whatsapp_session/` or `.linkedin_session/` to git
- Never share these folders
- Keep your `.env` file private
- Add to `.gitignore` (already done)

✅ **Best Practices:**
- Keep your phone nearby during WhatsApp setup
- Use a strong LinkedIn password
- Enable 2FA on LinkedIn
- Monitor your account activity

---

## Troubleshooting

### "Browser won't open"
- Make sure Playwright is installed: `pip install playwright`
- Try running again

### "WhatsApp QR code not scanning"
- Make sure WhatsApp is open on your phone
- Try Settings → Linked Devices → Link a Device again
- Check internet connection

### "LinkedIn login fails"
- Verify email and password are correct
- Check if account is locked
- Try logging in manually first
- Complete 2FA if prompted

### "Sessions not saving"
- Check folder permissions
- Make sure browser stayed open
- Try deleting the session folder and running again

---

## Next Steps

1. ✅ Run: `python setup_credentials.py`
2. ✅ Follow the on-screen instructions
3. ✅ Verify sessions created
4. ✅ Run: `python orchestrator.py`
5. ✅ Check dashboard for messages

---

## Support

If you have issues:
1. Check WHATSAPP_LINKEDIN_SETUP.md for detailed guide
2. Check CREDENTIALS_SETUP.md for Gmail setup
3. Check logs in Logs/ folder
4. Review error messages carefully

Good luck! Your AI Employee Vault is almost ready! 🚀
