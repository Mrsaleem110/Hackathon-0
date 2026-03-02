"""
Real Data Checker - Check actual data from Gmail, LinkedIn, WhatsApp
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

print("\n" + "="*70)
print("REAL DATA CHECK - Your Actual Accounts")
print("="*70 + "\n")

# ============ GMAIL CHECK ============
print("[GMAIL] Real Email Check")
print("-" * 70)

gmail_id = os.getenv('GMAIL_CLIENT_ID')
gmail_secret = os.getenv('GMAIL_CLIENT_SECRET')
token_path = Path('token.json')

if gmail_id and gmail_secret:
    print("✓ Gmail credentials in .env: YES")
    if token_path.exists():
        print("✓ Gmail authenticated (token.json exists): YES")
        print("✓ Status: READY - Can fetch real emails")

        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build

            creds = Credentials.from_authorized_user_file(str(token_path))
            service = build('gmail', 'v1', credentials=creds)

            # Get unread emails
            results = service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=5
            ).execute()

            messages = results.get('messages', [])
            print(f"\n✓ Unread Emails Found: {len(messages)}")

            if messages:
                print("\nRecent Unread Emails:")
                for i, msg in enumerate(messages[:3], 1):
                    full_msg = service.users().messages().get(
                        userId='me',
                        id=msg['id'],
                        format='metadata',
                        metadataHeaders=['From', 'Subject', 'Date']
                    ).execute()

                    headers = {h['name']: h['value'] for h in full_msg['payload']['headers']}
                    print(f"\n  {i}. From: {headers.get('From', 'Unknown')}")
                    print(f"     Subject: {headers.get('Subject', 'No Subject')}")
                    print(f"     Date: {headers.get('Date', 'Unknown')}")
        except Exception as e:
            print(f"✗ Error: {e}")
    else:
        print("✗ Gmail authenticated (token.json exists): NO")
        print("✗ Status: NEEDS AUTHENTICATION")
        print("  → Run: python gmail_watcher.py (first time)")
else:
    print("✗ Gmail credentials in .env: NO")

# ============ LINKEDIN CHECK ============
print("\n\n[LINKEDIN] Real Data Check")
print("-" * 70)

linkedin_id = os.getenv('LINKEDIN_CLIENT_ID')
linkedin_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
linkedin_session = Path('.linkedin_session')

if linkedin_id and linkedin_secret:
    print("✓ LinkedIn credentials in .env: YES")
    if linkedin_session.exists():
        print("✓ LinkedIn session folder exists: YES")
        print("✓ Status: READY - Can post to LinkedIn")

        session_files = list(linkedin_session.glob('**/*'))
        print(f"  Session files: {len(session_files)} items")
    else:
        print("✗ LinkedIn session folder exists: NO")
        print("✗ Status: NEEDS LOGIN")
        print("  → Run: python linkedin_login.py (first time)")
else:
    print("✗ LinkedIn credentials in .env: NO")

# ============ WHATSAPP CHECK ============
print("\n\n[WHATSAPP] Real Data Check")
print("-" * 70)

whatsapp_session = Path('.whatsapp_session')

if whatsapp_session.exists():
    print("✓ WhatsApp session folder exists: YES")
    print("✓ Status: READY - Can send WhatsApp messages")

    session_files = list(whatsapp_session.glob('**/*'))
    print(f"  Session files: {len(session_files)} items")
else:
    print("✗ WhatsApp session folder exists: NO")
    print("✗ Status: NEEDS LOGIN")
    print("  → Run: python Watchers/whatsapp_watcher.py (first time)")

# ============ SUMMARY ============
print("\n\n" + "="*70)
print("SUMMARY")
print("="*70)

gmail_ready = gmail_id and gmail_secret and token_path.exists()
linkedin_ready = linkedin_id and linkedin_secret and linkedin_session.exists()
whatsapp_ready = whatsapp_session.exists()

print(f"\nGmail:    {'✓ READY' if gmail_ready else '✗ NOT READY'}")
print(f"LinkedIn: {'✓ READY' if linkedin_ready else '✗ NOT READY'}")
print(f"WhatsApp: {'✓ READY' if whatsapp_ready else '✗ NOT READY'}")

if gmail_ready and linkedin_ready and whatsapp_ready:
    print("\n✓ ALL SYSTEMS READY - Full automation active!")
else:
    print("\n✗ Some systems need setup:")
    if not gmail_ready:
        print("  - Gmail: Run 'python gmail_watcher.py' to authenticate")
    if not linkedin_ready:
        print("  - LinkedIn: Run 'python linkedin_login.py' to authenticate")
    if not whatsapp_ready:
        print("  - WhatsApp: Run 'python Watchers/whatsapp_watcher.py' to authenticate")

print("\n" + "="*70 + "\n")
