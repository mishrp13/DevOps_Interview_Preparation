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