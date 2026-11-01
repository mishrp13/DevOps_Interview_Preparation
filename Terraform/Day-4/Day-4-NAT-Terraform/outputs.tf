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