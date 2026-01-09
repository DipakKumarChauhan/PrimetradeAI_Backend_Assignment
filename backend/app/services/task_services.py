from bson import ObjectId
from fastapi import HTTPException, status
from app.core import database
from app.models.task import TaskModel
from datetime import datetime

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
    tasks_col = database.db["tasks"]

    # 1️⃣ Existence check
    task = tasks_col.find_one({"_id": task_id})
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # 2️⃣ Authorization
    is_owner = task["owner_id"] == user["_id"]
    is_admin = user["role"] == "admin"

    if not (is_owner or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this task"
        )

    # 3️⃣ Prepare update payload
    # update_data = {
    #     **{k: v for k, v in data.dict().items() if v is not None},
    #     "updated_at": datetime.utcnow(),
    #     "updated_by": user["_id"]
    # }
    update_data = data.dict(exclude_unset=True)

    if not update_data:
        return  # nothing to update

    update_data["updated_at"] = datetime.utcnow()
    update_data["updated_by"] = user["_id"]

    # 4️⃣ Apply update
    tasks_col.update_one(
        {"_id": task_id},
        {"$set": update_data}
    )

def delete_task(task_id: ObjectId, user):
    tasks_col = database.db["tasks"]

    # 1️⃣ Existence check
    task = tasks_col.find_one({"_id": task_id})
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # 2️⃣ Authorization
    if task["owner_id"] != user["_id"] and user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this task"
        )

    # 3️⃣ Delete
    tasks_col.delete_one({"_id": task_id})