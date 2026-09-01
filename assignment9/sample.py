

import sqlite3
with sqlite3.connect("school.db") as conn:
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        student_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        age INTEGER,
        major TEXT
    )""")


def enroll_student(cursor, student, course):

    # Find student
    cursor.execute(
        "SELECT * FROM Students WHERE name = ?",
        (student,)
    )

    results = cursor.fetchall()

    if len(results) > 0:
        student_id = results[0][0]
    else:
        print(f"There was no student named {student}.")
        return

    # Find course
    cursor.execute(
        "SELECT * FROM Courses WHERE course_name = ?",
        (course,)
    )

    results = cursor.fetchall()

    if len(results) > 0:
        course_id = results[0][0]
    else:
        print(f"There was no course named {course}.")
        return

    # Check if already enrolled
    cursor.execute(
        "SELECT * FROM Enrollments WHERE student_id = ? AND course_id = ?",
        (student_id, course_id)
    )

    results = cursor.fetchall()

    if len(results) > 0:
        print(f"Student {student} is already enrolled in course {course}.")


        return



cursor.execute("""SELECT Students.name, Enrollments.course_id
FROM Students
LEFT JOIN Enrollments ON Students.student_id = Enrollments.student_id;""")


