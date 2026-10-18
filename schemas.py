# schemas.py
from pydantic import BaseModel, Field
from typing import Optional


# ==================== SKILL SCHEMAS ====================

class SkillBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="The name of the skill or technology",
        examples=["FastAPI", "Python", "Docker"]
    )
    category: str = Field(
        ...,
        min_length=2,
        max_length=30,
        description="The category this skill belongs to",
        examples=["Backend", "Frontend", "DevOps", "Data Science"]
    )
    rating: int = Field(
        ...,
        ge=1,
        le=10,
        description="Your proficiency level from 1 (beginner) to 10 (expert)",
        examples=[5, 8, 10]
    )


class SkillCreate(SkillBase):
    """Schema for creating a new skill"""
    pass


class SkillUpdate(BaseModel):
    """Schema for updating an existing skill. All fields are optional."""
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50,
        description="New name for the skill",
        examples=["FastAPI Advanced"]
    )
    category: Optional[str] = Field(
        None,
        min_length=2,
        max_length=30,
        description="New category for the skill",
        examples=["Backend"]
    )
    rating: Optional[int] = Field(
        None,
        ge=1,
        le=10,
        description="New proficiency rating",
        examples=[9]
    )


class SkillResponse(SkillBase):
    """Schema for returning skill data to the client"""
    id: int = Field(
        ...,
        description="Unique identifier for the skill",
        examples=[1]
    )


# ==================== JOURNAL SCHEMAS ====================

class JournalBase(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="A short title for this journal entry",
        examples=["Learned Pydantic validation", "Practiced error handling"]
    )
    content: str = Field(
        ...,
        min_length=10,
        description="Detailed notes about what you learned",
        examples=["Today I learned how Pydantic automatically validates request bodies."]
    )
    skill_id: Optional[int] = Field(
        None,
        description="ID of the skill this journal is about. Null if not linked to any skill.",
        examples=[1]
    )


class JournalCreate(JournalBase):
    """Schema for creating a new journal entry"""
    pass


class JournalUpdate(BaseModel):
    """Schema for updating an existing journal entry. All fields are optional."""
    title: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        description="New title for the journal entry",
        examples=["Mastered Pydantic validation"]
    )
    content: Optional[str] = Field(
        None,
        min_length=10,
        description="Updated notes",
        examples=["I now fully understand how Pydantic validation works."]
    )
    skill_id: Optional[int] = Field(
        None,
        description="New skill ID to link to. Use null to unlink.",
        examples=[2]
    )


class JournalResponse(JournalBase):
    """Schema for returning journal data to the client"""
    id: int = Field(
        ...,
        description="Unique identifier for the journal entry",
        examples=[1]
    )