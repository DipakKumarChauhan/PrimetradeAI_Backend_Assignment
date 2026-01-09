from bson import ObjectId
from fastapi import HTTPException, status
from app.core import database
from app.models.task import TaskModel


def create_task(data, current_user):
    tasks_col = database.db["tasks"]
    users_col = database.db["users"]

    tasks_to_create = []

    # USER: can assign only to self
    if current_user["role"] == "user":
        task = TaskModel(
            title=data.title,
            description=data.description,
            status=data.status,
            owner_id=current_user["_id"]
        )
        tasks_to_create.append(task)

    # ADMIN logic
    else:
        # Assign to specific user
        if data.assignee_id:
            user = users_col.find_one({"_id": ObjectId(data.assignee_id)})
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="Assignee not found"
                )

            tasks_to_create.append(
                TaskModel(
                    title=data.title,
                    description=data.description,
                    status=data.status,
                    owner_id=user["_id"]
                )
            )

        # Assign to all users
        else:
            all_users = users_col.find({"role": "user"})
            for user in all_users:
                tasks_to_create.append(
                    TaskModel(
                        title=data.title,
                        description=data.description,
                        status=data.status,
                        owner_id=user["_id"]
                    )
                )

    # Bulk insert
    if tasks_to_create:
        tasks_col.insert_many([t.to_dict() for t in tasks_to_create])

    return len(tasks_to_create)

def get_tasks(user, status: str | None = None):
    query = {}

    if user["role"] != "admin":
        query["owner_id"] = user["_id"]

    if status:
        query["status"] = status

    return list(database.db["tasks"].find(query))


def get_task_by_id(task_id: ObjectId):
    task = database.db["tasks"].find_one({"_id": task_id})
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


def update_task(task_id: ObjectId, data, user):
    task = get_task_by_id(task_id)

    if user["role"] != "admin" and task["owner_id"] != user["_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this task"
        )

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    database.db["tasks"].update_one(
        {"_id": task_id},
        {"$set": update_data}
    )


def delete_task(task_id: ObjectId, user):
    task = get_task_by_id(task_id)

    if user["role"] != "admin" and task["owner_id"] != user["_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this task"
        )

    database.db["tasks"].delete_one({"_id": task_id})
