from Service.TaskManager import TaskManager

def main():
    manager = TaskManager()

    def fetch_valid_task_id():
        while True:
            tid = input("Enter Task ID: ")
            if not tid.strip():
                print("Task ID cannot be empty.")
            elif not tid.isdigit():
                print("Task ID must be numeric.")
            else:
                return int(tid)

    while True:
        print("\n--- Task Manager ---")
        print("1. Add User")
        print("2. Add Task")
        print("3. Assign Task")
        print("4. View All Tasks")
        print("5. View Tasks by User")
        print("6. View Tasks by Status")
        print("7. Remove Task")
        print("8. Exit")

        try:
            choice = int(input("Your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            try:
                uid = int(input("User ID: "))
            except ValueError:
                print("User ID must be numeric.")
                continue
            name = input("Name: ")
            email = input("Email: ")
            manager.create_user(uid, name, email)

        elif choice == 2:
            tid = fetch_valid_task_id()
            title = input("Title: ")
            desc = input("Description: ")
            priority = input("Priority (Low/Medium/High): ")
            due = input("Due Date (YYYY-MM-DD): ")
            status = input("Status (To-Do/In Progress/Done): ")
            manager.create_task(tid, title, desc, priority, due, status, None)

        elif choice == 3:
            tid = fetch_valid_task_id()
            try:
                uid = int(input("User ID: "))
            except ValueError:
                print("User ID must be numeric.")
                continue
            manager.assign_task_to_user(tid, uid)

        elif choice == 4:
            manager.list_all_tasks()

        elif choice == 5:
            try:
                uid = int(input("User ID: "))
            except ValueError:
                print("User ID must be numeric.")
                continue
            manager.list_tasks_by_user(uid)

        elif choice == 6:
            status = input("Enter status to filter by: ")
            manager.list_tasks_by_status(status)

        elif choice == 7:
            tid = fetch_valid_task_id()
            manager.delete_task(tid)

        elif choice == 8:
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
