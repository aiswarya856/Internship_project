from flask import Flask, request, jsonify
from Service.TaskManager import TaskManager



app = Flask(__name__)
manager = TaskManager()

@app.route('/')
def home():
    return "🚀 Task Management API is up and running!"

# ----------------------- USER ENDPOINTS ------------------------

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        user_id = data.get('user_id')
        name = data.get('name')
        email = data.get('email')

        manager.create_user(user_id, name, email)
        return jsonify({'message': f'✅ User {user_id} created successfully.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ----------------------- TASK ENDPOINTS ------------------------

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.json
        task_id = data.get('task_id')
        title = data.get('title')
        description = data.get('description')
        priority = data.get('priority')
        due_date = data.get('due_date')
        status = data.get('status')
        assigned_to = data.get('assigned_to', None)

        manager.create_task(task_id, title, description, priority, due_date, status, assigned_to)
        return jsonify({'message': f'✅ Task {task_id} created.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>/assign/<int:user_id>', methods=['PUT'])
def assign_task(task_id, user_id):
    try:
        manager.assign_task_to_user(task_id, user_id)
        return jsonify({'message': f'🔗 Task {task_id} assigned to User {user_id}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        conn = manager.conn or manager._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT t.task_id, t.title, t.status, t.priority, t.due_date, u.name
            FROM Task t LEFT JOIN User u ON t.assigned_to = u.user_id
        """)

        tasks = cursor.fetchall()
        result = []
        for t in tasks:
            result.append({
                'task_id': t[0],
                'title': t[1],
                'status': t[2],
                'priority': t[3],
                'due_date': str(t[4]),
                'assigned_to': t[5] or "Unassigned"
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_tasks_for_user(user_id):
    try:
        conn = manager.conn or manager._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT task_id, title, status, priority, due_date
            FROM Task
            WHERE assigned_to = %s
        """, (user_id,))

        records = cursor.fetchall()
        task_list = []
        for r in records:
            task_list.append({
                'task_id': r[0],
                'title': r[1],
                'status': r[2],
                'priority': r[3],
                'due_date': str(r[4])
            })

        return jsonify(task_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    try:
        manager.delete_task(task_id)
        return jsonify({'message': f'🗑️ Task {task_id} deleted.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/shutdown', methods=['POST'])
def shutdown_app():
    try:
        manager.close()
        return jsonify({'message': '🔒 Database connection closed.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
