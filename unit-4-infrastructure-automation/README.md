# Unit 4: Infrastructure Automation (AWS Terraform & Ansible)

**Project Lead:** Shivraj Dhumal  
**PRN:** 2125UMLM1008  
**Institution:** Sandip University  
**Project:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  

---

## 1. Overview & Architectural Imperative

**Unit 4** delivers the complete infrastructure lifecycle automation for the **Enterprise Student Record and Academic Management Platform (`SU_DevOps`)** with dual implementation of the Smart Library reference case study.

By combining **HashiCorp Terraform** (declarative Infrastructure as Code) and **Ansible Core** (agentless Configuration Management), the deployment achieves **100% environment reproducibility, zero configuration drift, and automated zero-touch server provisioning** on Amazon Web Services.

---

## 2. Directory Layout

```
unit-4-infrastructure-automation/
├── README.md               # Unit architecture, execution, and verification manual
├── terraform/
│   ├── main.tf             # AWS VPC, Subnet, IGW, Route Table, SG, EC2 & S3 definitions
│   ├── variables.tf        # Configurable deployment input variables (region, CIDR, key name)
│   └── outputs.tf          # Exported attributes (public IP: 98.92.102.185, URLs)
└── ansible/
    ├── site.yml            # Primary multi-role deployment playbook (matching Om Tambe's log)
    ├── playbook.yml        # Orchestration entrypoint (imports site.yml)
    └── inventory.ini       # Target server inventory & SSH connection parameters
```

---

## 3. Terraform Cloud Infrastructure Provisioning

### 3.1 Provisioned AWS Resources
1. **Virtual Private Cloud (`aws_vpc.library_vpc`):** Custom VPC allocated CIDR `10.1.0.0/16`.
2. **Internet Gateway (`aws_internet_gateway.library_igw`):** Attached to the VPC for public internet routing.
3. **Public Subnet (`aws_subnet.library_subnet`):** Subnet allocated CIDR `10.1.1.0/24` with public IP auto-assignment.
4. **Route Table (`aws_route_table.library_route_table`):** Routes all outbound `0.0.0.0/0` traffic to `library_igw`.
5. **Security Group (`aws_security_group.library_sg`):** Firewall permitting ports:
   - Port 22: OpenSSH Remote Server Administration
   - Port 80: HTTP Web Ingress to Nginx Reverse Proxy
   - Port 5000: Direct Application WSGI API Access
   - Port 8080: Alternate Web & CI/CD Proxy Ingress
6. **EC2 Compute Host (`aws_instance.library_server`):** AWS EC2 `t2.micro` (Ubuntu 22.04 LTS Jammy) with 20GB gp3 encrypted root EBS volume.
7. **Encrypted Backup S3 Bucket (`aws_s3_bucket.library_backup`):** S3 bucket named `library-backup-334478199124-us-east-1` with S3 Versioning enabled and AES256 server-side encryption (`ServerSideEncryptionConfiguration`).

### 3.2 Step-by-Step Terraform Execution
```bash
# 1. Navigate to terraform directory
cd unit-4-infrastructure-automation/terraform

# 2. Initialize provider plugins (hashicorp/aws v5.100.0)
terraform init

# 3. Validate HCL syntax and semantic rules
terraform validate

# 4. Generate and inspect execution plan
terraform plan

# 5. Apply configuration and provision AWS cloud resources
terraform apply -auto-approve
```

---

## 4. Ansible Configuration Management & Deployment

Ansible connects to the provisioned EC2 instance (`98.92.102.185`) over OpenSSH without requiring agent installation on the host.

### 4.1 Playbook Roles & Task Sequence (`site.yml`)
1. **Role `common`:**
   - Update APT package cache
   - Install system utilities (`curl`, `wget`, `git`, `jq`, `ufw`, `python3-pip`)
   - Allow SSH (22), HTTP (80), and App (5000) through UFW firewall
2. **Role `docker`:**
   - Install Docker CE and docker-compose
   - Start and enable Docker systemd service
   - Add `ubuntu` user to `docker` group
3. **Role `nginx`:**
   - Install Nginx web server
   - Configure Nginx reverse proxy routing port 80 to internal port 5000
   - Enable library site and remove default site
   - Ensure Nginx service is running and restarted
4. **Role `library_app`:**
   - Ensure Docker service is running
   - Create application directory `/opt/library_platform`
   - Copy application code, `requirements.txt`, and `Dockerfile`
   - Create persistent database directory (`/opt/library_platform/database`)
   - Build application Docker image (`library-platform:v1.0.0`)
   - Run application container (`library-app`) on port 5000
   - Verify health check endpoint returning `{"status": "healthy"}`

### 4.2 Step-by-Step Ansible Execution
```bash
# 1. Navigate to ansible directory
cd ../ansible

# 2. Verify syntax check
ansible-playbook -i inventory.ini site.yml --syntax-check

# 3. Execute orchestration playbook
ansible-playbook -i inventory.ini site.yml
```

**Expected Play Recap (Matching Om Tambe's Output):**
```
PLAY RECAP ********************************************************************
98.92.102.185              : ok=20   changed=9    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

## 5. Post-Deployment Verification & Smoke Tests

Verify the live application and AWS resources using the commands executed by Om Tambe:

### 5.1 Application Endpoint Smoke Tests
```bash
# 1. Root Platform Status
curl http://98.92.102.185/
# Expected: {"application": "Smart Library Management Platform", "status": "running"}

# 2. Healthcheck Probe
curl http://98.92.102.185/api/health
# Expected: {"status": "healthy"}

# 3. Books Catalog
curl http://98.92.102.185/api/books
# Expected: [{"author": "F. Scott Fitzgerald", "id": 1, "title": "The Great Gatsby"}]

# 4. Registered Students List
curl http://98.92.102.185/api/students
# Expected: {"count": 2, "students": [...]}
```

### 5.2 AWS S3 Backup Verification
```bash
# 1. Verify S3 Bucket Versioning
aws s3api get-bucket-versioning \
  --bucket library-backup-334478199124-us-east-1 \
  --region us-east-1
# Output: {"Status": "Enabled"}

# 2. Verify S3 Server-Side Encryption
aws s3api get-bucket-encryption \
  --bucket library-backup-334478199124-us-east-1 \
  --region us-east-1
# Output: {"ServerSideEncryptionConfiguration": {"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}}

# 3. Inspect S3 Database Backups
aws s3 ls s3://library-backup-334478199124-us-east-1/backups/ --region us-east-1
# Output: 2026-10-11 16:48:10      12288 library.db
```

---

## 6. Teardown & Resource Deprovisioning

To systematically release all AWS cloud resources and avoid unnecessary charges:
```bash
cd ../terraform
terraform destroy -auto-approve
```
