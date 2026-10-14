# Functional & Non-Functional Requirements Specification (FRS / NFRS)

**Project Name:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  
**Document Version:** 1.0.0  
**Status:** Approved for Agile Release Planning  
**Domain:** Higher Education Academic ERP & Student Lifecycle Management  

---

## 1. Executive Summary & System Scope

The **Enterprise Student Record & Academic Management Platform** is a scalable, cloud-native web system designed to modernize and unify university academic operations. Legacy academic administration suffers from fragmented paper records, manual spreadsheet-based grade entry, disconnected attendance logging, and sluggish response times during peak enrollment windows. 

This specification defines the functional behaviors, operational boundaries, security baselines, and quality metrics governing the core platform.

### 1.1 Core System Objectives
- Provide centralized, tamper-resistant management of student profiles, enrollments, course catalogs, attendance records, and academic evaluations.
- Support role-based self-service for Students, Faculty, Department Chairs, Examination Controllers, and System Administrators.
- Guarantee sub-second response times, zero data loss, audit compliance, and seamless multi-tier cloud deployment using DevOps automation.

---

## 2. Stakeholders & Role-Based Access Control (RBAC) Matrix

| Role | Description | Core Capabilities |
| :--- | :--- | :--- |
| **Student** | Enrolled undergraduate/graduate student | View personal profile, register for courses, inspect daily attendance, view marks/grades, download academic transcripts. |
| **Faculty Member** | Instructor delivering courses | Take session-wise attendance, record continuous assessments and exam marks, view roster, flag at-risk students. |
| **Department Chair** | Head of academic department | Approve course offerings, review department-wide grade distributions, assign faculty to course sections. |
| **Registrar / Exam Cell** | Academic records controller | Publish semester results, issue official transcripts, enforce academic suspension/good standing criteria, audit grade changes. |
| **System Administrator** | DevOps & Cloud Operations | Manage user provisioning, configure OAuth/JWT settings, monitor system health, inspect audit logs, manage backups. |

### Role Permissions Grid

| Functional Capability | Student | Faculty | Department Chair | Registrar | System Admin |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Authenticate / Reset Password | ✅ | ✅ | ✅ | ✅ | ✅ |
| View Own Student Record | ✅ | ❌ | ❌ | ❌ | ❌ |
| View Assigned Course Rosters | ❌ | ✅ | ✅ | ✅ | ✅ |
| Create / Edit Student Records | ❌ | ❌ | ❌ | ✅ | ✅ |
| Course Catalog Creation | ❌ | ❌ | ✅ | ✅ | ✅ |
| Submit Daily Attendance | ❌ | ✅ | ❌ | ❌ | ✅ |
| Enter Assessment Marks | ❌ | ✅ | ❌ | ❌ | ✅ |
| Finalize & Lock Semester Grades| ❌ | ❌ | ✅ | ✅ | ❌ |
| Generate Official Transcripts | ❌ | ❌ | ❌ | ✅ | ✅ |
| Infrastructure & Service Health | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 3. Functional Requirements Specification (FRS)

### 3.1 Module 1: Authentication & Identity Management
- **FR-1.1:** The system shall authenticate users using secure credentials (email/password) and issue cryptographically signed JSON Web Tokens (JWT) with configurable expiry (default: 60 minutes).
- **FR-1.2:** The system shall enforce role-based access control (RBAC), rejecting unauthorized API requests with HTTP `403 Forbidden`.
- **FR-1.3:** The platform shall support self-service password reset via one-time cryptographically secure verification tokens sent to registered university email addresses.
- **FR-1.4:** Passwords must meet NIST SP 800-63B standards: minimum 10 characters, requiring uppercase, lowercase, numerical, and special characters. Passwords must be hashed using `bcrypt` (work factor 12) or `Argon2id`.
- **FR-1.5:** The system shall automatically terminate idle sessions after 15 minutes of inactivity and invalidate invalidated tokens against a distributed blacklist (Redis).

### 3.2 Module 2: Student Records Management
- **FR-2.1:** The system shall maintain an immutable, unique Student Identification Number (`student_id`, e.g., `STD2026001`) for each enrolled student.
- **FR-2.2:** Each student profile must record: Full Legal Name, University Email, Department/Branch, Current Semester (1–12), Enrolled Credits, Cumulative Grade Point Average (CGPA), and Academic Standing (`Good Standing`, `Academic Probation`, `Suspended`, `Graduated`).
- **FR-2.3:** The system must provide REST endpoints to create, retrieve, search, filter (by department, semester, academic standing), and archive student records.
- **FR-2.4:** Student record creation shall validate email uniqueness, standard telephone format, and valid semester constraints.
- **FR-2.5:** Soft deletion must be implemented; student historical records and audit logs must be retained for compliance purposes.

### 3.3 Module 3: Course Management & Enrollment
- **FR-3.1:** The system shall allow authorized administrators and chairs to define courses with: Course Code (e.g., `CS301`), Title, Credit Hours (1–5), Department, Max Capacity, and Prerequisites.
- **FR-3.2:** Course registration logic shall prevent enrollment if the course capacity is reached or if the student has not completed mandatory prerequisite courses with passing marks.
- **FR-3.3:** The system shall enforce an enrollment credit boundary: minimum 12 credits, maximum 24 credits per semester for full-time students.
- **FR-3.4:** Students shall be permitted to add or drop courses within a designated add/drop window governed by academic calendar timestamps.

### 3.4 Module 4: Attendance Management
- **FR-4.1:** Faculty shall be able to record session attendance for enrolled students marked as `Present`, `Absent`, or `Excused`.
- **FR-4.2:** Attendance records must store: Course Code, Session Date, Time Block, Faculty ID, Student ID, and Attendance Status.
- **FR-4.3:** The system shall automatically compute aggregate attendance percentages per student per course in real-time.
- **FR-4.4:** When a student's attendance drops below 75%, the platform must generate an automated low-attendance warning alert to the student and their designated academic advisor.
- **FR-4.5:** Attendance records for past dates shall be locked from retroactive alteration unless approved by the Department Chair with an accompanying audit justification.

### 3.5 Module 5: Marks & Academic Performance
- **FR-5.1:** The system shall support weighted continuous internal assessment (quizzes, assignments, mid-terms) and end-semester examinations.
- **FR-5.2:** Faculty shall enter assessment marks scaled between 0 and 100 with validation rejecting values outside numerical bounds or non-numeric inputs.
- **FR-5.3:** The system shall automatically compute letter grades and grade points based on standardized university grading scales:
  - 90–100%: Grade **S / A+** (10.0)
  - 80–89%: Grade **A** (9.0)
  - 70–79%: Grade **B** (8.0)
  - 60–69%: Grade **C** (7.0)
  - 50–59%: Grade **D** (6.0)
  - 40–49%: Grade **E** (5.0)
  - < 40%: Grade **F** (0.0)
- **FR-5.4:** The system shall calculate Semester Grade Point Average (SGPA) and Cumulative Grade Point Average (CGPA) automatically upon grade finalization.
- **FR-5.5:** The platform shall generate exportable student report cards and official transcripts in digitally signed PDF format.

### 3.6 Module 6: Notification & Reporting
- **FR-6.1:** System shall generate asynchronous notifications for attendance warnings, exam schedule publications, and grade postings.
- **FR-6.2:** Administrative reporting engine shall export analytics on department-wide grade distributions, student retention rates, and course enrollment density.

---

## 4. Non-Functional Requirements Specification (NFRS)

### 4.1 Security & Compliance
- **NFR-SEC-1:** All communication between clients, reverse proxies, and microservices must be encrypted using TLS 1.3 in transit.
- **NFR-SEC-2:** Sensitive data at rest (database storage volumes, S3 backup buckets) must be encrypted using AES-256 (AWS KMS or standard envelope encryption).
- **NFR-SEC-3:** All API endpoints must protect against OWASP Top 10 vulnerabilities (SQL Injection, Cross-Site Scripting, Insecure Direct Object References, Broken Object Level Authorization).
- **NFR-SEC-4:** Rate limiting must be enforced at the API gateway / reverse proxy level: maximum 100 requests per minute per IP for public endpoints; 600 requests per minute for authenticated sessions.
- **NFR-SEC-5:** An immutable security audit log must capture every state-mutating transaction (`POST`, `PUT`, `DELETE`), including User ID, timestamp, IP address, and payload delta.

### 4.2 Performance & Scalability
- **NFR-PERF-1:** API latency for all read requests (`GET /api/students`, `GET /api/health`) must have a 95th percentile (p95) response time under 150 milliseconds under standard load.
- **NFR-PERF-2:** State-altering operations (`POST /api/students`, mark uploads) must complete within 300 milliseconds.
- **NFR-PERF-3:** The architecture must horizontally scale compute workers to support up to 5,000 concurrent active users during peak semester enrollment and grade release days.
- **NFR-PERF-4:** Database queries must utilize composite indexing on frequently queried columns (`student_id`, `department`, `course_code`).

### 4.3 Availability & Fault Tolerance
- **NFR-AVAIL-1:** The platform shall provide 99.9% uptime during operational academic semesters (unscheduled downtime < 43 minutes/month).
- **NFR-AVAIL-2:** The application must implement liveness (`/api/health`) and readiness health probes for automated self-healing container restarts.
- **NFR-AVAIL-3:** Mean Time to Recovery (MTTR) must be less than 15 minutes through automated container orchestration and cloud infrastructure redeployment via Terraform and Ansible.
- **NFR-AVAIL-4:** Automated backups of persistent database stores must occur daily with S3 cross-region versioning and a Recovery Point Objective (RPO) of < 1 hour.

### 4.4 Maintainability, Portability & DevOps
- **NFR-DEV-1:** The backend application must adhere strictly to the Twelve-Factor App methodology, separating configuration from code via environment variables.
- **NFR-DEV-2:** The microservice must be packaged into an OCI-compliant lightweight Docker image based on Alpine Linux or Debian-slim, keeping production image size under 200MB.
- **NFR-DEV-3:** Automated unit and integration test coverage must exceed 85%, verified through Pytest in continuous integration pipelines.
- **NFR-DEV-4:** Infrastructure must be 100% reproducible through declarative code (HashiCorp Terraform) and idempotent configuration playbooks (Ansible) without manual "ClickOps" dependencies.

---

## 5. Traceability & Acceptance Verification Matrix

| Requirement ID | Module / Category | Verification Method | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **FR-1.1 / 1.2** | Auth / RBAC | Automated Integration Test | Unauthorized calls yield HTTP 401/403; valid token returns HTTP 200. |
| **FR-2.1 / 2.3** | Student Management | Pytest Unit Tests (`test_app.py`)| Correct status codes: 200 (list/get), 201 (created), 404 (not found). |
| **FR-4.4** | Attendance Alerts | Event-driven functional test | Attendance < 75% triggers alert payload in message queue. |
| **FR-5.3** | Grading System | Deterministic unit tests | Verified marks-to-grade mapping across all boundary conditions. |
| **NFR-SEC-1** | TLS & Encryption | SSL Labs / OpenSSL scan | Only TLS 1.2 / 1.3 accepted; all HTTP redirects to HTTPS. |
| **NFR-PERF-1** | API Latency | Apache Bench / Locust load test | P95 latency < 150ms over 1,000 concurrent iterations. |
| **NFR-DEV-2** | Dockerization | Docker CLI inspection | Production image builds successfully, runs as non-root user, size < 200MB. |
| **NFR-DEV-4** | IaC Automation | Terraform Plan & Ansible Playbook| Zero syntax errors, clean provisioning on AWS EC2 with reverse proxy. |

---
*Signed and Approved by:*  
**Chief Technical Architect & Lead DevOps Engineer**  
*SU_DevOps Engineering Curriculum*
