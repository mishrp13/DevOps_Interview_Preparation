
import boto3
from datetime import datetime, timezone, timedelta

iam = boto3.client("iam")

# Access key rotation threshold
threshold = datetime.now(timezone.utc) - timedelta(days=90)

# Get all IAM users
paginator = iam.get_paginator("list_users")

for page in paginator.paginate():
    for user in page["Users"]:
        username = user["UserName"]

        # Get access keys for each user
        response = iam.list_access_keys(UserName=username)

        for key in response["AccessKeyMetadata"]:
            key_id = key["AccessKeyId"]
            created = key["CreateDate"]
            status = key["Status"]

            if created < threshold and status == "Active":
                age = (datetime.now(timezone.utc) - created).days

                print(
                    f"User: {username} | "
                    f"Key: {key_id} | "
                    f"Age: {age} days | "
                    f"Status: {status}"
                )

                # Rotate only after replacing the key
                # in dependent applications and verifying it.

