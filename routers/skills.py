# routers/skills.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/skills",
    tags=["Skills"],
)


@router.post(
    "/",
    response_model=schemas.SkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new skill",
    description="Add a new skill to your tracker with a name, category, and proficiency rating (1-10).",
    response_description="The created skill with its assigned ID."
)
def create_skill(skill_data: schemas.SkillCreate, db: Session = Depends(get_db)):
    # Convert Pydantic schema to SQLAlchemy model
    new_skill = models.Skill(**skill_data.model_dump())

    # Add to session (stages the insert)
    db.add(new_skill)

    # Commit to database (actually saves it)
    db.commit()

    # Refresh to get the auto-generated ID
    db.refresh(new_skill)

    return new_skill


@router.get(
    "/",
    response_model=List[schemas.SkillResponse],
    summary="List all skills",
    description="Retrieve all skills. Optionally filter by category using the query parameter.",
    response_description="A list of skills matching the filter criteria."
)
def get_skills(category: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Skill)

    # Filter by category (case-insensitive)
    if category:
        query = query.filter(func.lower(models.Skill.category) == category.lower())

    return query.all()


@router.get(
    "/{skill_id}",
    response_model=schemas.SkillResponse,
    summary="Get a specific skill",
    description="Retrieve a single skill by its unique ID.",
    response_description="The skill data."
)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found"
        )

    return skill


@router.get(
    "/{skill_id}/details",
    response_model=schemas.SkillWithJournalsResponse,
    summary="Get a skill with all its journals",
    description="Retrieve a skill and all journals linked to it.",
    response_description="The skill data with nested journals."
)
def get_skill_details(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found"
        )

    # skill.journals is automatically populated by the relationship
    return skill


@router.put(
    "/{skill_id}",
    response_model=schemas.SkillResponse,
    summary="Update a skill",
    description="Update one or more fields of an existing skill. Only provided fields will be changed.",
    response_description="The updated skill data."
)
def update_skill(skill_id: int, update_data: schemas.SkillUpdate, db: Session = Depends(get_db)):
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found"
        )

    # Only update fields that were actually provided
    update_fields = update_data.model_dump(exclude_unset=True)

    for key, value in update_fields.items():
        setattr(skill, key, value)

    db.commit()
    db.refresh(skill)

    return skill


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a skill",
    description="Delete a skill by its ID. This will fail if any journals are linked to this skill.",
    response_description="No content returned on successful deletion."
)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found"
        )

    # RESTRICT: Check if any journals are linked to this skill
    journal_count = db.query(models.Journal).filter(
        models.Journal.skill_id == skill_id
    ).count()

    if journal_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete skill '{skill.name}' because {journal_count} journal(s) are linked to it. Delete or unlink the journals first."
        )

    db.delete(skill)
    db.commit()

    return None