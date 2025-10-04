import smtplib
from email.mime.text import MIMEText

EMAIL_ADDRESS = "hs6202888927@gmail.com"         # ✅ Your Gmail address
EMAIL_PASSWORD = "tkpyofixnkztwjoj"    # <-- Your new app password (no spaces)

def send_reminder_email(to_email, name, reason, date, reminder_type):
    subject = f"⏰ Reminder: {reminder_type} on {date}"
    body = f"""
Hi {name},

This is a reminder for your upcoming {reminder_type}.

📅 Date: {date}
📝 Reason: {reason}

Best regards,  
Swastha AI - Health Reminder System
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print("❌ Failed to send email:", e)
        return False




