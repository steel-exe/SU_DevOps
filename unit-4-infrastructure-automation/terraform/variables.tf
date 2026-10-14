# =============================================================================
# Terraform Input Variables Specification
# Project: Enterprise Student Record & Smart Library Platform (SU_DevOps)
# Student Lead: Shivraj Dhumal (PRN: 2125UMLM1008) - Sandip University
# =============================================================================

variable "aws_region" {
  type        = string
  description = "Target AWS deployment region"
  default     = "us-east-1"
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the dedicated VPC (library_vpc)"
  default     = "10.1.0.0/16"
}

variable "subnet_cidr" {
  type        = string
  description = "CIDR block for the public subnet (library_subnet)"
  default     = "10.1.1.0/24"
}

variable "availability_zone" {
  type        = string
  description = "Target AWS Availability Zone for subnet placement"
  default     = "us-east-1a"
}

variable "instance_type" {
  type        = string
  description = "EC2 compute instance size"
  default     = "t2.micro"
}

variable "key_name" {
  type        = string
  description = "Name of the OpenSSH key pair imported in AWS EC2"
  default     = "library-aws-key"
}

variable "s3_backup_bucket_name" {
  type        = string
  description = "Unique S3 bucket name for database snapshots and state backups"
  default     = "library-backup-334478199124-us-east-1"
}

variable "environment" {
  type        = string
  description = "Deployment lifecycle environment tier"
  default     = "production"
}

variable "project_name" {
  type        = string
  description = "Standardized project namespace prefix"
  default     = "SU_DevOps"
}
