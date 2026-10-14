# Unit 1: Product Engineering & Design Thinking

**Project Lead:** Om Tambe  
**PRN:** 2125UMLM1065  
**Institution:** Sandip University  
**Project:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  

---

## 1. Overview & Objectives

**Unit 1** establishes the comprehensive product engineering foundation, design thinking inquiry, and system architecture for the **Enterprise Student Record and Academic Management Platform (`SU_DevOps`)**.

Before writing code or provisioning cloud infrastructure, modern DevOps mandates a structured product discovery phase to translate ambiguous stakeholder needs into verifiable software specifications, user journeys, and architectural designs.

---

## 2. Directory Artifacts & Deliverables

This directory contains six comprehensive engineering specifications authored by **Om Tambe (PRN: 2125UMLM1065)**:

1. **[`BRD.md`](./BRD.md)** — **Business Requirements Document:**
   - Executive summary, business problem statements (data fragmentation, manual attendance, grading bottlenecks, infrastructure unreliability).
   - Core project objectives, measurable success criteria (KPIs: 95% turnaround reduction, sub-1.5s latency, 99.9% uptime).
   - Stakeholder analysis, RACI governance matrix, and institutional ROI analysis.

2. **[`FRS_NFRS_Specification.md`](./FRS_NFRS_Specification.md)** — **Functional & Non-Functional Requirements Specification:**
   - **FR-01:** Authentication & Role-Based Access Control (Admin, Faculty, Student, Exam Cell).
   - **FR-02:** Student Registration (Single record JSON & Bulk CSV entry).
   - **FR-03:** Course & Elective Management.
   - **FR-04:** Attendance Module with automatic low-attendance (<75%) warning flags.
   - **FR-05:** Marks & Grade Processing (SGPA/CGPA calculation engine on a 10-point scale).
   - **FR-06:** Official Report & Transcript Generation.
   - **NFR-01 to NFR-05:** Performance (<1.5s response, 1000 users), Security (bcrypt, AES-256 at rest, TLS 1.3), Availability (99.9%), Usability (WCAG 2.1 AA), and Scalability.
   - Complete Requirements Traceability Matrix.

3. **[`Design_Thinking_Report.md`](./Design_Thinking_Report.md)** — **IBM Design Thinking Report:**
   - Implementation of the **IBM Loop (Observe, Reflect, Make)**.
   - Formalization of the **Three IBM Hills**:
     - *Student Hill:* Aarav Patel 60-second course registration, attendance check, and transcript access.
     - *Faculty Hill:* Dr. Priya Sharma 2-minute 90-student lecture attendance and mark upload.
     - *Admin Hill:* Rahul Verma zero-defect end-semester result processing and transcript generation across 10,000+ students.
   - Stanford d.school 5-Stage human-centered design execution (Empathize, Define, Ideate, Prototype, Test).

4. **[`User_Personas.md`](./User_Personas.md)** — **Detailed User Personas & Empathy Maps:**
   - Comprehensive ethnographic study of **Aarav Patel** (Undergraduate Student), **Dr. Priya Sharma** (Senior Faculty Member), and **Rahul Verma** (University Registrar & Administrator).
   - Detailed Empathy Maps (Says, Thinks, Does, Feels), core pain points, motivations, and user journey narratives.

5. **[`System_Architecture.md`](./System_Architecture.md)** — **System Architecture & Technical Design:**
   - Multi-tier cloud-native architecture blueprint (Client Edge, Nginx reverse proxy, Docker container, Flask REST API, SQLite datastore, AWS VPC, EC2, and S3).
   - Security topology (AWS Security Groups, UFW firewall, container non-root execution, AES-256 encryption).
   - End-to-end request lifecycle and Mermaid flowcharts.

---

## 3. Transition to Unit 2 (Agile Release Planning)

The specifications and user stories developed in Unit 1 directly feed into **Unit 2: Agile Planning**, where they are structured into a prioritized Product Backlog and broken down across a 2-Sprint execution plan.
