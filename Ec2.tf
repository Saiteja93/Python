resource "aws_spot_instance_request" "Workstation" {
  ami                    = "ami-1234"
  instance_type          = 
  spot_type              = "Persistent"
  vpc_security_group_ids =
  wait_for_fulfillment   = true


}