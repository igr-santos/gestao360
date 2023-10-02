terraform {
  required_version = ">= 1.0.8"
  required_providers {
    aws = {
      version = ">= 4.15.0"
      source  = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "gestao360" {
  vpc_id      = data.aws_vpc.default.id
  name        = "gestao360"
  description = "Allow all inbound for Postgres"
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "gestao360-db" {
  identifier = "gestao360-db"
  # name                   = "gestao360"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "15.3"
  skip_final_snapshot    = true
  publicly_accessible    = true
  vpc_security_group_ids = [aws_security_group.gestao360.id]
  username               = var.db_user
  password               = var.db_password
}
