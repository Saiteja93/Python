terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "saiteja-remote-state"
    key            = "python-ec2_teja"
    region         = "us-east-1"
    dynamodb_table = "terraform_lock"
  }
}

provider "aws" {
  region = "us-east-1"
}