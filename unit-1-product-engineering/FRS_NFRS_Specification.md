# Functional & Non-Functional Requirements Specification (FRS / NFRS)

**Project Name:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  
**Student / Project Lead:** Om Tambe  
**PRN:** 2125UMLM1065  
**Institution:** Sandip University  
**Document Version:** 1.0.0  
**Status:** Approved for Agile Release Planning  

---

## 1. Introduction & Purpose

This document provides the formal software engineering specification for the **Enterprise Student Record & Academic Management Platform**. It details the exact functional behaviors, operational constraints, and non-functional engineering standards required to build, test, containerize, and deploy the application.

---

## 2. Functional Requirements Specification (FRS)

### FR-01: Authentication & Role-Based Access Control (RBAC)
- **FR-01.1:** The system shall authenticate users using email and password credentials, returning signed JSON Web Tokens (JWT) with configurable 60-minute expiration.
- **FR-01.2:** The system shall enforce four distinct operational roles with hierarchical permissions:
  1. **Admin:** Full system governance, user provisioning, audit inspection, and infrastructure telemetry.
  2. **Faculty:** Course roster access, daily attendance entry, and continuous assessment marks entry.
  3. **Student:** Self-service profile inspection, course registration, attendance monitoring, and grade card downloads.
  4. **Exam Cell:** End-semester marks finalization, grade lock enforcement, and official transcript generation.
- **FR-01.3:** Passwords must be hashed using `bcrypt` (work factor 12) with salt generation. Plaintext passwords must never be stored or logged.
- **FR-01.4:** API requests without valid bearer tokens or with insufficient role permissions shall be rejected with HTTP `401 Unauthorized` or HTTP `403 Forbidden`.

### FR-02: Student Registration & Profile Management
- **FR-02.1:** The system shall support single record student registration via JSON payload:
  - Required fields: `student_id` (alphanumeric, 3–20 chars), `name`, `email` (valid university email), `department`, and `semester` (integer between 1 and 12).
- **FR-02.2:** The system shall support **Bulk CSV Registration**:
  - Administrators can upload CSV files containing multiple student records.
  - The system shall validate all rows in a batch transaction, rejecting malformed rows while reporting exact line-level errors.
- **FR-02.3:** Uniqueness of `student_id` and `email` must be strictly enforced, returning HTTP `409 Conflict` on duplicate entries.
- **FR-02.4:** Student lookup must be supported by unique ID (`GET /api/students/<student_id>`) and by filtered queries (`GET /api/students?department=CS&semester=3`).

### FR-03: Course & Elective Management
- **FR-03.1:** Administrators and Department Chairs shall be able to create and manage courses with attributes: Course Code (e.g., `CS301`), Title, Credit Hours (1–5), Department, Max Enrollment Capacity, and Prerequisite Course IDs.
- **FR-03.2:** Course registration logic shall enforce credit boundaries: minimum 12 credits, maximum 24 credits per semester for full-time enrolled students.
- **FR-03.3:** The system shall prevent enrollment when course section capacity is reached and validate that students have cleared all required prerequisite courses.

### FR-04: Attendance Module with Automated Low-Attendance Alerts
- **FR-04.1:** Faculty shall be able to record session-wise attendance marking enrolled students as `Present`, `Absent`, or `Excused`.
- **FR-04.2:** Each attendance transaction shall record Course Code, Lecture Date, Time Slot, Faculty ID, Student ID, and Attendance Status.
- **FR-04.3:** The system shall compute aggregate attendance percentage in real-time using the formula:
  $$\text{Attendance \%} = \left(\frac{\text{Attended Sessions}}{\text{Total Conducted Sessions}}\right) \times 100$$
- **FR-04.4:** **Automated Low-Attendance Flag:** When a student's aggregate attendance falls below **75%**, the system shall automatically set an `attendance_warning: true` flag and generate an alert notification to the student and their designated academic mentor.

### FR-05: Marks & Grade Processing (SGPA / CGPA Engine)
- **FR-05.1:** Faculty shall submit continuous internal evaluation and final examination marks scaled between 0.0 and 100.0.
- **FR-05.2:** The grading engine shall deterministically convert percentage scores into letter grades and 10-point grade points:
  - **90.0 – 100.0%:** Grade `S` / `A+` (Grade Point: 10.0)
  - **80.0 – 89.9%:** Grade `A` (Grade Point: 9.0)
  - **70.0 – 79.9%:** Grade `B` (Grade Point: 8.0)
  - **60.0 – 69.9%:** Grade `C` (Grade Point: 7.0)
  - **50.0 – 59.9%:** Grade `D` (Grade Point: 6.0)
  - **40.0 – 49.9%:** Grade `E` (Grade Point: 5.0)
  - **< 40.0%:** Grade `F` (Grade Point: 0.0 — Fail)
- **FR-05.3:** **SGPA Calculation Engine:** The Semester Grade Point Average is computed dynamically as:
  $$\text{SGPA} = \frac{\sum (\text{Course Credits} \times \text{Grade Points})}{\sum \text{Course Credits}}$$
- **FR-05.4:** **CGPA Calculation Engine:** Cumulative Grade Point Average aggregates all completed semester credits across the student's academic history. If CGPA falls below 5.0, the student's status is automatically updated to `Academic Warning`.

### FR-06: Official Report & Transcript Generation
- **FR-06.1:** The platform shall generate digitally signed semester grade reports containing university emblems, student metadata, course-wise letter grades, SGPA, CGPA, and official clearance seals.
- **FR-06.2:** Grade records become immutable once finalized and locked by the Examination Cell; changes require documented administrative audit authorization.

---

## 3. Non-Functional Requirements Specification (NFRS)

### NFR-01: Performance
- **NFR-01.1:** The API shall achieve a 95th percentile (p95) response latency of **under 1.5 seconds** under a standard concurrent load of **1,000 active users**.
- **NFR-01.2:** Healthcheck probes (`GET /api/health`) must return HTTP 200 within **50 milliseconds**.
- **NFR-01.3:** Database indexing must be configured on primary lookup columns (`student_id`, `email`, `department`, `course_code`).

### NFR-02: Security
- **NFR-02.1: Data at Rest:** All persistent database stores and cloud storage volumes (AWS EBS gp3 root volumes and S3 backup buckets) must be encrypted using **AES-256**.
- **NFR-02.2: Data in Transit:** All network communication between web browsers, reverse proxies, and microservices must be encrypted using **TLS 1.3** (minimum TLS 1.2).
- **NFR-02.3: Credential Security:** User passwords must be hashed with **bcrypt** (work factor 12) with random per-user salt.
- **NFR-02.4: OWASP Compliance:** The application must enforce parameterized SQL queries, strict JSON input sanitization, and CORS headers to prevent SQL Injection (SQLi) and Cross-Site Scripting (XSS).

### NFR-03: Availability & Fault Tolerance
- **NFR-03.1:** The application shall maintain a **99.9% uptime target** during operational semesters (total unscheduled downtime < 43 minutes/month).
- **NFR-03.2:** The container runtime must execute continuous health checks (`HEALTHCHECK`) with automatic restart policies (`restart: always`).
- **NFR-03.3:** Mean Time to Recovery (MTTR) must be under 10 minutes using automated Terraform re-provisioning and Ansible playbook re-runs.

### NFR-04: Usability & Accessibility
- **NFR-04.1:** Web interfaces must adhere to **WCAG 2.1 Level AA** accessibility standards, supporting screen readers, keyboard navigation, and minimum 4.5:1 color contrast ratios.
- **NFR-04.2:** User interfaces must be responsive across mobile (375px+), tablet, and desktop viewports.
- **NFR-04.3:** Clear, descriptive error messages must accompany every non-200 HTTP response.

### NFR-05: Scalability & DevOps Maintainability
- **NFR-05.1:** The microservice architecture must follow Twelve-Factor App principles, storing all configuration in environment variables.
- **NFR-05.2:** Cloud infrastructure must support horizontal scaling behind Nginx reverse proxy buffering and AWS Elastic Load Balancing.
- **NFR-05.3:** Infrastructure and server configuration must be 100% codified using HashiCorp Terraform and Ansible without manual intervention.

---

## 4. Verification & Traceability Matrix

| Requirement | Module | Verification Method | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **FR-01** | Auth & RBAC | Automated Integration Test | Valid JWT grants access; invalid credentials return HTTP 401; unauthorized roles return HTTP 403. |
| **FR-02** | Student Registration | Pytest Suite (`test_app.py`) | Single record returns HTTP 201; duplicates return HTTP 409; invalid emails return HTTP 400. |
| **FR-04** | Attendance (<75%) | Automated Unit Test | When attendance ratio < 0.75, `attendance_warning` evaluates to `true`. |
| **FR-05** | Grading Engine | Pytest Suite (`test_app.py`) | Deterministic mapping: 95% = S (10.0), 85% = A (9.0), 35% = F (0.0). |
| **NFR-01** | Latency (<1.5s) | Apache Bench / Locust Load Test | P95 latency < 1.5 seconds across 1,000 concurrent threads. |
| **NFR-02** | AES-256 Encryption | AWS S3 CLI Inspection | `aws s3api get-bucket-encryption` confirms `SSEAlgorithm: AES256`. |
| **NFR-03** | 99.9% Availability | `/api/health` Liveness Probe | Probe consistently returns `{"status": "healthy"}` with HTTP 200. |

---
*Submitted by:*  
**Om Tambe (PRN: 2125UMLM1065)**  
*Sandip University — SU_DevOps Engineering Program*
