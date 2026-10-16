```

Drill 1: Provider and remote backend
Task: Pin Terraform and the AWS provider with required_version and required_providers. Configure an S3 backend with encryption and state locking (DynamoDB table, or use_lockfile on newer Terraform versions). Add default_tags on the provider.
Key constructs: terraform {}, backend "s3", provider "aws" { default_tags {} }.
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "my-tf-state"
    key            = "dev/network/terraform.tfstate"
    region         = "ap-south-1"
    encrypt        = true
    dynamodb_table = "tf-locks"
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = { Project = var.project, Env = var.env, ManagedBy = "terraform" }
  }
}
Follow-ups: Why lock state? What if two people apply at once? How do you bootstrap the backend bucket itself?