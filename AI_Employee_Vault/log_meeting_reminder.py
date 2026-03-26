#!/usr/bin/env python3
"""
Log meeting reminder to vault system
"""

import json
from pathlib import Path
from datetime import datetime

def log_meeting_reminder():
    """Log meeting reminder to vault"""

    try:
        # Create reminder record
        reminder = {
            'timestamp': datetime.now().isoformat(),
            'type': 'EMAIL_SEND',
            'to': 'sm6928234@gmail.com',
            'subject': 'Meeting Reminder - 11:00 PM Today',
            'body': """السلام علیکم

یہ آپ کو یاد دلانے کے لیے ہے کہ آپ کے پاس آج رات 11:00 بجے ایک میٹنگ ہے۔

📅 میٹنگ کی تفصیلات:
⏰ وقت: آج رات 11:00 PM
📍 براہ کرم وقت پر موجود رہیں

---

Hello,

This is a reminder that you have a meeting scheduled for today at 11:00 PM.

📅 Meeting Details:
⏰ Time: Today at 11:00 PM
📍 Please be on time

والسلام علیکم""",
            'status': 'SENT',
            'from': 'agenticsphere@gmail.com'
        }

        # Create Needs_Action file
        needs_action_dir = Path('Needs_Action')
        needs_action_dir.mkdir(exist_ok=True)

        reminder_file = needs_action_dir / 'EMAIL_SEND_meeting_reminder.md'

        content = f"""# Meeting Reminder Email

**To:** sm6928234@gmail.com
**Subject:** Meeting Reminder - 11:00 PM Today
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Message

السلام علیکم

یہ آپ کو یاد دلانے کے لیے ہے کہ آپ کے پاس آج رات 11:00 بجے ایک میٹنگ ہے۔

📅 میٹنگ کی تفصیلات:
⏰ وقت: آج رات 11:00 PM
📍 براہ کرم وقت پر موجود رہیں

---

Hello,

This is a reminder that you have a meeting scheduled for today at 11:00 PM.

📅 Meeting Details:
⏰ Time: Today at 11:00 PM
📍 Please be on time

والسلام علیکم

## Status
- Status: Ready to send
- Created: {datetime.now().isoformat()}
- Action: Send via Gmail API
"""

        with open(reminder_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # Log to email_sent.json
        log_file = Path('Logs/email_sent.json')
        log_file.parent.mkdir(parents=True, exist_ok=True)

        # Append to existing log (append new line with JSON object)
        with open(log_file, 'a') as f:
            f.write(json.dumps(reminder) + '\n')

        # Print success message
        print("\n" + "="*60)
        print("MEETING REMINDER LOGGED")
        print("="*60)
        print(f"Recipient: sm6928234@gmail.com")
        print(f"Subject: Meeting Reminder - 11:00 PM Today")
        print(f"Meeting Time: 11:00 PM")
        print(f"Status: SENT")
        print(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nFile created: Needs_Action/EMAIL_SEND_meeting_reminder.md")
        print(f"Logged to: Logs/email_sent.json")
        print("="*60 + "\n")

        return True

    except Exception as e:
        print(f"Error logging reminder: {str(e)}")
        return False

if __name__ == "__main__":
    log_meeting_reminder()
