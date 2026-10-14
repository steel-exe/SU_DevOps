"""
Automated Pytest Suite for Enterprise Academic Platform.
Authored by Om Tambe (PRN: 2125UMLM1065) - Sandip University.
Validates /, /api/health, /api/books, /api/students, /api/marks, and HTTP status codes.
"""

import pytest
import sys
import os

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import create_app
from app.models import datastore


@pytest.fixture
def client():
    """Configures a test client with fresh seed state for each test run."""
    app = create_app({"TESTING": True})
    datastore.reset(seed=True)
    with app.test_client() as test_client:
        yield test_client
    datastore.reset(seed=True)


class TestRootAndHealthEndpoints:
    """Verifies root platform status and health probes."""

    def test_root_endpoint_returns_running_status(self, client):
        """Verifies GET / returns Smart Library application status (Om Tambe verification)."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.get_json()
        assert data["application"] == "Smart Library Management Platform"
        assert data["status"] == "running"
        assert "Om Tambe" in data["lead"]

    def test_health_endpoint_returns_healthy(self, client):
        """Verifies GET /api/health returns status 'healthy' (Om Tambe verification)."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
        assert data["total_students"] >= 2


class TestBooksCatalog:
    """Verifies catalog retrieval for Smart Library compatibility."""

    def test_get_books_returns_great_gatsby(self, client):
        """Verifies GET /api/books returns seeded book record."""
        response = client.get("/api/books")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        book = data[0]
        assert book["author"] == "F. Scott Fitzgerald"
        assert book["title"] == "The Great Gatsby"
        assert book["id"] == 1


class TestStudentManagementEndpoints:
    """Verifies student registration, filtering, and lookup."""

    def test_get_students_list(self, client):
        """Verifies GET /api/students returns seeded list."""
        response = client.get("/api/students")
        assert response.status_code == 200
        data = response.get_json()
        assert data["count"] >= 2
        student_ids = [s["student_id"] for s in data["students"]]
        assert "STD2026001" in student_ids

    def test_get_students_filter_by_department(self, client):
        """Verifies department filtering."""
        response = client.get("/api/students?department=Computer%20Science")
        assert response.status_code == 200
        data = response.get_json()
        assert data["count"] >= 1
        for s in data["students"]:
            assert s["department"] == "Computer Science"

    def test_get_students_invalid_semester_returns_400(self, client):
        """Negative test: Non-numeric semester query returns 400."""
        response = client.get("/api/students?semester=abc")
        assert response.status_code == 400

    def test_create_student_success(self, client):
        """Verifies POST /api/students creates new record returning HTTP 201."""
        payload = {
            "student_id": "STD2026099",
            "name": "Om Tambe",
            "email": "om.tambe@sandipuniversity.edu.in",
            "department": "Computer Science",
            "semester": 6,
            "attendance_percentage": 95.0,
        }
        response = client.post("/api/students", json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Student record created successfully."
        assert data["student"]["student_id"] == "STD2026099"
        assert data["student"]["name"] == "Om Tambe"

    def test_create_student_missing_fields_returns_400(self, client):
        """Negative test: Missing student_id returns HTTP 400."""
        payload = {"name": "No ID", "email": "noid@sandipuniversity.edu.in"}
        response = client.post("/api/students", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert "Student ID is mandatory" in data["message"]

    def test_create_student_duplicate_id_returns_409(self, client):
        """Negative test: Duplicate student_id returns HTTP 409 Conflict."""
        payload = {
            "student_id": "STD2026001",
            "name": "Duplicate Student",
            "email": "duplicate@sandipuniversity.edu.in",
        }
        response = client.post("/api/students", json=payload)
        assert response.status_code == 409
        data = response.get_json()
        assert data["error"] == "Conflict"

    def test_get_student_by_id_success(self, client):
        """Verifies GET /api/students/<id> returns student profile."""
        response = client.get("/api/students/STD2026001")
        assert response.status_code == 200
        data = response.get_json()
        assert data["student"]["student_id"] == "STD2026001"
        assert data["student"]["name"] == "Aarav Patel"

    def test_get_student_by_id_not_found(self, client):
        """Negative test: Non-existent ID returns HTTP 404."""
        response = client.get("/api/students/INVALID_ID")
        assert response.status_code == 404


class TestAttendanceAndGrading:
    """Verifies low-attendance flags and SGPA/CGPA grading."""

    def test_low_attendance_flag_triggered_below_75(self, client):
        """Verifies that attendance < 75% sets attendance_warning = True."""
        response = client.get("/api/students/STD2026002")
        assert response.status_code == 200
        data = response.get_json()
        assert data["student"]["attendance_percentage"] < 75.0
        assert data["student"]["attendance_warning"] is True

    def test_record_marks_and_compute_gpa(self, client):
        """Verifies POST /api/students/<id>/marks records marks and updates GPA."""
        payload = {
            "course_code": "CS305",
            "marks": 96.0,
            "credits": 4,
        }
        response = client.post("/api/students/STD2026001/marks", json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert data["mark_entry"]["letter_grade"] == "S"
        assert data["mark_entry"]["grade_points"] == 10.0
        assert data["cumulative_gpa"] > 0.0

    def test_record_marks_out_of_range_returns_400(self, client):
        """Negative test: Marks > 100 returns HTTP 400."""
        payload = {"course_code": "CS101", "marks": 105.0}
        response = client.post("/api/students/STD2026001/marks", json=payload)
        assert response.status_code == 400
