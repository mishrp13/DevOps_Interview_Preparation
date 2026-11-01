resource "aws_eip" "nat" {
  for_each = toset(local.nat_azs)

  domain = "vpc"

  tags = {
    Name = "nat-eip-${each.key}"
  }
}

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

resource "aws_route_table" "private" {
  for_each = local.subnet_map

  vpc_id = aws_vpc.main.id

  tags = {
    Name = "private-route-${each.key}"
  }
}

resource "aws_route" "private_nat" {
  for_each = local.subnet_map

  route_table_id         = aws_route_table.private[each.key].id
  destination_cidr_block = "0.0.0.0/0"

  nat_gateway_id = aws_nat_gateway.nat[
    var.single_nat ? local.azs[0] : each.key
  ].id
}

resource "aws_route_table_association" "private" {
  for_each = aws_subnet.private

  subnet_id      = each.value.id
  route_table_id = aws_route_table.private[each.key].id
}