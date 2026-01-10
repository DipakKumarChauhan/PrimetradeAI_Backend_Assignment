from fastapi import APIRouter, Depends, status, HTTPException
from bson import ObjectId
from bson.errors import InvalidId

from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.utils.dependencies import get_current_user
from app.services import note_service
from app.core import database

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    payload: NoteCreate,
    current_user=Depends(get_current_user)
):
    note_id = note_service.create_note(payload, current_user)
    
    # Fetch the created note to get the actual created_at timestamp
    note = note_service.get_note_by_id(note_id, current_user)

    # Fetch owner email
    owner = database.get_user_collection().find_one({"_id": note["owner_id"]})
    owner_email = owner["email"] if owner else None

    return {
        "id": str(note["_id"]),
        "title": note["title"],
        "content": note["content"],
        "owner_id": str(note["owner_id"]),
        "owner_email": owner_email,
        "visibility": note.get("visibility", "private"),
        "created_at": note["created_at"]
    }

@router.get("", response_model=list[NoteResponse])
def get_notes(current_user=Depends(get_current_user)):
    notes = note_service.get_notes(current_user)
    users_col = database.get_user_collection()

    # Get all unique owner IDs (they are ObjectId objects from MongoDB)
    # Filter out any invalid owner_ids and ensure we only have ObjectIds
    owner_ids_set = set()
    for note in notes:
        owner_id = note.get("owner_id")
        if owner_id:
            # owner_id from MongoDB should be an ObjectId
            if isinstance(owner_id, ObjectId):
                owner_ids_set.add(owner_id)
    
    owner_ids = list(owner_ids_set)
    
    # Fetch all owner emails in one query for efficiency (only if we have owner_ids)
    owners = {}
    if owner_ids:
        for owner in users_col.find({"_id": {"$in": owner_ids}}):
            owners[str(owner["_id"])] = owner.get("email")

    return [
        {
            "id": str(note["_id"]),
            "title": note["title"],
            "content": note["content"],
            "owner_id": str(note.get("owner_id", "")),
            "owner_email": owners.get(str(note.get("owner_id", ""))) if isinstance(note.get("owner_id"), ObjectId) else None,
            "visibility": note.get("visibility", "private"),
            "created_at": note["created_at"]
        }
        for note in notes
    ]

# @router.put("/{note_id}")
# def update_note(
#     note_id: str,
#     payload: NoteUpdate,
#     current_user=Depends(get_current_user)
# ):
#     note_service.update_note(ObjectId(note_id), payload, current_user)
#     return {"message": "Note updated successfully"}

@router.patch("/{note_id}")
def update_note(
    note_id: str,
    payload: NoteUpdate,
    current_user=Depends(get_current_user)
):
    try:
        object_id = ObjectId(note_id)
    except (InvalidId, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid note ID format: {note_id}"
        )
    note_service.update_note(object_id, payload, current_user)
    return {"message": "Note updated successfully"}



@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: str,
    current_user=Depends(get_current_user)
):
    try:
        object_id = ObjectId(note_id)
    except (InvalidId, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid note ID format: {note_id}"
        )
    note_service.delete_note(object_id, current_user)






