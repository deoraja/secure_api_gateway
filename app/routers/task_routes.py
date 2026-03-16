from fastapi import APIRouter,Depends
from app.core.dependencies import get_current_user
from app.models.task_model import Task
from app.services.task_service import create_task, get_all_tasks, get_task_by_id, delete_task
from fastapi import HTTPException

router = APIRouter()


@router.post("/tasks")
def create_task(task: Task, user=Depends(get_current_user)):
    return create_task(task,user)

@router.get("/tasks")
def get_tasks(user=Depends(get_current_user)):
    return get_all_tasks

@router.get("/tasks/{task_id}")
def get_task(task_id: int,user = Depends(get_current_user)):

    task = get_task_by_id(task_id)

    if not task:
       raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, user=Depends(get_current_user)):
    
    deleted = delete_task(task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task deleted"}

