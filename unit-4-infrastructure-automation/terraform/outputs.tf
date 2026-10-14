# =============================================================================
# Terraform Outputs Specification
# Enterprise Student Record & Academic Management Platform (SU_DevOps)
# =============================================================================

output "ec2_public_ip" {
  description = "Public IPv4 address of the provisioned EC2 application host"
  value       = aws_instance.student_server.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS hostname of the EC2 instance"
  value       = aws_instance.student_server.public_dns
}

output "ec2_instance_id" {
  description = "AWS EC2 instance identifier"
  value       = aws_instance.student_server.id
}

output "vpc_id" {
  description = "Identifier of the created Virtual Private Cloud"
  value       = aws_vpc.student_vpc.id
}

output "subnet_id" {
  description = "Identifier of the public subnet"
  value       = aws_subnet.student_public_subnet.id
}

output "security_group_id" {
  description = "Identifier of the security group firewall"
  value       = aws_security_group.student_sg.id
}

output "s3_backup_bucket" {
  description = "Name of the encrypted S3 bucket created for database backups"
  value       = aws_s3_bucket.backup_bucket.id
}

output "ssh_connection_command" {
  description = "Command string to establish OpenSSH session with the EC2 host"
  value       = "ssh -i ~/.ssh/${var.key_name}.pem ubuntu@${aws_instance.student_server.public_ip}"
}

output "api_endpoint_via_nginx" {
  description = "Public HTTP URL of the application served via Nginx reverse proxy (Port 80)"
  value       = "http://${aws_instance.student_server.public_ip}/api/health"
}

output "api_endpoint_direct_flask" {
  description = "Direct microservice application URL (Port 5000)"
  value       = "http://${aws_instance.student_server.public_ip}:5000/api/health"
}
