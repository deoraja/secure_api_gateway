tasks = []

def create_task(task):
    task_data = task.dict()
    task_data["id"] = len(tasks) + 1
    tasks.append(task_data)
    return task_data

def get_all_tasks():
    return tasks

def get_task_by_id(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True
    return False