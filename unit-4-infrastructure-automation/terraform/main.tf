# =============================================================================
# HashiCorp Terraform Main Architecture Configuration
# Project: Enterprise Student Record & Smart Library Platform (SU_DevOps)
# Student Lead: Shivraj Dhumal (PRN: 2125UMLM1008) - Sandip University
# Provisions AWS VPC, Subnet, IGW, Route Table, SG, EC2 & Encrypted S3
# =============================================================================

terraform {
  required_version = ">= 1.7.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.100.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      Lead        = "Shivraj Dhumal (2125UMLM1008)"
      Institution = "Sandip University"
      ManagedBy   = "Terraform"
    }
  }
}

# -----------------------------------------------------------------------------
# 1. AWS Account Context & AMI SSM Parameter Discovery
# -----------------------------------------------------------------------------
data "aws_caller_identity" "current" {}

data "aws_ssm_parameter" "ubuntu_ami" {
  name = "/aws/service/canonical/ubuntu/server/22.04/stable/current/amd64/hvm/ebs-gp2/ami-id"
}

# -----------------------------------------------------------------------------
# 2. Virtual Private Cloud (VPC) & Networking Fabric
# -----------------------------------------------------------------------------
resource "aws_vpc" "library_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "library_vpc"
  }
}

resource "aws_internet_gateway" "library_igw" {
  vpc_id = aws_vpc.library_vpc.id

  tags = {
    Name = "library_igw"
  }
}

resource "aws_subnet" "library_subnet" {
  vpc_id                  = aws_vpc.library_vpc.id
  cidr_block              = var.subnet_cidr
  availability_zone       = var.availability_zone
  map_public_ip_on_launch = true

  tags = {
    Name = "library_subnet"
    Tier = "Public"
  }
}

resource "aws_route_table" "library_route_table" {
  vpc_id = aws_vpc.library_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.library_igw.id
  }

  tags = {
    Name = "library_route_table"
  }
}

resource "aws_route_table_association" "library_route_assoc" {
  subnet_id      = aws_subnet.library_subnet.id
  route_table_id = aws_route_table.library_route_table.id
}

# -----------------------------------------------------------------------------
# 3. Stateful Security Group (library_sg)
# -----------------------------------------------------------------------------
resource "aws_security_group" "library_sg" {
  name        = "library_sg"
  description = "Security firewall permitting SSH, HTTP (Nginx), Application (5000), and Alternate (8080)"
  vpc_id      = aws_vpc.library_vpc.id

  # Port 22: OpenSSH Remote Server Administration
  ingress {
    description = "SSH administrative access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 80: Nginx Reverse Proxy Public Web Ingress
  ingress {
    description = "HTTP web ingress to Nginx reverse proxy"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 5000: Direct Application API Ingress
  ingress {
    description = "Direct application access (Flask WSGI container)"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 8080: Alternate Web & CI/CD Proxy Ingress
  ingress {
    description = "Alternate web and CI/CD proxy port"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound Egress: Unrestricted for Ubuntu updates & Docker image pulls
  egress {
    description = "Permit all outbound egress traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "library_sg"
  }
}

# -----------------------------------------------------------------------------
# 4. EC2 Compute Host (library_server)
# -----------------------------------------------------------------------------
resource "aws_instance" "library_server" {
  ami                         = data.aws_ssm_parameter.ubuntu_ami.value
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.library_subnet.id
  vpc_security_group_ids      = [aws_security_group.library_sg.id]
  key_name                    = var.key_name
  associate_public_ip_address = true

  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
    tags = {
      Name = "library_server_root_ebs"
    }
  }

  user_data = <<-EOF
              #!/bin/bash
              set -e
              apt-get update -y
              apt-get install -y python3 python3-pip apt-transport-https ca-certificates curl gnupg lsb-release
              echo "Server baseline ready for Ansible configuration" > /tmp/bootstrap.log
              EOF

  tags = {
    Name = "library_server"
    Role = "ApplicationHost"
  }
}

# -----------------------------------------------------------------------------
# 5. Encrypted S3 Bucket for Database Backups & State Artifacts
# -----------------------------------------------------------------------------
resource "aws_s3_bucket" "library_backup" {
  bucket        = var.s3_backup_bucket_name
  force_destroy = true

  tags = {
    Name        = var.s3_backup_bucket_name
    Description = "Encrypted storage for SQLite database backups (library.db)"
  }
}

resource "aws_s3_bucket_versioning" "library_backup_versioning" {
  bucket = aws_s3_bucket.library_backup.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "library_backup_encryption" {
  bucket = aws_s3_bucket.library_backup.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = false
  }
}
