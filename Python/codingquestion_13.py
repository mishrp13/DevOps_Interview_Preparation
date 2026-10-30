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
