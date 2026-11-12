import json
import os

FILE_NAME = "students.json"


# Load student records
def load_students():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                print("Invalid file format. Starting empty.")
        except (json.JSONDecodeError, OSError):
            print("File is empty or unreadable. Starting empty.")
    return []


# Save student records
def save_students():
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


students = load_students()


# Add student
def add_student():
    student_id = input("Enter Student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    if any(s["id"] == student_id for s in students):
        print("Student ID already exists!")
        return

    name = input("Enter Student Name: ").strip()
    department = input("Enter Department: ").strip()

    if not name or not department:
        print("Name and department cannot be empty.")
        return

    try:
        age = int(input("Enter Age: "))
        if age <= 0:
            print("Age must be positive.")
            return

        marks = [
            float(x.strip())
            for x in input("Enter Marks separated by commas: ").split(",")
        ]

        if not marks or any(m < 0 or m > 100 for m in marks):
            print("Marks must be between 0 and 100.")
            return

        attendance = float(input("Enter Attendance: "))

        if not 0 <= attendance <= 100:
            print("Attendance must be between 0 and 100.")
            return

    except ValueError:
        print("Please enter valid numbers.")
        return

    student = {
        "id": student_id,
        "name": name,
        "age": age,
        "department": department,
        "marks": marks,
        "attendance": attendance
    }

    students.append(student)
    save_students()
    print("Student added successfully!")


# View students
def view_students():
    if not students:
        print("No student records found.")
        return

    print("\n--- All Student Records ---")

    for s in students:
        print("\nID:", s["id"])
        print("Name:", s["name"])
        print("Age:", s["age"])
        print("Department:", s["department"])
        print("Marks:", s["marks"])
        print("Attendance:", str(s["attendance"]) + "%")


# Search student
def search_student():
    student_id = input("Enter Student ID to search: ").strip()

    for s in students:
        if s["id"] == student_id:
            print("\nStudent Found")
            print("Name:", s["name"])
            print("Department:", s["department"])
            print("Average:", round(sum(s["marks"]) / len(s["marks"]), 1))
            print("Attendance:", str(s["attendance"]) + "%")
            return

    print("Student not found!")


# Update student
def update_student():
    student_id = input("Enter Student ID to update: ").strip()

    for s in students:
        if s["id"] == student_id:
            print("Leave blank to keep existing values.")

            name = input("Enter new name: ").strip()
            if name:
                s["name"] = name

            department = input("Enter new department: ").strip()
            if department:
                s["department"] = department

            try:
                age = input("Enter new age: ").strip()
                if age:
                    if int(age) <= 0:
                        print("Invalid age.")
                        return
                    s["age"] = int(age)

                marks = input("Enter new marks separated by commas: ").strip()
                if marks:
                    new_marks = [float(x.strip()) for x in marks.split(",")]
                    if not new_marks or any(m < 0 or m > 100 for m in new_marks):
                        print("Invalid marks.")
                        return
                    s["marks"] = new_marks

                attendance = input("Enter new attendance: ").strip()
                if attendance:
                    new_attendance = float(attendance)
                    if not 0 <= new_attendance <= 100:
                        print("Invalid attendance.")
                        return
                    s["attendance"] = new_attendance

            except ValueError:
                print("Invalid input. Update cancelled.")
                return

            save_students()
            print("Student updated successfully!")
            return

    print("Student not found!")


# Delete student
def delete_student():
    student_id = input("Enter Student ID to delete: ").strip()

    for s in students:
        if s["id"] == student_id:
            students.remove(s)
            save_students()
            print("Student deleted successfully!")
            return

    print("Student not found!")


# Performance report
def performance_report():
    if not students:
        print("No records available.")
        return

    print("\n--- Performance Report ---")

    for s in students:
        average = sum(s["marks"]) / len(s["marks"])
        result = "PASS" if all(m >= 40 for m in s["marks"]) else "FAIL"

        print("\nStudent:", s["name"])
        print("Average:", round(average, 1))
        print("Result:", result)
        print("Attendance:", str(s["attendance"]) + "%")

    top = max(students, key=lambda s: sum(s["marks"]) / len(s["marks"]))

    print("\nTop Performer:", top["name"])
    print("Average:", round(sum(top["marks"]) / len(top["marks"]), 1))


# Main menu
while True:
    print("\n===== STUDENT RECORD MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Performance Report")
    print("7. Exit")

    choice = input("\nChoose an option: ").strip()

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        performance_report()

    elif choice == "7":
        save_students()
        print("Records saved successfully!")
        print("Thank you!")
        break

    else:
        print("Invalid choice! Try again.")