import os
from datetime import datetime

# Constants
DATABASE = "students.txt"

def initialize_database():
    """
    Initialize the database file if it does not exist.
    Creates 'students.txt' with a header if it doesn't exist.
    """
    if not os.path.exists(DATABASE):
        with open(DATABASE, 'w') as f:
            f.write("ID, Name, Attendance History\n")

def add_student(student_id, name):
    """
    Add a new student to the database if the ID does not already exist.
    Returns a success or error message.
    """
    initialize_database()
    with open(DATABASE, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:  # Skip header
            if line.startswith(f"{student_id},"):
                return f"Error: Student ID {student_id} already exists."
    
    with open(DATABASE, 'a') as f:
        f.write(f"{student_id}, {name}, []\n")
    return f"Success: Student {name} (ID: {student_id}) added."

def mark_attendance(student_id):
    """
    Mark attendance for a student for today's date.
    Returns a confirmation or error message.
    """
    initialize_database()
    today = datetime.now().strftime("%Y-%m-%d")
    lines = []
    found = False
    
    with open(DATABASE, 'r') as f:
        lines = f.readlines()
    
    with open(DATABASE, 'w') as f:
        f.write(lines[0])  # Write header
        for line in lines[1:]:
            if line.startswith(f"{student_id},"):
                found = True
                parts = line.strip().split(", ", 2)
                attendance = eval(parts[2]) if parts[2] else []
                if today in attendance:
                    return f"Error: Attendance for {student_id} already marked for {today}."
                attendance.append(today)
                f.write(f"{parts[0]}, {parts[1]}, {attendance}\n")
            else:
                f.write(line)
    
    if not found:
        return f"Error: Student ID {student_id} not found."
    return f"Attendance marked for student ID {student_id} on {today}."

def view_attendance(student_id):
    """
    View the attendance history for a specific student.
    Returns the history or an error message.
    """
    initialize_database()
    with open(DATABASE, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:  # Skip header
            if line.startswith(f"{student_id},"):
                parts = line.strip().split(", ", 2)
                attendance = eval(parts[2]) if parts[2] else []
                return f"Attendance for {parts[1]} (ID: {student_id}): {attendance}"
    return f"Student ID {student_id} not found."

def view_all_attendance():
    """
    View attendance records for all students.
    Returns formatted records.
    """
    initialize_database()
    result = "All Attendance Records:\n"
    with open(DATABASE, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:  # Skip header
            parts = line.strip().split(", ", 2)
            attendance = eval(parts[2]) if parts[2] else []
            result += f"ID: {parts[0]}, Name: {parts[1]}, Attendance: {attendance}\n"
    return result if len(lines) > 1 else "No students found."

def generate_report():
    """
    Generate a report of attendance counts for each student.
    Returns a formatted report.
    """
    initialize_database()
    result = "Attendance Report:\n"
    with open(DATABASE, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:  # Skip header
            parts = line.strip().split(", ", 2)
            attendance = eval(parts[2]) if parts[2] else []
            result += f"{parts[1]} (ID: {parts[0]}): {len(attendance)} day(s)\n"
    return result if len(lines) > 1 else "No students found."

if __name__ == "__main__":
    initialize_database()
    print("Attendance Tracker")
    print(add_student("001", "Alice Johnson"))
    print(add_student("002", "Bob Smith"))
    print(mark_attendance("001"))
    print(view_attendance("001"))
    print(view_all_attendance())
    print(generate_report())