# =============================================================================
# HashiCorp Terraform Main Architecture Configuration
# Enterprise Student Record & Academic Management Platform (SU_DevOps)
# Provisions AWS VPC, Internet Gateway, Subnet, Security Group, EC2 & S3
# =============================================================================

terraform {
  required_version = ">= 1.7.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
      Platform    = "StudentAcademicManagement"
    }
  }
}

# -----------------------------------------------------------------------------
# 1. Virtual Private Cloud (VPC) & Networking Fabric
# -----------------------------------------------------------------------------
resource "aws_vpc" "student_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_internet_gateway" "student_igw" {
  vpc_id = aws_vpc.student_vpc.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_subnet" "student_public_subnet" {
  vpc_id                  = aws_vpc.student_vpc.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = var.availability_zone
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-subnet"
    Tier = "Public"
  }
}

resource "aws_route_table" "student_public_rt" {
  vpc_id = aws_vpc.student_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.student_igw.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

resource "aws_route_table_association" "student_public_assoc" {
  subnet_id      = aws_subnet.student_public_subnet.id
  route_table_id = aws_route_table.student_public_rt.id
}

# -----------------------------------------------------------------------------
# 2. Stateful Security Group (Virtual Firewall)
# -----------------------------------------------------------------------------
resource "aws_security_group" "student_sg" {
  name        = "${var.project_name}-web-sg"
  description = "Security firewall permitting SSH, HTTP (Nginx), API (5000), and Alternate (8080)"
  vpc_id      = aws_vpc.student_vpc.id

  # Port 22: OpenSSH Remote Server Administration
  ingress {
    description = "SSH administrative access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 80: Nginx Reverse Proxy Public HTTP Traffic
  ingress {
    description = "HTTP web ingress to Nginx reverse proxy"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 5000: Direct Flask Microservice Application Ingress
  ingress {
    description = "Direct application API access (Flask WSGI container)"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 8080: Alternate Ingress / Automation / Jenkins Controller
  ingress {
    description = "Alternate web and CI/CD proxy port"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound Egress: Unrestricted egress for OS package updates and Docker pulls
  egress {
    description = "Permit all outbound egress traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-security-group"
  }
}

# -----------------------------------------------------------------------------
# 3. Dynamic AMI Discovery (Ubuntu 22.04 LTS Jammy)
# -----------------------------------------------------------------------------
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical official AWS account ID
}

# -----------------------------------------------------------------------------
# 4. EC2 Compute Host for Application & Container Runtime
# -----------------------------------------------------------------------------
resource "aws_instance" "student_server" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.student_public_subnet.id
  vpc_security_group_ids      = [aws_security_group.student_sg.id]
  key_name                    = var.key_name
  associate_public_ip_address = true

  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
    tags = {
      Name = "${var.project_name}-root-ebs"
    }
  }

  # Cloud-init baseline provisioning
  user_data = <<-EOF
              #!/bin/bash
              set -e
              apt-get update -y
              apt-get install -y python3 python3-pip apt-transport-https ca-certificates curl gnupg lsb-release
              echo "Workstation baseline ready for Ansible configuration management" > /tmp/bootstrap.log
              EOF

  tags = {
    Name = "${var.project_name}-ec2-app-host"
    Role = "ApplicationHost"
  }
}

# -----------------------------------------------------------------------------
# 5. Encrypted S3 Bucket for Database Backups & State Artifacts
# -----------------------------------------------------------------------------
resource "aws_s3_bucket" "backup_bucket" {
  bucket_prefix = "su-devops-backup-"
  force_destroy = true

  tags = {
    Name        = "${var.project_name}-backup-store"
    Description = "Persistent storage for SQLite database snapshots and audit archives"
  }
}

resource "aws_s3_bucket_versioning" "backup_versioning" {
  bucket = aws_s3_bucket.backup_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "backup_encryption" {
  bucket = aws_s3_bucket.backup_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
