from fastapi import APIRouter, Depends, status
from bson import ObjectId

from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.utils.dependencies import get_current_user
from app.services import note_service

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    payload: NoteCreate,
    current_user=Depends(get_current_user)
):
    note_id = note_service.create_note(payload, current_user)
    
    # Fetch the created note to get the actual created_at timestamp
    note = note_service.get_note_by_id(note_id, current_user)

    return {
        "id": str(note["_id"]),
        "title": note["title"],
        "content": note["content"],
        "owner_id": str(note["owner_id"]),
        "visibility": note.get("visibility", "private"),
        "created_at": note["created_at"]
    }

@router.get("", response_model=list[NoteResponse])
def get_notes(current_user=Depends(get_current_user)):
    notes = note_service.get_notes(current_user)

    return [
        {
            "id": str(note["_id"]),
            "title": note["title"],
            "content": note["content"],
            "owner_id": str(note["owner_id"]),
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
    note_service.update_note(ObjectId(note_id), payload, current_user)
    return {"message": "Note updated successfully"}



@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: str,
    current_user=Depends(get_current_user)
):
    note_service.delete_note(ObjectId(note_id), current_user)






