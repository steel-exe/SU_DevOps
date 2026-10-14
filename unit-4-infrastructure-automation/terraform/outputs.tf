# =============================================================================
# Terraform Outputs Specification
# Project: Enterprise Student Record & Smart Library Platform (SU_DevOps)
# Student Lead: Shivraj Dhumal (PRN: 2125UMLM1008) - Sandip University
# =============================================================================

output "ec2_public_ip" {
  description = "Public IPv4 address of the provisioned library_server instance (e.g. 98.92.102.185)"
  value       = aws_instance.library_server.public_ip
}

output "ec2_instance_id" {
  description = "AWS EC2 instance identifier"
  value       = aws_instance.library_server.id
}

output "vpc_id" {
  description = "Identifier of the created Virtual Private Cloud (library_vpc)"
  value       = aws_vpc.library_vpc.id
}

output "subnet_id" {
  description = "Identifier of the public subnet (library_subnet)"
  value       = aws_subnet.library_subnet.id
}

output "security_group_id" {
  description = "Identifier of the security group firewall (library_sg)"
  value       = aws_security_group.library_sg.id
}

output "s3_backup_bucket" {
  description = "Name of the encrypted S3 bucket created for database backups"
  value       = aws_s3_bucket.library_backup.id
}

output "ssh_connection_command" {
  description = "Command string to establish OpenSSH session with the EC2 host"
  value       = "ssh -i ~/.ssh/${var.key_name} ubuntu@${aws_instance.library_server.public_ip}"
}

output "curl_root_url" {
  description = "Verification URL for root endpoint"
  value       = "http://${aws_instance.library_server.public_ip}/"
}

output "curl_health_url" {
  description = "Verification URL for healthcheck endpoint"
  value       = "http://${aws_instance.library_server.public_ip}/api/health"
}

output "curl_books_url" {
  description = "Verification URL for books catalog endpoint"
  value       = "http://${aws_instance.library_server.public_ip}/api/books"
}
