from task_manager import Task

while True:
    print("WELLCOME")
    print("1. Add task\n2. view task\n3. manage task")
    ch = input("choose : ")

    if ch == '1':
        t = Task()
        t.add_task()
    elif ch == '2':
        t = Task()
        t.view_task()
    elif ch == '3':
        t = Task()
        t.manage_task()
    else:
        print("Invalid choose")

    print("Thanks for using Task_manager")