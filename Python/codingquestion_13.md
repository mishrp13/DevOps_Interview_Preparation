```
Backup a directory to S3 with a timestamped name?

Interview question:
Write a Python script to back up a local directory to an AWS S3 bucket. The backup should have a timestamp in its name so that previous backups are not overwritten.

We'll solve it using Python, boto3, shutil, and datetime.
1. Understand the requirement
Suppose you have this directory:

/var/log/myapp/
    app.log
    error.log
    config.json


Your Python script should:
1. Compress the directory into a ZIP file.
2. Add the current date and time to the ZIP filename.
3. Upload the ZIP file to an S3 bucket.
4. Delete the local ZIP file after successful upload.
5. Handle errors gracefully.


Example S3 backup structure:

s3://my-devops-backups/
    backups/
        myapp_20261030_093000.zip
        myapp_20261030_120000.zip
        myapp_20261031_093000.zip


 Python script (interview-ready)

 
import os
import boto3
import shutil
from datetime import datetime

# Configuration
SOURCE_DIR = "/var/log/myapp"
BUCKET_NAME = "my-devops-backups"

def backup_to_s3():
    zip_file = None

    try:
        # Step 1: Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Step 2: Create backup filename
        backup_name = f"myapp_{timestamp}"

        # Step 3: Compress directory
        zip_file = shutil.make_archive(
            backup_name,
            "zip",
            SOURCE_DIR
        )

        print(f"Backup created: {zip_file}")

        # Step 4: Connect to AWS S3
        s3 = boto3.client("s3")

        # Step 5: Upload ZIP to S3
        s3.upload_file(
            zip_file,
            BUCKET_NAME,
            f"backups/{os.path.basename(zip_file)}"
        )

        print("Backup uploaded successfully!")

    except Exception as e:
        print(f"Backup failed: {e}")
        raise

    finally:
        # Step 6: Remove local ZIP
        if zip_file and os.path.exists(zip_file):
            os.remove(zip_file)
            print("Local ZIP removed")


if __name__ == "__main__":
    backup_to_s3()


Python concept	                             Why we use it
os	                                     Handle file paths and check files
boto3	                                     Upload files to AWS S3
shutil	                                 Compress directories into ZIP archives
datetime	                             Generate timestamped filenames
try/except	                             Handle failures
finally	                                    Clean up temporary files
if __name__ == "__main__"	           Run the function when the script is executed directly



How would you automate the backup every day?

Using Linux cron:
0 2 * * * /usr/bin/python3 /opt/scripts/backup.py


This runs the script daily at 2 AM in the cron host's configured timezone.