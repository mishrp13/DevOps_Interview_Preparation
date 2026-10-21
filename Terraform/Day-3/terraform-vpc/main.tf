data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  azs = slice(
    data.aws_availability_zones.available.names,
    0,
    2
  )
}

resource "aws_vpc" "this" {
  cidr_block = var.vpc_cidr

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "drill3-vpc"
  }
}

resource "aws_subnet" "public" {
  for_each = {
    for i, az in local.azs : az => i
  }

  vpc_id            = aws_vpc.this.id
  availability_zone = each.key

  cidr_block = cidrsubnet(
    var.vpc_cidr,
    8,
    each.value
  )

  map_public_ip_on_launch = true

  tags = {
    Name = "public-${each.key}"
    Type = "Public"
  }
}

resource "aws_subnet" "private" {
  for_each = {
    for i, az in local.azs : az => i
  }

  vpc_id            = aws_vpc.this.id
  availability_zone = each.key

  cidr_block = cidrsubnet(
    var.vpc_cidr,
    8,
    each.value + 10
  )

  map_public_ip_on_launch = false

  tags = {
    Name = "private-${each.key}"
    Type = "Private"
  }
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "drill3-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }

  tags = {
    Name = "public-route-table"
  }
}

resource "aws_route_table_association" "public" {
  for_each = aws_subnet.public

  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}