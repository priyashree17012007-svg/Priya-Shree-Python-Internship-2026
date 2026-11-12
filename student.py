import json
import os


# Parent Class
class Person:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self.__name = value


# Child Class (Inheritance)
class Student(Person):
    def __init__(self, student_id, name, department,
                 average, attendance, status):
        super().__init__(name)

        self.__student_id = student_id
        self.__department = department
        self.__average = average
        self.__attendance = attendance
        self.__status = status

    @property
    def student_id(self):
        return self.__student_id

    @property
    def department(self):
        return self.__department

    @department.setter
    def department(self, value):
        self.__department = value

    @property
    def average(self):
        return self.__average

    @average.setter
    def average(self, value):
        if not 0 <= value <= 100:
            raise ValueError("Average must be between 0 and 100")
        self.__average = value

    @property
    def attendance(self):
        return self.__attendance

    @attendance.setter
    def attendance(self, value):
        if not 0 <= value <= 100:
            raise ValueError("Attendance must be between 0 and 100")
        self.__attendance = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    def get_performance(self):
        if self.average >= 75:
            return "Good"
        elif self.average >= 50:
            return "Average"
        return "Needs Improvement"

    # Polymorphism
    def display_info(self):
        print(f"\n{self.student_id} | {self.name} | {self.department}")
        print(f"Average: {self.average}%")
        print(f"Attendance: {self.attendance}%")
        print(f"Status: {self.status}")


# Student Manager Class
class StudentManager:
    def __init__(self):
        self.students = {}

    def add_student(self):
        try:
            sid = input("Enter Student ID: ")

            if sid in self.students:
                print("Student ID already exists!")
                return

            name = input("Enter Student Name: ")
            department = input("Enter Department: ")
            average = float(input("Enter Average: "))
            attendance = float(input("Enter Attendance: "))
            status = input("Enter Status: ")

            student = Student(
                sid, name, department,
                average, attendance, status
            )

            self.students[sid] = student
            print("Student added successfully!")

        except ValueError as e:
            print("Invalid input:", e)

    def view_students(self):
        if not self.students:
            print("No student records found!")
            return

        for student in self.students.values():
            student.display_info()

    def search_student(self):
        sid = input("Enter Student ID: ")

        student = self.students.get(sid)

        if student:
            student.display_info()
        else:
            print("Student not found!")

    def update_student(self):
        sid = input("Enter Student ID: ")

        student = self.students.get(sid)

        if not student:
            print("Student not found!")
            return

        try:
            student.name = input("Enter New Name: ")
            student.department = input("Enter New Department: ")
            student.average = float(input("Enter New Average: "))
            student.attendance = float(input("Enter New Attendance: "))
            student.status = input("Enter New Status: ")

            print("Student updated successfully!")

        except ValueError as e:
            print("Invalid input:", e)

    def delete_student(self):
        sid = input("Enter Student ID: ")

        if sid in self.students:
            del self.students[sid]
            print("Student deleted successfully!")
        else:
            print("Student not found!")


# Report Generator Class
class ReportGenerator:
    @staticmethod
    def generate(manager):
        if not manager.students:
            print("No records available!")
            return

        print("\n===== STUDENT REPORT =====")

        for student in manager.students.values():
            student.display_info()
            print("Performance:", student.get_performance())


# File Manager Class
class FileManager:
    FILE_NAME = "students.json"

    @staticmethod
    def save(manager):
        data = {}

        for sid, student in manager.students.items():
            data[sid] = {
                "name": student.name,
                "department": student.department,
                "average": student.average,
                "attendance": student.attendance,
                "status": student.status
            }

        try:
            with open(FileManager.FILE_NAME, "w") as file:
                json.dump(data, file, indent=4)

            print("Data saved successfully!")

        except OSError:
            print("Error saving data!")

    @staticmethod
    def load(manager):
        if not os.path.exists(FileManager.FILE_NAME):
            print("No saved data found!")
            return

        try:
            with open(FileManager.FILE_NAME, "r") as file:
                data = json.load(file)

            loaded_students = {}

            for sid, details in data.items():
                loaded_students[sid] = Student(
                    sid,
                    details["name"],
                    details["department"],
                    float(details["average"]),
                    float(details["attendance"]),
                    details["status"]
                )

            manager.students = loaded_students
            print("Data loaded successfully!")

        except (OSError, ValueError, KeyError, TypeError):
            print("Error loading data!")


# Main Program
def main():
    manager = StudentManager()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Generate Report")
        print("7. Save Data")
        print("8. Load Data")
        print("9. Exit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                manager.add_student()

            elif choice == 2:
                manager.view_students()

            elif choice == 3:
                manager.search_student()

            elif choice == 4:
                manager.update_student()

            elif choice == 5:
                manager.delete_student()

            elif choice == 6:
                ReportGenerator.generate(manager)

            elif choice == 7:
                FileManager.save(manager)

            elif choice == 8:
                FileManager.load(manager)

            elif choice == 9:
                print("Thank you! Exiting program.")
                break

            else:
                print("Invalid choice! Try again.")

        except ValueError:
            print("Please enter a valid number!")


if __name__ == "__main__":
    main()