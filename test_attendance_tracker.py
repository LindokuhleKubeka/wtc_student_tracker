# test_attendance_tracker.py

import os
import unittest
from attendance_tracker import (
    initialize_database,
    add_student,
    mark_attendance,
    view_attendance,
    view_all_attendance,
    generate_report,
    DATABASE
)

class TestAttendanceTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the test database file before any tests run
        cls.test_db = "test_students.txt"
        global DATABASE
        DATABASE = cls.test_db
        initialize_database()

    @classmethod
    def tearDownClass(cls):
        # Clean up the test database file after all tests run
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

    def setUp(self):
        # Clear contents of the test database file for a clean slate each test
        with open(self.test_db, 'w') as f:
            f.write("ID, Name, Attendance History\n")

    def test_initialize_database(self):
        # Test if the database file initializes correctly
        initialize_database()
        self.assertTrue(os.path.exists(self.test_db))
        with open(self.test_db, 'r') as f:
            header = f.readline().strip()
        self.assertEqual(header, "ID, Name, Attendance History")

    def test_add_student(self):
        # Test adding a new student
        response = add_student("001", "Alice Johnson")
        self.assertIn("success", response.lower())
        with open(self.test_db, 'r') as f:
            data = f.read()
        self.assertIn("001, Alice Johnson", data)

    def test_add_student_duplicate(self):
        # Test adding a duplicate student ID
        add_student("001", "Alice Johnson")
        response = add_student("001", "Bob Smith")
        self.assertIn("error", response.lower())
        
    def test_mark_attendance(self):
        # Test marking attendance for an existing student
        add_student("001", "Alice Johnson")
        response = mark_attendance("001")
        self.assertIn("marked", response.lower())
        with open(self.test_db, 'r') as f:
            data = f.read()
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertIn(today, data)

    def test_mark_attendance_not_found(self):
        # Test marking attendance for a non-existent student
        response = mark_attendance("999")
        self.assertIn("error", response.lower())

    def test_view_attendance(self):
        # Test viewing attendance for a student
        add_student("001", "Alice Johnson")
        mark_attendance("001")
        response = view_attendance("001")
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertIn(today, response)

    def test_view_attendance_not_found(self):
        # Test viewing attendance for a non-existent student
        response = view_attendance("999")
        self.assertIn("not found", response.lower())

    def test_view_all_attendance(self):
        # Test viewing all attendance records
        add_student("001", "Alice Johnson")
        mark_attendance("001")
        add_student("002", "Bob Smith")
        response = view_all_attendance()
        self.assertIn("Alice Johnson", response)
        self.assertIn("Bob Smith", response)

    def test_generate_report(self):
        # Test generating an attendance report
        add_student("001", "Alice Johnson")
        mark_attendance("001")
        add_student("002", "Bob Smith")
        mark_attendance("002")
        mark_attendance("002")  # Mark Bob's attendance twice
        response = generate_report()
        self.assertIn("Alice Johnson: 1 day(s)", response)
        self.assertIn("Bob Smith: 2 day(s)", response)

if __name__ == "__main__":
    unittest.main()
