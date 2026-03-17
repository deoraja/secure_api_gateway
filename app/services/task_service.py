tasks = []

def create_task_service(task,owner):
    task_data = task.model_dump()
    task_data["id"] = len(tasks) + 1
    task_data["owner"] = owner
    tasks.append(task_data)
    return task_data

def get_all_tasks():
    print("tasks:", tasks)
    return tasks

def get_task_by_id(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def delete_task_service(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True
    return False