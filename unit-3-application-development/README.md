# Unit 3: Application Development & Microservices

## 1. Overview & Objectives

**Unit 3** implements the core backend microservice for the **Enterprise Student Record and Academic Management Platform (`SU_DevOps`)**. 

Built with **Python 3.10+ / Flask 3.0**, this REST API provides deterministic, thread-safe student record management, course marks entry, and automated GPA calculations. The application is packaged in a security-hardened, multi-stage Docker container configured to run under unprivileged user execution.

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
│   └── models.py           # Student domain model, grading logic & thread-safe repository
└── tests/
    ├── __init__.py         # Test package initialization
    └── test_app.py         # Pytest verification suite (200, 201, 400, 404, 409 status codes)
```

---

## 3. REST API Contract & Specification

| Method | Endpoint | Description | Request Body | Success Code | Error Codes |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `GET` | `/api/health` | Service liveness & readiness probe | None | `200 OK` | — |
| `GET` | `/api/students` | List all students (supports `?department=` & `?semester=`) | None | `200 OK` | `400 Bad Request` |
| `POST` | `/api/students` | Register a new student record | `{"student_id", "name", "email", "department", "semester"}` | `201 Created` | `400`, `409 Conflict` |
| `GET` | `/api/students/<student_id>` | Retrieve student profile and mark history by ID | None | `200 OK` | `404 Not Found` |
| `POST` | `/api/students/<student_id>/marks` | Submit assessment mark and recalculate GPA | `{"course_code", "marks", "credits"}` | `201 Created` | `400`, `404 Not Found` |

### Sample Payload: Register Student (`POST /api/students`)
```json
{
  "student_id": "STD2026010",
  "name": "DevOps Engineer",
  "email": "devops@university.edu",
  "department": "Computer Science",
  "semester": 4
}
```

### Sample Response: (`201 Created`)
```json
{
  "message": "Student record created successfully.",
  "student": {
    "student_id": "STD2026010",
    "name": "DevOps Engineer",
    "email": "devops@university.edu",
    "department": "Computer Science",
    "semester": 4,
    "enrolled_credits": 0,
    "cumulative_gpa": 0.0,
    "academic_standing": "Good Standing",
    "marks_count": 0
  }
}
```

---

## 4. Local Development & Testing

### 4.1 Prerequisites
- Python 3.10+ installed
- `pip` package manager

### 4.2 Setup & Dependencies
```bash
# Navigate to the unit directory
cd unit-3-application-development

# Create and activate virtual environment
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 4.3 Running Unit & Integration Tests
Execute the comprehensive Pytest suite:
```bash
pytest tests/test_app.py -v
```

To run with coverage metrics:
```bash
pytest --cov=app tests/
```

### 4.4 Running Locally via Flask Dev Server
```bash
python -m app.main
# Server listens on http://127.0.0.1:5000
```

---

## 5. Docker Containerization

The container is built using a **multi-stage build pattern**:
- **Builder Stage (`python:3.10-slim`):** Compiles wheels and installs dependencies.
- **Runner Stage (`python:3.10-slim`):** Minimal runtime container, creates non-root user `appuser` (UID 1001), runs Gunicorn WSGI server, and implements active healthcheck probes.

### 5.1 Build the Docker Image
```bash
docker build -t student-academic-platform:latest .
```

### 5.2 Run the Docker Container
```bash
docker run -d \
  --name student-api \
  -p 5000:5000 \
  --restart unless-stopped \
  student-academic-platform:latest
```

### 5.3 Verify Container Status & Smoke Test
```bash
# Check container status and health
docker ps --filter "name=student-api"

# Healthcheck probe
curl -i http://localhost:5000/api/health

# Query student list
curl -i http://localhost:5000/api/students
```

---

## 6. Next Step in Delivery Continuum

With the application containerized and tested, proceed to **Unit 4: Infrastructure Automation**, where HashiCorp Terraform provisions AWS cloud resources and Ansible automates Docker and Nginx reverse proxy deployment.
