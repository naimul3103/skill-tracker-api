# routers/skills.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas import SkillCreate, SkillUpdate, SkillResponse
import db

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
     
)


@router.post(
    "/",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new skill",
    description="Add a new skill to your tracker with a name, category, and proficiency rating (1-10).",
    response_description="The created skill with its assigned ID."
)
def create_skill(skill_data: SkillCreate):
    new_skill = skill_data.model_dump()
    new_skill["id"] = db.next_skill_id
    db.SKILLS_DB[db.next_skill_id] = new_skill
    db.next_skill_id += 1
    return new_skill


@router.get(
    "/",
    response_model=List[SkillResponse],
    summary="List all skills",
    description="Retrieve all skills. Optionally filter by category using the query parameter.",
    response_description="A list of skills matching the filter criteria."
)
def get_skills(category: str = None):
    if category is None:
        return list(db.SKILLS_DB.values())
    
    filtered_skills = [
        skill for skill in db.SKILLS_DB.values()
        if skill["category"].lower() == category.lower()
    ]
    return filtered_skills


@router.get(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Get a specific skill",
    description="Retrieve a single skill by its unique ID.",
    response_description="The skill data."
)
def get_skill(skill_id: int):
    skill = db.SKILLS_DB.get(skill_id)
    
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found"
        )
    
    return skill


@router.put(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Update a skill",
    description="Update one or more fields of an existing skill. Only provided fields will be changed.",
    response_description="The updated skill data."
)
def update_skill(skill_id: int, update_data: SkillUpdate):
    skill = db.SKILLS_DB.get(skill_id)
    
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found"
        )
    
    updated_fields = update_data.model_dump(exclude_unset=True)
    
    for key, value in updated_fields.items():
        skill[key] = value
    
    return skill


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a skill",
    description="Delete a skill by its ID. This will fail if any journals are linked to this skill.",
    response_description="No content returned on successful deletion."
)
def delete_skill(skill_id: int):
    skill = db.SKILLS_DB.get(skill_id)
    
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found"
        )
    
    # RESTRICT: Check if any journals are linked to this skill
    linked_journals = [
        journal for journal in db.JOURNALS_DB.values()
        if journal["skill_id"] == skill_id
    ]
    
    if linked_journals:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete skill '{skill['name']}' because {len(linked_journals)} journal(s) are linked to it. Delete or unlink the journals first."
        )
    
    del db.SKILLS_DB[skill_id]
    return None