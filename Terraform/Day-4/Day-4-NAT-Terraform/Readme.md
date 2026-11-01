```
Day 4 – Terraform: NAT Gateway and Private Routing
Drill 4: Configure NAT Gateway with a single-NAT or multi-AZ option

Today you'll build Terraform infrastructure that allows instances in private subnets to access the internet without exposing them directly to inbound internet traffic.

We'll configure:
1. VPC
2. Two public subnets in different Availability Zones (AZs).
3. Two private subnets in different AZs.
4. Internet Gateway (IGW).
5. Public route table.
6. Elastic IP (EIP).
7. NAT Gateway.
8. Private route tables.
9. single_nat boolean variable to switch between one NAT Gateway and one NAT Gateway per AZ.
We'll also configure the Terraform code so you can switch NAT architecture without rewriting resources.
1. Architecture







stackoverflow.com


There are two possible architectures:

Option A: Single NAT Gateway
- One NAT Gateway in one public subnet.
- Both private subnets use that NAT Gateway.
- Lower cost.
- Single point of failure.
Option B: One NAT Gateway per AZ
- One NAT Gateway in each public subnet.
- Each private subnet uses its NAT Gateway in the same AZ.
- Higher cost.
- Better availability and AZ isolation.
2. Project folder structure
Create a folder named day4-nat-terraform.
day4-nat-terraform/
│
├── provider.tf
├── variables.tf
├── main.tf
├── networking.tf
├── nat.tf
├── outputs.tf
└── terraform.tfvars


3. Complete Terraform code
File 1: provider.tf
This file configures AWS as the cloud provider.
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}


Explanation:
- terraform: Defines Terraform configuration.
- required_version: Requires Terraform 1.5 or newer.
- required_providers: Specifies the AWS provider.
- source: Downloads the official AWS provider.
- version: Uses AWS provider 5.x.
- provider "aws": Configures AWS.
- region: Reads the AWS region from variables.
File 2: variables.tf
This file declares all variables used in the project.
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability Zones"
  type        = list(string)

  default = [
    "ap-south-1a",
    "ap-south-1b"
  ]
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDR blocks"
  type        = list(string)

  default = [
    "10.0.1.0/24",
    "10.0.2.0/24"
  ]
}

variable "private_subnet_cidrs" {
  description = "Private subnet CIDR blocks"
  type        = list(string)

  default = [
    "10.0.11.0/24",
    "10.0.12.0/24"
  ]
}

variable "single_nat" {
  description = "Use one NAT Gateway for the whole VPC"
  type        = bool
  default     = true
}


Important variable:
variable "single_nat" {
  type    = bool
  default = true
}


This variable controls the NAT Gateway architecture.
Value	Architecture
true	One NAT Gateway for the entire VPC
false	One NAT Gateway per Availability Zone

File 3: main.tf
This file creates the VPC and Availability Zone mapping.
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "day4-nat-vpc"
  }
}

locals {
  azs = var.availability_zones

  subnet_map = {
    for index, az in local.azs : az => {
      public_cidr  = var.public_subnet_cidrs[index]
      private_cidr = var.private_subnet_cidrs[index]
    }
  }

  nat_azs = var.single_nat ? [local.azs[0]] : local.azs
}


Explanation:

aws_vpc.main creates our VPC.
enable_dns_support = true
enable_dns_hostnames = true


Enables DNS resolution and DNS hostnames inside the VPC.

Understanding locals:
locals {
  azs = var.availability_zones
}


Stores the Availability Zone list in a local variable.
nat_azs = var.single_nat ? [local.azs[0]] : local.azs


This is the most important conditional expression.

It means:
- If single_nat = true, select only the first AZ.
- If single_nat = false, select all AZs.
For example:
single_nat = true


Result:
nat_azs = ["ap-south-1a"]


But:
single_nat = false


Result:
nat_azs = [
  "ap-south-1a",
  "ap-south-1b"
]


File 4: networking.tf
This file creates public and private subnets, an Internet Gateway, and route tables.

A. Public subnets
resource "aws_subnet" "public" {
  for_each = local.subnet_map

  vpc_id                  = aws_vpc.main.id
  availability_zone       = each.key
  cidr_block              = each.value.public_cidr
  map_public_ip_on_launch = true

  tags = {
    Name = "public-${each.key}"
    Tier = "Public"
  }
}


Explanation:
- for_each: Creates one public subnet per AZ.
- each.key: Gets the AZ name.
- each.value.public_cidr: Gets that AZ's public subnet CIDR.
- map_public_ip_on_launch: Automatically assigns public IPv4 addresses to newly launched instances.
B. Private subnets
resource "aws_subnet" "private" {
  for_each = local.subnet_map

  vpc_id                  = aws_vpc.main.id
  availability_zone       = each.key
  cidr_block              = each.value.private_cidr
  map_public_ip_on_launch = false

  tags = {
    Name = "private-${each.key}"
    Tier = "Private"
  }
}


Explanation:
- Creates one private subnet per AZ.
- Does not automatically assign public IPv4 addresses.
- These subnets will use NAT Gateway for outbound internet access.
C. Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "day4-igw"
  }
}


The Internet Gateway connects the VPC to the internet.

D. Public route table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "public-route-table"
  }
}


Add a default route:
resource "aws_route" "public_internet" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}


Explanation:

0.0.0.0/0 means all IPv4 destinations.

gateway_id points to the Internet Gateway.

This allows public subnet resources with suitable public IPs and security rules to access the internet.

E. Public route table association
resource "aws_route_table_association" "public" {
  for_each = aws_subnet.public

  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}


Associates the public route table with both public subnets.
File 5: nat.tf
This is the main file for today's drill.

A. Elastic IP
resource "aws_eip" "nat" {
  for_each = toset(local.nat_azs)

  domain = "vpc"

  tags = {
    Name = "nat-eip-${each.key}"
  }
}


Explanation:
- aws_eip: Creates Elastic IP addresses.
- for_each: Creates one EIP for each required NAT Gateway.
- domain = "vpc": Allocates the EIP for use with a VPC.
- Each NAT Gateway receives its own Elastic IP.
B. NAT Gateway
resource "aws_nat_gateway" "nat" {
  for_each = toset(local.nat_azs)

  allocation_id = aws_eip.nat[each.key].id
  subnet_id     = aws_subnet.public[each.key].id

  tags = {
    Name = "nat-${each.key}"
  }

  depends_on = [
    aws_internet_gateway.igw
  ]
}


Explanation:
- aws_nat_gateway: Creates NAT Gateways.
- for_each: Controls how many NAT Gateways are created.
- allocation_id: Attaches the corresponding Elastic IP.
- subnet_id: Places the NAT Gateway in the public subnet of that AZ.
- depends_on: Ensures the Internet Gateway is created before the NAT Gateway.
C. Private route tables
resource "aws_route_table" "private" {
  for_each = local.subnet_map

  vpc_id = aws_vpc.main.id

  tags = {
    Name = "private-route-${each.key}"
  }
}


Creates one private route table per AZ.

D. Private default routes
resource "aws_route" "private_nat" {
  for_each = local.subnet_map

  route_table_id         = aws_route_table.private[each.key].id
  destination_cidr_block = "0.0.0.0/0"

  nat_gateway_id = aws_nat_gateway.nat[
    var.single_nat ? local.azs[0] : each.key
  ].id
}


This is the second most important conditional expression.

Let's understand it.
var.single_nat ? local.azs[0] : each.key


If single_nat = true:

Both private route tables point to the first NAT Gateway.

If single_nat = false:

Each private route table points to its own AZ's NAT Gateway.

Example:
When single_nat = true
One NAT Gateway
Public subnet – AZ A

NAT Gateway A

Private AZ A

Route → NAT A


Private AZ B

Route → NAT A




When single_nat = false
Two NAT Gateways
Public AZ A
NAT Gateway A

Private AZ A

Route → NAT A


Public AZ B
NAT Gateway B

Private AZ B

Route → NAT B




E. Private route table associations
resource "aws_route_table_association" "private" {
  for_each = aws_subnet.private

  subnet_id      = each.value.id
  route_table_id = aws_route_table.private[each.key].id
}


Associates each private subnet with its corresponding private route table.
File 6: outputs.tf
This file displays useful information after deployment.
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = {
    for az, subnet in aws_subnet.public :
    az => subnet.id
  }
}

output "private_subnet_ids" {
  value = {
    for az, subnet in aws_subnet.private :
    az => subnet.id
  }
}

output "nat_gateway_ids" {
  value = {
    for az, nat in aws_nat_gateway.nat :
    az => nat.id
  }
}

output "nat_gateway_public_ips" {
  value = {
    for az, eip in aws_eip.nat :
    az => eip.public_ip
  }
}

output "single_nat_enabled" {
  value = var.single_nat
}


File 7: terraform.tfvars
aws_region = "ap-south-1"

vpc_cidr = "10.0.0.0/16"

availability_zones = [
  "ap-south-1a",
  "ap-south-1b"
]

public_subnet_cidrs = [
  "10.0.1.0/24",
  "10.0.2.0/24"
]

private_subnet_cidrs = [
  "10.0.11.0/24",
  "10.0.12.0/24"
]

single_nat = true


4. Execute the Terraform project
Open your terminal inside day4-nat-terraform.

Step 1: Format the code
terraform fmt -recursive


Formats all Terraform files.

Step 2: Initialize Terraform
terraform init


Downloads the AWS provider.

Step 3: Validate configuration
terraform validate


Checks Terraform syntax and configuration.

Step 4: Preview infrastructure
terraform plan


Review which AWS resources Terraform will create.

Step 5: Deploy infrastructure
terraform apply


Type yes when prompted.

Step 6: Check outputs
terraform output


You should see:
- VPC ID
- Public subnet IDs
- Private subnet IDs
- NAT Gateway IDs
- NAT Gateway public IPs
5. Test the single_nat variable
This is an important part of your assignment.

Test A: Single NAT Gateway

In terraform.tfvars:
single_nat = true


Run:
terraform plan
terraform apply


Expected architecture:
Resource	Count
VPC	1
Public subnets	2
Private subnets	2
Internet Gateway	1
Elastic IPs	1
NAT Gateways	1
Private route tables	2

Test B: NAT Gateway per AZ

Change:
single_nat = false


Run:
terraform plan
terraform apply


Expected architecture:
Resource	Count
VPC	1
Public subnets	2
Private subnets	2
Internet Gateway	1
Elastic IPs	2
NAT Gateways	2
Private route tables	2

Terraform will create the second NAT Gateway and EIP and update the private routes.
6. Follow-up interview questions
Q1. What is the cost difference between one NAT Gateway and one NAT Gateway per AZ?
Single NAT Gateway:
- Only one NAT Gateway hourly charge.
- Lower data-processing charges overall if traffic is low.
- Cross-AZ data transfer charges can occur when another AZ uses that NAT Gateway.
- Less infrastructure cost.
One NAT Gateway per AZ:
- Each NAT Gateway has its own hourly charge.
- Each NAT Gateway has data-processing charges.
- Avoids cross-AZ NAT traffic when each private subnet uses its local NAT.
- Better availability and AZ isolation.
Remember that NAT Gateway pricing depends on region and data usage. Public IPv4 address charges may also apply.
Q2. What happens if a single NAT Gateway fails?
Imagine this architecture:
Private AZ A ──┐
               │
               ├── NAT Gateway A
               │
Private AZ B ──┘


Suppose NAT Gateway A becomes unavailable.

Result:
1. Private AZ A loses outbound internet connectivity.
2. Private AZ B also loses outbound internet connectivity.
3. Applications cannot reach external APIs or download updates through that NAT.
4. Incoming connections to private instances are not automatically affected by this NAT failure.
A NAT Gateway is an Availability Zone-scoped resource. A single-NAT architecture therefore creates an AZ-level dependency.
Q3. Does NAT Gateway allow inbound internet traffic?
No.

NAT Gateway primarily allows resources in private subnets to initiate outbound connections to the internet.

For example:
Private EC2 → NAT Gateway → Internet


The response traffic can return through the established connection.

But an internet user cannot directly initiate a connection to your private EC2 instance through the NAT Gateway.
Q4. Why do we need an Elastic IP for NAT Gateway?
The NAT Gateway requires an Elastic IP address for internet-facing communication.

The EIP provides a stable public IPv4 address for outbound connections.
Q5. Why do we use 0.0.0.0/0?
destination_cidr_block = "0.0.0.0/0"


It represents all IPv4 destinations.

In a private route table, we use it to send internet-bound traffic to the NAT Gateway.

7. Important cleanup
NAT Gateways incur charges while they exist, even when you aren't actively using them.

After completing your practice:
terraform destroy


Type yes to confirm.

This removes the resources managed by this Terraform configuration.
Day 4 assignment complete
8. What you should be able to explain after Day 4
- [ ] Difference between public and private subnets.
- [ ] Purpose of Internet Gateway.
- [ ] Purpose of Elastic IP.
- [ ] How NAT Gateway works.
- [ ] Why NAT Gateway must be in a public subnet.
- [ ] How private route tables use 0.0.0.0/0.
- [ ] How Terraform for_each works.
- [ ] How conditional expressions work.
- [ ] Difference between single NAT and multi-AZ NAT.
- [ ] Cost and availability trade-offs.
One practical interview challenge: Deploy this infrastructure with single_nat = true, then change it to false. Explain exactly which resources Terraform creates, retains, and updates.

That will demonstrate that you understand both Terraform resource lifecycle and AWS networking—not just Terraform syntax.