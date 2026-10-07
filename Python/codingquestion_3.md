```
3.Find unattached EBS volumes or unused Elastic IPs and report them?

This is a very common AWS + Python automation question for a DevOps interview. The interviewer is usually testing whether you can use Python + Boto3 to identify unused AWS resources and generate a report.

Interview-ready explanation

“I can automate AWS resource cleanup using Python and Boto3. For EBS volumes, I would use the EC2 API to list volumes and identify volumes whose state is available, because an EBS volume in available state is not attached to any EC2 instance. For Elastic IPs, I would check whether the address has an associated instance or network interface. If it is not associated, I consider it unused. I would then generate a report containing the resource ID, region, size, creation details, and estimated cost or other useful metadata. I would normally report first rather than automatically delete, because deletion is a destructive operation.”

1. Finding unattached EBS volumes

An EBS volume can have states such as:

in-use
available

The important one is:

available

It means the EBS volume is not currently attached to an EC2 instance.

For example:

Volume ID       State       Size
vol-123456      in-use      100 GB
vol-789012      available   50 GB   ← Unattached
vol-345678      in-use      200 GB

With Python, we'd use Boto3, AWS's Python SDK.

Example
import boto3

ec2 = boto3.client("ec2", region_name="us-east-1")

response = ec2.describe_volumes(
    Filters=[
        {
            "Name": "status",
            "Values": ["available"]
        }
    ]
)

for volume in response["Volumes"]:
    print(
        volume["VolumeId"],
        volume["Size"],
        volume["AvailabilityZone"]
    )

The important part is:

"Name": "status",
"Values": ["available"]

This asks AWS:

"Give me EBS volumes that are currently unattached."

2. Finding unused Elastic IPs

An Elastic IP is a static public IPv4 address.

You don't want to keep unnecessary Elastic IPs because they can incur charges depending on AWS's current pricing rules.

We can use:

ec2.describe_addresses()

Example:

import boto3

ec2 = boto3.client("ec2", region_name="us-east-1")

response = ec2.describe_addresses()

for address in response["Addresses"]:
    if "AssociationId" not in address:
        print(
            "Unused Elastic IP:",
            address["PublicIp"]
        )

The basic logic is:

Elastic IP
    |
    ├── Associated → In use
    |
    └── No AssociationId → Potentially unused
3. Combining both into one Python script

This is closer to what I'd give in an interview.

import boto3


def find_unused_resources(region):
    ec2 = boto3.client("ec2", region_name=region)

    # Find unattached EBS volumes
    volumes = ec2.describe_volumes(
        Filters=[
            {
                "Name": "status",
                "Values": ["available"]
            }
        ]
    )

    print("Unattached EBS Volumes:")

    for volume in volumes["Volumes"]:
        print(
            f"Volume: {volume['VolumeId']}, "
            f"Size: {volume['Size']} GB, "
            f"AZ: {volume['AvailabilityZone']}"
        )

    # Find unused Elastic IPs
    addresses = ec2.describe_addresses()

    print("\nUnused Elastic IPs:")

    for address in addresses["Addresses"]:
        if "AssociationId" not in address:
            print(
                f"Elastic IP: {address['PublicIp']}"
            )


find_unused_resources("us-east-1")

The output might look like:

Unattached EBS Volumes:

Volume: vol-0123456789abcdef0, Size: 100 GB, AZ: us-east-1a
Volume: vol-0987654321abcdef0, Size: 50 GB, AZ: us-east-1b

Unused Elastic IPs:

Elastic IP: 54.123.45.67
Elastic IP: 18.234.56.78
4. How would you make this production-ready?

This is where you can make your answer stronger in a DevOps interview.

Instead of simply printing the resources, I would generate a report such as:

Resource Type    Resource ID        Region       Size
EBS              vol-123456         us-east-1   100 GB
EBS              vol-789012         us-east-1   50 GB
Elastic IP       54.123.45.67       us-east-1   -

You could write it to CSV:

import csv

with open("unused_resources.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Resource Type",
        "Resource ID",
        "Region",
        "Size"
    ])

    for volume in volumes["Volumes"]:
        writer.writerow([
            "EBS",
            volume["VolumeId"],
            region,
            volume["Size"]
        ])

Then the script could be executed automatically from a Jenkins/GitHub Actions/AWS Lambda/cron job.

5. Important DevOps consideration: Don't immediately delete

This is a very important interview point.

The requirement says:

"Find and report"

not:

"Find and delete."

So I would not automatically delete the resources.

For example, an unattached EBS volume might contain important data and simply be waiting for a future deployment.

A safer workflow is:

Python/Boto3
     ↓
Find unused resources
     ↓
Generate report
     ↓
Send report to team
     ↓
Review/approval
     ↓
Delete after approval

You could also add an age condition:

Unattached EBS
      ↓
Is it unattached?
      ↓
Yes
      ↓
Has it been unattached for > 30 days?
      ↓
Yes
      ↓
Report it

This reduces false positives.

6. What AWS permissions are needed?

The Python script needs IAM permissions to describe these resources.

For EBS:

ec2:DescribeVolumes

For Elastic IPs:

ec2:DescribeAddresses

If you're only reporting, you don't need delete permissions.

That's a good security principle:

Give the automation only the permissions it actually needs.

⭐ Best interview answer

If the interviewer asks:

"How would you find unattached EBS volumes or unused Elastic IPs using Python?"

Say:

“I would use Boto3, the AWS SDK for Python. For EBS, I would call describe_volumes() and filter for volumes with status available, because that indicates the volume is not attached to an EC2 instance. For Elastic IPs, I would call describe_addresses() and identify addresses without an AssociationId. I would collect details such as resource ID, region, size, and creation or allocation information and generate a CSV or other report. I would run this through a scheduled Lambda or CI/CD job and send the report to the team. I would not automatically delete the resources unless there was an approved cleanup policy, because an apparently unused resource may still contain important data.”

Keywords to remember

Python → Boto3 → EC2 API → describe_volumes() → available → describe_addresses() → no AssociationId → report → IAM least privilege → scheduled automation → approval before deletion

That is the kind of answer that demonstrates both Python knowledge and real DevOps thinking.