"""
Automated Pytest Suite for Student Record & Academic Management Platform.
Validates all REST endpoints against FRS requirements: 200, 201, 400, 404, 409 responses.
"""

import pytest
import sys
import os

# Add parent directory to sys.path so app can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import create_app
from app.models import student_store, Student


@pytest.fixture
def client():
    """Configures a test client with fresh seed state for each test run."""
    app = create_app({"TESTING": True})
    student_store.reset(seed=True)
    with app.test_client() as test_client:
        yield test_client
    student_store.reset(seed=True)


class TestHealthCheck:
    """Verifies service liveness and readiness probes."""

    def test_health_endpoint_returns_200_and_up(self, client):
        """FR-Health: Health probe must return HTTP 200 with status 'UP'."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "UP"
        assert data["service"] == "student-academic-platform"
        assert "version" in data
        assert "timestamp" in data
        assert data["total_students"] >= 2


class TestStudentListing:
    """Verifies retrieval of student records."""

    def test_get_students_returns_200_with_list(self, client):
        """FR-2.3: Retrieve all student records with HTTP 200."""
        response = client.get("/api/students")
        assert response.status_code == 200
        data = response.get_json()
        assert "students" in data
        assert data["count"] >= 2
        student_ids = [s["student_id"] for s in data["students"]]
        assert "STD2026001" in student_ids

    def test_get_students_filter_by_department(self, client):
        """FR-2.3: Filter student records by department."""
        response = client.get("/api/students?department=Computer%20Science")
        assert response.status_code == 200
        data = response.get_json()
        assert data["count"] >= 1
        for s in data["students"]:
            assert s["department"] == "Computer Science"

    def test_get_students_filter_by_invalid_semester(self, client):
        """Negative test: Non-numeric semester query param returns HTTP 400."""
        response = client.get("/api/students?semester=invalid")
        assert response.status_code == 400
        data = response.get_json()
        assert data["error"] == "Bad Request"


class TestStudentCreation:
    """Verifies student record creation and schema validation."""

    def test_create_student_success(self, client):
        """FR-2.1: Valid student payload successfully returns HTTP 201 Created."""
        payload = {
            "student_id": "STD2026099",
            "name": "Devops Student",
            "email": "devops.student@university.edu",
            "department": "Computer Science",
            "semester": 4,
        }
        response = client.post("/api/students", json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Student record created successfully."
        assert data["student"]["student_id"] == "STD2026099"
        assert data["student"]["name"] == "Devops Student"
        assert data["student"]["academic_standing"] == "Good Standing"

    def test_create_student_missing_id_returns_400(self, client):
        """Negative test: Missing student_id must return HTTP 400."""
        payload = {
            "name": "Missing ID",
            "email": "noid@university.edu",
        }
        response = client.post("/api/students", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert data["error"] == "Bad Request"
        assert "Student ID is mandatory" in data["message"]

    def test_create_student_invalid_email_returns_400(self, client):
        """Negative test: Invalid email format must return HTTP 400."""
        payload = {
            "student_id": "STD999",
            "name": "Invalid Email",
            "email": "notanemail",
        }
        response = client.post("/api/students", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert "valid university email" in data["message"] or "email" in data["message"].lower()

    def test_create_student_invalid_semester_returns_400(self, client):
        """Negative test: Semester out of 1-12 bounds must return HTTP 400."""
        payload = {
            "student_id": "STD998",
            "name": "Bad Semester",
            "email": "bad.sem@university.edu",
            "semester": 15,
        }
        response = client.post("/api/students", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert "Semester must be an integer between 1 and 12" in data["message"]

    def test_create_student_duplicate_id_returns_409(self, client):
        """Negative test: Attempting to create duplicate student_id returns HTTP 409 Conflict."""
        payload = {
            "student_id": "STD2026001",  # Already seeded
            "name": "Duplicate Student",
            "email": "duplicate@university.edu",
        }
        response = client.post("/api/students", json=payload)
        assert response.status_code == 409
        data = response.get_json()
        assert data["error"] == "Conflict"
        assert "already exists" in data["message"].lower()


class TestStudentLookup:
    """Verifies single student retrieval by ID."""

    def test_get_student_by_id_success(self, client):
        """FR-2.2: Existing student lookup returns HTTP 200 with details."""
        response = client.get("/api/students/STD2026001")
        assert response.status_code == 200
        data = response.get_json()
        assert data["student"]["student_id"] == "STD2026001"
        assert data["student"]["name"] == "Aarav Patel"
        assert "marks_history" in data

    def test_get_student_by_id_not_found_returns_404(self, client):
        """Negative test: Non-existent student lookup returns HTTP 404 Not Found."""
        response = client.get("/api/students/STD_DOES_NOT_EXIST")
        assert response.status_code == 404
        data = response.get_json()
        assert data["error"] == "Not Found"
        assert "does not exist" in data["message"]


class TestAcademicMarksAndGrading:
    """Verifies marks entry and automatic GPA calculation."""

    def test_record_marks_success(self, client):
        """FR-5.2: Recording valid marks returns HTTP 201 and updates GPA."""
        payload = {
            "course_code": "CS305",
            "marks": 95.0,
            "credits": 4,
        }
        response = client.post("/api/students/STD2026001/marks", json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert data["mark_entry"]["letter_grade"] == "S"
        assert data["mark_entry"]["grade_points"] == 10.0
        assert data["cumulative_gpa"] > 0.0

    def test_record_marks_non_existent_student_returns_404(self, client):
        """Negative test: Posting marks for non-existent student returns HTTP 404."""
        payload = {"course_code": "CS101", "marks": 85.0}
        response = client.post("/api/students/UNKNOWN_ID/marks", json=payload)
        assert response.status_code == 404

    def test_record_marks_out_of_range_returns_400(self, client):
        """Negative test: Marks > 100 must return HTTP 400 Bad Request."""
        payload = {"course_code": "CS101", "marks": 150.0}
        response = client.post("/api/students/STD2026001/marks", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert "between 0.0 and 100.0" in data["message"]
