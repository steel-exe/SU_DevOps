# Agile Product Backlog & Story Point Estimation

**Project Name:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  
**Student / Project Lead:** Om Tambe (PRN: 2125UMLM1065)  
**Academic Institution:** Sandip University  
**Target Release:** Release v1.0.0 (MVP)  
**Estimation Scale:** Modified Fibonacci Planning Poker (`1, 2, 3, 5, 8, 13`)  

---

## 1. Product Backlog Overview & Strategic Alignment

The Product Backlog is the authoritative, prioritized registry of functional requirements for the **Enterprise Student Record & Academic Management Platform**. Authored by **Om Tambe (PRN: 2125UMLM1065)**, each story translates the Unit 1 FRS/NFRS specifications into an executable Agile format:

> **"As a [User Persona], I want to [Perform Action] so that [Achieve Business Value]."**

Every User Story is accompanied by concrete **Acceptance Criteria**, an estimated **Story Point** weight based on technical complexity and uncertainty, and a **MoSCoW / Business Priority** classification.

---

## 2. Epics Breakdown

The system is decomposed into six core functional Epics and one cross-cutting DevOps Enablement Epic:
1. **Epic 1: Authentication & Role-Based Access Control (RBAC)**
2. **Epic 2: Student Management & Profile Administration**
3. **Epic 3: Attendance Management & Warning Alerts**
4. **Epic 4: Course & Elective Management**
5. **Epic 5: Marks & Grading Processing Engine**
6. **Epic 6: Reporting & Official Transcript Generation**
7. **Epic 7: DevOps Infrastructure Automation & Cloud Deployment**

---

## 3. Prioritized Product Backlog Matrix

| Story ID | Epic | User Story | Acceptance Criteria | Story Points | Priority | Target Sprint |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **US-01** | Epic 1: Auth & RBAC | **As a Student / Faculty member**, I want to securely log into the portal with my email and password so that I can access my authorized role dashboard. | • Valid credentials issue signed JWT with 60-min TTL.<br>• Password verified against bcrypt hash.<br>• Invalid credentials return HTTP 401 Unauthorized with descriptive JSON error. | **5** | Must Have / High | Sprint 1 |
| **US-02** | Epic 1: Auth & RBAC | **As an Administrator**, I want role-based access control (RBAC) enforced on all endpoints so that students cannot modify attendance or grades. | • JWT claims (`role`) verified via decorator/middleware.<br>• Unauthorized role requests yield HTTP 403 Forbidden.<br>• Four roles enforced: Admin, Faculty, Student, Exam Cell. | **5** | Must Have / High | Sprint 1 |
| **US-03** | Epic 2: Student Management | **As an Administrator**, I want to register a new student record with demographic and academic fields so that their profile is recorded. | • Validates `student_id`, name, university email, department, semester (1–12).<br>• Enforces uniqueness on ID and email (HTTP 409 on duplicates).<br>• Returns HTTP 201 Created with JSON payload. | **5** | Must Have / High | Sprint 1 |
| **US-04** | Epic 2: Student Management | **As an Administrator**, I want to upload a bulk CSV file containing student records so that hundreds of students can be onboarded in one batch. | • Parses standard UTF-8 CSV with validation on each row.<br>• Rollback transaction if critical headers missing.<br>• Returns total processed, succeeded, and detailed line-level error list. | **8** | Should Have / Medium | Sprint 2 |
| **US-05** | Epic 2: Student Management | **As an Academic Advisor**, I want to query a student record by ID so that I can review their academic status and contact details. | • `GET /api/students/<student_id>` returns full student profile.<br>• Returns HTTP 200 with schema payload.<br>• Non-existent ID returns HTTP 404 with structured error message. | **2** | Must Have / High | Sprint 1 |
| **US-06** | Epic 2: Student Management | **As a Faculty Member**, I want to retrieve and filter registered students by department and semester so that I can review course enrollments. | • `GET /api/students` lists all students.<br>• Query parameters supported: `?department=CS&semester=3`.<br>• Empty match returns HTTP 200 with `count: 0`. | **3** | Must Have / High | Sprint 1 |
| **US-07** | Epic 4: Course Management | **As a Department Chair**, I want to define new courses with course codes, credits, and seat limits so that courses are offered for the semester. | • Course code uniqueness enforced (e.g., `CS301`).<br>• Credit hours validated between 1 and 5.<br>• Capacity capped with validation. | **5** | Must Have / High | Sprint 2 |
| **US-08** | Epic 4: Course Management | **As a Student**, I want to register for approved elective courses within credit boundaries so that I can fulfill graduation requirements. | • Validates minimum 12 and maximum 24 credits per semester.<br>• Prevents enrollment if course capacity reached.<br>• Validates completion of prerequisite courses. | **5** | Should Have / Medium | Sprint 2 |
| **US-09** | Epic 3: Attendance | **As a Faculty Member**, I want to mark session-wise student attendance so that daily lecture attendance is accurately maintained. | • Faculty selects course code, session date, and section.<br>• Marks each enrolled student `Present`, `Absent`, or `Excused`.<br>• Saves records idempotently and returns HTTP 201. | **5** | Must Have / High | Sprint 2 |
| **US-10** | Epic 3: Attendance | **As a Student**, I want to view my real-time aggregate attendance percentage per course so that I can track my standing against the 75% rule. | • Calculates percentage: `(Attended / Total Sessions) * 100`.<br>• Displays clear warning badge if attendance falls below 75%.<br>• Renders clean mobile-friendly percentage bar. | **3** | Must Have / High | Sprint 2 |
| **US-11** | Epic 3: Attendance | **As an Academic Advisor**, I want automated warning flags triggered for students below 75% attendance so that intervention occurs before exams. | • Daily cron evaluates attendance ratios across all sections.<br>• Sets `attendance_warning: true` flag on student profile.<br>• Sends email alert payload to student and mentor. | **5** | Should Have / Medium | Sprint 2 |
| **US-12** | Epic 5: Grading Engine | **As a Faculty Member**, I want to enter continuous assessment and exam marks (0–100) so that student performance is recorded. | • Validates scores strictly between 0.0 and 100.0 (HTTP 400 on error).<br>• `POST /api/students/<id>/marks` maps score to letter grade (S, A, B, C, D, E, F).<br>• Assigns 10-point grade points and recalculates GPA. | **5** | Must Have / High | Sprint 2 |
| **US-13** | Epic 5: Grading Engine | **As a Student**, I want to inspect my calculated SGPA and CGPA so that I can verify my semester grade point average. | • SGPA calculated as weighted sum of credits × grade points.<br>• CGPA computed cumulatively across completed semesters.<br>• Flags `Academic Warning` if CGPA drops below 5.0. | **5** | Must Have / High | Sprint 2 |
| **US-14** | Epic 6: Reporting | **As an Examination Controller**, I want to lock grades and generate digitally verified semester grade sheets and transcripts. | • Renders official header, student metadata, course table, and seals.<br>• Computes SGPA, CGPA, and academic standing.<br>• Generates exportable PDF format with cryptographic checksum. | **5** | Should Have / Medium | Sprint 2 |
| **US-15** | Epic 7: DevOps IaC | **As a DevOps Engineer**, I want to containerize the Flask microservice using Docker so that the app runs consistently across all environments. | • Multi-stage Dockerfile based on `python:3.10-slim`.<br>• Executes as unprivileged non-root user `appuser` (UID 1001).<br>• Passes container healthcheck probe `/api/health`. | **5** | Must Have / High | Sprint 1 |
| **US-16** | Epic 7: DevOps IaC | **As a Cloud Engineer**, I want to provision AWS VPC, subnet, security group, and EC2 instance via Terraform so that infrastructure is codified. | • Modular HCL provisions `library_vpc` (10.1.0.0/16) and `library_subnet`.<br>• Security group configures ports 22, 80, 5000, 8080.<br>• Provisions EC2 instance and encrypted S3 bucket (`library-backup-...`). | **8** | Must Have / High | Sprint 1 |
| **US-17** | Epic 7: DevOps IaC | **As a DevOps Engineer**, I want to automate Docker, Nginx reverse proxy, and container deployment via Ansible so that server setup is zero-touch. | • Multi-tier playbook (`site.yml` / `playbook.yml`) executing all roles.<br>• Nginx proxies port 80 to container port 5000.<br>• Executes 4 Post-Deployment Validation Gates verifying live health. | **8** | Must Have / High | Sprint 2 |

---

## 4. Estimation Rationale (Planning Poker Scale)

- **1 Point:** Trivial documentation or configuration tweak (e.g., updating `.gitignore`).
- **2 Points:** Straightforward lookup endpoint with existing repository helper.
- **3 Points:** Standard CRUD endpoint with basic query parameter filtering and unit tests.
- **5 Points:** Multi-step business logic, authentication decorators, grading algorithms, or Docker packaging.
- **8 Points:** Complex multi-tier integration (e.g., bulk CSV parsing engine, end-to-end Terraform AWS infrastructure provisioning, full Ansible deployment).
- **13 Points:** Distributed cross-region database replication with zero-downtime automated failover.

---
*Authored by:*  
**Om Tambe (PRN: 2125UMLM1065)**  
*Sandip University — SU_DevOps Engineering Program*
