# Enterprise Student Record & Academic Management Platform (`SU_DevOps`)

**Project Lead:** Shivraj Dhumal  
**PRN:** 2125UMLM1008  
**Academic Institution:** Sandip University  
**Curriculum:** DevOps & Cloud Engineering Series  

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Manifests-326CE5.svg)](https://kubernetes.io/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939.svg)](https://www.jenkins.io/)
[![Terraform](https://img.shields.io/badge/Terraform-v1.7%2B-7B42BC.svg)](https://www.terraform.io/)
[![Ansible](https://img.shields.io/badge/Ansible-v2.16%2B-EE0000.svg)](https://www.ansible.com/)
[![AWS Cloud](https://img.shields.io/badge/AWS-VPC%20%7C%20EC2%20%7C%20S3-FF9900.svg)](https://aws.amazon.com/)

> **Comprehensive DevOps Engineering Repository across Units 1, 2, 3, and 4.**  
> Built and submitted by **Shivraj Dhumal (PRN: 2125UMLM1008)**. Demonstrates the complete software delivery lifecycle—from initial product discovery, Word (.docx) formal project submissions, and Agile backlog grooming, to full-stack microservice engineering, continuous integration with Jenkins, and automated multi-tier AWS cloud infrastructure provisioning using Terraform and Ansible.

---

## 1. Repository Directory Structure

```
SU_DevOps/
├── README.md                                    # Master repository overview & execution manual
├── .gitignore                                   # Standardized Git exclusion rules
├── .github/
│   └── workflows/
│       └── ci.yml                               # Automated GitHub Actions CI test pipeline
│
├── unit-1-product-engineering/                  # Unit 1: Product Discovery & Specification
│   └── Unit-1-Product-Engineering.docx          # Formal Word Submission Document
│
├── unit-2-agile-planning/                       # Unit 2: Agile Project Management & Scrum
│   └── Unit-2-Agile-Mini-Project.docx           # Formal Word Agile Submission Document
│
├── unit-3-application-development/              # Unit 3: Enterprise Microservice & Full Stack Task
│   ├── Dockerfile                               # Multi-stage production container definition
│   ├── Jenkinsfile                              # Declarative Jenkins automated CI/CD pipeline
│   ├── package.json                             # Frontend & application metadata
│   ├── requirements.txt                         # Production & testing dependencies
│   ├── run.py                                   # Server entrypoint (0.0.0.0:5000)
│   ├── README.md                                # Microservice setup & deployment guide
│   ├── app/
│   │   ├── __init__.py                          # Application factory pattern
│   │   ├── main.py                              # Entrypoint wrapper
│   │   ├── models.py                            # Domain entity exports
│   │   ├── models/                              # Domain models (Student, Course, Enrollment, Grade)
│   │   ├── routes/                              # Blueprint routes (api.py, views.py)
│   │   ├── services/                            # Business services (StudentService, CourseService, GradeService)
│   │   ├── static/                              # CSS styling & JS scripts
│   │   └── templates/                           # HTML5 templates (Dashboard, Students, Courses)
│   ├── database/
│   │   └── db.py                                # SQLite database connector & schema migrations
│   ├── k8s/                                     # Kubernetes deployment and service manifests
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── tests/                                   # 43 automated Pytest unit tests (100% pass rate)
│       ├── __init__.py
│       ├── test_api_endpoints.py
│       ├── test_app.py
│       ├── test_course_enrollment.py
│       ├── test_marks_mgmt.py
│       └── test_student_service.py
│
└── unit-4-infrastructure-automation/            # Unit 4: Cloud IaC & Config Automation
    ├── README.md                                # Two-tier DevOps orchestration handbook
    ├── app/                                     # Smart Library Management Platform microservice
    │   ├── app.py                               # Flask app serving /, /api/health, /api/books
    │   ├── requirements.txt                     # Dependencies (Flask, Gunicorn)
    │   └── Dockerfile                           # Production container exposing port 5000
    ├── terraform/
    │   ├── main.tf                              # AWS VPC, Subnet, IGW, Route Table, SG, EC2 & S3
    │   ├── variables.tf                         # Configurable deployment input variables
    │   └── outputs.tf                           # Exported attributes (public IP: 98.92.102.185, URLs)
    └── ansible/
        ├── site.yml                             # Primary multi-role deployment playbook
        ├── playbook.yml                         # Orchestration entrypoint (imports site.yml)
        └── inventory.ini                        # Target server inventory & SSH connection parameters
```

---

## 2. Four-Unit Project Summary

### Unit 1: Product Engineering & Design Thinking
- **Documentation:** [`BRD.md`](./unit-1-product-engineering/BRD.md), [`FRS_NFRS_Specification.md`](./unit-1-product-engineering/FRS_NFRS_Specification.md), [`Design_Thinking_Report.md`](./unit-1-product-engineering/Design_Thinking_Report.md), [`User_Personas.md`](./unit-1-product-engineering/User_Personas.md), [`System_Architecture.md`](./unit-1-product-engineering/System_Architecture.md).
- **Formal Word Document:** [`Om_Tambe_2125UMLM1065_DevOps_Unit1_MiniProject.docx`](./unit-1-product-engineering/Om_Tambe_2125UMLM1065_DevOps_Unit1_MiniProject.docx) & [`Unit-1-Product-Engineering.docx`](./unit-1-product-engineering/Unit-1-Product-Engineering.docx).
- **Highlights:** Full business requirements, IBM Design Thinking framework (Observe, Reflect, Make), Three IBM Hills (Student, Faculty, Admin), Personas (Aarav Patel, Dr. Priya Sharma, Rahul Verma), and complete architectural blueprints.

### Unit 2: Agile Project Planning & Scrum
- **Documentation:** [`Product_Backlog.md`](./unit-2-agile-planning/Product_Backlog.md), [`Sprint_Plan.md`](./unit-2-agile-planning/Sprint_Plan.md).
- **Formal Word Document:** [`Unit-2-Agile-Mini-Project.docx`](./unit-2-agile-planning/Unit-2-Agile-Mini-Project.docx) & [`Om_Tambe_2125UMLM1065_DevOps_Unit2_MiniProject.docx`](./unit-2-agile-planning/Om_Tambe_2125UMLM1065_DevOps_Unit2_MiniProject.docx).
- **Highlights:** 17 prioritized user stories, Planning Poker story point estimations (1 to 13), 2-Sprint execution breakdown with DoD/DoR, Scrum ceremony logs, and comparative evaluation of 7 Agile frameworks.

### Unit 3: Application Development & Microservices (Shifted Task)
- **Full-Stack Application:** Modular Python Flask microservice with REST API endpoints, web dashboards, SQLite ACID storage, continuous marks grading, course enrollments, and low-attendance alerts.
- **Automated Testing:** 43 automated Pytest test cases across 5 test suites with a **100% pass rate** in 0.36s.
- **DevOps CI/CD:** Automated Jenkinsfile pipeline, GitHub Actions workflow, Dockerfile, and Kubernetes orchestration manifests (`k8s/`).

### Unit 4: Infrastructure Automation (Smart Library App, Terraform & Ansible)
- **Smart Library App:** Standalone Python Flask microservice (`app.py`, `requirements.txt`, `Dockerfile`) backed by SQLite `library.db` serving `/`, `/api/health`, and `/api/books`.
- **Terraform Cloud Fabric:** Modular HCL provisioning AWS VPC (`library_vpc`), public subnet (`library_subnet`), Internet Gateway, Route Table, Security Group (`library_sg`), EC2 instance (`library_server`), and encrypted S3 bucket (`library-backup-334478199124-us-east-1`).
- **Ansible Automation:** Idempotent playbook (`site.yml`) configuring system utilities, Docker, Nginx reverse proxy on port 80, deploying the application container, and verifying health check probes.

---

## 3. Automated Test Verification Results

```bash
cd unit-3-application-development
pytest tests/ -v
```

```
============================= 43 passed in 0.36s ==============================
```

```bash
cd unit-4-infrastructure-automation/app
python -c "from app import app; c = app.test_client(); print(c.get('/').get_json()); print(c.get('/api/health').get_json()); print(c.get('/api/books').get_json())"
```

```
{'application': 'Smart Library Management Platform', 'status': 'running'}
{'status': 'healthy'}
[{'author': 'F. Scott Fitzgerald', 'id': 1, 'title': 'The Great Gatsby'}]
```

---

## 4. Remote GitHub Deployment Instructions

To push this repository to GitHub inside your repository:

```bash
# 1. Navigate to the repository root
cd "c:\Users\shivraj\Documents\std\devops\SU_DevOps"

# 2. Add the remote GitHub repository URL
git remote add origin https://github.com/steel-exe/SU_DevOps.git

# 3. Ensure branch is main
git branch -M main

# 4. Push all commits to GitHub
git push -u origin main
```

---
*Created and submitted by **Shivraj Dhumal (PRN: 2125UMLM1008)**, Sandip University.*
