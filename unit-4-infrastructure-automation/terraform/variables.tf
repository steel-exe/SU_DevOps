# =============================================================================
# Terraform Variables Specification
# Enterprise Student Record & Academic Management Platform (SU_DevOps)
# =============================================================================

variable "aws_region" {
  type        = string
  description = "Target AWS deployment region"
  default     = "us-east-1"
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the dedicated Student Platform VPC"
  default     = "10.1.0.0/16"
}

variable "public_subnet_cidr" {
  type        = string
  description = "CIDR block for the public subnet hosting the application server"
  default     = "10.1.1.0/24"
}

variable "availability_zone" {
  type        = string
  description = "Target AWS Availability Zone for resource placement"
  default     = "us-east-1a"
}

variable "instance_type" {
  type        = string
  description = "AWS EC2 instance sizing tier for workload execution"
  default     = "t2.micro"
}

variable "key_name" {
  type        = string
  description = "Name of the pre-imported OpenSSH key pair in AWS EC2"
  default     = "student-aws-key"
}

variable "environment" {
  type        = string
  description = "Deployment lifecycle environment (dev, staging, production)"
  default     = "production"
}

variable "project_name" {
  type        = string
  description = "Standardized project namespace for naming and tagging"
  default     = "SU_DevOps"
}
