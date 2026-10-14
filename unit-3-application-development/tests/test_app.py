"""
Automated Pytest Suite for Enterprise Academic Platform.
Authored by Om Tambe (PRN: 2125UMLM1065) - Sandip University.
Validates /, /api/health, /api/books, /api/students, /api/courses, and HTTP status codes.
"""

import pytest
from app import create_app
from database.db import db


@pytest.fixture
def client():
    """Configures a test client with fresh database state for each test run."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        db.reset()
        yield test_client
        db.reset()


def test_root_status_endpoint(client):
    """Verifies GET / returns running application status."""
    response = client.get("/", headers={"Accept": "application/json"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["application"] == "Smart Library Management Platform"
    assert data["status"] == "running"


def test_health_check_endpoint(client):
    """Verifies GET /api/health returns status UP."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "UP"


def test_books_catalog_endpoint(client):
    """Verifies GET /api/books returns catalog record."""
    response = client.get("/api/books")
    assert response.status_code == 200
    books = response.get_json()
    assert isinstance(books, list)
    assert len(books) >= 1
    assert books[0]["title"] == "The Great Gatsby"


def test_list_students_endpoint(client):
    """Verifies GET /api/students returns registered students."""
    response = client.get("/api/students")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] >= 4


def test_register_student_endpoint(client):
    """Verifies POST /api/students registers a student with HTTP 201."""
    payload = {
        "student_id": "S999",
        "name": "Om Tambe",
        "email": "om.tambe@sandipuniversity.edu.in",
        "department": "Computer Science",
        "semester": 6,
    }
    response = client.post("/api/students", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Student registered successfully"
    assert data["student"]["student_id"] == "S999"


def test_get_student_by_id_endpoint(client):
    """Verifies GET /api/students/<id> returns profile."""
    response = client.get("/api/students/S101")
    assert response.status_code == 200
    data = response.get_json()
    assert data["student_id"] == "S101"
