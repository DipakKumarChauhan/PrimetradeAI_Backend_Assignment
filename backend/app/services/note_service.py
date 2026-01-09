from bson import ObjectId
from fastapi import HTTPException, status
from app.core import database
from app.models.note import NoteModel
from datetime import datetime


def _resolve_shared_users(emails: list[str]) -> list[ObjectId]:

    users = database.db["users"].find({"email": {"$in": emails}})
    user_ids = [u["_id"] for u in users]

    if len(user_ids) != len(emails):
        raise HTTPException(
            status_code=400,
            detail="One or more shared users do not exist"
        )

    return user_ids


def create_note(data, user):
    shared_ids = []

    if data.visibility == "shared":
        if not data.shared_with_emails:
            raise HTTPException(
                status_code=400,
                detail="Shared notes require shared_with_emails"
            )
        shared_ids = _resolve_shared_users(data.shared_with_emails)

    note = NoteModel(
        title=data.title,
        content=data.content,
        owner_id=user["_id"],
        visibility=data.visibility,
        shared_with=shared_ids
    )

    result = database.db["notes"].insert_one(note.to_dict())
    return result.inserted_id


def get_notes(user):

    query = {
        "$or": [
            {"owner_id": user["_id"]},
            {"visibility": "public"},
            {
                "visibility": "shared",
                "shared_with": user["_id"]
            }
        ]
    }

    return list(database.db["notes"].find(query))


def get_note_by_id(note_id: ObjectId, user):

    note = database.db["notes"].find_one({
        "_id": note_id,
        "$or": [
            {"owner_id": user["_id"]},
            {"visibility": "public"},
            {
                "visibility": "shared",
                "shared_with": user["_id"]
            }
        ]
    })

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found or access denied"
        )

    return note



def update_note(note_id: ObjectId, data, user):

    # note = database.db["notes"].find_one({
    #     "_id": note_id,
    #     "owner_id": user["_id"]
    # })

    
    # if not note:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="Only owner can update note"
    #     )
    # Issue above is that it doesnot check if note_id is valid so if owner is right one but note_id s wrong 
    # Then also it will say owner is not right  

    notes_col = database.db["notes"]

    # 1️⃣ Check existence first
    note = notes_col.find_one({"_id": note_id})

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    # 2️⃣ Check ownership
    if note["owner_id"] != user["_id"]:
        raise HTTPException(
            status_code=403,
            detail="Only owner can update note"
        )


    # Issue Below is that if we update just one field and leave other untoched then defalut values where updated into thatone field
    # update_data = {}

    # if data.title is not None:
    #     update_data["title"] = data.title
    # if data.content is not None:
    #     update_data["content"] = data.content
    # if data.visibility is not None:
    #     update_data["visibility"] = data.visibility

    # if data.visibility == "shared":
    #     if not data.shared_with_emails:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="Shared notes require shared_with_emails"
    #         )
    #     update_data["shared_with"] = _resolve_shared_users(
    #         data.shared_with_emails
    #     )

    update_data = data.dict(exclude_unset=True) # This Line Means Only update when explicitly provided 
    
    if not update_data:
        return  # nothing to update
    
    if "visibility" in update_data and update_data["visibility"] == "shared":
        if not data.shared_with_emails:
            raise HTTPException(
                status_code=400,
                detail="Shared notes require shared_with_emails"
            )
        update_data["shared_with"] = _resolve_shared_users(
            data.shared_with_emails
        )
        update_data.pop("shared_with_emails", None)

    update_data["updated_at"] = datetime.utcnow()
    update_data["updated_by"] = user["_id"]


    notes_col.update_one(
        {"_id": note_id},
        {"$set": update_data}
    )



def delete_note(note_id: ObjectId, user):
    notes_col = database.db["notes"]

    # 1️⃣ Check existence
    note = notes_col.find_one({"_id": note_id})
    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    # 2️⃣ Check ownership
    if note["owner_id"] != user["_id"]:
        raise HTTPException(
            status_code=403,
            detail="Only owner can delete note"
        )

    # 3️⃣ Delete
    notes_col.delete_one({"_id": note_id})
