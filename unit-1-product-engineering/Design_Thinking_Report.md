# Design Thinking Engineering Report: IBM Framework

**Project Name:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  
**Student / Project Lead:** Om Tambe  
**PRN:** 2125UMLM1065  
**Institution:** Sandip University  
**Framework:** IBM Enterprise Design Thinking & Stanford d.school Methodology  
**Document Version:** 1.0.0  

---

## 1. Executive Summary & IBM Design Thinking Framework

Engineering robust software requires prioritizing genuine human user needs over pure technical assumptions. For the **Enterprise Student Record & Academic Management Platform**, project lead **Om Tambe (PRN: 2125UMLM1065)** implemented the **IBM Enterprise Design Thinking Framework** paired with the Stanford d.school 5-stage human-centered model.

```
                      ┌────────────────────────────────────────┐
                      │             THE IBM LOOP               │
                      │                                        │
                      │      OBSERVE ──> REFLECT ──> MAKE      │
                      │         ▲                     │        │
                      │         └─────────────────────┘        │
                      └──────────────────┬─────────────────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        │                                │                                │
┌───────▼────────┐              ┌────────▼────────┐              ┌────────▼────────┐
│  STUDENT HILL  │              │  FACULTY HILL   │              │   ADMIN HILL    │
│ Aarav Patel    │              │ Dr. Priya Sharma│              │ Rahul Verma     │
│ 60-Sec Portal  │              │ 2-Min Mark Flow │              │ 10k Transcripts │
└────────────────┘              └─────────────────┘              └─────────────────┘
```

The framework is anchored by two core operational principles:
1. **The IBM Loop (Observe, Reflect, Make):** A continuous behavioral feedback cycle ensuring that user observations immediately drive collaborative reflection, prototype realization, and empirical testing.
2. **IBM Hills:** Ambitious, user-focused intent statements that define project success not in technical terms, but by empowering real campus users to achieve measurable objectives.

---

## 2. The IBM Loop in Practice

### 2.1 Observe: Deep User Inquiries
- Conducted contextual inquiry interviews with 15 undergraduate students, 6 senior faculty members, and 3 academic registrar personnel at Sandip University.
- Observed faculty spending 8–10 minutes per lecture manually calling out names from paper registers.
- Documented student frustration during semester grade publication when legacy university servers suffered timeout errors.

### 2.2 Reflect: Synthesis & Alignment
- Mapped qualitative feedback into Empathy Maps and Journey Maps.
- Identified recurring systemic bottlenecks: manual transcript reconciliation, unnotified attendance drops, and lack of horizontal cloud scalability.
- Aligned cross-functional priorities across business goals, architectural feasibility, and user satisfaction.

### 2.3 Make: Rapid Prototyping & DevOps Automation
- Prototyped modular REST API blueprints with Flask 3.0.
- Implemented lightweight Docker containerization to eliminate developer environment discrepancies ("works on my machine").
- Engineered declarative Terraform scripts and idempotent Ansible automation on AWS to guarantee zero-downtime scalability.

---

## 3. IBM Hills: User-Centric Intent Statements

In IBM Design Thinking, **Hills** establish the project's North Star goals, structured around:
> **Who** (User Persona) + **What** (Measurable Action / Capability) + **Wow** (Delightful Differentiator).

```
+-------------------------------------------------------------------------------+
|                                  THE 3 IBM HILLS                              |
+-------------------------------------------------------------------------------+
|  1. THE STUDENT HILL                                                          |
|     Who: Aarav Patel (3rd Year Computer Science Student)                      |
|     What: Can register for courses, monitor daily attendance, and download    |
|           verified semester grade reports in under 60 seconds                 |
|     Wow:  With zero administrative queuing and automatic threshold warnings.  |
|                                                                               |
|  2. THE FACULTY HILL                                                          |
|     Who: Dr. Priya Sharma (Senior Associate Professor & Academic Advisor)     |
|     What: Can record 90-student lecture attendance and upload assessment      |
|           marks in less than 2 minutes                                        |
|     Wow:  With automatic validation boundaries and instant outlier detection. |
|                                                                               |
|  3. THE ADMIN & REGISTRAR HILL                                                |
|     Who: Rahul Verma (University Registrar & Examination Controller)          |
|     What: Can process semester-end results and issue official transcripts      |
|           across 10,000+ enrolled students                                    |
|     Wow:  With 100% cryptographic data integrity and automated cloud failover.|
+-------------------------------------------------------------------------------+
```

---

## 4. The 5-Stage Human-Centered Design Cycle

### 4.1 Stage 1: Empathize
Through shadowing and empathy mapping, we analyzed three primary campus personas:
1. **Aarav Patel (Student):** Needs transparency in cumulative attendance and grade point forecasts.
2. **Dr. Priya Sharma (Faculty):** Needs rapid, validated data entry for daily attendance and continuous evaluations.
3. **Rahul Verma (Admin / Registrar):** Needs automated compliance auditing, bulk CSV student enrollment, and infrastructure reliability.

### 4.2 Stage 2: Define (Point of View & HMW Statements)
- **POV 1 (Student):** *Aarav Patel needs* real-time access to his attendance ratio *because* sudden last-minute exam disqualification due to attendance falling below 75% damages his academic career.
- **POV 2 (Faculty):** *Dr. Priya Sharma needs* single-click attendance and validated score entry *because* reconciling separate Excel spreadsheets consumes hours of research and teaching time.
- **POV 3 (Admin):** *Rahul Verma needs* declarative infrastructure automation *because* manual server configuration causes catastrophic server crashes during peak grade publishing hours.
- **"How Might We" Inquiries:**
  - *HMW-1:* How might we alert students before they cross below the 75% attendance threshold?
  - *HMW-2:* How might we guarantee sub-1.5 second API response times under 1,000 concurrent student logins?
  - *HMW-3:* How might we eliminate configuration drift between testing and AWS production?

### 4.3 Stage 3: Ideate (Prioritization Matrix)
Features were brainstormed and plotted on an **Impact vs. Feasibility Matrix**:
- **High Impact, High Feasibility (Sprint 1 & 2 Focus):**
  - Modular Flask REST API microservice (`/api/health`, `/api/students`, `/api/marks`).
  - Automated low-attendance (<75%) warning flag engine.
  - Multi-stage Docker containerization running under non-root security.
  - HashiCorp Terraform AWS VPC, Subnet, Security Group, and EC2 provisioning.
  - Ansible-driven Docker and Nginx reverse proxy configuration.
- **High Impact, Medium Feasibility (Future Releases):**
  - Bulk CSV student import with transactional row rollbacks.
  - Multi-AZ RDS PostgreSQL migration.

### 4.4 Stage 4: Prototype (System Blueprint)
Developed working prototypes spanning:
1. REST API contract definitions with deterministic JSON schemas.
2. Thread-safe in-memory domain model with instant recalculation of SGPA and CGPA.
3. Declarative Terraform HCL scripts provisioning AWS VPC `10.1.0.0/16` and EC2 `t2.micro` instances.
4. Ansible playbook configuring Nginx reverse proxy on port 80 forwarding to container port 5000.

### 4.5 Stage 5: Test & Validate
- **Automated Pytest Suite:** 14 unit tests executed in 0.27s validating HTTP 200, 201, 400, 404, and 409 status codes.
- **Docker Health Probing:** Containerized runtime tested with active curl probes against `/api/health`.
- **Ansible 4-Gate Smoke Testing:** Automated verification confirming port 80 open, Docker daemon active, container running, and API responding with `{"status": "healthy"}`.

---
*Submitted by:*  
**Om Tambe (PRN: 2125UMLM1065)**  
*Sandip University — SU_DevOps Engineering Curriculum*
