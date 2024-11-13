# attendance_tracker.py

import os
from datetime import datetime

# Constants
DATABASE = "students.txt"


def initialize_database():
    """
    Initialize the database file if it does not exist.

    Instructions:
    - Check if 'students.txt' exists in the project folder.
    - If it does not exist, create the file and add a header like "ID, Name, Attendance History".
    - Ensure that this function is called at the start of the program to set up the database.
    """
    pass  # TODO: Implement this function to set up the database file if it doesn't exist.


def add_student(student_id, name):
    """
    Add a new student to the database if the ID does not already exist.

    Instructions:
    - Open 'students.txt' and check if 'student_id' already exists.
    - If 'student_id' exists, return an error message indicating duplication.
    - If 'student_id' does not exist, write a new line in the format: 'student_id, name, []'.
    - Return a success message after adding the student.
    """
    pass  # TODO: Implement this function to add a student if the ID is unique.


def mark_attendance(student_id):
    """
    Mark attendance for a student for today's date.

    Instructions:
    - Open 'students.txt' and read all lines to locate the student by 'student_id'.
    - If the student is not found, return an error message.
    - If found, check if today's date is already in their attendance history.
    - If today's date is not already marked, append it to their attendance history.
    - Save the updated data back to 'students.txt' after marking attendance.
    - Return a message confirming the attendance was marked.
    """
    pass  # TODO: Implement this function to mark attendance for today if not already marked.


def view_attendance(student_id):
    """
    View the attendance history for a specific student.

    Instructions:
    - Open 'students.txt' and search for the student by 'student_id'.
    - If the student is not found, return an error message.
    - If found, return their attendance history in a readable format.
    """
    pass  # TODO: Implement this function to view a specific student's attendance history.


def view_all_attendance():
    """
    View attendance records for all students.

    Instructions:
    - Open 'students.txt' and read each student's attendance record.
    - Format each record to display 'student_id', 'name', and 'attendance history'.
    - Return all attendance records in a readable format.
    """
    pass  # TODO: Implement this function to view all students' attendance history.


def generate_report():
    """
    Generate a report of attendance counts for each student.

    Instructions:
    - Open 'students.txt' and read each student's record.
    - Count the number of attendance entries for each student.
    - Return a report with 'student_id', 'name', and 'total attendance days'.
    """
    pass  # TODO: Implement this function to generate an attendance report.


if __name__ == "__main__":
    # Example usage (You may replace this with actual menu-driven code for students to interact with)

    # Initialize the database on program start
    initialize_database()

    # Sample actions (to be replaced with user interaction or testing)
    print("Attendance Tracker")
    print(add_student("001", "Alice Johnson"))
    print(add_student("002", "Bob Smith"))
    print(mark_attendance("001"))
    print(view_attendance("001"))
    print(view_all_attendance())
    print(generate_report())
