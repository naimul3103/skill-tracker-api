# routers/journals.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/journals",
    tags=["Journals"],
)


def validate_skill_exists(skill_id: int, db: Session):
    """
    Helper function to check if a skill exists.
    Raises 400 error if the skill doesn't exist.
    """
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Skill with ID {skill_id} does not exist. Cannot link journal to a non-existent skill."
        )


@router.post(
    "/",
    response_model=schemas.JournalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new journal entry",
    description="Add a new learning journal entry. Optionally link it to a skill by providing skill_id.",
    response_description="The created journal entry with its assigned ID."
)
def create_journal(journal_data: schemas.JournalCreate, db: Session = Depends(get_db)):
    # VALIDATION: If skill_id is provided, check that the skill exists
    if journal_data.skill_id is not None:
        validate_skill_exists(journal_data.skill_id, db)

    # Convert Pydantic schema to SQLAlchemy model
    new_journal = models.Journal(**journal_data.model_dump())

    # Add, commit, refresh
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)

    return new_journal


@router.get(
    "/",
    response_model=List[schemas.JournalResponse],
    summary="List all journal entries",
    description="Retrieve all journal entries. Optionally filter by skill_id to see journals about a specific skill.",
    response_description="A list of journal entries matching the filter criteria."
)
def get_journals(skill_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Journal)

    if skill_id is not None:
        query = query.filter(models.Journal.skill_id == skill_id)

    return query.all()


@router.get(
    "/{journal_id}",
    response_model=schemas.JournalResponse,
    summary="Get a specific journal entry",
    description="Retrieve a single journal entry by its unique ID.",
    response_description="The journal entry data."
)
def get_journal(journal_id: int, db: Session = Depends(get_db)):
    journal = db.query(models.Journal).filter(models.Journal.id == journal_id).first()

    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Journal with ID {journal_id} not found"
        )

    return journal


@router.put(
    "/{journal_id}",
    response_model=schemas.JournalResponse,
    summary="Update a journal entry",
    description="Update one or more fields of an existing journal entry. Only provided fields will be changed.",
    response_description="The updated journal entry data."
)
def update_journal(journal_id: int, update_data: schemas.JournalUpdate, db: Session = Depends(get_db)):
    journal = db.query(models.Journal).filter(models.Journal.id == journal_id).first()

    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Journal with ID {journal_id} not found"
        )

    # VALIDATION: If skill_id is being updated, check that the new skill exists
    if update_data.skill_id is not None:
        validate_skill_exists(update_data.skill_id, db)

    # Only update fields that were actually provided
    update_fields = update_data.model_dump(exclude_unset=True)

    for key, value in update_fields.items():
        setattr(journal, key, value)

    db.commit()
    db.refresh(journal)

    return journal


@router.delete(
    "/{journal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a journal entry",
    description="Delete a journal entry by its ID. This does not affect any linked skills.",
    response_description="No content returned on successful deletion."
)
def delete_journal(journal_id: int, db: Session = Depends(get_db)):
    journal = db.query(models.Journal).filter(models.Journal.id == journal_id).first()

    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Journal with ID {journal_id} not found"
        )

    db.delete(journal)
    db.commit()

    return None