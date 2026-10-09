```
4.Delete S3 objects older than N days?

For a Python + DevOps interview, this question tests your ability to automate AWS S3 cleanup using Python and the boto3 SDK.

The requirement is: Delete S3 objects older than N days, for example, delete log files older than 30 days to reduce storage costs.

1. Interview-ready Python code

This is a good solution to write in an interview. It checks each object's last-modified time and deletes objects older than the specified number of days.


import boto3
from datetime import datetime, timedelta, timezone

s3 = boto3.client("s3")

bucket_name = "my-log-bucket"
days = 30

cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

paginator = s3.get_paginator("list_objects_v2")

for page in paginator.paginate(Bucket=bucket_name):
    for obj in page.get("Contents", []):
        if obj["LastModified"] < cutoff_date:
            s3.delete_object(
                Bucket=bucket_name,
                Key=obj["Key"]
            )
            print(f"Deleted: {obj['Key']}")
2. Understand the code step by step

Step 1: Import libraries

import boto3
from datetime import datetime, timedelta, timezone

boto3 lets Python interact with AWS services.

datetime gets the current date and time.

timedelta calculates how many days ago the cutoff is.

timezone.utc ensures timezone-aware comparisons.

Step 2: Connect to S3

s3 = boto3.client("s3")
bucket_name = "my-log-bucket"
days = 30

This creates an S3 client using your configured AWS credentials and region. Replace the bucket name with the actual bucket.

Step 3: Calculate the cutoff date

cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

If today is October 9 and days = 30, the cutoff is September 9.

Objects last modified before the cutoff are candidates for deletion.

Step 4: List objects using a paginator

paginator = s3.get_paginator("list_objects_v2")

for page in paginator.paginate(Bucket=bucket_name):

S3 returns objects in pages, so the paginator lets you process buckets containing more objects than a single API response can return.

Step 5: Check the object's age

for obj in page.get("Contents", []):
    if obj["LastModified"] < cutoff_date:

Contents contains the objects in that page.

LastModified gives the object's last-modified timestamp.

If it is earlier than the cutoff, the object qualifies for deletion.

Using .get("Contents", []) safely handles an empty bucket or a page with no objects.

Step 6: Delete the object

s3.delete_object(
    Bucket=bucket_name,
    Key=obj["Key"]
)

This requests deletion of the matching S3 object.

3. What should you say in the interview?

"I would use Python's boto3 SDK to connect to AWS S3. First, I calculate a cutoff timestamp using the current UTC time minus N days. Then I use the list_objects_v2 paginator to iterate through all objects in the bucket. For each object, I compare its LastModified timestamp with the cutoff. If the object is older than N days, I delete it using delete_object. I use pagination to handle large buckets and UTC-aware timestamps to avoid timezone comparison issues."

4. Common DevOps interview follow-ups


Interview question	Answer
Why use boto3?	                 Python SDK for AWS services.
Why use a paginator?	         To process all objects across multiple API pages.
Why use UTC?	             T   To compare timezone-aware timestamps consistently.
What if the bucket is empty?	 page.get("Contents", []) handles missing object lists.
What permissions are required?	 Typically s3:ListBucket and s3:DeleteObject on the relevant bucket and objects.
How can this be automated?	     Schedule a script with cron, or run it through EventBridge and Lambda.


5. Important production best practice

Before running deletion code against a real bucket, perform a dry run: print the keys that would be deleted without calling delete_object. Verify the candidates, then enable deletion. Also check S3 versioning and retention policies, because deleting a versioned object may create a delete marker rather than permanently removing all stored versions.

Memory trick for the interview:

Connect → Calculate cutoff → List with paginator → Compare LastModified → Delete


****************************************************************


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


Explain it in 4 points

boto3.client("s3") connects to AWS S3.

cutoff calculates the timestamp 30 days ago.

The paginator lists all objects, including across multiple pages.

LastModified checks the object's age; delete_object() deletes objects older than 30 days.

Interview tip: Remember the logic: Connect → Calculate cutoff → List objects → Compare dates → Delete.

Use a test bucket or dry run before deleting real production data.

*********************************************************************************