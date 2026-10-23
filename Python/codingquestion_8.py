import shutil
import smtplib
import os
from email.message import EmailMessage

THRESHOLD = 80

def send_alert(usage):
    msg = EmailMessage()
    msg["Subject"] = "Disk Usage Alert"
    msg["From"] = os.environ["SMTP_USER"]
    msg["To"] = os.environ["ALERT_EMAIL"]

    msg.set_content(
        f"Alert! Disk usage is {usage:.2f}%"
    )

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(
            os.environ["SMTP_USER"],
            os.environ["SMTP_PASSWORD"]
        )
        server.send_message(msg)    

def check_disk():
    disk = shutil.disk_usage("/")
    usage = (disk.used / disk.total) * 100

    print(f"Disk Usage: {usage:.2f}%")

    if usage > THRESHOLD:
        print("ALERT: Disk usage exceeded 80%")
        send_alert(usage)
    else:
        print("Disk usage is normal")

if __name__ == "__main__":
    check_disk()


# For actual sending, your organization must allow the chosen authentication method. If SMTP username/password
#  authentication is blocked, use OAuth2 or Microsoft Graph API instead