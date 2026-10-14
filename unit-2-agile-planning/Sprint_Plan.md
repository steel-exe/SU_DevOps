# Agile Sprint Execution Plan & Scrum Framework

**Project Name:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  
**Sprint Cadence:** 2-Week Sprints (10 Working Days per Sprint)  
**Team Composition:** 1 Product Owner, 1 Scrum Master, 3 Full-Stack Developers, 1 QA Engineer, 1 DevOps Engineer  
**Document Version:** 1.0.0  

---

## 1. Scrum Team Roles & Responsibilities

```
                      ┌────────────────────────────────────────┐
                      │             PRODUCT OWNER              │
                      │  * Backlog Prioritization & Vision     │
                      │  * Acceptance Criteria Verification    │
                      └──────────────────┬─────────────────────┘
                                         │
                      ┌──────────────────▼─────────────────────┐
                      │              SCRUM MASTER              │
                      │  * Facilitates Scrum Ceremonies        │
                      │  * Removes Technical Impediments      │
                      └──────────────────┬─────────────────────┘
                                         │
         ┌───────────────────────────────┴───────────────────────────────┐
         │                               │                               │
┌────────▼───────────────┐   ┌───────────▼────────────┐   ┌──────────────▼────────┐
│  DEVELOPMENT TEAM (3)  │   │    QA AUTOMATION (1)   │   │  DEVOPS ENGINEER (1)  │
│  * Flask Microservice  │   │  * Pytest Unit & Int.  │   │  * Docker Packaging   │
│  * Domain Models & API │   │  * API Performance     │   │  * Terraform & Ansible│
└────────────────────────┘   └────────────────────────┘   └───────────────────────┘
```

| Role | Assigned Name | Core Responsibilities |
| :--- | :--- | :--- |
| **Product Owner** | Maya Sen | Owns product vision, manages and prioritizes the Product Backlog, signs off on User Stories, liaises with university registrar and faculty stakeholders. |
| **Scrum Master** | David Chen | Shields the development team from external disruptions, facilitates Daily Standups, Sprint Planning, Reviews, and Retrospectives, enforces Agile principles. |
| **Backend Engineer 1** | Priya Sharma | Implements Flask REST API endpoints, domain models (`models.py`), schema validations, and database interactions. |
| **Backend Engineer 2** | Alex Rivera | Builds grading logic, attendance calculations, GPA algorithms, and error-handling middlewares. |
| **Frontend/API Dev** | Rohan Das | Develops API contract schemas, OpenAPI documentation, and client-side testing fixtures. |
| **QA Automation** | Ananya Verma | Author of Pytest unit and integration test suite (`tests/test_app.py`), validates acceptance criteria, conducts smoke testing. |
| **DevOps Specialist** | Shivraj K | Authors multi-stage Dockerfile, HashiCorp Terraform AWS IaC modules, and Ansible idempotent playbooks. |

---

## 2. Sprint 1 Execution Plan: Foundation, Auth & Project Setup

- **Sprint Goal:** Establish repository foundation, continuous integration, user authentication architecture, and core project containerization setup.
- **Sprint Duration:** Weeks 1–2 (10 Working Days)
- **Target Velocity / Capacity:** 20 Story Points (160 Total Engineering Hours)

### 2.1 Sprint 1 Backlog & Detailed Task Breakdown

| Story ID | Task ID | Task Description | Assignee | Est. Hours | Status |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **US-001** | T-101 | Initialize Git repository with Units 1–4 folder structure and `.gitignore`. | Shivraj K | 4h | Done |
| **US-001** | T-102 | Create Unit 1 FRS, NFRS, and Design Thinking architecture documentation. | Maya Sen | 12h | Done |
| **US-001** | T-103 | Configure Python virtual environment, `requirements.txt`, and Pytest test runner. | Priya Sharma | 6h | Done |
| **US-002** | T-104 | Implement password hashing helper utilities using `bcrypt` and salt generation. | Alex Rivera | 8h | Done |
| **US-002** | T-105 | Build JWT token generation and authorization header validation decorator. | Priya Sharma | 12h | Done |
| **US-002** | T-106 | Implement `/api/auth/login` endpoint with credential verification and rate limit. | Alex Rivera | 10h | Done |
| **US-003** | T-107 | Design time-expiring one-time password reset token mechanism. | Rohan Das | 8h | Done |
| **US-004** | T-108 | Implement Role-Based Access Control (RBAC) middleware for Student vs. Faculty. | Priya Sharma | 10h | Done |
| **US-004** | T-109 | Author Pytest tests for unauthorized (`401`) and forbidden (`403`) access cases. | Ananya Verma | 10h | Done |
| **US-019** | T-110 | Author lightweight multi-stage Dockerfile with non-root security execution. | Shivraj K | 8h | Done |
| **US-001** | T-111 | Setup `/api/health` heartbeat endpoint for container health probes. | Rohan Das | 4h | Done |

### 2.2 Sprint 1 Scrum Ceremonies Simulation Log

#### Daily Scrum Sample (Sprint 1, Day 4):
- **Priya Sharma (Backend):**
  - *Yesterday:* Completed JWT token decorator logic and claims extraction.
  - *Today:* Integrating RBAC decorator with the `/api/students` route handlers.
  - *Blockers:* None; waiting for QA to review the mock payload fixtures.
- **Ananya Verma (QA):**
  - *Yesterday:* Wrote 8 unit test cases for password hashing and invalid login boundaries.
  - *Today:* Automating token expiration tests with Pytest fixtures.
  - *Blockers:* None.
- **Shivraj K (DevOps):**
  - *Yesterday:* Tested Docker container build on `python:3.10-slim`.
  - *Today:* Adding non-root user `appuser` and validating healthcheck directive.
  - *Blockers:* None.

#### Sprint 1 Review & Demo:
- Demonstrated live containerized Flask application running locally on port 5000.
- Successfully demonstrated `/api/health` returning `{"status": "UP"}`.
- Simulated JWT authentication flow rejecting invalid credentials and generating valid tokens.
- **Sprint 1 Retrospective:**
  - *What went well:* Early containerization prevented dependency discrepancies across developer machines.
  - *What can improve:* Mock data generation needs to be standardized across models to speed up unit test creation.

---

## 3. Sprint 2 Execution Plan: Student Management & Infrastructure Automation

- **Sprint Goal:** Implement the complete Student Records REST API, validation logic, Pytest verification suite, and automated AWS Cloud deployment using Terraform & Ansible.
- **Sprint Duration:** Weeks 3–4 (10 Working Days)
- **Target Velocity / Capacity:** 26 Story Points (180 Total Engineering Hours)

### 3.1 Sprint 2 Backlog & Detailed Task Breakdown

| Story ID | Task ID | Task Description | Assignee | Est. Hours | Status |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **US-005** | T-201 | Build `Student` domain model (`app/models.py`) with strict validation rules. | Priya Sharma | 8h | Done |
| **US-005** | T-202 | Implement `POST /api/students` endpoint returning HTTP 201 on success. | Priya Sharma | 10h | Done |
| **US-006** | T-203 | Implement `GET /api/students/<student_id>` with HTTP 200/404 handling. | Alex Rivera | 6h | Done |
| **US-007** | T-204 | Implement `GET /api/students` with query parameter filtering (department, semester). | Alex Rivera | 8h | Done |
| **US-014** | T-205 | Build `POST /api/students/<id>/marks` for academic performance and GPA update. | Rohan Das | 10h | Done |
| **US-005** | T-206 | Author comprehensive Pytest suite (`tests/test_app.py`) covering all status codes. | Ananya Verma | 14h | Done |
| **US-020** | T-207 | Write Terraform configuration (`main.tf`, `variables.tf`, `outputs.tf`) for AWS VPC & EC2. | Shivraj K | 16h | Done |
| **US-020** | T-208 | Configure AWS Security Group opening ports 22 (SSH), 80 (HTTP), 5000, and 8080. | Shivraj K | 6h | Done |
| **US-020** | T-209 | Author Ansible playbook (`playbook.yml`) installing Docker, Nginx, and deploying container. | Shivraj K | 16h | Done |
| **US-020** | T-210 | Configure Ansible inventory (`inventory.ini`) and Nginx reverse proxy to port 5000. | Shivraj K | 8h | Done |
| **US-005** | T-211 | Execute end-to-end smoke test gate verifying live API health on AWS EC2. | Team | 6h | Done |

### 3.2 Sprint 2 Scrum Ceremonies Simulation Log

#### Daily Scrum Sample (Sprint 2, Day 7):
- **Priya Sharma (Backend):**
  - *Yesterday:* Completed model validation rejecting empty IDs and malformed emails.
  - *Today:* Connecting in-memory and persistence layer to the Flask route blueprint.
  - *Blockers:* None.
- **Shivraj K (DevOps):**
  - *Yesterday:* Tested Terraform provisioning of AWS VPC (10.1.0.0/16) and Security Group.
  - *Today:* Authoring Ansible reverse proxy configuration templating Nginx to forward port 80 to container port 5000.
  - *Blockers:* Needed confirmed list of security group ports (22, 80, 5000, 8080)—now resolved.

---

## 4. Definition of Done (DoD) & Definition of Ready (DoR)

### 4.1 Definition of Ready (DoR)
A User Story is marked **Ready** for Sprint Backlog inclusion only if:
- [x] Written in standard format with clear business rationale.
- [x] Acceptance Criteria are explicitly defined, unambiguous, and testable.
- [x] Dependencies on external systems or prior stories are resolved.
- [x] Story points estimated collaboratively via Planning Poker.
- [x] Story size fits comfortably within a single sprint duration (< 8 points).

### 4.2 Definition of Done (DoD)
A User Story is marked **Done** and releasable only if:
- [x] Code adheres to PEP 8 Python coding standards and has passed static linting.
- [x] All unit and integration tests execute cleanly with 100% pass rate in Pytest.
- [x] Code test coverage exceeds 85% with zero regressions.
- [x] Dockerfile builds cleanly without root privilege execution.
- [x] Peer code review approved by at least one Senior Engineer.
- [x] Documentation, API contracts, and README files are updated.
- [x] Verified in a production-identical staging environment.

---

## 5. Scrum Board Workflow & Visual Representation

```
┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│   BACKLOG    │    TO DO     │ IN PROGRESS  │   TESTING    │     DONE     │
├──────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ US-010       │ US-008       │ US-014       │ US-005       │ US-001       │
│ Add Course   │ Update Std   │ Add Marks    │ Create Std   │ Project Setup│
│              │              │              │              │              │
│ US-011       │ US-009       │ US-020       │ US-006       │ US-002       │
│ Enroll Std   │ Archive Std  │ Ansible Play │ Get Std by ID│ Login Auth   │
│              │              │              │              │              │
│ US-012       │ US-013       │              │ US-007       │ US-019       │
│ Attendance   │ Att. View    │              │ Filter Stds  │ Dockerfile   │
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 6. Sprint Velocity & Burndown Projections

```
Story
Points
  30 ┼───●
     │    \
  25 ┼     \
     │      ●
  20 ┼       \
     │        \
  15 ┼         ●
     │          \
  10 ┼           \
     │            ●
   5 ┼             \
     │              \
   0 ┼───┴───┴───┴───┴──●────
     D1  D3  D5  D7  D9 D10   (Days)
     ─── Actual Remaining Points   ┈┈┈ Ideal Burn
```

- **Sprint 1 Velocity:** 20 Story Points completed.
- **Sprint 2 Velocity:** 26 Story Points completed.
- **Total Release Velocity:** 46 Story Points across 4 calendar weeks.

---

## 7. Comparative Study of Agile Frameworks

To determine the optimal engineering methodology for the Student Record and Academic Management Platform, we evaluated 7 industry-recognized Agile frameworks:

| Agile Framework | Core Mechanism | Strengths | Limitations | Best Fit For | Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Scrum** | Time-boxed iterations (1–4 wk sprints), designated roles (PO, SM, Dev), 4 ceremonies. | Predictable cadence, clear accountability, excellent team transparency. | Scope change overhead during active sprint. | Small-to-medium cross-functional teams (5–9 people) with evolving feature scopes. | **SELECTED (Optimal for SU_DevOps)** |
| **Kanban** | Continuous flow, visual work-in-progress (WIP) limits, cycle time optimization. | Highly flexible, minimizes context switching, excellent for support/maintenance. | Lack of fixed release commitments, no time-boxed accountability. | Maintenance teams, IT operations, continuous bug-fixing teams. | **Adopted for DevOps Ops** |
| **Extreme Programming (XP)** | Test-Driven Development (TDD), Pair Programming, Continuous Refactoring. | Uncompromising code quality, immediate regression detection. | High developer fatigue, resistance from non-technical stakeholders. | High-risk algorithmic engineering, mission-critical systems. | **Engineering Practices Integrated** |
| **Lean Development** | Eliminate waste, amplify learning, deliver as fast as possible. | Lean resource utilization, hyper-focused on customer value. | Requires deeply mature organizational discipline. | Early-stage startup MVP hypothesis validation. | **Principles Adopted** |
| **Large Scale Scrum (LeSS)** | Scales standard Scrum across 2–8 teams working on a single product backlog. | Minimal management overhead, preserves true Scrum essence. | Complex backlog synchronization when teams exceed 8. | Mid-size multi-team product expansions (20–60 devs). | Evaluated for Future Phase |
| **Scaled Agile Framework (SAFe)** | Highly structured enterprise framework with PI Planning, ARTs, and portfolio tiers. | Strong governance, aligns hundreds of developers to corporate goals. | Heavyweight, bureaucratic, expensive certification overhead. | Large enterprises (500+ developers), defense, banking institutions. | Overkill for current scope |
| **Scrum@Scale** | Modular network of Scrum teams coordinating through Scrum of Scrums (SoS). | Highly scalable, preserves organic team agility without SAFe bureaucracy. | Requires experienced Scrum practitioners to avoid governance drift. | Fast-scaling technology organizations. | Evaluated for Campus-wide rollout |

### Conclusion & Recommendation:
**Scrum** supplemented by **Extreme Programming (XP)** engineering practices (automated Pytest suites, TDD, and CI/CD pipelines) was chosen as the most suitable framework for the Student Record Platform. It delivers strict sprint accountability while maintaining rapid adaptability to university stakeholder feedback.
