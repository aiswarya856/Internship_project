"""
Handles core business logic for student management.
"""

from dto.student import Student
from util.exceptions import (
    StudentNotFoundException,
    DuplicateRollNumberException,
    ValidationError,
    InvalidInputError
)
from util.validators import validate_name, validate_roll_number, validate_marks


class StudentService:
    """
    Service class to manage student operations such as adding students,
    retrieving data, and computing report cards.
    """

    def __init__(self):
        self._students = {}

    def add_student(self, name: str, roll_number: int, marks: list[int]) -> Student:
        """
        Adds a new student after validating the input.

        Args:
            name (str): The name of the student.
            roll_number (int): The unique roll number of the student.
            marks (list[int]): Marks in 5 subjects.

        Returns:
            Student: The newly created student object.

        Raises:
            ValidationError: If any of the input validations fail.
            DuplicateRollNumberException: If a student with the roll number already exists.
        """
        try:
            try:
                validate_name(name)
            except ValidationError as e:
                raise ValidationError("Name validation failed.") from e

            try:
                validate_roll_number(roll_number)
            except ValidationError as e:
                raise ValidationError("Roll number validation failed.") from e

            try:
                validate_marks(marks)
            except ValidationError as e:
                raise ValidationError("Marks validation failed.") from e

            if roll_number in self._students:
                raise DuplicateRollNumberException(
                    message="Student with this roll number already exists.",
                    roll_number=roll_number
                )

            student = Student(name, roll_number, marks)
            self._students[roll_number] = student
            return student

        except (ValidationError, DuplicateRollNumberException) as e:
            raise e
        except Exception as e:
            raise InvalidInputError("Unexpected error while adding student.", e)

    def get_student(self, roll_number: int) -> Student:
        """
        Fetches a student by their roll number.

        Args:
            roll_number (int): The roll number of the student.

        Returns:
            Student: The student object.

        Raises:
            StudentNotFoundException: If student not found with given roll number.
        """
        try:
            return self._students[roll_number]
        except KeyError as e:
            raise StudentNotFoundException(
                message="Student with this roll number not found.",
                roll_number=roll_number
            ) from e

    def get_all_students(self) -> list[Student]:
        """
        Returns the list of all students in the system.

        Returns:
            list[Student]: List of student objects.
        """
        return list(self._students.values())

    def calculate_total(self, student: Student) -> int:
        """
        Calculates the total marks of a student.

        Args:
            student (Student): The student object.

        Returns:
            int: Total marks.
        """
        return sum(student.get_marks())

    def calculate_average(self, student: Student) -> float:
        """
        Calculates the average marks of a student.

        Args:
            student (Student): The student object.

        Returns:
            float: Average marks.
        """
        return self.calculate_total(student) / len(student.get_marks())

    def get_grade(self, student: Student) -> str:
        """
        Determines grade based on average marks.

        Args:
            student (Student): The student object.

        Returns:
            str: Grade character.
        """
        avg = self.calculate_average(student)
        if avg >= 90:
            return 'A'
        elif avg >= 75:
            return 'B'
        elif avg >= 60:
            return 'C'
        elif avg >= 50:
            return 'D'
        else:
            return 'F'

    def generate_report_card_data(self, roll_number: int) -> dict:
        """
        Generates the report card dictionary for a student.

        Args:
            roll_number (int): The roll number of the student.

        Returns:
            dict: Report card data including name, marks, total, average, grade.
        """
        student = self.get_student(roll_number)
        total = self.calculate_total(student)
        avg = self.calculate_average(student)
        grade = self.get_grade(student)

        return {
            "name": student.get_name(),
            "roll_number": student.get_roll_number(),
            "marks": student.get_marks(),
            "total_marks": total,
            "average_marks": avg,
            "grade": grade
        }
