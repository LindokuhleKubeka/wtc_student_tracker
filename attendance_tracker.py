import os
from datetime import datetime
from flask import Flask, request, jsonify  # Added Flask imports

app = Flask(__name__)  # Initialize Flask app

# Constants
DATABASE = os.getenv("DATABASE", "test_students.txt")  # Use test_students.txt for tests

def initialize_database():
    """Initialize the database file if it does not exist."""
    print(f"Creating database at: {os.path.abspath(DATABASE)}")  # Debug logging added
    if not os.path.exists(DATABASE):
        with open(DATABASE, 'w', encoding='utf-8') as f:
            f.write("ID, Name, Attendance History\n")

def add_student(student_id, name):
    """Add a new student to the database if the ID does not already exist."""
    initialize_database()
    try:
        with open(DATABASE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[1:]:  # Skip header
                if line.strip() and line.split(",")[0].strip() == student_id:
                    return f"Error: Student ID {student_id} already exists."
    except FileNotFoundError:
        initialize_database()
    try:
        with open(DATABASE, 'a', encoding='utf-8') as f:
            f.write(f"{student_id}, {name}, []\n")  # Add space after commas
        return f"Success: Student {name} (ID: {student_id}) added."
    except Exception as e:
        return f"Error: Failed to add student {name} (ID: {student_id}). {str(e)}"

def mark_attendance(student_id):
    """Mark attendance for a student for today's date."""
    initialize_database()
    today = datetime.now().strftime("%Y-%m-%d")
    lines = []
    found = False
    try:
        with open(DATABASE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return f"Error: Database file not found."
    
    try:
        with open(DATABASE, 'w', encoding='utf-8') as f:
            f.write(lines[0])  # Write header
            for line in lines[1:]:
                if line.strip() and line.split(",")[0].strip() == student_id:
                    found = True
                    parts = line.strip().split(",", 2)
                    attendance = eval(parts[2].strip()) if parts[2].strip() else []
                    if today in attendance:
                        return f"Error: Attendance for {student_id} already marked for {today}."
                    attendance.append(today)
                    f.write(f"{parts[0]}, {parts[1]}, {attendance}\n")
                else:
                    f.write(line)
        if not found:
            return f"Error: Student ID {student_id} not found."
        return f"Attendance marked for student ID {student_id} on {today}."
    except Exception as e:
        return f"Error: Failed to mark attendance for {student_id}. {str(e)}"

def view_attendance(student_id):
    """View the attendance history for a specific student."""
    initialize_database()
    try:
        with open(DATABASE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[1:]:
                if line.strip() and line.split(",")[0].strip() == student_id:
                    parts = line.strip().split(",", 2)
                    attendance = eval(parts[2].strip()) if parts[2].strip() else []
                    return f"Attendance for {parts[1].strip()} (ID: {student_id}): {attendance}"
        return f"Student ID {student_id} not found."
    except FileNotFoundError:
        return f"Error: Database file not found."
    except Exception as e:
        return f"Error: Failed to view attendance for {student_id}. {str(e)}"

def view_all_attendance():
    """View attendance records for all students."""
    initialize_database()
    result = "All Attendance Records:\n"
    try:
        with open(DATABASE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) <= 1:
                return "No students found."
            for line in lines[1:]:
                if line.strip():
                    parts = line.strip().split(",", 2)
                    attendance = eval(parts[2].strip()) if parts[2].strip() else []
                    result += f"ID: {parts[0].strip()}, Name: {parts[1].strip()}, Attendance: {attendance}\n"
        return result
    except FileNotFoundError:
        return "No students found."
    except Exception as e:
        return f"Error: Failed to view all attendance. {str(e)}"

# Flask Routes
@app.route('/students', methods=['POST'])
def api_add_student():
    """Add a new student via POST request with JSON payload."""
    try:
        raw_data = request.get_data(as_text=True)  # Log raw request data
        print(f"Raw request data: {raw_data}")
        data = request.get_json(force=True, silent=True)  # Robust JSON parsing
        if data is None:
            print("Failed to parse JSON")
            return jsonify({"error": "Invalid JSON format"}), 400
        print(f"Parsed JSON: {data}")
        student_id = data.get('student_id')
        name = data.get('name')
        if not student_id or not name:
            print(f"Missing fields: student_id={student_id}, name={name}")
            return jsonify({"error": "Missing student_id or name"}), 400
        result = add_student(student_id, name)
        print(f"Add student result: {result}")
        return jsonify({"message": result})
    except Exception as e:
        print(f"Error in api_add_student: {str(e)}")
        return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400

@app.route('/attendance/<student_id>', methods=['POST'])
def api_mark_attendance(student_id):
    """Mark attendance for a student via POST request."""
    result = mark_attendance(student_id)
    print(f"Mark attendance result: {result}")
    return jsonify({"message": result})

@app.route('/attendance/<student_id>', methods=['GET'])
def api_view_attendance(student_id):
    """Retrieve attendance history for a specific student via GET request."""
    result = view_attendance(student_id)
    print(f"View attendance result: {result}")
    return jsonify({"message": result})

@app.route('/attendance', methods=['GET'])
def api_view_all_attendance():
    """Retrieve attendance records for all students via GET request."""
    result = view_all_attendance()
    print(f"View all attendance result: {result}")
    return jsonify({"message": result})

if __name__ == "__main__":
    initialize_database()
    print("Attendance Tracker")
    print(add_student("001", "Alice Johnson"))
    print(add_student("002", "Bob Smith"))
    print(mark_attendance("001"))
    print(mark_attendance("002"))
    print(mark_attendance("002"))  # Add second attendance for Bob
    print(view_attendance("001"))
    print(view_all_attendance())
    app.run(host='0.0.0.0', port=5000, debug=True)  # Run Flask app in debug mode