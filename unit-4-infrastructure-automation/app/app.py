"""
Enterprise Smart Library Management Platform - Application Server
Unit 4 Reference Microservice Deployment.
Authored by Shivraj Dhumal (PRN: 2125UMLM1008) - Sandip University.
"""

import os
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_DIR = os.environ.get("DB_DIR", os.path.join(os.path.dirname(__file__), "database"))
DB_PATH = os.path.join(DB_DIR, "library.db")


def init_db():
    """Initializes SQLite database and seeds default book catalog."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT,
            status TEXT DEFAULT 'available'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrow_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            borrower_name TEXT,
            borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    """)
    conn.commit()

    # Seed baseline catalog if empty (matching Om Tambe's verification output)
    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO books (id, title, author, isbn, status) VALUES (?, ?, ?, ?, ?)",
            (1, "The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565", "available"),
        )
        conn.commit()
    conn.close()


init_db()


@app.route("/", methods=["GET"])
def root():
    """Root endpoint matching Om Tambe's verification output."""
    return jsonify({
        "application": "Smart Library Management Platform",
        "status": "running"
    }), 200


@app.route("/api/health", methods=["GET"])
def health():
    """Health status probe matching Om Tambe's verification output."""
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/api/books", methods=["GET"])
def get_books():
    """Catalog retrieval endpoint matching Om Tambe's verification output."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author FROM books")
    rows = cursor.fetchall()
    conn.close()

    books = [{"author": r[2], "id": r[0], "title": r[1]} for r in rows]
    return jsonify(books), 200


@app.route("/api/books", methods=["POST"])
def add_book():
    """Registers a new book in the library catalog."""
    data = request.get_json() or {}
    title = data.get("title")
    author = data.get("author")
    if not title or not author:
        return jsonify({"error": "Title and author are required"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    book_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({"message": "Book added successfully", "id": book_id}), 201


@app.route("/api/borrow", methods=["POST"])
def borrow_book():
    """Borrows a book by book_id."""
    data = request.get_json() or {}
    book_id = data.get("book_id", 1)
    borrower = data.get("borrower_name", "Student")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()

    if not book:
        conn.close()
        return jsonify({"error": "Book not found"}), 404

    cursor.execute("UPDATE books SET status = 'borrowed' WHERE id = ?", (book_id,))
    cursor.execute("INSERT INTO borrow_records (book_id, borrower_name) VALUES (?, ?)", (book_id, borrower))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Book '{book_id}' successfully borrowed by {borrower}"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
