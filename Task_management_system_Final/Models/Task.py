class Task:
    def __init__(self, task_id: int, title: str, description: str, priority: str, due_date: str, status: str = "To-Do", assigned_to=None):
        if priority not in ['Low', 'Medium', 'High']:
            raise ValueError("Priority must be 'Low', 'Medium', or 'High'.")
        if status not in ['To-Do', 'In Progress', 'Done']:
            raise ValueError("Invalid status. Choose from 'To-Do', 'In Progress', or 'Done'.")

        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.status = status
        self.assigned_to = assigned_to

    def update_status(self, new_status):
        if new_status not in ['To-Do', 'In Progress', 'Done']:
            raise ValueError("Invalid status.")
        self.status = new_status

    def update_priority(self, new_priority):
        if new_priority not in ['Low', 'Medium', 'High']:
            raise ValueError("Invalid priority.")
        self.priority = new_priority

    def assign_to(self, user_id):
        self.assigned_to = user_id

    def __str__(self):
        return f"{self.task_id}, {self.title}, {self.description}, {self.priority}, {self.due_date}, {self.status}, {self.assigned_to or 'Unassigned'}"
