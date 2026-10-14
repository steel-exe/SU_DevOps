from flask import Blueprint, render_template, request, jsonify
from app.services.student_service import StudentService

views_bp = Blueprint("views", __name__)


@views_bp.route("/", methods=["GET"])
def dashboard():
    """Enterprise Student Record & Academic Management Dashboard View."""
    if request.headers.get("Accept") == "application/json" or request.args.get("format") == "json":
        return jsonify({
            "application": "Smart Library Management Platform",
            "status": "running",
            "platform": "Student Record & Academic Management Platform",
            "lead": "Shivraj Dhumal (PRN: 2125UMLM1008)",
            "institution": "Sandip University",
        }), 200
    stats = StudentService.get_dashboard_stats()
    students = StudentService.list_students()
    courses = StudentService.list_courses()
    return render_template("index.html", stats=stats, students=students, courses=courses)
