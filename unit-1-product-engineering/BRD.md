# Business Requirements Document (BRD)

**Project Name:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  
**Student / Project Lead:** Om Tambe  
**PRN:** 2125UMLM1065  
**Course / Curriculum:** DevOps & Cloud Engineering Series  
**Academic Institution:** Sandip University  
**Document Version:** 1.0.0  
**Status:** Approved for Agile Release Planning  

---

## 1. Executive Summary

The **Enterprise Student Record & Academic Management Platform** is a unified, cloud-native information system engineered to modernize, streamline, and secure academic workflows across higher education institutions. 

In traditional university administration, academic records, attendance logs, and grading registers are stored across isolated physical registers, disparate spreadsheets, and disconnected departmental databases. This decentralized operational model introduces severe vulnerabilities:
- High human error rates during continuous assessment entry and grade calculations.
- Extreme server latency and downtime during peak course registration and exam result publishing cycles.
- Lack of an auditable, single source of truth for student academic standing and graduation clearances.
- Excessive clerical burden on faculty members, diverting time from pedagogy and research.

This project, spearheaded by **Om Tambe (PRN: 2125UMLM1065)**, defines the end-to-end DevOps delivery lifecycle—from initial product discovery and Agile backlog grooming to containerized microservice development and automated multi-tier AWS cloud infrastructure provisioning using HashiCorp Terraform and Ansible.

---

## 2. Business Problem Statements

| Problem ID | Problem Description | Institutional Impact |
| :--- | :--- | :--- |
| **BP-01** | **Fragmented Student Data:** Student demographic profiles, course registrations, and historical transcripts are distributed across legacy databases without real-time synchronization. | Inconsistent student records, delayed transcript verification, and audit non-compliance during regulatory inspections. |
| **BP-02** | **Manual Attendance Accounting:** Daily attendance is recorded on paper sheets and manually transcribed at semester ends. | Students unaware of falling below the mandatory 75% attendance threshold until exam hall tickets are withheld; high dispute overhead. |
| **BP-03** | **Grading Bottlenecks & Calculation Errors:** Faculty calculate GPA and CGPA manually using spreadsheet formulas with differing rounding rules. | Grade calculation discrepancies, student grievances, delayed semester result publishing by 4–6 weeks. |
| **BP-04** | **Infrastructure Unreliability ("ClickOps"):** University servers are configured manually without Infrastructure as Code, crashing when 1,000+ students access portals concurrently. | Catastrophic outages during semester enrollment and result announcement windows; zero disaster recovery capability. |

---

## 3. Project Objectives & Success Criteria

### 3.1 Primary Business Objectives
1. **Centralize Academic Lifecycle Management:** Consolidate student admission, registration, course allotment, attendance, and grading into a single role-based platform.
2. **Automate Attendance Governance:** Deliver instant, automated warning notifications when a student's aggregate attendance drops below 75%.
3. **Automate Grade Processing:** Eliminate manual grading errors with an automated SGPA/CGPA processing engine adhering to 10-point academic scales.
4. **Zero-Touch Cloud Deployment:** Achieve 100% environment parity and zero configuration drift across local, staging, and AWS cloud environments via declarative IaC (Terraform) and idempotent configuration (Ansible).

### 3.2 Measurable Business Metrics (KPIs)

```
+-------------------------------------------------------------------------------+
|                           KEY PERFORMANCE INDICATORS (KPIs)                   |
|                                                                               |
|  [ 95% Reduction ]     [ Sub-1.5s Latency ]   [ 99.9% Uptime ]  [ 0% Drift ]  |
|  in grade calculation  in API response time   availability      in server     |
|  turnaround time       under 1,000 users      during exams      configuration |
+-------------------------------------------------------------------------------+
```

- **Administrative Efficiency:** Reduce student onboarding and registration turnaround time from 3 days to under 5 minutes.
- **System Responsiveness:** Maintain API response times under 1.5 seconds for 1,000 concurrent active users.
- **Audit & Compliance:** 100% immutable audit trail for grade modifications and transcript releases.
- **Reliability:** 99.9% availability SLA with automated health checks (`/api/health`) and self-healing container restarts.

---

## 4. Stakeholder Analysis & RACI Matrix

The platform serves four primary campus stakeholder groups:
1. **Students:** Enrolled undergraduate and graduate learners requiring transparent academic tracking.
2. **Faculty Members:** Instructors managing course rosters, daily attendance, and continuous assessment marks.
3. **University Examination Cell / Registrar:** Administrators responsible for academic compliance, official result publishing, and transcript generation.
4. **DevOps & IT Operations Team:** System administrators managing cloud infrastructure, security firewalls, and deployment pipelines.

### RACI Governance Matrix
*(R = Responsible, A = Accountable, C = Consulted, I = Informed)*

| Functional Capability | Student | Faculty | Exam Cell | DevOps / IT |
| :--- | :---: | :---: | :---: | :---: |
| Self-Registration & Profile View | R / A | I | C | I |
| Course Catalog & Elective Selection | R | C | A | I |
| Daily Lecture Attendance Entry | I | R / A | C | I |
| Continuous Assessment & Mark Entry | I | R / A | C | I |
| SGPA / CGPA Calculation & Locking | I | C | R / A | I |
| Official Transcript Generation | I | I | R / A | I |
| Infrastructure Provisioning & IaC | I | I | I | R / A |
| Container Orchestration & Nginx Proxy | I | I | I | R / A |

---

## 5. Scope of the System

### 5.1 In-Scope Capabilities (MVP Release v1.0.0)
- **Role-Based Authentication & Authorization:** Multi-role access control for Admin, Faculty, Student, and Examination Cell.
- **Student Record Management:** Bulk CSV student ingestion and single record CRUD operations.
- **Course & Elective Management:** Departmental course catalogs, credit constraints (12–24 credits/semester), and capacity limits.
- **Attendance Module:** Session-wise attendance marking with automatic low-attendance (<75%) warning flags.
- **Marks & Grading Processing:** Scaled marks entry (0–100), automated letter grade mapping, and SGPA/CGPA computation engine.
- **Official Reporting:** Generation of verifiable student grade sheets and system health telemetry.
- **DevOps Cloud Automation:** Terraform AWS VPC and EC2 provisioning with Ansible-driven Docker and Nginx reverse proxy deployment.

### 5.2 Out-of-Scope (Future Phase Enhancements)
- Integrated online tuition payment gateway (Stripe / Razorpay).
- AI-driven facial recognition biometric attendance hardware integration.
- Native iOS and Android mobile app store applications (progressive web application provided in Phase 1).

---

## 6. Financial & Operational ROI Analysis

- **Labor Cost Savings:** Eliminates 300+ manual administrative hours per department each semester previously spent transcribing paper attendance sheets and verifying grade spreadsheets.
- **Paper & Printing Reduction:** Digitizing student registrations, attendance registers, and grade sheets reduces institutional paper usage by over 80,000 sheets annually.
- **Cloud Cost Optimization:** Automated AWS resource provisioning via Terraform ensures exact resource allocation (`t2.micro` instances and S3 lifecycle storage), keeping infrastructure running costs minimal.

---
*Submitted by:*  
**Om Tambe (PRN: 2125UMLM1065)**  
*Lead DevOps Engineer & Full-Stack Developer*  
*Sandip University — SU_DevOps Initiative*
