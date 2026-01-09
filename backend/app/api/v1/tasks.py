from fastapi import APIRouter, Depends, status, HTTPException
from bson import ObjectId

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.utils.dependencies import get_current_user
from app.services import task_services
from app.core import database

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    current_user=Depends(get_current_user)
):
    count = task_services.create_task(payload, current_user)

    return {
        "message": f"{count} task(s) created successfully"
    }

@router.get("", response_model=list[TaskResponse])
def get_tasks(
    status: str | None = None,
    current_user=Depends(get_current_user)
):
    tasks = task_services.get_tasks(current_user, status)

    return [
        {
            "id": str(task["_id"]),
            "title": task["title"],
            "description": task.get("description"),
            "status": task["status"],
            "owner_id": str(task["owner_id"]),
            "created_at": task["created_at"],
            "updated_at": task.get("updated_at"),
        "updated_by": (
            str(task["updated_by"]) if task.get("updated_by") else None),
        }
        for task in tasks
    ]


# @router.put("/{task_id}")
# def update_task(
#     task_id: str,
#     payload: TaskUpdate,
#     current_user=Depends(get_current_user)
# ):
#     task_services.update_task(
#         ObjectId(task_id),
#         payload,
#         current_user
#     )
#     return {"message": "Task updated successfully"}

@router.patch("/{task_id}")
def update_task(
    task_id: str,
    payload: TaskUpdate,
    current_user=Depends(get_current_user)
):
    task_services.update_task(
        ObjectId(task_id),
        payload,
        current_user
    )
    return {"message": "Task updated successfully"}




@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    current_user=Depends(get_current_user)
):
    task_services.delete_task(ObjectId(task_id), current_user)



