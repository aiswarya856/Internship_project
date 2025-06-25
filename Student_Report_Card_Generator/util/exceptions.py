"""
Defines all custom exceptions for the Student Report Card System.
"""

class StudentReportCardException(Exception):
    """Base exception for the Student Report Card System."""
    pass


class InvalidInputError(StudentReportCardException):
    def __init__(self, message="Invalid input provided.", original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception


class ValidationError(StudentReportCardException):
    def __init__(self, message="Validation failed.", field=None, value=None):
        super().__init__(message)
        self.field = field
        self.value = value


class StudentNotFoundException(StudentReportCardException):
    def __init__(self, message="Student not found.", roll_number=None):
        super().__init__(message)
        self.roll_number = roll_number


class DuplicateRollNumberException(StudentReportCardException):
    def __init__(self, message="Student with this roll number already exists.", roll_number=None):
        super().__init__(message)
        self.roll_number = roll_number
