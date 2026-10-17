```
•	Designed and provisioned cloud infrastructure using Terraform, following Infrastructure as Code practices for repeatable and scalable environments.


In my project, I used Terraform as an Infrastructure as Code tool to provision and manage AWS infrastructure. The main objective was to make infrastructure provisioning repeatable, consistent, and easier to maintain across environments.

I started by configuring the AWS provider and defining the required infrastructure in Terraform. I provisioned the networking layer, including a VPC, public and private subnets, route tables, internet connectivity, and security groups.

For the compute layer, the infrastructure could use EC2 instances or an EKS cluster, depending on the application's deployment architecture. I also configured the necessary IAM roles and policies following the principle of least privilege.

I organized the Terraform code into separate files for providers, variables, main resources, outputs, and environment-specific configuration. For reusable infrastructure, I used modules so that components such as networking and compute could be managed independently.

My usual workflow was to run `terraform init`, `terraform fmt`, `terraform validate`, and `terraform plan` before applying any changes. I reviewed the plan to understand which resources would be created, modified, or destroyed. After confirming the changes were expected, I ran `terraform apply`.

For state management, I used or would configure a remote S3 backend so the team could share the Terraform state. Where supported by the backend configuration, I enabled state locking to prevent concurrent operations.

I also followed security best practices by keeping credentials and sensitive values out of the Terraform code, using IAM-based access and a secure secrets-management solution where appropriate.

Overall, Terraform helped us standardize infrastructure provisioning, reduce manual configuration, and make infrastructure changes more predictable and maintainable.