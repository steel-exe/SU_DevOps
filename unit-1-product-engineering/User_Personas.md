# Comprehensive User Personas & Empathy Maps

**Project Name:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  
**Student / Project Lead:** Om Tambe (PRN: 2125UMLM1065)  
**Academic Institution:** Sandip University  
**Document Version:** 1.0.0  

---

## 1. Persona 1: Aarav Patel — The Undergraduate Student

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PERSONA: Aarav Patel                                                        │
│ Age: 20 | Role: 3rd Year B.Tech Computer Science | Tech Fluency: Expert     │
│ Location: Sandip University Campus, Nashik                                 │
│ Quote: "I need to know my attendance and grades in real time, not at the    │
│         end of the semester when it's too late to fix anything."           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.1 Demographic & Behavioral Profile
- **Academic Context:** Enrolled in 6 theory courses and 2 laboratory sections in Semester 5. Balancing rigorous coursework, campus recruitment training, and software development projects.
- **Tech Habits:** Mobile-first user; expects responsive user interfaces, instant push notifications, and sub-second load times similar to consumer mobile apps.
- **Motivations:** Maintain a CGPA above 8.5 for campus placements, ensure attendance stays well above the 75% cutoff to remain eligible for examinations, and register for preferred high-demand elective courses quickly.

### 1.2 Empathy Map: Aarav Patel

| Dimension | Observations & Verbatim Insights |
| :--- | :--- |
| **Says** | • *"Our current university portal crashes every time course registration opens."*<br>• *"I have no idea if my attendance was marked correctly until exam admit cards are issued."*<br>• *"Calculating my CGPA from different semester mark sheets is confusing and error-prone."* |
| **Thinks** | • *"What if I'm at 74.5% attendance and miss an exam because a professor made a clerical error?"*<br>• *"Why can't our college system be as fast and reliable as modern cloud platforms?"*<br>• *"Will my official transcript be ready in time for my summer internship applications?"* |
| **Does** | • Takes photos of physical classroom attendance rosters on his smartphone as backup proof.<br>• Manages personal Google Spreadsheets trying to estimate his continuous evaluation scores.<br>• Sends anxious emails to faculty asking for current internal assessment totals. |
| **Feels** | • **Anxious** during end-semester registration due to fear of server crashes.<br>• **Distrustful** of manual paper attendance books that can be misplaced.<br>• **Empowered** when provided with transparent, real-time academic analytics. |

### 1.3 Key Pains & Desired Gains
- **Pain Points:** Unpredictable downtime during peak traffic; no early-warning alerts for low attendance; fragmented portals for fees, attendance, and grades.
- **Desired Gains:** Mobile-friendly dashboard with real-time attendance percentage indicators (<75% warning flag); 1-click course elective registration; instant digital transcript access.

---

## 2. Persona 2: Dr. Priya Sharma — The Senior Faculty Member

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PERSONA: Dr. Priya Sharma                                                   │
│ Age: 46 | Role: Associate Professor & Academic Mentor | Tech Fluency: Mod. │
│ Department: Computer Science & Engineering, Sandip University               │
│ Quote: "I want to spend my time mentoring students and doing research, not  │
│         spending 10 hours a week reconciling Excel spreadsheets."           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Demographic & Behavioral Profile
- **Academic Context:** Instructs 2 lecture sections with 90 students each; acts as the primary academic advisor for 30 undergraduate mentees.
- **Tech Habits:** Primarily uses institutional laptops; prefers clean, predictable desktop web applications with clear confirmation dialogues and minimal clicks.
- **Motivations:** Accurately track student attendance, identify struggling students early in the semester, submit mid-term continuous assessment marks smoothly, and avoid clerical disputes.

### 2.2 Empathy Map: Dr. Priya Sharma

| Dimension | Observations & Verbatim Insights |
| :--- | :--- |
| **Says** | • *"Calling out 90 student names in a 50-minute lecture wastes almost 15 minutes of lecture time."*<br>• *"Copy-pasting quiz scores from spreadsheet to spreadsheet always introduces accidental typos."*<br>• *"I need a system that prevents me from entering 105 when the maximum mark is 100."* |
| **Thinks** | • *"I wish I had an automatic alert showing me which students have missed 3 consecutive lectures."*<br>• *"If the system was intuitive, I could finish grading before the weekend."*<br>• *"Is this portal secure, or will grades be altered accidentally?"* |
| **Does** | • Carries heavy paper registers to every classroom and laboratory session.<br>• Spends late evenings re-entering marks into departmental spreadsheets.<br>• Manually calculates attendance percentages with a desktop calculator before departmental review meetings. |
| **Feels** | • **Overwhelmed** by non-academic administrative paperwork.<br>• **Protective** of student privacy and grading fairness.<br>• **Relieved** when automated tools handle repetitive calculation tasks accurately. |

### 2.3 Key Pains & Desired Gains
- **Pain Points:** Cumbersome multi-step data entry interfaces; no automatic score boundary validation; manual calculation of complex SGPA formulas.
- **Desired Gains:** Rapid 1-click batch attendance submission; automated input validation rejecting values outside 0–100; automated list of at-risk students falling below 75% attendance.

---

## 3. Persona 3: Rahul Verma — The University Registrar & System Administrator

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PERSONA: Rahul Verma                                                        │
│ Age: 52 | Role: University Registrar & IT Operations Lead | Tech: Pragmatic │
│ Office: Office of Academic Affairs & Controller of Examinations             │
│ Quote: "Data integrity and high availability are non-negotiable. A single    │
│         corrupted record or server crash compromises institutional trust."  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Demographic & Behavioral Profile
- **Administrative Context:** Responsible for student admissions, official enrollment records, examination scheduling, semester transcript releases, and regulatory compliance for 8,000+ students.
- **Tech Habits:** Focuses on system security, audit compliance, database backups, and cloud infrastructure reliability. Values automated deployment scripts and declarative configuration over manual server setups.
- **Motivations:** Maintain 99.9% portal uptime during admissions and result releases; eliminate manual "ClickOps" server administration; ensure 100% compliance with university accreditation standards.

### 3.2 Empathy Map: Rahul Verma

| Dimension | Observations & Verbatim Insights |
| :--- | :--- |
| **Says** | • *"Last semester our legacy servers crashed when 3,000 students tried to download results at once."*<br>• *"We cannot afford unrecorded grade modifications; every database update must have an audit log."*<br>• *"Manual server setup is obsolete; everything must be reproducible through Infrastructure as Code."* |
| **Thinks** | *"How can I guarantee our AWS infrastructure automatically handles traffic surges without inflating our budget?"*<br>*"Are all student records encrypted at rest using AES-256 according to data privacy laws?"* |
| **Does** | • Reviews server monitoring dashboards, CPU utilization metrics, and Nginx access logs.<br>• Authorizes student enrollment batches via bulk CSV files.<br>• Enforces strict role-based access control policies across departments. |
| **Feels** | • **Accountable** for the security and uptime of institutional IT assets.<br>• **Vulnerable** to human error when server administration is performed manually via SSH.<br>• **Confident** when infrastructure is declared via Terraform and managed with Ansible. |

### 3.3 Key Pains & Desired Gains
- **Pain Points:** Server downtime during peak registration events; manual student profile entry; unversioned backups; configuration drift across staging and production servers.
- **Desired Gains:** Declarative AWS infrastructure provisioning via Terraform; automated Docker container orchestration via Ansible; bulk CSV student onboarding; automated AES-256 encrypted S3 backups.

---
*Authored by:*  
**Om Tambe (PRN: 2125UMLM1065)**  
*Sandip University — SU_DevOps Engineering Curriculum*
