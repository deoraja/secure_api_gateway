from fastapi import APIRouter,Depends
from app.core.dependencies import get_current_user
from app.models.task_model import Task
from app.services.task_service import create_task, get_all_tasks, get_task_by_id, delete_task
from fastapi import HTTPException

router = APIRouter()

tasks = []

@router.post("/tasks")
def create_task(task: Task, user=Depends(get_current_user)):

    task_data = task.model_dump()
    task_data["id"] = len(tasks)+1
    task_data["owner"] = user

    tasks.append(task_data)

    return task_data

@router.get("/tasks")
def get_tasks(user=Depends(get_current_user)):
    return tasks

@router.get("/tasks/{task_id}")
def get_task(task_id: int,user = Depends(get_current_user)):

    task = get_task_by_id(task_id)

    if not task:
       raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, user=Depends(get_current_user)):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "task deleted"}

    raise HTTPException(status_code=404, detail="Task not found")