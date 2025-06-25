from service.student_service import StudentService
from util.exceptions import (
    InvalidInputError, ValidationError,
    StudentReportCardException, StudentNotFoundException,
    DuplicateRollNumberException
)

def get_integer_input(prompt: str) -> int:
    """
    Helper function to get integer input from the user.

    Args:
        prompt (str): The prompt message to display.

    Returns:
        int: A valid integer entered by the user.

    Raises:
        InvalidInputError: If the input is not an integer.
    """
    while True:
        try:
            value_str = input(prompt).strip()
            return int(value_str)
        except ValueError as e:
            raise InvalidInputError("Please enter a valid integer.", e)

def get_marks_input() -> list[int]:
    """
    Helper function to get marks for 5 subjects.

    Returns:
        list[int]: A list of 5 valid integers between 0 and 100.

    Raises:
        InvalidInputError: If input is not an integer.
        ValidationError: If input is out of valid range (0–100).
    """
    marks = []
    print("Enter marks for 5 subjects (0-100):")
    for i in range(5):
        while True:
            try:
                mark = get_integer_input(f"Subject {i+1}: ")
                if 0 <= mark <= 100:
                    marks.append(mark)
                    break
                else:
                    raise ValidationError("Mark must be between 0 and 100.")
            except (InvalidInputError, ValidationError) as e:
                print(f"Error: {e}")
                if isinstance(e, InvalidInputError) and e.original_exception:
                    print(f"Details: {e.original_exception}")
    return marks

def print_report_card(report_data: dict):
    """
    Prints the report card in a formatted style.

    Args:
        report_data (dict): The computed student data including marks, total, average, and grade.
    """
    print("\n--- Report Card ---")
    print(f"Name         : {report_data['name']}")
    print(f"Roll Number  : {report_data['roll_number']}")
    print(f"Marks        : {report_data['marks']}")
    print(f"Total Marks  : {report_data['total_marks']}")
    print(f"Average Marks: {report_data['average_marks']:.2f}")
    print(f"Grade        : {report_data['grade']}")
    print("-------------------")

def main():
    """
    Entry point of the Student Report Card application.
    Handles the main menu and user interaction.
    """
    service = StudentService()

    while True:
        print("\n--- Student Report Card Menu ---")
        print("1. Add new student")
        print("2. Generate report card for a student")
        print("3. Generate report cards for all students")
        print("4. Exit")

        choice = input("Enter choice (1-4): ").strip()

        if choice == '1':
            try:
                name = input("Enter student name: ").strip()
                roll_number = get_integer_input("Enter roll number: ")
                marks = get_marks_input()
                student = service.add_student(name, roll_number, marks)
                print(f"Student {student.get_name()} added successfully!")
            except (InvalidInputError, ValidationError, DuplicateRollNumberException) as e:
                print(f"Error: {e}")
                if isinstance(e, InvalidInputError) and e.original_exception:
                    print(f"Details: {e.original_exception}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '2':
            try:
                roll_number = get_integer_input("Enter roll number: ")
                report = service.generate_report_card_data(roll_number)
                print_report_card(report)
            except StudentNotFoundException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '3':
            students = service.get_all_students()
            if not students:
                print("No students found.")
            for student in students:
                report = service.generate_report_card_data(student.get_roll_number())
                print_report_card(report)

        elif choice == '4':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
