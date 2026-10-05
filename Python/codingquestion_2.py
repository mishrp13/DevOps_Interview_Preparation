import boto3

ec2 = boto3.client("ec2")

TAG_KEY = "Environment"
DRY_RUN = True


def get_running_instances():
    paginator = ec2.get_paginator("describe_instances")

    for page in paginator.paginate(
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"]
            }
        ]
    ):
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                yield instance


def has_tag(instance, tag_key):
    return any(
        tag["Key"] == tag_key
        for tag in instance.get("Tags", [])
    )


def main():

    instances_to_stop = []

    for instance in get_running_instances():

        instance_id = instance["InstanceId"]

        if not has_tag(instance, TAG_KEY):
            instances_to_stop.append(instance_id)

    print(
        f"Found {len(instances_to_stop)} "
        f"running instances without '{TAG_KEY}' tag."
    )

    for instance_id in instances_to_stop:
        print(instance_id)

    if not instances_to_stop:
        return

    if DRY_RUN:
        print(
            "[DRY RUN] No instances were stopped."
        )
        return

    response = ec2.stop_instances(
        InstanceIds=instances_to_stop
    )

    print("Stop request submitted:")
    print(response)


if __name__ == "__main__":
    main()