from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("task_manager.db")
    conn.row_factory = sqlite3.Row
    return conn

with get_db_connection() as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS task_manager(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT,
                    deadline DATE,
                    status TEXT)''')
    conn.commit()

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM task_manager').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    data = request.json
    task = data['task']
    deadline = data['deadline']
    status = data['status']

    conn = get_db_connection()
    conn.execute("INSERT INTO task_manager (task, deadline, status) VALUES (?, ?, ?)", (task, deadline, status))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task added successfully'})

@app.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM task_manager WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted'})

@app.route('/complete/<int:task_id>', methods=['PATCH'])
def complete_task(task_id):
    conn = get_db_connection()
    conn.execute("UPDATE task_manager SET status = 'Completed' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task marked complete'})

if __name__ == '__main__':
    app.run(debug=True)
