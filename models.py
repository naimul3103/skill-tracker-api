# models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    category = Column(String(30), nullable=False)
    rating = Column(Integer, nullable=False)

    # Relationship: A skill can have many journals
    journals = relationship("Journal", back_populates="skill")


class Journal(Base):
    __tablename__ = "journals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(String, nullable=False)

    # Foreign Key: Links to skills table (nullable because journals can be unlinked)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)

    # Relationship: A journal belongs to one skill
    skill = relationship("Skill", back_populates="journals")