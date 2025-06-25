from typing import List
from Models.Task import Task
from Models.User import User
from Config.db import get_connection

class TaskManager:
    """Central controller for managing tasks and users with MySQL integration"""

    def __init__(self):
        self.task_store: List[Task] = []
        self.user_store: List[User] = []
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def _get_connection(self):
        return get_connection()

    def create_task(self, task_id, title, description, priority, due_date, status, assigned_to):
        """Insert a new task into the Task table"""
        try:
            db = self._get_connection()
            cur = db.cursor()
            query = """
                INSERT INTO Task (task_id, title, description, priority, due_date, status, assigned_to)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (task_id, title, description, priority, due_date, status, assigned_to))
            db.commit()
            print(f"✅ Task {task_id} added successfully.")
        except Exception as err:
            print(f"❌ Failed to create task: {err}")
        finally:
            db.close()

    def delete_task(self, task_id):
        """Remove a task from the database by ID"""
        try:
            db = self._get_connection()
            cur = db.cursor()
            cur.execute("DELETE FROM Task WHERE task_id = %s", (task_id,))
            db.commit()
            if cur.rowcount == 0:
                print(f"⚠️ Task ID {task_id} not found.")
            else:
                print(f"🗑️ Task {task_id} deleted.")
        except Exception as err:
            print(f"❌ Error deleting task: {err}")
        finally:
            db.close()

    def get_task(self, task_id):
        """Display task details by ID"""
        try:
            db = self._get_connection()
            cur = db.cursor()
            cur.execute("SELECT * FROM Task WHERE task_id = %s", (task_id,))
            task = cur.fetchone()
            if task:
                print("📋 Task Details:", task)
            else:
                print(f"❌ Task {task_id} not found.")
        except Exception as err:
            print(f"Error fetching task: {err}")
        finally:
            db.close()

    def list_all_tasks(self):
        """Show all tasks in the system"""
        try:
            db = self._get_connection()
            cur = db.cursor()
            cur.execute("SELECT * FROM Task")
            tasks = cur.fetchall()

            if not tasks:
                print("📭 No tasks available.")
                return

            for t in tasks:
                task_id, title, description, priority, due_date, status, assigned_to = t
                print(f"""
Task ID     : {task_id}
Title       : {title}
Description : {description}
Priority    : {priority}
Due Date    : {due_date}
Status      : {status}
Assigned To : {assigned_to if assigned_to else 'Not Assigned'}
                """)
        except Exception as err:
            print(f"Error listing tasks: {err}")
        finally:
            db.close()

    def list_tasks_by_user(self, user_id):
        """List tasks that belong to a specific user"""
        try:
            db = self._get_connection()
            cur = db.cursor()

            cur.execute("SELECT * FROM User WHERE user_id = %s", (user_id,))
            user = cur.fetchone()
            if not user:
                print(f"❌ No user with ID {user_id}")
                return

            cur.execute("SELECT * FROM Task WHERE assigned_to = %s", (user_id,))
            tasks = cur.fetchall()

            if tasks:
                print(f"📌 Tasks for User {user_id}:")
                for t in tasks:
                    task_id, title, desc, priority, due, status, assigned_to = t
                    print(f"""
Task ID   : {task_id}
Title     : {title}
Status    : {status}
Priority  : {priority}
Due Date  : {due}
                    """)
            else:
                print(f"ℹ️ No tasks assigned to User {user_id}")

        except Exception as err:
            print(f"Error retrieving tasks: {err}")
        finally:
            db.close()

    def list_tasks_by_status(self, status):
        """List tasks filtered by status"""
        try:
            valid_status = ['To-Do', 'In Progress', 'Done']
            if status not in valid_status:
                print("Invalid status. Choose from: To-Do, In Progress, Done")
                return

            db = self._get_connection()
            cur = db.cursor()
            cur.execute("SELECT * FROM Task WHERE status = %s", (status,))
            tasks = cur.fetchall()

            if tasks:
                print(f"📄 Tasks with status '{status}':")
                for t in tasks:
                    task_id, title, desc, priority, due, _, assigned_to = t
                    print(f"""
Task ID   : {task_id}
Title     : {title}
Priority  : {priority}
Due Date  : {due}
Assigned  : {assigned_to if assigned_to else 'None'}
                    """)
            else:
                print(f"⚠️ No tasks with status '{status}' found.")

        except Exception as err:
            print(f"Error filtering tasks: {err}")
        finally:
            db.close()

    def create_user(self, user_id, name, email):
        """Create a new user"""
        try:
            db = self._get_connection()
            cur = db.cursor()
            cur.execute(
                "INSERT INTO User (user_id, name, email) VALUES (%s, %s, %s)",
                (user_id, name, email)
            )
            db.commit()
            print(f"👤 User {user_id} added.")
        except Exception as err:
            print(f"Error creating user: {err}")
        finally:
            db.close()

    def assign_task_to_user(self, task_id, user_id):
        """Assign an existing task to a user"""
        try:
            db = self._get_connection()
            cur = db.cursor()

            cur.execute("SELECT * FROM Task WHERE task_id = %s", (task_id,))
            task = cur.fetchone()
            if not task:
                print(f"❌ Task {task_id} not found.")
                return

            cur.execute("SELECT * FROM User WHERE user_id = %s", (user_id,))
            user = cur.fetchone()
            if not user:
                print(f"❌ User {user_id} not found.")
                return

            cur.execute("UPDATE Task SET assigned_to = %s WHERE task_id = %s", (user_id, task_id))
            db.commit()
            print(f"🔗 Task {task_id} assigned to User {user_id}.")
        except Exception as err:
            print(f"Error assigning task: {err}")
        finally:
            db.close()
