import sys
import json
from enum import Enum
def main():
    data = []
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        pass
    cmd = sys.argv[1]
    if cmd == "add":
        add()
    elif cmd == "list":
        list()
    elif cmd == "delete":
        delete()
    elif cmd == "update":
        update()
    elif cmd == "mark-done":
        mark_done()
    elif cmd == "mark-doing":
        mark_doing()
    else:
        print("Command not found")

def mark_done():
    try:
        with open('data.json', 'r+') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Task not found")
        return
    if len(sys.argv) < 3:
        print("please provide a task id")
        return
    task_id = sys.argv[2]
    if task_id == "--help":
        print("Usage: mark-done <task_id>")
        return

    task = [task for task in data if task['id'] == int(task_id)]
    task = task[0] if len(task) > 0 else None
    if task == None:
        print("Task not found")
        return
    data.remove(task)
    input_data = {
        "id": task['id'],
        "name": task['name'],
        "status": TaskStatus.DONE.value,
    }
    with open('data.json', 'w') as f:
        json.dump(data + [input_data], f, ensure_ascii=False, indent=4)

    print("%s marked as done" % task['name'])

def mark_doing():
    try:
        with open('data.json', 'r+') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Task not found")
        return
    if len(sys.argv) < 3:
        print("please provide a task id")
        return
    task_id = sys.argv[2]
    if task_id == "--help":
        print("Usage: mark-doing <task_id>")
        return

    task = [task for task in data if task['id'] == int(task_id)]
    task = task[0] if len(task) > 0 else None
    if task == None:
        print("Task not found")
        return
    data.remove(task)
    input_data = {
        "id": task['id'],
        "name": task['name'],
        "status": TaskStatus.DOING.value,
    }
    with open('data.json', 'w') as f:
        json.dump(data + [input_data], f, ensure_ascii=False, indent=4)

    print("%s marked as doing" % task['name'])

def add():
    if len(sys.argv) < 3:
        print("please provide a task")
        return
    task = sys.argv[2]
    if task == "--help":
        print("Usage: add <task>")
        return
    try:
        with open('data.json', 'r+') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    id = 1
    if len(data) > 0:
        id = max([task['id'] for task in data]) + 1
    input_data = {
        "id": id,
        "name": task,
        "status": 0,
    }
    with open('data.json', 'w') as f:
        json.dump(data + [input_data], f, ensure_ascii=False, indent=4)

    print("%s added" % task)

def list():
    status = None
    if len(sys.argv) == 3:
        if sys.argv[2] == "--help":
            print("Usage: list <status>")
            return
        status = sys.argv[2]
        if status not in [stat.name for stat in TaskStatus]:
            print("Status not found")
            return
        status = TaskStatus[status]
    data = []
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        pass

    if status != None:
        data = [task for task in data if task['status'] == status.value]
    if len(data) == 0:
        print("No tasks found")
        return

    for task in data:
        print("%s: %s %s" % (task['id'], task['name'], TaskStatus(task['status']).name))

def update():
    try:
        with open('data.json', 'r+') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Task not found")
        return
    if len(sys.argv) < 4:
        print("please provide a task id and a new task")
        return
    task_id = sys.argv[2]
    task_name = sys.argv[3]
    if task_name == "--help":
        print("Usage: update <task_id> <task>")
        return

    task = [task for task in data if task['id'] == int(task_id)]
    task = task[0] if len(task) > 0 else None
    if task == None:
        print("Task not found")
        return
    data.remove(task)
    input_data = {
        "id": task['id'],
        "name": task_name,
        "status": task['status'],
    }
    with open('data.json', 'w') as f:
        json.dump(data + [input_data], f, ensure_ascii=False, indent=4)

    print("Task id:%s updated to: %s" % (task['id'], task_name))


def delete():
    try:
        with open('data.json', 'r+') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Task not found")
        return
    if len(sys.argv) < 3:
        print("please provide a task id")
        return
    task_id = sys.argv[2]
    if task_id == "--help":
        print("Usage: delete <task_id>")
        return

    task = [task for task in data if task['id'] == int(task_id)]
    task = task[0] if len(task) > 0 else None
    if task == None:
        print("Task not found")
        return
    data.remove(task)
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("%s deleted" % task['name'])

class TaskStatus(Enum):
    TODO = 0
    DOING = 1
    DONE = 2

if __name__ == "__main__":
    main()
