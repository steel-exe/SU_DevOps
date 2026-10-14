# Unit 4: Infrastructure Automation (AWS, Terraform & Ansible)

## 1. Overview & Architectural Imperative

**Unit 4** delivers the complete production infrastructure lifecycle automation for the **Enterprise Student Record and Academic Management Platform (`SU_DevOps`)**.

In modern cloud engineering, manual server administration ("ClickOps") leads to configuration drift, human errors, slow deployments, and security vulnerabilities. Unit 4 achieves **100% environment reproducibility, zero configuration drift, and automated zero-touch server provisioning** by combining:

1. **HashiCorp Terraform (v1.7+):** Declarative **Infrastructure as Code (IaC)** provisioning cloud fabric: custom AWS VPC, public subnet, Internet Gateway, route tables, security group firewall, EC2 compute instance, and encrypted S3 backup storage.
2. **Ansible Core (v2.16+):** Agentless, idempotent **Configuration Management** over OpenSSH: installs Docker CE, configures an Nginx reverse proxy buffering to port 5000, deploys the Unit 3 containerized microservice, and executes automated multi-gate smoke tests.

---

## 2. Directory Layout

```
unit-4-infrastructure-automation/
├── README.md               # Unit architecture, execution, and validation guide
├── terraform/
│   ├── main.tf             # Core HCL provisioning VPC, IGW, Subnet, SG, EC2, and S3
│   ├── variables.tf        # Configurable deployment parameters (region, CIDR, key name)
│   └── outputs.tf          # Exported infrastructure attributes (public IP, DNS, URLs)
└── ansible/
    ├── playbook.yml        # Multi-tier playbook for Docker, Nginx, and App container
    └── inventory.ini       # Static host inventory with SSH variables
```

---

## 3. The Two-Tier DevOps Orchestration Handshake

```
┌────────────────────────────────┐                 ┌───────────────────────────────┐
│     TIER 1: TERRAFORM          │                 │       TIER 2: ANSIBLE         │
│     (Cloud IaC Fabric)         │                 │   (Configuration Management)  │
├────────────────────────────────┤                 ├───────────────────────────────┤
│ • AWS VPC (10.1.0.0/16)        │  Public IP      │ • Installs Docker CE & Nginx  │
│ • Public Subnet (10.1.1.0/24)  │ ──────────────> │ • Deploys Student App (v1.0.0)│
│ • Security Group (22,80,5000)  │  Handshake      │ • Configures Reverse Proxy    │
│ • EC2 Ubuntu 22.04 LTS         │                 │ • Executes 4-Gate Smoke Tests │
└────────────────────────────────┘                 └───────────────────────────────┘
```

### The Handshake Sequence
1. **Terraform** provisions the AWS cloud fabric and outputs the public IP:
   ```bash
   app_server_ip=$(terraform -chdir=terraform output -raw ec2_public_ip)
   ```
2. The dynamic IP is injected into the Ansible inventory:
   ```bash
   sed -i "s/YOUR_EC2_PUBLIC_IP/$app_server_ip/g" ansible/inventory.ini
   ```
3. **Ansible** executes the idempotent playbook against the newly created EC2 host via SSH.

---

## 4. Workstation Prerequisites & Toolchain Setup

### 4.1 Toolchain Matrix

| Tool | Minimum Version | Verification Command | Purpose |
| :--- | :--- | :--- | :--- |
| **AWS CLI v2** | `2.15.x+` | `aws --version` | Programmatic AWS authentication & STS checks |
| **Terraform** | `1.7.x+` | `terraform -version` | Declarative cloud resource provisioning |
| **Ansible Core**| `2.16.x+` | `ansible --version` | Agentless configuration & container orchestration |
| **OpenSSH** | `8.0+` | `ssh -V` | Secure cryptographic communication |

### 4.2 Step 1: AWS Programmatic Authentication
Configure your AWS credentials:
```bash
aws configure
# AWS Access Key ID: <YOUR_ACCESS_KEY>
# AWS Secret Access Key: <YOUR_SECRET_KEY>
# Default region name: us-east-1
# Default output format: json

# Verify STS caller identity
aws sts get-caller-identity
```

### 4.3 Step 2: SSH Key Pair Generation & AWS Import
Generate a dedicated 4096-bit RSA SSH key pair and import it into AWS EC2 in `us-east-1`:
```bash
mkdir -p ~/.ssh
ssh-keygen -t rsa -b 4096 -f ~/.ssh/student-aws-key -N "" -C "devops@student-academic-platform"
chmod 400 ~/.ssh/student-aws-key
chmod 644 ~/.ssh/student-aws-key.pub

# Import key pair into AWS EC2
aws ec2 import-key-pair \
  --key-name "student-aws-key" \
  --public-key-material fileb://~/.ssh/student-aws-key.pub \
  --region us-east-1
```

---

## 5. Phase 1: Terraform Cloud Provisioning

### 5.1 Navigate to Terraform Directory
```bash
cd unit-4-infrastructure-automation/terraform
```

### 5.2 Initialize Terraform Working Directory
Downloads the `hashicorp/aws` provider plugin and configures backend state:
```bash
terraform init
```

### 5.3 Validate HCL Syntax
Verifies configuration files syntactically and semantically:
```bash
terraform validate
```

### 5.4 Generate Execution Plan
Inspects cloud state and outputs topological creation graph:
```bash
terraform plan -out=tfplan
```

### 5.5 Apply Configuration & Provision Resources
Provisions VPC, Subnet, Route Table, Internet Gateway, Security Group, EC2 instance, and S3 bucket:
```bash
terraform apply tfplan
```

### 5.6 View Outputs
```bash
terraform output
```

Example Outputs:
```
ec2_public_ip          = "54.210.88.14"
vpc_id                 = "vpc-0a8b9c7d1e"
security_group_id      = "sg-0987654321fedcba"
api_endpoint_via_nginx = "http://54.210.88.14/api/health"
```

---

## 6. Phase 2: Ansible Configuration & Deployment

### 6.1 Update Ansible Inventory
Navigate to the Ansible directory and update `inventory.ini` with the provisioned EC2 public IP:
```bash
cd ../ansible

# Replace placeholder with Terraform output IP
EC2_IP=$(terraform -chdir=../terraform output -raw ec2_public_ip)
sed -i "s/YOUR_EC2_PUBLIC_IP/$EC2_IP/g" inventory.ini
```

### 6.2 Test SSH Connectivity (Ping)
```bash
ansible -i inventory.ini academic_servers -m ping
```

### 6.3 Execute Deployment Playbook
Run the multi-tier automation playbook:
```bash
ansible-playbook -i inventory.ini playbook.yml
```

---

## 7. Post-Deployment Validation & Four Verification Gates

| Validation Gate | Verification Objective | Automated Command | Expected Output |
| :--- | :--- | :--- | :--- |
| **Gate 1: Network & OS** | Confirms host reachability and OpenSSH daemon | `nc -zv -w 5 $EC2_IP 22`<br>`ssh -i ~/.ssh/student-aws-key ubuntu@$EC2_IP uptime` | Open socket, system uptime displayed |
| **Gate 2: Daemons & Ports**| Confirms Docker & Nginx services active | `ansible -i inventory.ini academic_servers -m systemd -a "name=docker state=started"`<br>`ansible -i inventory.ini academic_servers -m systemd -a "name=nginx state=started"` | `status=started` (ok) |
| **Gate 3: App Container** | Verifies container is running with port 5000 | `ssh -i ~/.ssh/student-aws-key ubuntu@$EC2_IP "docker ps --filter name=student-academic-api --format '{{.Status}}'"` | Up X minutes (healthy) |
| **Gate 4: API Smoke Tests**| End-to-end HTTP validation through Nginx (:80) | `curl -s -f http://$EC2_IP/api/health \| jq .status`<br>`curl -s -f http://$EC2_IP/api/students \| jq .count` | `"UP"`<br>`>= 2` |

### Manual Live Smoke Test Commands
```bash
# Test 1: Service Healthcheck (via Nginx Port 80)
curl -i http://$EC2_IP/api/health

# Test 2: List Registered Students
curl -i http://$EC2_IP/api/students

# Test 3: Create New Student
curl -i -X POST http://$EC2_IP/api/students \
  -H "Content-Type: application/json" \
  -d '{"student_id": "STD2026888", "name": "Live Student", "email": "live@university.edu", "department": "CS", "semester": 3}'

# Test 4: Record Marks & Calculate GPA
curl -i -X POST http://$EC2_IP/api/students/STD2026888/marks \
  -H "Content-Type: application/json" \
  -d '{"course_code": "CS301", "marks": 92.5, "credits": 4}'
```

---

## 8. Clean De-provisioning & Teardown

To release AWS cloud resources and prevent ongoing costs:
```bash
cd ../terraform
terraform destroy -auto-approve
```
This systematically terminates the EC2 host, removes the security group, deletes the public subnet, detaches the Internet Gateway, and destroys the VPC in topological order.
