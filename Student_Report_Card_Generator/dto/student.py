class Student:
    """
    Represents a student with basic academic details.

    Args:
        name (str): The name of the student.
        roll_number (int): The unique roll number of the student.
        marks (list[int]): Marks obtained in 5 subjects.

    Returns:
        Student: The newly created student object.
    """

    def __init__(self, name: str, roll_number: int, marks: list[int]):
        self._name = name
        self._roll_number = roll_number
        self._marks = marks

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the student.

        Returns:
            str: A formatted string containing student name, roll number, and marks.
        """
        return f"Student(Name: {self._name}, Roll: {self._roll_number}, Marks: {self._marks})"

    def __repr__(self) -> str:
        """
        Returns a detailed and official representation of the student object.

        Returns:
            str: A string suitable for debugging and logging.
        """
        return (f"Student(name='{self._name}', roll_number={self._roll_number}, marks={self._marks})")

    # Getter methods if you want to restrict direct access (optional)
    def get_name(self) -> str:
        return self._name

    def get_roll_number(self) -> int:
        return self._roll_number

    def get_marks(self) -> list[int]:
        return self._marks
