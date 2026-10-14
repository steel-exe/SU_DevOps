"""
Domain Models and In-Memory Data Store.
Authored by Om Tambe (PRN: 2125UMLM1065) - Sandip University.
Encapsulates Student, Book, Course, Attendance, and Grading business logic.
"""

import re
import threading
from typing import Dict, List, Optional, Any


class Book:
    """Library book domain entity supporting Smart Library platform compatibility."""

    def __init__(self, id: int, title: str, author: str):
        self.id = int(id)
        self.title = str(title).strip()
        self.author = str(author).strip()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
        }


class Student:
    """Student domain entity and academic performance calculator."""

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
        attendance_percentage: float = 100.0,
    ):
        self.student_id = str(student_id).strip()
        self.name = str(name).strip()
        self.email = str(email).strip().lower()
        self.department = str(department).strip()
        self.semester = int(semester)
        self.enrolled_credits = int(enrolled_credits)
        self.cumulative_gpa = float(cumulative_gpa)
        self.academic_standing = academic_standing
        self.attendance_percentage = float(attendance_percentage)
        self.attendance_warning = self.attendance_percentage < 75.0
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
        """Validates student domain attributes against institutional business rules."""
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
        """Converts percentage score (0-100) to Letter Grade and 10-point Grade Points."""
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
        """Submits course marks, calculates letter grade, and recalculates SGPA/CGPA."""
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

    def update_attendance(self, attended_sessions: int, total_sessions: int) -> float:
        """Computes aggregate attendance percentage and triggers <75% warning flag."""
        if total_sessions <= 0:
            raise ValueError("Total sessions must be greater than zero.")
        self.attendance_percentage = round((attended_sessions / total_sessions) * 100.0, 2)
        self.attendance_warning = self.attendance_percentage < 75.0
        return self.attendance_percentage

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
            "attendance_percentage": self.attendance_percentage,
            "attendance_warning": self.attendance_warning,
            "marks_count": len(self.marks_history),
        }


class DataStore:
    """Thread-safe in-memory store for Students and Books with baseline seed data."""

    def __init__(self, seed: bool = True):
        self._lock = threading.RLock()
        self._students: Dict[str, Student] = {}
        self._books: List[Book] = []
        if seed:
            self.seed_defaults()

    def seed_defaults(self) -> None:
        """Seeds default books and students for immediate functional demonstration."""
        with self._lock:
            self._students.clear()
            self._books.clear()

            # Seed Smart Library baseline book (matching Om Tambe's verification output)
            self._books.append(Book(id=1, title="The Great Gatsby", author="F. Scott Fitzgerald"))

            # Seed Student Platform baseline students
            s1 = Student(
                student_id="STD2026001",
                name="Aarav Patel",
                email="aarav.patel@sandipuniversity.edu.in",
                department="Computer Science",
                semester=5,
                enrolled_credits=18,
                cumulative_gpa=8.85,
                academic_standing="Good Standing",
                attendance_percentage=88.5,
            )
            s1.record_mark("CS301", 88.0, credits=4)
            s1.record_mark("CS302", 92.0, credits=4)

            s2 = Student(
                student_id="STD2026002",
                name="Pooja Sharma",
                email="pooja.sharma@sandipuniversity.edu.in",
                department="Information Technology",
                semester=4,
                enrolled_credits=20,
                cumulative_gpa=9.20,
                academic_standing="Good Standing",
                attendance_percentage=72.0,  # Below 75% -> attendance_warning: true
            )
            s2.record_mark("IT401", 94.0, credits=4)

            self._students[s1.student_id] = s1
            self._students[s2.student_id] = s2

    def get_books(self) -> List[Book]:
        """Returns all books in catalog."""
        with self._lock:
            return list(self._books)

    def get_all_students(self, department: Optional[str] = None, semester: Optional[int] = None) -> List[Student]:
        """Retrieves all students with optional filters."""
        with self._lock:
            results = list(self._students.values())
            if department:
                results = [s for s in results if s.department.lower() == department.lower()]
            if semester is not None:
                results = [s for s in results if s.semester == semester]
            return results

    def get_student_by_id(self, student_id: str) -> Optional[Student]:
        """Looks up a single student by student_id."""
        with self._lock:
            return self._students.get(student_id.strip())

    def create_student(self, data: Dict[str, Any]) -> Student:
        """Validates and creates a new student in store."""
        student_id = str(data.get("student_id", "")).strip()
        name = str(data.get("name", "")).strip()
        email = str(data.get("email", "")).strip()
        department = str(data.get("department", "Computer Science")).strip()
        semester = data.get("semester", 1)
        attendance = float(data.get("attendance_percentage", 100.0))

        Student.validate(student_id, name, email, department, semester)

        with self._lock:
            if student_id in self._students:
                raise KeyError(f"Student with ID '{student_id}' already exists.")
            for existing in self._students.values():
                if existing.email.lower() == email.lower():
                    raise ValueError(f"Student with email '{email}' already registered.")

            student = Student(
                student_id=student_id,
                name=name,
                email=email,
                department=department,
                semester=int(semester),
                attendance_percentage=attendance,
            )
            self._students[student_id] = student
            return student

    def reset(self, seed: bool = True) -> None:
        """Resets store for tests."""
        with self._lock:
            self._students.clear()
            self._books.clear()
            if seed:
                self.seed_defaults()


# Global datastore instance
datastore = DataStore(seed=True)
student_store = datastore  # Backwards compatibility alias
