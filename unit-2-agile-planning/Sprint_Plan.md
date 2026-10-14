# Agile Sprint Execution Plan & Scrum Framework

**Project Name:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  
**Student / Project Lead:** Om Tambe (PRN: 2125UMLM1065)  
**Academic Institution:** Sandip University  
**Sprint Cadence:** 2-Week Sprints (10 Working Days per Sprint)  
**Document Version:** 1.0.0  

---

## 1. Scrum Team Structure & Project Allocation

```
                      ┌────────────────────────────────────────┐
                      │             PRODUCT OWNER              │
                      │  * Om Tambe (PRN: 2125UMLM1065)        │
                      │  * Backlog Prioritization & Acceptance │
                      └──────────────────┬─────────────────────┘
                                         │
                      ┌──────────────────▼─────────────────────┐
                      │              SCRUM MASTER              │
                      │  * Facilitates Standups & Retros       │
                      │  * Removes Technical Impediments      │
                      └──────────────────┬─────────────────────┘
                                         │
         ┌───────────────────────────────┴───────────────────────────────┐
         │                               │                               │
┌────────▼───────────────┐   ┌───────────▼────────────┐   ┌──────────────▼────────┐
│  BACKEND DEVELOPERS    │   │    QA AUTOMATION       │   │  DEVOPS & CLOUD       │
│  * Flask REST API      │   │  * Pytest Unit & Int.  │   │  * Docker Packaging   │
│  * Domain Models & GPA │   │  * Status Code Gates   │   │  * Terraform & Ansible│
└────────────────────────┘   └────────────────────────┘   └───────────────────────┘
```

| Role | Assigned Member | Core Responsibilities |
| :--- | :--- | :--- |
| **Project Lead & Product Owner** | Om Tambe (PRN: 2125UMLM1065) | Defines product vision, prioritizes the Product Backlog, signs off on User Stories, coordinates academic compliance. |
| **Scrum Master** | Agile Delivery Coach | Shields team from external interruptions, conducts Daily Scrums, Sprint Reviews, and Retrospectives, enforces DoD. |
| **Backend & Microservice Devs** | Development Team | Implements Flask REST endpoints (`main.py`), validation rules, domain entities (`models.py`), and GPA calculation. |
| **QA Automation Engineer** | Test Automation Team | Develops automated Pytest suite (`test_app.py`), asserts HTTP status codes (200, 201, 400, 404, 409). |
| **DevOps & Cloud Architect** | Om Tambe & Cloud Ops | Authors Dockerfile, HashiCorp Terraform AWS configurations, Ansible automation playbooks, and smoke test gates. |

---

## 2. Sprint 1 Execution Plan: Foundation, Core API & Cloud Provisioning

- **Sprint Goal:** Establish repository foundation, implement the core Student Records REST API, package into Docker, and provision AWS cloud fabric via Terraform.
- **Sprint Duration:** Weeks 1–2 (10 Working Days)
- **Target Velocity / Capacity:** 25 Story Points (160 Engineering Hours)

### 2.1 Sprint 1 Backlog & Task Breakdown

| Story ID | Task ID | Description | Assignee | Est. Hours | Status |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **US-01** | T-101 | Implement credential hashing using `bcrypt` and JWT token generator with 60-min TTL. | Backend Dev | 8h | Done |
| **US-02** | T-102 | Create RBAC decorator enforcing Admin, Faculty, Student, and Exam Cell role permissions. | Backend Dev | 8h | Done |
| **US-03** | T-103 | Build `Student` domain model (`app/models.py`) with strict email, ID, and semester validation. | Backend Dev | 8h | Done |
| **US-03** | T-104 | Implement `POST /api/students` returning HTTP 201 on creation and HTTP 409 on duplicates. | Backend Dev | 6h | Done |
| **US-05** | T-105 | Implement `GET /api/students/<student_id>` returning HTTP 200 or HTTP 404 Not Found. | Backend Dev | 4h | Done |
| **US-06** | T-106 | Implement `GET /api/students` supporting `?department=` and `?semester=` query filters. | Backend Dev | 6h | Done |
| **US-15** | T-107 | Author multi-stage Dockerfile (`python:3.10-slim`) running under unprivileged user `appuser`. | Om Tambe | 8h | Done |
| **US-16** | T-108 | Write Terraform HCL provisioning AWS VPC (`library_vpc`), subnet, IGW, and security group. | Om Tambe | 14h | Done |
| **US-16** | T-109 | Configure Terraform resources for EC2 `library_server` and encrypted S3 backup bucket. | Om Tambe | 10h | Done |
| **US-03** | T-110 | Build automated Pytest suite asserting 200, 201, 400, 404, and 409 status codes. | QA Lead | 12h | Done |

### 2.2 Sprint 1 Scrum Ceremonies Log

#### Daily Scrum Sample (Sprint 1, Day 6):
- **Om Tambe (Project Lead / DevOps):**
  - *Yesterday:* Validated Terraform configuration syntax and verified execution plan creating VPC `10.1.0.0/16` and EC2 `t2.micro` compute instance.
  - *Today:* Configuring S3 bucket encryption with AES-256 and enabling S3 versioning.
  - *Blockers:* None; AWS credentials authenticated via STS.
- **Backend Developer:**
  - *Yesterday:* Finished student input validation rules for `student_id`, email regex, and semester constraints.
  - *Today:* Implementing the thread-safe repository store with re-entrant locking (`RLock`).
  - *Blockers:* None.

---

## 3. Sprint 2 Execution Plan: Academic Logic, Ansible Automation & Edge Proxy

- **Sprint Goal:** Deliver attendance tracking with automated low-attendance (<75%) flags, continuous marks grading, automated Ansible deployment with Nginx reverse proxy, and post-deployment validation.
- **Sprint Duration:** Weeks 3–4 (10 Working Days)
- **Target Velocity / Capacity:** 28 Story Points (180 Engineering Hours)

### 3.1 Sprint 2 Backlog & Task Breakdown

| Story ID | Task ID | Description | Assignee | Est. Hours | Status |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **US-09** | T-201 | Build session attendance submission endpoint supporting Present, Absent, and Excused. | Backend Dev | 8h | Done |
| **US-10** | T-202 | Implement real-time aggregate attendance formula with percentage calculations. | Backend Dev | 6h | Done |
| **US-11** | T-203 | Implement automatic low-attendance (<75%) warning flag engine and alert dispatcher. | Backend Dev | 8h | Done |
| **US-12** | T-204 | Implement `POST /api/students/<id>/marks` validating scores between 0.0 and 100.0. | Backend Dev | 8h | Done |
| **US-13** | T-205 | Build automatic SGPA and CGPA computation engine on a 10-point academic scale. | Backend Dev | 8h | Done |
| **US-17** | T-206 | Author Ansible playbook (`site.yml` / `playbook.yml`) with baseline utilities and UFW rules. | Om Tambe | 12h | Done |
| **US-17** | T-207 | Configure Ansible tasks to install Docker CE, containerd, and configure systemd service. | Om Tambe | 8h | Done |
| **US-17** | T-208 | Configure Nginx reverse proxy forwarding port 80 to container port 5000 with buffering. | Om Tambe | 10h | Done |
| **US-17** | T-209 | Build and launch application Docker container via Ansible with healthcheck probing. | Om Tambe | 8h | Done |
| **US-17** | T-210 | Execute Four-Tier Post-Deployment Validation Gates (Network, Daemons, Container, API). | Om Tambe | 6h | Done |

---

## 4. Definition of Done (DoD) & Definition of Ready (DoR)

### 4.1 Definition of Ready (DoR)
A User Story enters the sprint only when:
- [x] Clear business value statement adhering to Agile format.
- [x] Unambiguous, testable Acceptance Criteria established.
- [x] Story points estimated collaboratively via Planning Poker.
- [x] Cross-story dependencies resolved.
- [x] Architectural feasibility confirmed by Project Lead (Om Tambe).

### 4.2 Definition of Done (DoD)
A User Story is marked **Done** and releasable only when:
- [x] Code strictly adheres to PEP 8 standards with zero critical linting errors.
- [x] All Pytest automated unit tests pass with a **100% pass rate**.
- [x] Dockerfile builds successfully with multi-stage separation and non-root execution.
- [x] Terraform configuration passes `terraform validate` and `terraform plan`.
- [x] Ansible playbook runs idempotently without unexpected failures (`failed=0`).
- [x] Four Post-Deployment Validation Gates pass on live AWS EC2 host.
- [x] Documentation, API contracts, and README files are fully updated.

---

## 5. Scrum Board Workflow & Sprint Burndown

```
┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│   BACKLOG    │    TO DO     │ IN PROGRESS  │   TESTING    │     DONE     │
├──────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ US-04        │ US-08        │ US-12        │ US-03        │ US-01        │
│ Bulk CSV     │ Elective Reg │ Grade Engine │ Create Std   │ Login Auth   │
│              │              │              │              │              │
│ US-14        │ US-11        │ US-17        │ US-05        │ US-02        │
│ Transcripts  │ Att. Alerts  │ Ansible Play │ Get Std ID   │ RBAC Rules   │
│              │              │              │              │              │
│              │              │              │ US-06        │ US-15        │
│              │              │              │ Filter Stds  │ Dockerfile   │
│              │              │              │              │              │
│              │              │              │              │ US-16        │
│              │              │              │              │ Terraform    │
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

### Sprint Velocity Metrics
- **Sprint 1 Velocity:** 25 Story Points delivered.
- **Sprint 2 Velocity:** 28 Story Points delivered.
- **Total Release Velocity:** 53 Story Points across 4 calendar weeks.

---

## 6. Comparative Study of Agile Frameworks

| Framework | Cadence | Roles | Strengths | Limitations | Project Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Scrum** | 1–4 week sprints | PO, SM, Dev Team | High accountability, predictable delivery, clear ceremony structure. | Rigidity in changing sprint scope mid-iteration. | **SELECTED (Optimal for SU_DevOps)** |
| **Kanban** | Continuous flow | No mandated roles | Highly adaptive, visualizes WIP limits, minimizes cycle time. | Lack of time-boxed release commitments. | Adopted for infrastructure bug fixes |
| **Extreme Programming (XP)** | 1-week iterations | Customer, Devs | Test-Driven Development (TDD), continuous refactoring, pair programming. | High developer intensity, difficult for non-technical clients. | TDD & automated test practices adopted |
| **Lean Development** | Continuous | Flexible | Eliminates waste, optimizes whole value stream, rapid delivery. | Requires high organizational maturity. | Principles applied to lean Docker packaging |
| **Large Scale Scrum (LeSS)** | Multi-team sprint | Single PO, multi-team | Lightweight scaling for 2–8 teams on single backlog. | Coordination challenges when teams exceed 8. | Evaluated for university-wide rollout |
| **Scaled Agile Framework (SAFe)**| Quarterly PI Planning | Release Train Engineer, PMs | Strong enterprise governance across hundreds of engineers. | Heavyweight, bureaucratic overhead. | Deemed excessive for current team size |
| **Scrum@Scale** | Organic scaling | Scrum of Scrums | Scalable network of teams preserving standard Scrum. | Requires experienced Scrum leadership. | Suitable for future multi-campus expansion |

---
*Authored by:*  
**Om Tambe (PRN: 2125UMLM1065)**  
*Sandip University — SU_DevOps Engineering Curriculum*
