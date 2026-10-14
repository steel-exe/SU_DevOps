# Unit 3: Application Development & Microservices

**Project Lead:** Om Tambe  
**PRN:** 2125UMLM1065  
**Institution:** Sandip University  
**Project:** Enterprise Student Record & Academic Management Platform (`SU_DevOps`)  

---

## 1. Overview & Architectural Context

**Unit 3** delivers the complete application development and containerization lifecycle for the **Enterprise Student Record and Academic Management Platform (`SU_DevOps`)**.

The microservice is engineered using **Python 3.10+ / Flask 3.0** with SQLite ACID persistence, full domain entity modeling, and layered service architecture (Presentation, Application Service, Domain Model, and Database). It includes complete CI/CD support (Jenkinsfile and GitHub Actions), containerization via Docker, and declarative Kubernetes orchestration manifests (`k8s/`).

---

## 2. Directory Structure

```
unit-3-application-development/
├── Dockerfile              # Multi-stage production container definition
├── Jenkinsfile             # Declarative Jenkins CI/CD pipeline
├── package.json            # Node/frontend metadata
├── requirements.txt        # Production & testing dependencies
├── run.py                  # Application server entrypoint (0.0.0.0:5000)
├── README.md               # Unit engineering & deployment manual
├── app/
│   ├── __init__.py         # Application factory pattern
│   ├── models/             # Domain entities (Student, Course, Enrollment, Grade)
│   ├── routes/             # Blueprint route handlers (api.py, views.py)
│   ├── services/           # Business services (StudentService, CourseService, GradeService)
│   ├── static/             # CSS styling & JS scripts
│   └── templates/          # HTML5 templates (Dashboard, Student Directory, Courses)
├── database/
│   └── db.py               # SQLite database connector & schema migrations
├── k8s/                    # Kubernetes deployment and service manifests
│   ├── deployment.yaml
│   └── service.yaml
└── tests/                  # 37 automated Pytest unit tests (100% pass rate)
    ├── __init__.py
    ├── test_api_endpoints.py
    ├── test_course_enrollment.py
    ├── test_marks_mgmt.py
    └── test_student_service.py
```

---

## 3. REST API Contract & Specification

| Method | Endpoint | Description | Success Code | Sample Output |
| :--- | :--- | :--- | :---: | :--- |
| `GET` | `/` | Root endpoint (Web UI or JSON when `Accept: application/json`) | `200 OK` | `{"application": "Smart Library Management Platform", "status": "running"}` |
| `GET` | `/api/health` | Container liveness & readiness probe | `200 OK` | `{"status": "UP", "service": "Enterprise Student Record...", "version": "1.0.0"}` |
| `GET` | `/api/books` | Unit 4 Smart Library catalog compatibility | `200 OK` | `[{"author": "F. Scott Fitzgerald", "id": 1, "title": "The Great Gatsby"}]` |
| `GET` | `/api/dashboard` | High-level metrics and system statistics | `200 OK` | `{"status": "SUCCESS", "metrics": {...}}` |
| `GET` | `/api/students` | List all registered students (supports `?q=`) | `200 OK` | `{"count": 4, "students": [...]}` |
| `POST` | `/api/students` | Register a new student profile | `201 Created` | `{"message": "Student registered successfully", ...}` |
| `GET` | `/api/students/<id>` | Single student profile and transcript lookup | `200 OK` | `{"student_id": "S101", "name": "...", "cumulative_gpa": 8.75}` |
| `DELETE` | `/api/students/<id>` | Soft-delete student if no active enrollments | `200 OK` | `{"message": "Student '...' deleted successfully"}` |
| `GET` | `/api/courses` | List university course offerings | `200 OK` | `{"count": 6, "courses": [...]}` |
| `POST` | `/api/courses` | Create a new academic course | `201 Created` | `{"message": "Course created successfully", ...}` |
| `POST` | `/api/enrollments` | Enroll student into course with credit checking | `201 Created` | `{"message": "Enrolled successfully", ...}` |
| `POST` | `/api/enrollments/drop` | Drop enrolled course and restore credit limits | `200 OK` | `{"message": "Course dropped successfully", ...}` |
| `POST` | `/api/marks` | Record course marks and recalculate SGPA/CGPA | `201 Created` | `{"message": "Marks recorded successfully", ...}` |

---

## 4. Local Testing & Verification

Execute the complete 37-test Pytest test suite:
```bash
# Navigate to unit directory
cd unit-3-application-development

# Execute automated test suite
pytest tests/ -v
```

**Verification Results:**
```
tests/test_api_endpoints.py::test_healthcheck_endpoint PASSED            [  2%]
tests/test_api_endpoints.py::test_dashboard_endpoint PASSED              [  5%]
tests/test_api_endpoints.py::test_list_students_api PASSED               [  8%]
tests/test_api_endpoints.py::test_register_student_api PASSED            [ 10%]
tests/test_api_endpoints.py::test_register_student_invalid_fails PASSED  [ 13%]
tests/test_api_endpoints.py::test_get_student_api PASSED                 [ 16%]
tests/test_api_endpoints.py::test_list_courses_api PASSED                [ 18%]
tests/test_api_endpoints.py::test_add_course_api PASSED                  [ 21%]
tests/test_api_endpoints.py::test_api_enroll_and_drop_flow PASSED        [ 24%]
tests/test_api_endpoints.py::test_api_enroll_credit_limit_rejection PASSED [ 27%]
tests/test_api_endpoints.py::test_api_record_marks_and_transcript PASSED [ 29%]
tests/test_api_endpoints.py::test_delete_student_api PASSED              [ 32%]
tests/test_api_endpoints.py::test_get_course_api_and_add_failure PASSED  [ 35%]
tests/test_api_endpoints.py::test_web_ui_dashboard_route PASSED          [ 37%]
tests/test_api_endpoints.py::test_books_catalog_endpoint PASSED          [ 40%]
tests/test_api_endpoints.py::test_root_json_status_endpoint PASSED       [ 43%]
tests/test_course_enrollment.py::test_enroll_student_success PASSED      [ 45%]
tests/test_course_enrollment.py::test_duplicate_course_enrollment_fails PASSED [ 48%]
tests/test_course_enrollment.py::test_course_capacity_enforcement PASSED [ 51%]
tests/test_course_enrollment.py::test_credit_limit_18_enforcement PASSED [ 54%]
tests/test_course_enrollment.py::test_drop_course_restores_credits_and_capacity PASSED [ 56%]
tests/test_course_enrollment.py::test_drop_nonexistent_enrollment_fails PASSED [ 59%]
tests/test_marks_mgmt.py::test_record_marks_letter_grade_mapping PASSED  [ 62%]
tests/test_marks_mgmt.py::test_record_marks_out_of_bounds_fails PASSED   [ 64%]
tests/test_marks_mgmt.py::test_gpa_calculation_weighted_credits PASSED   [ 67%]
tests/test_marks_mgmt.py::test_academic_probation_evaluation PASSED      [ 70%]
tests/test_marks_mgmt.py::test_student_transcript_completeness PASSED    [ 72%]
tests/test_student_service.py::test_add_student_success PASSED           [ 75%]
tests/test_student_service.py::test_add_duplicate_student_raises_error PASSED [ 78%]
tests/test_student_service.py::test_add_student_invalid_email_fails PASSED [ 81%]
tests/test_student_service.py::test_add_student_missing_fields_fails PASSED [ 83%]
tests/test_student_service.py::test_delete_student_success PASSED        [ 86%]
tests/test_student_service.py::test_delete_student_with_active_enrollments_fails PASSED [ 89%]
tests/test_student_service.py::test_delete_nonexistent_student_fails PASSED [ 91%]
tests/test_student_service.py::test_search_students PASSED               [ 94%]
tests/test_student_service.py::test_course_models_and_validations PASSED [ 97%]
tests/test_student_service.py::test_models_to_dict PASSED                [100%]

============================= 37 passed in 0.34s ==============================
```

---

## 5. Docker Build & Container Execution

```bash
# Build the container
docker build -t student-academic-platform:latest .

# Run the container exposing port 5000
docker run -d -p 5000:5000 --name student-platform-app student-academic-platform:latest

# Verify health status
curl http://localhost:5000/api/health
```

---

## 6. Continuous Integration (Jenkins & GitHub Actions)

- **Jenkinsfile:** Defines automated multi-stage pipeline:
  1. `Checkout SCM`
  2. `Setup Python & Dependencies`
  3. `Linting Gate (flake8)`
  4. `Automated Pytest Execution`
  5. `Docker Image Build & Tagging`
  6. `Artifact Archival`
- **GitHub Actions (`.github/workflows/ci.yml`):** Automatically executes linting and Pytest test runs upon every push to `main`.
