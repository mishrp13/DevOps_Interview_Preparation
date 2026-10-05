```
•Users vs groups vs roles vs policies. When do you use a role instead of a user?

Absolutely. For an AWS DevOps interview, think of these four IAM concepts as layers:

1. User — “Who is this individual?”

An IAM user represents a specific person or long-lived application identity.

Example:

alice
bob
jenkins-user

A user can have credentials such as access keys or a console password.

Interview answer:

“I use an IAM user when I need a specific identity, typically for a human user, although for workloads I prefer roles whenever possible.”

2. Group — “Which users belong together?”

A group is a collection of IAM users.

For example:

Developers
 ├── Alice
 ├── Bob
 └── Charlie

You attach permissions to the group, rather than individually configuring every developer.

Example:

Developers group
       ↓
Read-only access to S3
       ↓
Alice, Bob, Charlie

This makes permission management easier.

3. Policy — “What are they allowed to do?”

A policy is a JSON document defining permissions.

For example:

{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::my-bucket/*"
}

It says:

This identity can read objects from this S3 bucket.

So:

User / Group / Role → Policy → Permissions

4. Role — “Who/what can temporarily assume this identity?”

This is the most important one for a DevOps interview.

An IAM role is an identity with permissions that can be assumed temporarily by:

EC2
ECS tasks
Lambda
EKS workloads
GitHub Actions
another AWS account
IAM users

For example:

EC2 instance
     ↓
assumes
     ↓
S3-Read-Role
     ↓
S3 GetObject

The EC2 instance doesn't need an AWS access key stored on the server.

When do you use a Role instead of a User?

This is a very common interview question.

❌ Bad DevOps approach

Suppose you have an EC2 server that needs to upload files to S3.

You create:

IAM user: ec2-s3-user
Access Key
Secret Key
       ↓
stored on EC2
       ↓
S3

This creates a credential-management problem.

If the keys leak, someone can potentially use them outside the EC2 instance.

✅ Better approach

Create:

EC2
 ↓
IAM Role
 ↓
S3 permissions

Attach the role to the EC2 instance.

AWS provides temporary credentials to the instance through the instance metadata service.

So there is no long-lived access key sitting in your application/server.

The interview rule of thumb

Remember this:

| Situation                            | Prefer                     |
| ------------------------------------ | -------------------------- |
| Specific human identity              | User                       |
| Multiple users with same permissions | Group                      |
| Define permissions                   | Policy                     |
| AWS service needs permissions        | **Role**                   |
| EC2 needs S3 access                  | **Role**                   |
| Lambda needs DynamoDB access         | **Role**                   |
| ECS task needs AWS access            | **Role**                   |
| EKS workload needs AWS access        | **Role**                   |
| GitHub Actions deploys to AWS        | **Role / OIDC federation** |
| Cross-account access                 | **Role**                   |
| Temporary access                     | **Role**                   |

A strong interview answer

If the interviewer asks:

“When would you use an IAM role instead of an IAM user?”

You can say:

“I use an IAM role when an AWS service, workload, or external identity needs access to AWS resources. Roles provide temporary credentials and avoid storing long-lived access keys. For example, if an EC2 instance needs to read from S3, I would attach an IAM role to the EC2 instance rather than creating an IAM user and storing access keys on the server. I would also use roles for cross-account access and CI/CD systems such as GitHub Actions.”

That's a very solid DevOps-level answer.

One mental model to remember
USER
  │
  ├── belongs to → GROUP
  │                 │
  │                 └── has → POLICY
  │
  └── can assume → ROLE
                       │
                       └── has → POLICY

The key distinction is:

User = identity you create and manage.
Role = identity that can be assumed temporarily.
Policy = permissions.
Group = way to organize users and attach common permissions.

For modern AWS DevOps, “prefer roles and temporary credentials over long-lived IAM user access keys” is an excellent principle to mention.