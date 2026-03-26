#!/usr/bin/env python3
"""
Send email via Gmail SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_email_smtp(to_email, subject, body):
    """Send email using Gmail SMTP"""

    try:
        # Gmail SMTP settings
        sender_email = "sm6928234@gmail.com"
        sender_password = "$@!eem1234"  # App password for Gmail

        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = to_email

        # Add body
        part = MIMEText(body, "plain", "utf-8")
        message.attach(part)

        # Send via Gmail SMTP
        print(f"Connecting to Gmail SMTP server...")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)

        print(f"Sending email to {to_email}...")
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()

        print(f"✅ Email sent successfully!")
        print(f"   To: {to_email}")
        print(f"   Subject: {subject}")

        return True

    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False

if __name__ == "__main__":
    # Test email
    to_email = "sm6928234@gmail.com"
    subject = "Agentic Sphere - Your Personal AI Employee"
    body = """السلام علیکم

میں آپ کو Agentic Sphere کا تعارف کرانا چاہتا ہوں - ایک انقلابی AI نظام جو آپ کے ذاتی اور کاروباری کاموں کو خودکار طریقے سے سنبھالتا ہے۔

Agentic Sphere کیا ہے؟
یہ ایک ذہین AI نظام ہے جو:
- آپ کی emails، WhatsApp، اور LinkedIn کو monitor کرتا ہے
- ذہین منصوبے بناتا ہے
- آپ کی منظوری سے کام انجام دیتا ہے
- ہر کام کا مکمل ریکارڈ رکھتا ہے

فوائل:
✅ 24/7 کام کرتا ہے
✅ ذہین فیصلے لیتا ہے
✅ آپ کے کنٹرول میں رہتا ہے
✅ مکمل شفافیت

یہ آپ کے لیے ایک ذاتی AI ملازم ہے جو ہمیشہ آپ کی خدمت میں ہے۔

والسلام علیکم"""

    print("Sending email via Gmail SMTP...")
    send_email_smtp(to_email, subject, body)
