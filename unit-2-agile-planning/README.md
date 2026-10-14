# Unit 2: Agile Project Planning & Scrum Framework

**Project Lead:** Om Tambe  
**PRN:** 2125UMLM1065  
**Institution:** Sandip University  
**Project:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  

---

## 1. Overview & Objectives

**Unit 2** operationalizes the product specifications developed in Unit 1 into an actionable, iterative Agile roadmap. Using the **Scrum Framework**, the functional and non-functional requirements are decomposed into Epics, User Stories, and measurable Acceptance Criteria, scheduled across two structured development sprints.

---

## 2. Directory Artifacts & Deliverables

This directory contains two core Agile planning documents authored by **Om Tambe (PRN: 2125UMLM1065)**:

1. **[`Product_Backlog.md`](./Product_Backlog.md)**
   - Prioritized backlog of 17 user stories across Epics: Authentication, Student Management, Attendance, Course Management, Grading Engine, Reporting, and DevOps IaC.
   - Story point estimations using the modified Fibonacci sequence (`1, 2, 3, 5, 8, 13`) based on Planning Poker criteria.
   - Concrete Acceptance Criteria and MoSCoW prioritization rankings.

2. **[`Sprint_Plan.md`](./Sprint_Plan.md)**
   - Scrum Team Structure and Project Allocation.
   - **Sprint 1 (25 SP):** Foundation, User Authentication, RBAC, Core Student API, Docker packaging, and AWS Terraform provisioning.
   - **Sprint 2 (28 SP):** Attendance tracking with low-attendance (<75%) flags, grading calculation engine (SGPA/CGPA), Ansible playbook automation, Nginx reverse proxy, and post-deployment validation gates.
   - Formal Definition of Ready (DoR) and Definition of Done (DoD).
   - Scrum Board Workflow & Sprint Burndown Projections.
   - Comparative analysis of 7 Agile frameworks (Scrum, Kanban, XP, Lean, LeSS, SAFe, Scrum@Scale).

---

## 3. Transition to Unit 3 (Application Development)

The user stories prioritized in Sprint 1 and Sprint 2 are implemented in **Unit 3: Application Development & Microservices**, where the Python Flask REST API, domain entities, and Docker container runtime are developed.
