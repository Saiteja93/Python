resource "aws_security_group" "allow_all_1" {
  name        = "aallow_all_1"
  description = "Allow all traffic"

  ingress {
    description = "Allow all traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = var.cidr_blocks
  }

  egress {
     from_port  = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = var.cidr_blocks
  }

  tags = {
    Name = "allow_all_1"
    terraform = true
  }
}