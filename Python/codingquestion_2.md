```

List all EC2 instances without a specific tag and stop them

Absolutely. If the interviewer asks this specifically in a DevOps + Python interview, they are likely testing whether you can combine Python automation + AWS SDK (boto3) + EC2 APIs + safe operational practices.

The key is: don't just write Python that stops instances. Show that you know how to make destructive automation safe.

1. Interview question

“Write a Python script to list all EC2 instances that don't have a specific tag and stop them.”

Let's assume the required tag is:

Environment=Production

There are actually two interpretations:

Tag is completely missing
Environment doesn't exist.
Specific tag/value is missing
Instance doesn't have Environment=Production.

Clarify this in an interview. I'll demonstrate missing tag key, because that's the literal interpretation.

2. Python / boto3 solution
import boto3

ec2 = boto3.client("ec2")

TAG_KEY = "Environment"


def get_running_instances():
    paginator = ec2.get_paginator("describe_instances")

    instances = []

    for page in paginator.paginate(
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"]
            }
        ]
    ):
        for reservation in page["Reservations"]:
            instances.extend(reservation["Instances"])

    return instances


def has_tag(instance, tag_key):
    for tag in instance.get("Tags", []):
        if tag["Key"] == tag_key:
            return True

    return False


def main():
    instances = get_running_instances()

    instances_to_stop = []

    for instance in instances:
        instance_id = instance["InstanceId"]

        if not has_tag(instance, TAG_KEY):
            instances_to_stop.append(instance_id)

    print("Instances without required tag:")

    for instance_id in instances_to_stop:
        print(instance_id)

    # Stop only after reviewing the candidates
    if instances_to_stop:
        response = ec2.stop_instances(
            InstanceIds=instances_to_stop
        )

        print("Stop request sent:")
        print(response)


if __name__ == "__main__":
    main()
3. Let's break this down like an interviewer would
Step 1 — Create the EC2 client
import boto3

ec2 = boto3.client("ec2")

boto3 is the AWS SDK for Python.

In production, I wouldn't hardcode AWS credentials.

I'd normally use:

Local development → AWS CLI/profile
EC2              → IAM role
ECS              → Task role
Lambda            → Execution role
GitHub Actions   → OIDC/IAM role
Jenkins           → IAM role/credentials mechanism

That's an important DevOps point.

4. Why use a paginator?

This is a very good interview detail.

You could write:

ec2.describe_instances()

But AWS APIs return results in pages.

For potentially large environments, use:

paginator = ec2.get_paginator("describe_instances")

Then:

for page in paginator.paginate(...):

This allows your script to handle many instances rather than assuming everything comes back in one response.

Interview line

“I'm using the boto3 paginator because DescribeInstances can return paginated results. This makes the script work reliably at scale.”

That's a strong answer.

5. Filtering only running instances

We don't want to stop instances that are already:

stopped
stopping
terminated
pending

So we filter:

Filters=[
    {
        "Name": "instance-state-name",
        "Values": ["running"]
    }
]

This reduces unnecessary API calls and makes the intention clear.

6. Why instance.get("Tags", [])?

This line is important:

for tag in instance.get("Tags", []):

Some EC2 instances might have no tags at all.

If you wrote:

for tag in instance["Tags"]:

you could get:

KeyError: 'Tags'

Using:

instance.get("Tags", [])

means:

Tags exists → use tags
Tags doesn't exist → use empty list

That's a small Python detail that shows practical coding knowledge.

7. Finding the missing tag

This function:

def has_tag(instance, tag_key):
    for tag in instance.get("Tags", []):
        if tag["Key"] == tag_key:
            return True

    return False

checks whether:

Environment

exists.

If not:

if not has_tag(instance, TAG_KEY):

we add the instance to:

instances_to_stop
8. But I would NOT immediately stop instances

This is where you can differentiate yourself in a DevOps interview.

Instead of:

ec2.stop_instances(
    InstanceIds=instances_to_stop
)

I'd initially run the script in dry-run mode:

DRY_RUN = True

Then:

if instances_to_stop:
    if DRY_RUN:
        print(
            f"[DRY RUN] Would stop: {instances_to_stop}"
        )
    else:
        ec2.stop_instances(
            InstanceIds=instances_to_stop
        )

Full safer version:

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
9. Why I like this version for an interview

It demonstrates several things:

                 Python
                   │
        ┌──────────┴──────────┐
        │                     │
     boto3                 functions
        │                     │
        ▼                     ▼
 DescribeInstances       has_tag()
        │
        ▼
    pagination
        │
        ▼
 running instances
        │
        ▼
   inspect tags
        │
        ▼
 missing tag
        │
        ▼
   DRY RUN
        │
        ▼
 stop_instances()

You're demonstrating more than AWS syntax.

10. What if they mean Environment=Production?

This is a very likely follow-up.

Suppose the requirement is:

Stop instances that don't have Environment=Production.

Then check both key and value:

def has_required_tag(instance, key, value):
    return any(
        tag["Key"] == key and tag["Value"] == value
        for tag in instance.get("Tags", [])
    )

Then:

if not has_required_tag(
    instance,
    "Environment",
    "Production"
):
    instances_to_stop.append(
        instance["InstanceId"]
    )

So:

Environment=Production   → SKIP
Environment=Dev          → STOP candidate
Environment=Test         → STOP candidate
No Environment tag       → STOP candidate

Again, I'd clarify the requirement before implementing destructive automation.

11. What about DoNotStop=true?

This is where I'd show production thinking.

Suppose someone forgot to tag:

database-prod-01

Your script could shut down production.

So I might implement:

Required tag:
Environment

Exception tag:
DoNotStop=true

Logic:

if (
    not has_required_tag(instance, "Environment", "Production")
    and not has_required_tag(instance, "DoNotStop", "true")
):
    instances_to_stop.append(instance["InstanceId"])

Conceptually:

                  Running EC2
                       │
                       ▼
             Environment tag?
                 /         \
               YES          NO
                │            │
               SKIP          ▼
                       DoNotStop=true?
                          /       \
                        YES       NO
                         │         │
                        SKIP      STOP
12. Another important DevOps question: IAM

The Python code doesn't magically get AWS access.

I'd use an IAM role with permissions such as:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:StopInstances"
      ],
      "Resource": "*"
    }
  ]
}

In an interview, say:

“I wouldn't hardcode AWS access keys in the Python script. I'd use IAM roles wherever possible and grant only the permissions required by the automation.”

That's a very important DevOps answer.

13. What if there are 1,000 EC2 instances?

The interviewer may ask:

“Will your script scale?”

Your answer:

“I'm using the boto3 paginator for DescribeInstances, so I don't assume all instances fit in one API response. I'd also avoid making a separate AWS API call for every instance just to retrieve tags because DescribeInstances already returns tags when available. That reduces API calls.”

That's actually a better implementation detail than the earlier describe-tags approach.

14. What if stop_instances() fails?

In production, I'd add:

try:
    response = ec2.stop_instances(
        InstanceIds=instances_to_stop
    )
except Exception as e:
    print(f"Failed to stop instances: {e}")

For a real production automation, I'd go further:

structured logging
retries/backoff for transient AWS errors
CloudWatch logs
alerting
audit trail
idempotency
exception handling
IAM least privilege
15. Where would you run this?

Another common DevOps follow-up:

“How would you automate this?”

I'd say:

Option 1 — Lambda
EventBridge
     │
     │ schedule
     ▼
 Lambda
     │
     ▼
  boto3
     │
     ▼
   EC2

Good for relatively simple scheduled automation.

Option 2 — Jenkins/GitHub Actions
Scheduled pipeline
       │
       ▼
Python script
       │
       ▼
AWS IAM/OIDC
       │
       ▼
EC2

Useful if your organization already has CI/CD infrastructure.

Option 3 — AWS Systems Manager

For larger AWS environments, I'd also consider Systems Manager automation/runbooks.

16. The answer I'd actually give in the interview

If they ask you this question, don't start coding immediately.

Start with:

“Before implementing this, I would clarify whether you mean instances missing the tag key entirely, or instances that don't have a specific key-value pair. Assuming you mean instances without the Environment tag, I'll retrieve only running instances using boto3, paginate through the response, inspect the tags, generate a candidate list, and use a dry-run before stopping anything.”

Then show the Python.

After the code, say:

“For production I'd add safeguards such as a DoNotStop=true exception tag, IAM least privilege, logging and alerting. I'd also run this as a scheduled Lambda triggered by EventBridge rather than from someone's machine.”

⭐ That's the DevOps-level thought process
Python knowledge
      +
boto3 knowledge
      +
AWS EC2 knowledge
      +
IAM
      +
pagination
      +
error handling
      +
dry-run
      +
safety controls
      +
automation
      =
Strong DevOps interview answer

One-liner to remember:

“Discover → Filter → Validate → Dry-run → Act → Log → Alert.”

That's the pattern you can reuse for almost any Python + AWS automation interview question.