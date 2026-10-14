"""
Enterprise Student Record & Academic Management Platform
Flask REST API Microservice Entrypoint.
Authored by Om Tambe (PRN: 2125UMLM1065) - Sandip University.
"""

from datetime import datetime, timezone
import os
from flask import Flask, jsonify, request
from .models import datastore, Student


def create_app(test_config=None) -> Flask:
    """Application factory for Flask REST microservice."""
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

    if test_config:
        app.config.update(test_config)

    # -------------------------------------------------------------
    # Error Handlers
    # -------------------------------------------------------------
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad Request",
            "message": str(error.description if hasattr(error, "description") else error),
            "status_code": 400,
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not Found",
            "message": str(error.description if hasattr(error, "description") else error),
            "status_code": 404,
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "Method Not Allowed",
            "message": "The HTTP method is not supported for this endpoint.",
            "status_code": 405,
        }), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected server error occurred.",
            "status_code": 500,
        }), 500

    # -------------------------------------------------------------
    # REST API Endpoints
    # -------------------------------------------------------------

    @app.route("/", methods=["GET"])
    def root():
        """
        Root endpoint displaying application operational status.
        Matches Om Tambe's verification output:
        {"application": "Smart Library Management Platform", "status": "running"}
        """
        return jsonify({
            "application": "Smart Library Management Platform",
            "status": "running",
            "platform": "Student Record & Academic Management Platform",
            "lead": "Om Tambe (PRN: 2125UMLM1065)",
            "institution": "Sandip University",
        }), 200

    @app.route("/api/health", methods=["GET"])
    def health_check():
        """
        Liveness and readiness health probe.
        Matches Om Tambe's verification output: {"status": "healthy"}.
        """
        return jsonify({
            "status": "healthy",
            "service": "student-academic-platform",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_students": len(datastore.get_all_students()),
        }), 200

    @app.route("/api/books", methods=["GET"])
    def get_books():
        """
        Catalog retrieval endpoint for Smart Library platform compatibility.
        Matches Om Tambe's verification output:
        [{"author": "F. Scott Fitzgerald", "id": 1, "title": "The Great Gatsby"}]
        """
        books = datastore.get_books()
        return jsonify([b.to_dict() for b in books]), 200

    @app.route("/api/students", methods=["GET"])
    def get_students():
        """
        Lists registered student records with optional filtering.
        Query Params:
            department (str): Filter by department name
            semester (int): Filter by semester number
        """
        dept = request.args.get("department")
        sem_param = request.args.get("semester")
        sem = None
        if sem_param is not None:
            try:
                sem = int(sem_param)
            except ValueError:
                return jsonify({
                    "error": "Bad Request",
                    "message": "Semester query parameter must be an integer.",
                    "status_code": 400,
                }), 400

        students = datastore.get_all_students(department=dept, semester=sem)
        return jsonify({
            "count": len(students),
            "students": [s.to_dict() for s in students],
        }), 200

    @app.route("/api/students", methods=["POST"])
    def create_student():
        """
        Registers a new student profile in the system.
        Expects JSON with student_id, name, email, department, semester.
        """
        if not request.is_json:
            return jsonify({
                "error": "Bad Request",
                "message": "Request body must be valid application/json.",
                "status_code": 400,
            }), 400

        data = request.get_json()
        if not data:
            return jsonify({
                "error": "Bad Request",
                "message": "Request payload cannot be empty.",
                "status_code": 400,
            }), 400

        try:
            student = datastore.create_student(data)
            return jsonify({
                "message": "Student record created successfully.",
                "student": student.to_dict(),
            }), 201
        except KeyError as ke:
            return jsonify({
                "error": "Conflict",
                "message": str(ke).strip("'\""),
                "status_code": 409,
            }), 409
        except ValueError as ve:
            err_msg = str(ve)
            if "already registered" in err_msg.lower():
                return jsonify({
                    "error": "Conflict",
                    "message": err_msg,
                    "status_code": 409,
                }), 409
            return jsonify({
                "error": "Bad Request",
                "message": err_msg,
                "status_code": 400,
            }), 400
        except Exception as e:
            return jsonify({
                "error": "Internal Server Error",
                "message": str(e),
                "status_code": 500,
            }), 500

    @app.route("/api/students/<student_id>", methods=["GET"])
    def get_student_by_id(student_id: str):
        """Retrieves a single student profile by student_id."""
        student = datastore.get_student_by_id(student_id)
        if not student:
            return jsonify({
                "error": "Not Found",
                "message": f"Student with ID '{student_id}' does not exist.",
                "status_code": 404,
            }), 404

        return jsonify({
            "student": student.to_dict(),
            "marks_history": student.marks_history,
        }), 200

    @app.route("/api/students/<student_id>/marks", methods=["POST"])
    @app.route("/api/marks", methods=["POST"])
    def record_marks(student_id: str = None):
        """
        Submits continuous assessment marks, converts to Letter Grade, and recalculates GPA.
        Expects: course_code (str), marks (float 0-100), credits (int, default 3).
        """
        if not request.is_json:
            return jsonify({
                "error": "Bad Request",
                "message": "Request body must be valid application/json.",
                "status_code": 400,
            }), 400

        data = request.get_json() or {}
        target_id = student_id or data.get("student_id")
        if not target_id:
            return jsonify({
                "error": "Bad Request",
                "message": "Student ID is required.",
                "status_code": 400,
            }), 400

        student = datastore.get_student_by_id(target_id)
        if not student:
            return jsonify({
                "error": "Not Found",
                "message": f"Student with ID '{target_id}' does not exist.",
                "status_code": 404,
            }), 404

        course_code = str(data.get("course_code", "")).strip()
        if not course_code:
            return jsonify({
                "error": "Bad Request",
                "message": "Course code is mandatory.",
                "status_code": 400,
            }), 400

        try:
            marks = float(data.get("marks"))
        except (ValueError, TypeError):
            return jsonify({
                "error": "Bad Request",
                "message": "Marks must be a valid numeric value between 0.0 and 100.0.",
                "status_code": 400,
            }), 400

        credits = int(data.get("credits", 3))

        try:
            entry = student.record_mark(course_code, marks, credits)
            return jsonify({
                "message": "Academic mark recorded successfully.",
                "mark_entry": entry,
                "cumulative_gpa": student.cumulative_gpa,
                "academic_standing": student.academic_standing,
            }), 201
        except ValueError as ve:
            return jsonify({
                "error": "Bad Request",
                "message": str(ve),
                "status_code": 400,
            }), 400

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
