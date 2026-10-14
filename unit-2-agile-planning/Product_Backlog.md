# Agile Product Backlog & Story Point Estimation

**Project Name:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  
**Product Owner:** Lead Academic Solutions Strategist  
**Scrum Master:** Agile Delivery Coach  
**Target Release:** Release v1.0.0 (MVP)  
**Estimation Technique:** Planning Poker using Modified Fibonacci Sequence (`1, 2, 3, 5, 8, 13`)  

---

## 1. Product Vision & Backlog Overview

The Product Backlog represents the prioritized single source of requirements for the Student Record and Academic Management Platform. Derived from the Unit 1 Product Engineering specifications (FRS/NFRS), each User Story follows the standard Agile template:

> **"As a [User Role], I want [Capability / Action] so that [Business Benefit / Outcome]."**

Every item includes measurable **Acceptance Criteria**, an estimated **Story Point** weight reflecting complexity, uncertainty, and effort, a **MoSCoW / Business Priority** rating, and allocation to release sprints.

---

## 2. Prioritized Product Backlog Matrix

| Story ID | Epic | User Story | Acceptance Criteria | Story Points | Priority | Sprint Target |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **US-001** | Epic 5: Auth & Security | **As an Administrator**, I want to initialize the project repository with standardized directory layouts, CI workflows, and linting rules so that the team can build code consistently. | • Git repository initialized with Units 1–4 layout.<br>• Automated linting and test workflows configured.<br>• `.gitignore` and base documentation in place. | **3** | High / Must Have | Sprint 1 |
| **US-002** | Epic 5: Auth & Security | **As a Student / Faculty member**, I want to securely log into the platform with my institutional email and password so that I can access my personalized dashboard. | • Secure login endpoint authenticates credentials.<br>• Issues signed JWT with 60-min TTL upon success.<br>• Returns HTTP 401 on invalid credentials with rate limiting. | **5** | High / Must Have | Sprint 1 |
| **US-003** | Epic 5: Auth & Security | **As a User**, I want to request a password reset via a secure one-time link sent to my registered email so that I can regain access if locked out. | • User enters email; system validates existence.<br>• Sends time-limited token valid for 15 minutes.<br>• Resets password with strength validation (min 10 chars). | **3** | Medium / Should Have | Sprint 1 |
| **US-004** | Epic 5: Auth & Security | **As a Security Admin**, I want role-based access control (RBAC) enforced on all endpoints so that students cannot modify grades or attendance. | • Middleware inspects JWT claims (`role`).<br>• Students restricted from faculty/admin endpoints (HTTP 403).<br>• Role permissions strictly enforced in test suite. | **5** | High / Must Have | Sprint 1 |
| **US-005** | Epic 1: Student Management | **As a Registrar**, I want to register a new student record with demographic and academic fields so that their profile is permanently stored. | • Validates `student_id`, legal name, email, department, and semester.<br>• Enforces unique `student_id` and email.<br>• Returns HTTP 201 Created with JSON payload. | **5** | High / Must Have | Sprint 2 |
| **US-006** | Epic 1: Student Management | **As an Academic Advisor**, I want to query a student record by ID so that I can view their current enrollment status and academic standing. | • `GET /api/students/<student_id>` returns student details.<br>• Returns HTTP 200 with schema payload.<br>• Returns HTTP 404 with structured error if ID not found. | **2** | High / Must Have | Sprint 2 |
| **US-007** | Epic 1: Student Management | **As a Faculty Member**, I want to list and filter all registered students by department and semester so that I can review class rosters. | • `GET /api/students` lists all students in database.<br>• Supports query filtering: `?department=CS&semester=3`.<br>• Returns empty list with HTTP 200 when no records match. | **3** | High / Must Have | Sprint 2 |
| **US-008** | Epic 1: Student Management | **As a Registrar**, I want to update student demographic details or academic standing so that their records reflect current statuses. | • `PUT /api/students/<student_id>` updates allowed fields.<br>• Validates input constraints before updating.<br>• Emits audit record tracking modified fields. | **3** | High / Must Have | Sprint 2 |
| **US-009** | Epic 1: Student Management | **As a System Admin**, I want to soft-delete or archive a graduated/withdrawn student record so that historical records remain compliant. | • `DELETE /api/students/<student_id>` marks status as `Archived`.<br>• Disallows physical deletion to protect academic audits.<br>• Returns HTTP 200 confirming archival status. | **3** | Medium / Should Have | Sprint 2 |
| **US-010** | Epic 2: Course Management | **As a Department Chair**, I want to create new courses with course code, title, credits, and capacity so that courses can be scheduled. | • Course code uniqueness enforced (e.g., `CS301`).<br>• Credit hours must be between 1 and 5.<br>• Capacity capped with validation. | **5** | High / Must Have | Sprint 3 |
| **US-011** | Epic 2: Course Management | **As a Student**, I want to enroll in approved courses for my semester so that I can attend classes and earn credits. | • Validates student semester eligibility.<br>• Prevents enrollment if section capacity reached.<br>• Enforces semester credit cap (maximum 24 credits). | **5** | High / Must Have | Sprint 3 |
| **US-012** | Epic 3: Attendance Management | **As a Faculty Member**, I want to record daily lecture attendance for a course section so that attendance records remain up to date. | • Faculty selects course code, lecture date, and section.<br>• Marks each student `Present`, `Absent`, or `Excused`.<br>• Saves records idempotently and returns HTTP 201. | **5** | High / Must Have | Sprint 3 |
| **US-013** | Epic 3: Attendance Management | **As a Student**, I want to view my cumulative attendance percentage per course so that I can maintain the mandatory 75% threshold. | • Calculates real-time percentage: `(Present / Total Sessions) * 100`.<br>• Renders clean visual percentage bar.<br>• Displays clear warning badge if below 75%. | **3** | High / Must Have | Sprint 3 |
| **US-014** | Epic 4: Marks & Performance | **As a Faculty Member**, I want to enter assessment marks (0–100) for students in my course so that grades can be computed. | • `POST /api/marks` validates student enrollment.<br>• Enforces score boundaries between 0.0 and 100.0.<br>• Persists marks and triggers grade point recalculation. | **5** | High / Must Have | Sprint 3 |
| **US-015** | Epic 4: Marks & Performance | **As a Student**, I want to view my published grades, SGPA, and CGPA so that I can monitor my academic progress. | • Calculates letter grade (S, A, B, C, D, E, F) from marks.<br>• Computes weighted SGPA based on course credits.<br>• Renders official breakdown of completed credits. | **5** | High / Must Have | Sprint 3 |
| **US-016** | Epic 6: Notifications | **As an Academic Advisor**, I want the system to trigger automated email/SMS alerts when a student drops below 75% attendance. | • Daily cron checks attendance thresholds.<br>• Dispatches notification payload asynchronously.<br>• Logs alert timestamp in student advisory history. | **3** | Medium / Should Have | Sprint 4 |
| **US-017** | Epic 7: Reporting | **As a Registrar**, I want to generate downloadable PDF semester grade sheets and transcripts for verified students. | • Renders university header, seal, and course table.<br>• Computes cumulative GPA and academic standing.<br>• Digital checksum embedded to prevent forgery. | **5** | Medium / Should Have | Sprint 4 |
| **US-018** | Epic 7: Reporting | **As a Department Chair**, I want to inspect aggregate pass/fail distribution analytics across my department's courses. | • Generates bar chart / summary metrics of grade tiers.<br>• Identifies outlier courses with failure rates > 25%.<br>• Exportable to CSV / Excel format. | **5** | Low / Could Have | Sprint 4 |
| **US-019** | DevOps & Cloud | **As a DevOps Engineer**, I want to containerize the Flask microservice using Docker so that it runs identically across dev, test, and prod. | • Multi-stage Dockerfile built on Python 3.10.<br>• Runs as unprivileged `appuser` exposing port 5000.<br>• Passes container healthcheck `/api/health`. | **5** | High / Must Have | Sprint 2 |
| **US-020** | DevOps & Cloud | **As a Cloud Engineer**, I want to provision AWS VPC, subnet, security group, and EC2 instance via Terraform so that infrastructure is automated. | • Modular HCL provisions VPC 10.1.0.0/16 and Subnet.<br>• Security group configures ports 22, 80, 5000, 8080.<br>• Outputs EC2 public IP and connection strings. | **8** | High / Must Have | Sprint 2 |

---

## 3. Story Point Estimation Reference Scale

Story points are assigned using **Planning Poker** based on complexity, effort, and technical uncertainty:

| Story Points | Complexity Level | Definition & Criteria | Example Task |
| :---: | :--- | :--- | :--- |
| **1** | Very Easy | Trivial change, zero external dependencies, immediate clarity. | Fix typo in error message, update `.gitignore`. |
| **2** | Easy | Straightforward logic, known implementation pattern, minimal testing. | Simple `GET` endpoint retrieval by primary key. |
| **3** | Moderate | Standard feature, basic input validation, standard unit tests required. | Student filtering endpoint, password reset token generator. |
| **5** | Difficult | Multi-table database interactions, business logic, authorization rules. | Mark entry & automatic GPA computation, Docker containerization. |
| **8** | Very Difficult | Complex integration, cross-system dependency, cloud infrastructure. | End-to-end Terraform AWS infrastructure provisioning. |
| **13** | Highly Complex | High architectural uncertainty, distributed system coordination. | Multi-AZ live database replication with automated failover. |

---

## 4. Backlog Prioritization Methodology

Backlog items are prioritized using four critical criteria:
1. **Business & Educational Value:** Capabilities critical to daily academic operations (Authentication, Student Records, Attendance, Marks).
2. **User Impact:** Direct enhancement to student transparency and faculty workload reduction.
3. **Technical Dependencies:** Foundational architectural setup (Repo init, Dockerization, IaC) must precede dependent feature rollouts.
4. **Risk & Complexity:** High-risk architectural decisions are tackled early to prevent late-stage delivery bottlenecks.
