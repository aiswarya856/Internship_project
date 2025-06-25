from typing import List
from .Task import Task

class User:
    def __init__(self, user_id: int, name: str, email: str):
        if not isinstance(user_id, int):
            raise ValueError("User ID should be an integer.")
        if not name.strip():
            raise ValueError("Name is mandatory.")
        if not email.strip():
            raise ValueError("Email is required.")

        self.user_id = user_id
        self.name = name
        self.email = email
        self.task_list: List[Task] = []

    def add_task(self, task):
        self.task_list.append(task)

    def remove_task(self, task_id):
        for task in self.task_list:
            if task.task_id == task_id:
                self.task_list.remove(task)
                return
        print(f"No task with ID {task_id}.")

    def __str__(self):
        return f"{self.user_id}, {self.name}, {self.email}"
