"""
Enterprise Student Record & Academic Management Platform
Flask REST API Microservice Entrypoint.
"""

from datetime import datetime, timezone
import os
from flask import Flask, jsonify, request
from .models import student_store, Student


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
            "message": "An unexpected error occurred on the server.",
            "status_code": 500,
        }), 500

    # -------------------------------------------------------------
    # REST API Endpoints
    # -------------------------------------------------------------

    @app.route("/api/health", methods=["GET"])
    def health_check():
        """
        Liveness and readiness health probe.
        Returns:
            JSON object confirming service status 'UP' with HTTP 200.
        """
        return jsonify({
            "status": "UP",
            "service": "student-academic-platform",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_students": len(student_store.get_all()),
        }), 200

    @app.route("/api/students", methods=["GET"])
    def get_students():
        """
        Lists all registered students with optional query filters.
        Query Params:
            department (str): Optional department filter (e.g. 'Computer Science')
            semester (int): Optional semester filter (e.g. 3)
        Returns:
            JSON array of students with HTTP 200.
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

        students = student_store.get_all(department=dept, semester=sem)
        return jsonify({
            "count": len(students),
            "students": [s.to_dict() for s in students],
        }), 200

    @app.route("/api/students", methods=["POST"])
    def create_student():
        """
        Registers a new student record.
        Expects JSON payload with student_id, name, email, department, semester.
        Returns:
            HTTP 201 Created with student payload on success.
            HTTP 400 Bad Request on validation errors.
            HTTP 409 Conflict if student_id or email already exists.
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
            student = student_store.create(data)
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
            # Check if this is duplicate email or validation failure
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
        """
        Retrieves a single student record by their unique student_id.
        Returns:
            HTTP 200 with student details on success.
            HTTP 404 if student does not exist.
        """
        student = student_store.get_by_id(student_id)
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
        Records marks for a student and computes cumulative GPA.
        Accepts either /api/students/<student_id>/marks or /api/marks with student_id in body.
        Expects:
            course_code (str), marks (float, 0-100), credits (optional int, default 3).
        Returns:
            HTTP 201 Created with mark record and recalculated GPA.
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

        student = student_store.get_by_id(target_id)
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
