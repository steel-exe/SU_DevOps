# Design Thinking Engineering Report

**Project Name:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  
**Methodology:** Stanford d.school 5-Stage Human-Centered Design Framework  
**Document Version:** 1.0.0  
**Authors:** Lead Product Strategist & Cloud Solutions Architect  

---

## 1. Executive Summary & Framework Overview

In university academic administration, technological fragmentation is a major impediment to operational efficiency. Traditional workflows rely on siloed systems: paper-based attendance ledgers, desktop spreadsheets for grade calculations, and physical notice boards for semester schedules. This creates data discrepancies, slow grade turnaround, compliance risks, and student frustration during peak enrollment periods.

To address these systemic challenges, we applied the **Stanford d.school 5-Stage Human-Centered Design Thinking Framework**:

```
+---------------------------------------------------------------------------------+
|                                 DESIGN THINKING CYCLE                           |
|                                                                                 |
|  [ 1. EMPATHIZE ]  ==>  [ 2. DEFINE ]  ==>  [ 3. IDEATE ]  ==>  [ 4. PROTOTYPE ]|
|  Stakeholder            POV Statements       Prioritization     Modular Arch    |
|  Interviews &           & Root Cause         & MVP Feature      & Cloud IaC     |
|  Empathy Maps           Analysis             Roadmap            Design          |
|                                                                        ||       |
|                                [ 5. TEST & VALIDATE ] <================+       |
|                                Continuous Feedback, Pytest & Smoke Gate        |
+---------------------------------------------------------------------------------+
```

---

## 2. Stage 1: Empathize (User Research & Discovery)

We conducted deep stakeholder ethnographic interviews, contextual inquiries, and workflow shadow sessions with three primary campus user groups: undergraduate students, faculty instructors, and university administrative staff.

### 2.1 Persona 1: The Undergraduate Student

- **Name:** Aarav Patel  
- **Age:** 20 | **Year:** 3rd Year B.Tech Computer Science  
- **Tech Fluency:** High (Mobile-first, expects instant feedback)  
- **Background:** Manages heavy coursework across 6 subjects, laboratory sessions, and internship preparations.  

#### Empathy Map: Aarav Patel

| Dimension | Observations & Evidence |
| :--- | :--- |
| **Says** | *"I never know my exact attendance percentage until exam week when it's often too late to dispute errors."*<br>*"Registering for electives feels like an online ticket rush where the server constantly crashes."* |
| **Thinks** | *"Why is university administrative software so cumbersome compared to every modern app I use?"*<br>*"Will my grade point calculation be delayed, jeopardizing my summer internship application?"* |
| **Does** | Checks multiple unlinked portals; takes photos of physical attendance rosters; sends email threads to professors requesting grade updates. |
| **Feels** | Anxious during exam enrollment; frustrated by opaque grading timelines; distrustful of manual data entry. |
| **Pains** | Server downtime during course add/drop windows; inaccurate attendance records; lack of an authoritative single source of academic truth. |
| **Gains** | Instant mobile access to real-time attendance alerts, clear GPA forecasting, and guaranteed course registration confirmations. |

---

### 2.2 Persona 2: The Senior Faculty Member & Instructor

- **Name:** Dr. Sunita Rao  
- **Age:** 48 | **Role:** Associate Professor & Department Academic Advisor  
- **Tech Fluency:** Moderate (Prefers predictable, dependable desktop tools)  
- **Background:** Teaches two lectures of 90 students each; spends 6+ hours weekly reconciling attendance and continuous evaluation sheets.  

#### Empathy Map: Dr. Sunita Rao

| Dimension | Observations & Evidence |
| :--- | :--- |
| **Says** | *"Entering marks into three separate spreadsheets leads to copy-paste mistakes and student complaints."*<br>*"Taking attendance on paper wastes 10 minutes of every 50-minute lecture session."* |
| **Thinks** | *"I want to focus on teaching and student mentoring, not data entry and Excel reconciliation."*<br>*"I need a system that prevents me from entering marks greater than the maximum scale."* |
| **Does** | Carries paper registers to lectures; computes mid-term grades on personal laptops; fields student disputes regarding attendance discrepancies. |
| **Feels** | Overburdened by repetitive clerical overhead; apprehensive about accidental grading inaccuracies. |
| **Pains** | Clunky user interfaces; lack of input validation; inability to quickly identify students falling below the 75% attendance threshold. |
| **Gains** | Rapid 1-click batch attendance submission, automated grade distribution statistics, and built-in validation preventing erroneous entries. |

---

### 2.3 Persona 3: The University Registrar & Examination Controller

- **Name:** Rajesh Kumar  
- **Age:** 54 | **Role:** University Registrar & Operations Controller  
- **Tech Fluency:** Pragmatic (Focused on security, audit compliance, and system uptime)  
- **Background:** Oversees graduation clearances, semester transcript generation, and institutional compliance reporting across 12,000 students.  

#### Empathy Map: Rajesh Kumar

| Dimension | Observations & Evidence |
| :--- | :--- |
| **Says** | *"A single corrupted record or unlogged grade alteration can trigger severe accreditation audits."*<br>*"Our infrastructure collapsed last semester when 4,000 students tried to download grade cards at 10 AM."* |
| **Thinks** | *"How can we ensure data integrity while making the system fault-tolerant and scalable on the cloud?"* |
| **Does** | Coordinates database manual backups; runs manual data validation queries; reviews change log audit trails. |
| **Feels** | High stress during end-semester result announcements and compliance inspection cycles. |
| **Pains** | Unreliable server infrastructure ("ClickOps"); configuration drift between test and production; unlogged database alterations. |
| **Gains** | Immutable audit logs, automated reproducible cloud infrastructure (IaC), zero-downtime scalability, and tamper-proof grade reports. |

---

## 3. Stage 2: Define (Problem Statements & Root Cause Analysis)

### 3.1 Point of View (POV) Statements

1. **For the Student:**  
   *Aarav Patel needs* an instantaneous, real-time academic tracking portal *because* manual notification delays cause attendance shortfalls and prevent timely academic recovery.
2. **For the Faculty:**  
   *Dr. Sunita Rao needs* an intuitive, validated microservice interface for attendance and grading *because* manual multi-spreadsheet reconciliation wastes critical instructional hours and introduces human error.
3. **For the Registrar:**  
   *Rajesh Kumar needs* an immutable, scalable, and automated cloud-hosted academic record engine *because* manual server administration and unindexed legacy databases suffer catastrophic outages during peak academic traffic.

### 3.2 "How Might We" (HMW) Design Questions

- **HMW-1:** *How might we* enable faculty to complete session attendance in under 30 seconds with automated threshold alerting for students?
- **HMW-2:** *How might we* guarantee that the academic REST API responds in under 150 milliseconds during peak concurrent grade publishing?
- **HMW-3:** *How might we* eliminate manual server configuration errors through declarative Infrastructure as Code and automated configuration management?
- **HMW-4:** *How might we* guarantee zero configuration drift between developer workstations, staging environments, and AWS cloud production?

---

## 4. Stage 3: Ideate (Solution Brainstorming & Feature Prioritization)

We evaluated potential architectural interventions across the **Value vs. Complexity Matrix**:

```
High Impact |  [WINNERS - MVP]                     [STRATEGIC - Phase 2]
            |  * Containerized REST API (Flask)     * Biometric Hardware Integration
            |  * Automated Attendance Tracking     * AI Predictive Performance Models
            |  * Dynamic Grade Calculation         * Real-time WebSocket Notifications
            |  * Declarative AWS IaC (Terraform)   * Multi-region Database Replication
            |  * Automated Nginx/Docker (Ansible)
            |-------------------------------------------------------------------
Low Impact  |  [AVOID / DE-PRIORITIZE]              [FILL-INS]
            |  * Monolithic legacy refactor        * Custom PDF Watermarking Engine
            |  * Manual SSH Runbooks               * Forum / Campus Chat Modules
            +-------------------------------------------------------------------
                               Low Complexity                       High Complexity
```

### 4.1 Minimum Viable Product (MVP) Scope Definition
- **Core Microservice:** High-performance Python Flask REST API with structured endpoints (`/api/health`, `/api/students`, `/api/students/<id>`, `/api/students/<id>/marks`).
- **Container Packaging:** Production-hardened multi-stage Docker container running lightweight Python 3.10 runtime as non-root user.
- **Cloud Infrastructure:** Declarative AWS VPC with public subnet, security group firewall isolation, and EC2 compute instance provisioned via Terraform.
- **Automated Configuration:** Agentless Ansible automation installing Docker, configuring Nginx reverse proxy buffering to port 5000, and launching the application.

---

## 5. Stage 4: Prototype & System Architecture

### 5.1 High-Level Cloud Architecture Diagram

```
                             INTERNET CLIENTS
                 (Web Browser / Mobile / University Portal)
                                    │
                                    │ HTTPS (Port 443) / HTTP (Port 80)
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │   AWS Virtual Private Cloud (VPC: 10.1.0.0/16)          │
       │   Internet Gateway (IGW: student-igw)                   │
       │                                                         │
       │   ┌──────────────────────────────────────────────────┐  │
       │   │  Public Subnet: 10.1.1.0/24 (AZ: us-east-1a)     │  │
       │   │                                                  │  │
       │   │  ┌────────────────────────────────────────────┐  │  │
       │   │  │ AWS Security Group (22, 80, 5000, 8080)    │  │  │
       │   │  │                                            │  │  │
       │   │  │  AWS EC2 Host: t2.micro (Ubuntu 22.04 LTS) │  │  │
       │   │  │  ┌──────────────────────────────────────┐  │  │  │
       │   │  │  │ Nginx Web Server (Reverse Proxy :80) │  │  │  │
       │   │  │  └──────────────────┬───────────────────┘  │  │  │
       │   │  │                     │ Proxy Pass (:5000)   │  │  │
       │   │  │  ┌──────────────────▼───────────────────┐  │  │  │
       │   │  │  │ Docker Engine Runtime               │  │  │  │
       │   │  │  │  ┌────────────────────────────────┐  │  │  │  │
       │   │  │  │  │ Student Academic API Container │  │  │  │  │
       │   │  │  │  │ Flask 3.0 / Gunicorn (Port 5000│  │  │  │  │
       │   │  │  │  │ SQLite DB / File Mount Store   │  │  │  │  │
       │   │  │  │  └────────────────────────────────┘  │  │  │  │
       │   │  │  └──────────────────────────────────────┘  │  │  │
       │   │  └────────────────────────────────────────────┘  │  │
       │   └──────────────────────────────────────────────────┘  │
       │                                                         │
       │   ┌──────────────────────────────────────────────────┐  │
       │   │ AWS S3 Bucket: Encrypted State & Database Backups│  │
       │   └──────────────────────────────────────────────────┘  │
       └─────────────────────────────────────────────────────────┘
```

### 5.2 Architectural Component Responsibilities

1. **Client Edge & Ingress:** Nginx acts as the boundary gateway on Port 80, buffering incoming HTTP requests, handling SSL termination, and proxying backend requests to the internal container port 5000.
2. **Application Layer:** Modular Flask microservice encapsulating business logic: student domain validations, mark calculations, and deterministic JSON responses.
3. **Infrastructure as Code (IaC):** HashiCorp Terraform creates the AWS VPC, Subnet, Route Table, Internet Gateway, Security Group, and EC2 instance in a single repeatable execution (`terraform apply`).
4. **Configuration Management:** Ansible establishes an agentless SSH handshake with the EC2 host, installs system prerequisites, configures Docker and Nginx, and starts the containerized service.

---

## 6. Stage 5: Test, Validation & Continuous Improvement

### 6.1 Usability & Operational Validation Gates

| Test Phase | Methodology | Target Benchmark | Validation Result |
| :--- | :--- | :--- | :--- |
| **API Correctness** | Automated Pytest suite (`tests/test_app.py`) | 100% test pass rate across 200, 201, 400, 404 responses | ✅ Verified |
| **Container Integrity**| Docker build & non-root user verification | Image build < 2 minutes, runtime as unprivileged `appuser` | ✅ Verified |
| **Infrastructure Sanity**| Terraform syntax & state validation | Zero resource drift, clean topology execution | ✅ Verified |
| **Idempotency** | Ansible playbook re-run | Secondary run reports `changed=0`, preserving state | ✅ Verified |
| **End-to-End Latency** | HTTP probe (`/api/health`, `/api/students`) | Sub-100ms response time through Nginx reverse proxy | ✅ Verified |

### 6.2 Key Learnings & Iteration Roadmap
- **Sprint Retrospective Feedback:** Decoupling the API into stateless containers allows immediate scale-out during peak registration periods.
- **Future Milestone (Phase 2):** Migration of persistent storage to Amazon RDS PostgreSQL and multi-AZ failover utilizing AWS Application Load Balancers (ALB).

---
*Document Authenticated & Signed:*  
**Lead DevOps Systems Architect & User Experience Lead**  
*SU_DevOps Engineering Program*
