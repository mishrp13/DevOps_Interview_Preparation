import boto3
import csv
from botocore.exceptions import ClientError


def find_unused_resources(region):
    ec2 = boto3.client("ec2", region_name=region)
    resources = []

    try:
        # Find unattached EBS volumes
        paginator = ec2.get_paginator("describe_volumes")

        for page in paginator.paginate(
            Filters=[{"Name": "status", "Values": ["available"]}]
        ):
            for volume in page["Volumes"]:
                resources.append({
                    "type": "EBS",
                    "id": volume["VolumeId"],
                    "region": region,
                    "size_gb": volume["Size"]
                })

        # Find unused Elastic IPs
        paginator = ec2.get_paginator("describe_addresses")

        for page in paginator.paginate():
            for address in page["Addresses"]:
                if "AssociationId" not in address:
                    resources.append({
                        "type": "Elastic IP",
                        "id": address["PublicIp"],
                        "region": region,
                        "size_gb": ""
                    })

        return resources

    except ClientError as e:
        print(f"AWS API error: {e}")
        return []


def generate_report(resources):
    with open("unused_resources.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["type", "id", "region", "size_gb"]
        )

        writer.writeheader()
        writer.writerows(resources)


if __name__ == "__main__":
    region = "us-east-1"

    resources = find_unused_resources(region)

    for resource in resources:
        print(resource)

    generate_report(resources)

    print(f"\nFound {len(resources)} unused resources.")