# routers/journals.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas import JournalCreate, JournalUpdate, JournalResponse
import db

router = APIRouter(
    prefix="/journals",
    tags=["Journals"]

)


def validate_skill_exists(skill_id: int):
    """Helper function to check if a skill exists."""
    if skill_id not in db.SKILLS_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Skill with ID {skill_id} does not exist. Cannot link journal to a non-existent skill."
        )


@router.post(
    "/",
    response_model=JournalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new journal entry",
    description="Add a new learning journal entry. Optionally link it to a skill by providing skill_id.",
    response_description="The created journal entry with its assigned ID."
)
def create_journal(journal_data: JournalCreate):
    if journal_data.skill_id is not None:
        validate_skill_exists(journal_data.skill_id)
    
    new_journal = journal_data.model_dump()
    new_journal["id"] = db.next_journal_id
    db.JOURNALS_DB[db.next_journal_id] = new_journal
    db.next_journal_id += 1
    return new_journal


@router.get(
    "/",
    response_model=List[JournalResponse],
    summary="List all journal entries",
    description="Retrieve all journal entries. Optionally filter by skill_id to see journals about a specific skill.",
    response_description="A list of journal entries matching the filter criteria."
)
def get_journals(skill_id: int = None):
    if skill_id is None:
        return list(db.JOURNALS_DB.values())
    
    filtered_journals = [
        journal for journal in db.JOURNALS_DB.values()
        if journal["skill_id"] == skill_id
    ]
    return filtered_journals


@router.get(
    "/{journal_id}",
    response_model=JournalResponse,
    summary="Get a specific journal entry",
    description="Retrieve a single journal entry by its unique ID.",
    response_description="The journal entry data."
)
def get_journal(journal_id: int):
    journal = db.JOURNALS_DB.get(journal_id)
    
    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Journal with ID {journal_id} not found"
        )
    
    return journal


@router.put(
    "/{journal_id}",
    response_model=JournalResponse,
    summary="Update a journal entry",
    description="Update one or more fields of an existing journal entry. Only provided fields will be changed.",
    response_description="The updated journal entry data."
)
def update_journal(journal_id: int, update_data: JournalUpdate):
    journal = db.JOURNALS_DB.get(journal_id)
    
    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Journal with ID {journal_id} not found"
        )
    
    if update_data.skill_id is not None:
        validate_skill_exists(update_data.skill_id)
    
    updated_fields = update_data.model_dump(exclude_unset=True)
    
    for key, value in updated_fields.items():
        journal[key] = value
    
    return journal


@router.delete(
    "/{journal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a journal entry",
    description="Delete a journal entry by its ID. This does not affect any linked skills.",
    response_description="No content returned on successful deletion."
)
def delete_journal(journal_id: int):
    journal = db.JOURNALS_DB.get(journal_id)
    
    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Journal with ID {journal_id} not found"
        )
    
    del db.JOURNALS_DB[journal_id]
    return None