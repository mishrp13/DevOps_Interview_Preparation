```
Write a script to monitor disk usage and send an alert if above 80%?

import shutil

# Set threshold
threshold = 80

# Check disk usage
disk = shutil.disk_usage("/")

# Calculate usage percentage
usage = (disk.used / disk.total) * 100

print(f"Disk Usage: {usage:.2f}%")

# Check threshold
if usage > threshold:
    print("ALERT: Disk usage is above 80%!")
else:
    print("Disk usage is normal.")




Explanation line by line
Code	                              Explanation
import shutil	                   Imports Python's built-in disk utility module
threshold = 80	                   Sets the alert threshold to 80%
shutil.disk_usage("/")	           Checks disk usage of the root filesystem
disk.used	                       Returns used disk space in bytes
disk.total	                       Returns total disk space in bytes
(disk.used / disk.total) * 100	   Calculates percentage used
if usage > threshold	           Checks whether usage exceeds 80%


In a real DevOps environment, just printing an alert isn't enough. We may need to notify the operations team via email.

import shutil
import smtplib
from email.message import EmailMessage

THRESHOLD = 80

def send_alert(usage):
    msg = EmailMessage()

    msg["Subject"] = "Disk Usage Alert"
    msg["From"] = "sender@example.com"
    msg["To"] = "admin@example.com"

    msg.set_content(
        f"WARNING! Disk usage is {usage:.2f}%"
    )

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login("sender@example.com", "APP_PASSWORD")
        server.send_message(msg)

def check_disk():
    disk = shutil.disk_usage("/")
    usage = (disk.used / disk.total) * 100

    print(f"Disk Usage: {usage:.2f}%")

    if usage > THRESHOLD:
        print("Disk usage exceeded 80%")
        send_alert(usage)
    else:
        print("Disk usage is normal")

check_disk()


Important: Replace the example SMTP settings with your email provider's configuration. In production, store credentials in environment variables or a secrets manager rather than hardcoding passwords. You should also add exception handling for email delivery failures


How to execute on a Linux server
First, create the Python file:

vi disk_monitor.py

Paste the script, save it, and run:
python3 disk_monitor.py

To check disk usage manually:
df -h

To automate the monitoring, use cron:
crontab -e


Add this entry:
*/5 * * * * /usr/bin/python3 /home/ubuntu/disk_monitor.py

This executes the script every 5 minutes. Make sure the script path and Python path match your server.

Production tip: A five-minute cron job could send repeated emails while usage stays above 80%. Implement alert deduplication or a cooldown period to prevent alert flooding.

How to explain this in a DevOps interview

I use Python's shutil module to monitor disk usage. The shutil.disk_usage() function provides total, used, and free disk space. I calculate the usage percentage and compare it with an 80% threshold. If the usage exceeds 80%, the script triggers an alert using SMTP. I can schedule the script using cron to monitor disk usage automatically every five minutes.


Common interview follow-up questions

1. Why do we use shutil?
shutil is a built-in Python module that provides disk usage information without installing external packages.

2. What is the difference between disk usage and memory usage?
Disk usage measures storage consumption on a filesystem. Memory usage measures RAM consumption. For RAM monitoring, we can use the psutil library.

3. How do you monitor multiple disks?
Use a loop over mount points such as /, /var, and /data, and call shutil.disk_usage() for each. Avoid duplicate alerts for paths on the same filesystem.

4. How do you automate this script?
Use Linux cron, a systemd timer, or a scheduled Kubernetes CronJob, depending on the environment.

5. What happens if disk usage reaches 90%?
The script triggers an alert because 90% exceeds the 80% threshold. We can also configure a critical alert level at 90%.