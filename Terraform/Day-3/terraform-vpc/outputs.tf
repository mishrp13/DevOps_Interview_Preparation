output "vpc_id" {
  value = aws_vpc.this.id
}

output "availability_zones" {
  value = local.azs
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

output "public_subnet_cidrs" {
  value = {
    for az, subnet in aws_subnet.public :
    az => subnet.cidr_block
  }
}

output "private_subnet_cidrs" {
  value = {
    for az, subnet in aws_subnet.private :
    az => subnet.cidr_block
  }
}

output "internet_gateway_id" {
  value = aws_internet_gateway.this.id
}