# Unit 2: Agile Project Planning & Scrum Framework

## 1. Overview & Objectives

**Unit 2** operationalizes the product specifications developed in Unit 1 into an actionable, iterative Agile roadmap. Using the **Scrum Framework**, the business requirements of the **Enterprise Student Record and Academic Management Platform (`SU_DevOps`)** are decomposed into Epics, User Stories, measurable Acceptance Criteria, and organized across time-boxed development sprints.

---

## 2. Unit Deliverables

This directory contains two core Agile planning documents:

1. **[`Product_Backlog.md`](./Product_Backlog.md)**
   - **Epics 1–7:** Student Management, Course Management, Attendance Tracking, Marks & Performance, Authentication & Security, Notifications, and Reporting.
   - **Prioritized User Story Table:** 20 user stories detailed with User Role, Goal, Business Value, Acceptance Criteria, Story Points (Modified Fibonacci: 1, 2, 3, 5, 8, 13), MoSCoW Priority ranking, and Sprint allocation.
   - **Story Point Estimation Guide:** Defined complexity rubrics based on Planning Poker sessions.

2. **[`Sprint_Plan.md`](./Sprint_Plan.md)**
   - **Scrum Team Structure & Roles:** Responsibilities defined for Product Owner, Scrum Master, Developers, QA Engineer, and DevOps Engineer.
   - **2-Sprint Execution Breakdown:**
     - **Sprint 1 (Velocity: 20 SP):** Foundation, User Authentication, RBAC, Base CI, and Containerization.
     - **Sprint 2 (Velocity: 26 SP):** Student Management REST API, Validation, Pytest Suite, and Cloud Infrastructure Automation.
   - **Scrum Ceremonies Simulation:** Real-world logs for Sprint Planning, Daily Scrum Standups, Sprint Review, and Retrospectives.
   - **Definition of Done (DoD) & Definition of Ready (DoR):** Quality checklists for zero-defect releases.
   - **Scrum Board Workflow & Burndown Projection:** Visual task tracking from Backlog to Done.
   - **Agile Frameworks Comparison Matrix:** Comparative analysis of Scrum, Kanban, XP, Lean, LeSS, SAFe, and Scrum@Scale.

---

## 3. Key Agile Metrics

- **Total Backlog Items:** 20 User Stories
- **Sprint Length:** 2 Weeks (10 working days)
- **Target Release Velocity:** 46 Story Points across Sprint 1 & Sprint 2
- **Test Automation Coverage Gate:** Minimum 85% branch coverage required for DoD signoff

---

## 4. Next Step in Delivery Continuum

The sprint backlog items designated for Sprint 1 and Sprint 2 are implemented in **Unit 3: Application Development & Microservices**, where the Python Flask REST API, domain models, and container runtime are engineered.
