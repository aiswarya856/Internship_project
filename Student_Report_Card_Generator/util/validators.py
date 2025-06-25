"""
Contains input validation functions used across the system.
"""

from util.exceptions import ValidationError

def validate_name(name: str):
    """
    Validates the student's name.

    Args:
        name (str): The name to validate.

    Raises:
        ValidationError: If name is empty or not a string.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("Name cannot be empty or non-string.", field="name", value=name)

def validate_roll_number(roll_number: int):
    """
    Validates the student's roll number.

    Args:
        roll_number (int): The roll number to validate.

    Raises:
        ValidationError: If roll number is not a positive integer.
    """
    if not isinstance(roll_number, int) or roll_number <= 0:
        raise ValidationError("Roll number must be a positive integer.", field="roll_number", value=roll_number)

def validate_marks(marks_list: list[int]):
    """
    Validates the student's marks list.

    Args:
        marks_list (list[int]): A list of 5 marks.

    Raises:
        ValidationError: If not a list of 5 integers between 0 and 100.
    """
    if not isinstance(marks_list, list) or len(marks_list) != 5:
        raise ValidationError("Marks must be a list of 5 integers.", field="marks", value=marks_list)
    for mark in marks_list:
        if not isinstance(mark, int) or not (0 <= mark <= 100):
            raise ValidationError("Each mark must be an integer between 0 and 100.", field="mark", value=mark)
