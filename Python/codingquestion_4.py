import boto3
from datetime import datetime, timedelta, timezone

s3 = boto3.client("s3")
bucket = "my-log-bucket"
cutoff = datetime.now(timezone.utc) - timedelta(days=30)

paginator = s3.get_paginator("list_objects_v2")

for page in paginator.paginate(Bucket=bucket):
    for obj in page.get("Contents", []):
        if obj["LastModified"] < cutoff:
            s3.delete_object(Bucket=bucket, Key=obj["Key"])
            print("Deleted:", obj["Key"])