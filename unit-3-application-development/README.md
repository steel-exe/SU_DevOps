# Unit 3: Application Development & Microservices

**Project Lead:** Om Tambe  
**PRN:** 2125UMLM1065  
**Institution:** Sandip University  
**Project:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  

---

## 1. Overview & Objectives

**Unit 3** implements the containerized backend microservice for the **Enterprise Student Record and Academic Management Platform (`SU_DevOps`)**. 

Developed using **Python 3.10+ / Flask 3.0**, this REST API delivers deterministic student lifecycle management, low-attendance (<75%) alerting, course mark grading, and backward compatibility with the Smart Library reference case study. The application is packaged in a security-hardened, multi-stage Docker container executed under non-root permissions.

---

## 2. Directory Layout

```
unit-3-application-development/
├── Dockerfile              # Multi-stage production container definition (Python 3.10-slim)
├── requirements.txt        # Production & testing Python dependencies (Flask, Gunicorn, Pytest)
├── README.md               # Unit engineering & deployment guide
├── app/
│   ├── __init__.py         # Flask app package initialization & factory export
│   ├── main.py             # REST API routes, error handlers, and application factory
│   └── models.py           # Domain models (Student, Book), grading engine & data store
└── tests/
    ├── __init__.py         # Test package initialization
    └── test_app.py         # Pytest verification suite (14 test cases, 100% pass rate)
```

---

## 3. REST API Contract & Endpoints

| Method | Endpoint | Description | Request Body | Success Code | Sample Response |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `GET` | `/` | Root platform status probe | None | `200 OK` | `{"application": "Smart Library Management Platform", "status": "running"}` |
| `GET` | `/api/health` | Service health status probe | None | `200 OK` | `{"status": "healthy"}` |
| `GET` | `/api/books` | Reference catalog retrieval | None | `200 OK` | `[{"author": "F. Scott Fitzgerald", "id": 1, "title": "The Great Gatsby"}]` |
| `GET` | `/api/students` | List student records (supports `?department=` & `?semester=`) | None | `200 OK` | `{"count": 2, "students": [...]}` |
| `POST` | `/api/students` | Register a new student profile | `{"student_id", "name", "email", "department", "semester"}` | `201 Created` | `{"message": "Student record created successfully.", ...}` |
| `GET` | `/api/students/<student_id>` | Single student profile lookup | None | `200 OK` | `{"student": {...}, "marks_history": [...]}` |
| `POST` | `/api/students/<student_id>/marks` | Submit assessment mark & calculate GPA | `{"course_code", "marks", "credits"}` | `201 Created` | `{"message": "Academic mark recorded successfully.", ...}` |

---

## 4. Local Development & Automated Testing

### 4.1 Prerequisites
- Python 3.10+
- `pip` package manager

### 4.2 Setup & Dependencies
```bash
# Navigate to unit directory
cd unit-3-application-development

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate       # On Linux/macOS
.\.venv\Scripts\Activate.ps1    # On Windows PowerShell

# Install dependencies
pip install -r requirements.txt
```

### 4.3 Running Pytest Test Suite
```bash
pytest tests/test_app.py -v
```

**Verification Output:**
```
tests/test_app.py::TestRootAndHealthEndpoints::test_root_endpoint_returns_running_status PASSED
tests/test_app.py::TestRootAndHealthEndpoints::test_health_endpoint_returns_healthy PASSED
tests/test_app.py::TestBooksCatalog::test_get_books_returns_great_gatsby PASSED
tests/test_app.py::TestStudentManagementEndpoints::test_get_students_list PASSED
tests/test_app.py::TestStudentManagementEndpoints::test_get_students_filter_by_department PASSED
tests/test_app.py::TestStudentManagementEndpoints::test_get_students_invalid_semester_returns_400 PASSED
tests/test_app.py::TestStudentManagementEndpoints::test_create_student_success PASSED
tests/test_app.py::TestStudentManagementEndpoints::test_create_student_missing_fields_returns_400 PASSED
tests/test_app.py::TestStudentManagementEndpoints::test_create_student_duplicate_id_returns_409 PASSED
tests/test_app.py::TestStudentManagementEndpoints::test_get_student_by_id_success PASSED
tests/test_app.py::TestStudentManagementEndpoints::test_get_student_by_id_not_found PASSED
tests/test_app.py::TestAttendanceAndGrading::test_low_attendance_flag_triggered_below_75 PASSED
tests/test_app.py::TestAttendanceAndGrading::test_record_marks_and_compute_gpa PASSED
tests/test_app.py::TestAttendanceAndGrading::test_record_marks_out_of_range_returns_400 PASSED

============================= 14 passed in 0.34s ==============================
```

---

## 5. Docker Containerization

The container is built using a **multi-stage build pattern**:
- **Builder Stage (`python:3.10-slim`):** Installs compiler tools and creates wheel packages.
- **Runner Stage (`python:3.10-slim`):** Lightweight runtime executing as unprivileged user `appuser` (UID 1001), serving on port `5000` via Gunicorn.

```bash
# Build the Docker image
docker build -t student-academic-platform:latest .

# Run the container
docker run -d -p 5000:5000 --name student-api student-academic-platform:latest

# Verify health status
curl http://localhost:5000/api/health
# {"status": "healthy"}
```

---

## 6. Transition to Unit 4 (Infrastructure Automation)

With the application containerized and tested, proceed to **Unit 4: Infrastructure Automation**, where HashiCorp Terraform provisions AWS cloud resources and Ansible automates Docker and Nginx reverse proxy deployment.
