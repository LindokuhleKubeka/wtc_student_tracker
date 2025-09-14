import os
import unittest
from datetime import datetime
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
        # Set up test database file
        cls.test_db = "test_students.txt"
        os.environ['DATABASE'] = cls.test_db  # Override DATABASE for tests
        initialize_database()

    @classmethod
    def tearDownClass(cls):
        # Clean up test database
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

    def setUp(self):
        # Clear test database for each test
        with open(self.test_db, 'w') as f:
            f.write("ID, Name, Attendance History\n")

    def test_initialize_database(self):
        initialize_database()
        self.assertTrue(os.path.exists(self.test_db))
        with open(self.test_db, 'r') as f:
            header = f.readline().strip()
        self.assertEqual(header, "ID, Name, Attendance History")

    def test_add_student(self):
        response = add_student("001", "Alice Johnson")
        self.assertIn("success", response.lower())
        with open(self.test_db, 'r') as f:
            data = f.read()
        self.assertIn("001, Alice Johnson", data)

    def test_add_student_duplicate(self):
        add_student("001", "Alice Johnson")
        response = add_student("001", "Bob Smith")
        self.assertIn("error", response.lower())
        
    def test_mark_attendance(self):
        add_student("001", "Alice Johnson")
        response = mark_attendance("001")
        self.assertIn("marked", response.lower())
        with open(self.test_db, 'r') as f:
            data = f.read()
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertIn(today, data)

    def test_mark_attendance_not_found(self):
        response = mark_attendance("999")
        self.assertIn("error", response.lower())

    def test_view_attendance(self):
        add_student("001", "Alice Johnson")
        mark_attendance("001")
        response = view_attendance("001")
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertIn(today, response)

    def test_view_attendance_not_found(self):
        response = view_attendance("999")
        self.assertIn("not found", response.lower())

    def test_view_all_attendance(self):
        add_student("001", "Alice Johnson")
        mark_attendance("001")
        add_student("002", "Bob Smith")
        response = view_all_attendance()
        self.assertIn("Alice Johnson", response)
        self.assertIn("Bob Smith", response)

    def test_generate_report(self):
        add_student("001", "Alice Johnson")
        mark_attendance("001")
        add_student("002", "Bob Smith")
        mark_attendance("002")
        mark_attendance("002")
        response = generate_report()
        self.assertIn("Alice Johnson: 1 day(s)", response)
        self.assertIn("Bob Smith: 2 day(s)", response)

if __name__ == "__main__":
    unittest.main()