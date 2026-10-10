```
.Rotate IAM access keys older than 90 days?

devops interview
For a DevOps interview, explain that you can use Python + Boto3 (AWS SDK) to identify IAM access keys older than 90 days and rotate them according to your organization's security policy.

Important: A safe rotation process creates a replacement key, updates the application or secret store, verifies that the new key works, and only then deactivates the old key. Don't deactivate keys blindly, because that can break production workloads.

Python code: Detect IAM access keys older than 90 days


Install Boto3:

pip install boto3

Configure AWS credentials using an IAM role or your AWS CLI profile.

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


How to explain it in an interview

Use Boto3 to connect to AWS IAM.

Retrieve IAM users using a paginator so all users are checked.

Retrieve each user's access key metadata.

Compare the key creation date with the current UTC time minus 90 days.

Report active keys older than 90 days for rotation.

Create a replacement key, securely update dependent applications, test it, and deactivate the old key only after verification.

Important interview point: This code identifies keys that need rotation; it does not perform the full rotation. Actual rotation requires updating the systems that consume each key. Prefer IAM roles and temporary credentials over long-lived access keys wherever possible.

