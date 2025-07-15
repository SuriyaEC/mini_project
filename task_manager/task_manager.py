import sqlite3

conn = sqlite3.connect("task_manager.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS task_manager(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               task TEXT,
               deadline DATE,
               status TEXT)''')
conn.commit()
class Task:
    def __init__(self):
        self.task = ''
        self.deadline = ''
        self.status = ''

    def add_task(self):
        self.task = input("Task : ")
        self.deadline = input("DeadLine : ")
        self.status = input("Status : ")
        
        cursor.execute('''INSERT INTO task_manager(task,deadline,status)
                       VALUES (?,?,?)''',(self.task,self.deadline,self.status))
        conn.commit()
        print("Task added successfully")

    def view_task(self):
        cursor.execute('''SELECT * FROM task_manager ''')
        rows = cursor.fetchall()
        if rows:
            print("Existing Task : \n")
            for row in rows:
                print(f'{row[0]} | {row[1]} | {row[2]} | {row[3]}')
        else:
            print("No existing task, please add task")
    
    def manage_task(self):
        task_id = input("Enter the task id which need to be updated : ")
        print("1. TASK\n2. DEADLINE\n3. STATUS")
        ch = input("What Would You Like To Update (1,2,3) : ")
       
        if ch == '1':
            new_task = input("Change_Task_to : ")
            cursor.execute('''UPDATE task_manager SET task = ? WHERE id = ? ''',(new_task,task_id))
        elif ch == '2':
            new_deadline = input("Change_deadline_to : ")
            cursor.execute('''UPDATE task_manager SET deadline = ? WHERE id = ? ''',(new_deadline,task_id))
        elif ch == '3':
            new_status = input("Change_status_to : ")
            cursor.execute('''UPDATE task_manager SET status = ? WHERE id = ? ''',(new_status,task_id))
        else:
            print("Invalid option")