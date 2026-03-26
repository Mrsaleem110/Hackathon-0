#!/usr/bin/env python3
"""
Send meeting reminder email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_meeting_reminder():
    """Send meeting reminder email"""

    try:
        # Gmail SMTP settings
        sender_email = "sm6928234@gmail.com"
        sender_password = "$@!eem1234"  # App password for Gmail
        to_email = "sm6928234@gmail.com"

        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Meeting Reminder - 11:00 PM Today"
        message["From"] = sender_email
        message["To"] = to_email

        # Email body in Urdu and English
        body = """السلام علیکم

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

والسلام علیکم"""

        # Add body
        part = MIMEText(body, "plain", "utf-8")
        message.attach(part)

        # Send via Gmail SMTP
        print(f"Connecting to Gmail SMTP server...")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)

        print(f"Sending meeting reminder to {to_email}...")
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()

        print(f"✅ Meeting reminder sent successfully!")
        print(f"   To: {to_email}")
        print(f"   Subject: Meeting Reminder - 11:00 PM Today")
        print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return True

    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False

if __name__ == "__main__":
    send_meeting_reminder()
