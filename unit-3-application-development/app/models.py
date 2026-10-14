"""
Student Domain Model and Repository Layer.
Provides domain entity validation, grading logic, and thread-safe data persistence.
"""

import re
import threading
from typing import Dict, List, Optional, Any


class Student:
    """Domain model representing a university student and academic performance."""

    def __init__(
        self,
        student_id: str,
        name: str,
        email: str,
        department: str = "Computer Science",
        semester: int = 1,
        enrolled_credits: int = 0,
        cumulative_gpa: float = 0.0,
        academic_standing: str = "Good Standing",
    ):
        self.student_id = str(student_id).strip()
        self.name = str(name).strip()
        self.email = str(email).strip().lower()
        self.department = str(department).strip()
        self.semester = int(semester)
        self.enrolled_credits = int(enrolled_credits)
        self.cumulative_gpa = float(cumulative_gpa)
        self.academic_standing = academic_standing
        self.marks_history: List[Dict[str, Any]] = []

    @classmethod
    def validate(
        cls,
        student_id: str,
        name: str,
        email: str,
        department: Optional[str] = None,
        semester: Any = 1,
    ) -> bool:
        """
        Validates student attributes against business rules.
        Raises ValueError if any field fails validation constraints.
        """
        if not student_id or not str(student_id).strip():
            raise ValueError("Student ID is mandatory and cannot be empty.")
        if not re.match(r"^[A-Za-z0-9_-]{3,20}$", str(student_id).strip()):
            raise ValueError("Student ID must be 3-20 alphanumeric characters (hyphens and underscores allowed).")

        if not name or not str(name).strip():
            raise ValueError("Student name is mandatory and cannot be empty.")
        if len(str(name).strip()) < 2:
            raise ValueError("Student name must be at least 2 characters long.")

        if not email or "@" not in str(email):
            raise ValueError("A valid university email address is mandatory.")
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, str(email).strip()):
            raise ValueError("Invalid email format.")

        try:
            sem = int(semester)
            if sem < 1 or sem > 12:
                raise ValueError("Semester must be an integer between 1 and 12.")
        except (ValueError, TypeError):
            raise ValueError("Semester must be an integer between 1 and 12.")

        return True

    @staticmethod
    def calculate_grade(marks: float) -> tuple[str, float]:
        """Maps percentage marks (0-100) to Letter Grade and Grade Points (10-point scale)."""
        if marks < 0 or marks > 100:
            raise ValueError("Marks must be between 0.0 and 100.0.")
        if marks >= 90.0:
            return "S", 10.0
        elif marks >= 80.0:
            return "A", 9.0
        elif marks >= 70.0:
            return "B", 8.0
        elif marks >= 60.0:
            return "C", 7.0
        elif marks >= 50.0:
            return "D", 6.0
        elif marks >= 40.0:
            return "E", 5.0
        else:
            return "F", 0.0

    def record_mark(self, course_code: str, marks: float, credits: int = 3) -> Dict[str, Any]:
        """Records academic marks for a course and updates cumulative GPA."""
        letter_grade, grade_points = self.calculate_grade(marks)
        mark_entry = {
            "course_code": course_code.strip().upper(),
            "marks": round(float(marks), 2),
            "credits": int(credits),
            "letter_grade": letter_grade,
            "grade_points": grade_points,
        }
        self.marks_history.append(mark_entry)

        # Recalculate CGPA
        total_points = sum(m["grade_points"] * m["credits"] for m in self.marks_history)
        total_credits = sum(m["credits"] for m in self.marks_history)
        self.enrolled_credits = total_credits
        self.cumulative_gpa = round(total_points / total_credits, 2) if total_credits > 0 else 0.0

        if self.cumulative_gpa < 5.0:
            self.academic_standing = "Academic Warning"
        else:
            self.academic_standing = "Good Standing"

        return mark_entry

    def to_dict(self) -> Dict[str, Any]:
        """Serializes domain model to JSON-compatible dictionary."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "semester": self.semester,
            "enrolled_credits": self.enrolled_credits,
            "cumulative_gpa": round(self.cumulative_gpa, 2),
            "academic_standing": self.academic_standing,
            "marks_count": len(self.marks_history),
        }


class StudentStore:
    """Thread-safe in-memory store for Student entities with baseline seed data."""

    def __init__(self, seed: bool = True):
        self._lock = threading.RLock()
        self._students: Dict[str, Student] = {}
        if seed:
            self.seed_defaults()

    def seed_defaults(self) -> None:
        """Seeds default students for immediate functional demonstration."""
        with self._lock:
            self._students.clear()
            s1 = Student(
                student_id="STD2026001",
                name="Aarav Patel",
                email="aarav.patel@university.edu",
                department="Computer Science",
                semester=3,
                enrolled_credits=18,
                cumulative_gpa=8.85,
                academic_standing="Good Standing",
            )
            s1.record_mark("CS301", 88.0, credits=4)
            s1.record_mark("CS302", 92.0, credits=4)

            s2 = Student(
                student_id="STD2026002",
                name="Pooja Sharma",
                email="pooja.sharma@university.edu",
                department="Information Technology",
                semester=4,
                enrolled_credits=20,
                cumulative_gpa=9.20,
                academic_standing="Good Standing",
            )
            s2.record_mark("IT401", 94.0, credits=4)

            self._students[s1.student_id] = s1
            self._students[s2.student_id] = s2

    def get_all(self, department: Optional[str] = None, semester: Optional[int] = None) -> List[Student]:
        """Retrieves all students, optionally filtered by department or semester."""
        with self._lock:
            results = list(self._students.values())
            if department:
                results = [s for s in results if s.department.lower() == department.lower()]
            if semester is not None:
                results = [s for s in results if s.semester == semester]
            return results

    def get_by_id(self, student_id: str) -> Optional[Student]:
        """Finds a student by their unique student_id."""
        with self._lock:
            return self._students.get(student_id.strip())

    def create(self, data: Dict[str, Any]) -> Student:
        """Validates and creates a new student in the datastore."""
        student_id = str(data.get("student_id", "")).strip()
        name = str(data.get("name", "")).strip()
        email = str(data.get("email", "")).strip()
        department = str(data.get("department", "Computer Science")).strip()
        semester = data.get("semester", 1)

        # Validate domain constraints
        Student.validate(student_id, name, email, department, semester)

        with self._lock:
            if student_id in self._students:
                raise KeyError(f"Student with ID '{student_id}' already exists.")
            # Check email uniqueness
            for existing in self._students.values():
                if existing.email.lower() == email.lower():
                    raise ValueError(f"Student with email '{email}' already registered.")

            student = Student(
                student_id=student_id,
                name=name,
                email=email,
                department=department,
                semester=int(semester),
            )
            self._students[student_id] = student
            return student

    def update(self, student_id: str, data: Dict[str, Any]) -> Optional[Student]:
        """Updates mutable fields on an existing student."""
        with self._lock:
            student = self._students.get(student_id.strip())
            if not student:
                return None

            if "name" in data and data["name"]:
                student.name = str(data["name"]).strip()
            if "department" in data and data["department"]:
                student.department = str(data["department"]).strip()
            if "semester" in data:
                sem = int(data["semester"])
                if 1 <= sem <= 12:
                    student.semester = sem
                else:
                    raise ValueError("Semester must be between 1 and 12.")
            if "academic_standing" in data and data["academic_standing"]:
                student.academic_standing = str(data["academic_standing"]).strip()

            return student

    def delete(self, student_id: str) -> bool:
        """Deletes a student record by ID."""
        with self._lock:
            if student_id.strip() in self._students:
                del self._students[student_id.strip()]
                return True
            return False

    def reset(self, seed: bool = True) -> None:
        """Resets the repository to empty or seed state for tests."""
        with self._lock:
            self._students.clear()
            if seed:
                self.seed_defaults()


# Global repository instance
student_store = StudentStore(seed=True)
