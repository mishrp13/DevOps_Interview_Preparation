```

- Developed and deployed **Python-based AWS automation using Boto3 and AWS Lambda** to identify running EC2 instances missing mandatory `Environment` tags, improving resource governance and compliance.
- Automated monthly EC2 resource checks using **scheduled Lambda execution**, implementing pagination, tag validation, and dry-run safeguards to support cloud cost optimization and reduce manual intervention.

You can explain this project in an interview as a real-time AWS automation use case involving Python, Boto3, EC2, Lambda, IAM, and EventBridge.

I'll explain it in the same order an interviewer would expect: business requirement, script development, Lambda deployment, scheduling, testing, and challenges.

-----------------------------------------------------------------------------------------------------
1. Interview answer: Explain your project (2–3 minutes)
In my company, we had a requirement to identify running EC2 instances that were missing the mandatory Environment tag.
Manually checking EC2 instances was time-consuming, so I developed a Python automation script using the Boto3 SDK.
First, I created an EC2 client using Boto3 and used the describe_instances API with a filter to retrieve only running instances.
I implemented pagination because AWS can return instance information across multiple pages.
Then I iterated through each EC2 instance and checked whether the Environment tag existed. If the tag was missing, I added that instance ID to a list.
I also implemented a dry-run flag to prevent accidental shutdowns during testing.
After developing and testing the script, I deployed it as an AWS Lambda function. I configured the Lambda execution role with the required IAM permissions and used Amazon EventBridge to trigger the function once every month.
I monitored execution results and errors using Amazon CloudWatch Logs.
This automation helped us reduce manual EC2 resource checks and improve tagging compliance. The script also supported stopping non-compliant instances when dry-run mode was disabled.

Use the CloudWatch monitoring and stopping statements only if those steps were actually part of your implementation.

2. How you developed the Python script
You can explain the code in five steps.

Step 1: Create the EC2 client

import boto3
ec2 = boto3.client("ec2")
Boto3 is the AWS SDK for Python. It allows the script to communicate with AWS services through API calls.

Step 2: Retrieve running EC2 instances
paginator = ec2.get_paginator("describe_instances")

I used the instance-state-name filter with running so the script processes only running instances. Pagination ensures it can handle multiple pages of results.

Step 3: Validate the Environment tag
if not has_tag(instance, TAG_KEY):    instances_to_stop.append(instance_id)
I checked the tags on every running instance and collected IDs where the Environment tag key was missing.

Step 4: Implement the safety check
if DRY_RUN:    
print("[DRY RUN] No instances were stopped.")    
return

With DRY_RUN = True, the script only reports matching instances and does not stop them.

Step 5: Stop instances when enabled
ec2.stop_instances(    InstanceIds=instances_to_stop)

When dry run is disabled, the script requests AWS to stop the collected EC2 instances.

-------------------------------------------------------------------------------------

3. How you deployed and executed the script through Lambda
This is the most important part for your interview.
Automation architecture
Amazon EventBridge
(Monthly scheduled trigger)

AWS Lambda

Python script + Boto3

Amazon EC2

List running instances and validate tags

Dry-run / Stop decision

Report or request instance shutdown

CloudWatch Logs

Execution logs and errors


Step A: Create the Lambda function
In AWS Console:
1. Open AWS Lambda → Create function.
2. Select Author from scratch.
3. Enter a function name, such as ec2-tag-compliance-check.
4. Select Python runtime.
5. Configure an execution role with the required IAM permissions.
6. Paste or upload the Python script.
Step B: Configure the Lambda handler
Your existing script contains:
if __name__ == "__main__":  
  main()

This works when running the script directly, but Lambda needs a handler.
Add:

def lambda_handler(event, context):
    main()
    return {
        "statusCode": 200,
        "body": "EC2 tag compliance check completed"
    }



If your Python file is named lambda_function.py, configure the handler as:
lambda_function.lambda_handler

Lambda calls lambda_handler(), which then calls your existing main() function.

Step C: Configure IAM permissions
The Lambda execution role needs permission to describe instances and, if stopping is enabled, stop them.
Example IAM policy for demonstration:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:DescribeInstances",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "ec2:StopInstances",
      "Resource": "*"
    }
  ]
}



For production, restrict ec2:StopInstances to the intended resources and conditions. The execution role also needs CloudWatch Logs permissions if you're using CloudWatch logging.
-----------------------------------------------------------------------------------------

Step D: Schedule monthly execution
In Amazon EventBridge, create a schedule to invoke your Lambda function.
For example, to run on the first day of every month at 2:00 AM UTC:
cron(0 2 1 * ? *)


This schedule runs automatically once a month. With EventBridge Scheduler, configure the target Lambda function and an invocation role; for an EventBridge scheduled rule, configure the Lambda target and its resource-based invocation permission.

Step E: Test and monitor
I would explain testing like this:
I initially kept DRY_RUN = True and manually invoked the Lambda function with a test event. I verified the identified EC2 instance IDs and execution results in CloudWatch Logs. After validating the behavior, the monthly schedule could execute the same function automatically.

4. Common interview questions and answers
1. Why did you use AWS Lambda instead of an EC2 server?
Lambda is serverless, so I don't need to maintain a dedicated server. Since the script runs only once a month, Lambda is a suitable option for scheduled automation.

2. Why did you use Boto3?
Boto3 is the AWS SDK for Python. It lets me interact with EC2 programmatically, retrieve instance details, inspect tags, and call the StopInstances API.

3. Why did you implement pagination?
DescribeInstances can return multiple pages of results. Pagination ensures the script processes all returned instances rather than only the first page.

4. How does Lambda authenticate to AWS?
Lambda uses temporary credentials provided through its IAM execution role. I don't need to hardcode access keys in the Python script.
5. What happens if an instance has an Environment tag with an empty value?
My current function checks only whether the tag key exists. Even an empty Environment tag value would pass. If we need to validate values, I would extend the function to check the tag value as well.

6. What happens if Lambda fails?
The error can be investigated using CloudWatch Logs. For better production reliability, I could configure failure notifications, alarms, and appropriate retry handling.
7. Does DRY_RUN = True use AWS's native dry-run API?
No. It is a custom Python safety flag. When True, the script returns before calling StopInstances. AWS also has a separate DryRun API parameter.
8. Does the script check all AWS regions?
No. It checks the region configured for the Boto3 EC2 client. To cover multiple regions, I would list the required regions and create a client for each.

5. Final 60-second interview answer to practice
I worked on an AWS EC2 automation task where the requirement was to identify running instances that were missing the mandatory Environment tag.
I developed a Python script using Boto3. It uses the DescribeInstances API with pagination to retrieve running EC2 instances, validates their tags, and collects instance IDs that are missing the Environment tag.
I implemented a dry-run mechanism to prevent accidental shutdowns. The script also supports stopping the identified instances when dry-run mode is disabled.
For automation, I deployed the script as an AWS Lambda function, configured the required IAM execution role, and scheduled it to run monthly using Amazon EventBridge. I used CloudWatch Logs to verify the execution results.
This reduced the need for manual EC2 checks and helped improve resource tagging compliance and cloud cost governance.

One important interview distinction: Your script with DRY_RUN = True only identifies instances; it doesn't stop them or directly save EC2 compute costs. Claim actual automated shutdowns or measured cost savings only if those occurred in your company.
If you can confidently explain Boto3 → EC2 API → tag validation → Lambda handler → IAM role → EventBridge schedule → CloudWatch Logs, you'll be well prepared to discuss this project in a DevOps interview.

