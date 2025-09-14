import os
from datetime import datetime

# Constants
DATABASE = os.getenv("DATABASE", "students.txt")

def initialize_database():
    """
    Initialize the database file if it does not exist.
    """
    if not os.path.exists(DATABASE):
        with open(DATABASE, 'w') as f:
            f.write("ID, Name, Attendance History\n")

def add_student(student_id, name):
    """
    Add a new student to the database if the ID does not already exist.
    """
    initialize_database()
    with open(DATABASE, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:  # Skip header
            if line.strip() and line.split(",")[0].strip() == student_id:
                return f"Error: Student ID {student_id} already exists."
    
    with open(DATABASE, 'a') as f:
        f.write(f"{student_id}, {name}, []\n")
    return f"Success: Student {name} (ID: {student_id}) added."

def mark_attendance(student_id):
    """
    Mark attendance for a student for today's date.
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
            if line.strip() and line.split(",")[0].strip() == student_id:
                found = True
                parts = line.strip().split(", ", 2)
                attendance = eval(parts[2]) if parts[2].strip() else []
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
    """
    initialize_database()
    with open(DATABASE, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            if line.strip() and line.split(",")[0].strip() == student_id:
                parts = line.strip().split(", ", 2)
                attendance = eval(parts[2]) if parts[2].strip() else []
                return f"Attendance for {parts[1]} (ID: {student_id}): {attendance}"
    return f"Student ID {student_id} not found."

def view_all_attendance():
    """
    View attendance records for all students.
    """
    initialize_database()
    result = "All Attendance Records:\n"
    with open(DATABASE, 'r') as f:
        lines = f.readlines()
        if len(lines) <= 1:
            return "No students found."
        for line in lines[1:]:
            if line.strip():
                parts = line.strip().split(", ", 2)
                attendance = eval(parts[2]) if parts[2].strip() else []
                result += f"ID: {parts[0]}, Name: {parts[1]}, Attendance: {attendance}\n"
    return result

def generate_report():
    """
    Generate a report of attendance counts for each student.
    """
    initialize_database()
    result = "Attendance Report:\n"
    with open(DATABASE, 'r') as f:
        lines = f.readlines()
        if len(lines) <= 1:
            return "No students found."
        for line in lines[1:]:
            if line.strip():
                parts = line.strip().split(", ", 2)
                attendance = eval(parts[2]) if parts[2].strip() else []
                result += f"{parts[1]} (ID: {parts[0]}): {len(attendance)} day(s)\n"
    return result

if __name__ == "__main__":
    initialize_database()
    print("Attendance Tracker")
    print(add_student("001", "Alice Johnson"))
    print(add_student("002", "Bob Smith"))
    print(mark_attendance("001"))
    print(view_attendance("001"))
    print(view_all_attendance())
    print(generate_report())