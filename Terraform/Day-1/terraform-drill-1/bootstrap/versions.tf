
terraform {
  required_version = ">= 1.10.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}



# Understand each line:
# - required_version: Terraform CLI must be at least 1.10.0 and below 2.0.0.
# - required_providers: Declares external plugins Terraform needs.
# - source = "hashicorp/aws": Downloads the official AWS provider from the Terraform Registry.
# - version = "~> 5.0": Accepts AWS provider 5.x versions, but not 6.x.
# For stricter reproducibility, you can pin an exact tested
#provider version and commit .terraform.lock.hcl. 
#The ~> constraint allows compatible updates; it is not an exact pin.