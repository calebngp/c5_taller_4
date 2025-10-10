# ============================================================
# DevMatch AI - Database Models
# ============================================================

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, Table, Column, ForeignKey
from typing import List
import json

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Association table for many-to-many relationship between projects and required technologies
project_technologies = Table(
    'project_technologies',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('technology_id', Integer, ForeignKey('technologies.id'), primary_key=True)
)

# Association table for many-to-many relationship between developers and skills
developer_skills = Table(
    'developer_skills', 
    Base.metadata,
    Column('developer_id', Integer, ForeignKey('developers.id'), primary_key=True),
    Column('technology_id', Integer, ForeignKey('technologies.id'), primary_key=True)
)

class Technology(db.Model):
    __tablename__ = 'technologies'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=True)  # backend, frontend, mobile, etc.
    
    # Relationships
    projects: Mapped[List["Project"]] = relationship(
        secondary=project_technologies, back_populates="required_technologies"
    )
    developers: Mapped[List["Developer"]] = relationship(
        secondary=developer_skills, back_populates="skills"
    )
    
    def __repr__(self):
        return f'<Technology {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category
        }

class Project(db.Model):
    __tablename__ = 'projects'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    experience_level: Mapped[str] = mapped_column(String(50), nullable=False)  # Beginner, Intermediate, Advanced
    project_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Web, Mobile, Desktop
    status: Mapped[str] = mapped_column(String(50), default='Open', nullable=False)  # Open, Closed, In Progress
    
    # Relationships
    required_technologies: Mapped[List["Technology"]] = relationship(
        secondary=project_technologies, back_populates="projects"
    )
    
    def __repr__(self):
        return f'<Project {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'experience_level': self.experience_level,
            'project_type': self.project_type,
            'status': self.status,
            'required_technologies': [tech.name for tech in self.required_technologies]
        }

class Experience(db.Model):
    __tablename__ = 'experiences'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    developer_id: Mapped[int] = mapped_column(Integer, ForeignKey('developers.id'), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=True)  # work, education, project, etc.
    
    # Relationships
    developer: Mapped["Developer"] = relationship(back_populates="experiences")
    
    def __repr__(self):
        return f'<Experience {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'category': self.category
        }

class Developer(db.Model):
    __tablename__ = 'developers'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    experience_level: Mapped[str] = mapped_column(String(50), nullable=False)  # Beginner, Intermediate, Advanced
    motivation: Mapped[str] = mapped_column(Text, nullable=True)
    email: Mapped[str] = mapped_column(String(200), nullable=True, unique=True)
    linkedin: Mapped[str] = mapped_column(String(500), nullable=True)
    github: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Relationships
    skills: Mapped[List["Technology"]] = relationship(
        secondary=developer_skills, back_populates="developers"
    )
    experiences: Mapped[List["Experience"]] = relationship(
        back_populates="developer", cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f'<Developer {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'experience_level': self.experience_level,
            'motivation': self.motivation,
            'email': self.email,
            'linkedin': self.linkedin,
            'github': self.github,
            'skills': [skill.name for skill in self.skills],
            'experiences': [exp.description for exp in self.experiences]
        }

class MatchResult(db.Model):
    __tablename__ = 'match_results'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.id'), nullable=False)
    developer_id: Mapped[int] = mapped_column(Integer, ForeignKey('developers.id'), nullable=False)
    technical_match: Mapped[float] = mapped_column(nullable=False)
    ai_technical_affinity: Mapped[int] = mapped_column(Integer, nullable=True)
    ai_motivational_affinity: Mapped[int] = mapped_column(Integer, nullable=True)
    ai_experience_relevance: Mapped[int] = mapped_column(Integer, nullable=True)
    ai_comment: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Relationships
    project: Mapped["Project"] = relationship()
    developer: Mapped["Developer"] = relationship()
    
    def __repr__(self):
        return f'<MatchResult P{self.project_id}-D{self.developer_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'developer_id': self.developer_id,
            'technical_match': self.technical_match,
            'ai_technical_affinity': self.ai_technical_affinity,
            'ai_motivational_affinity': self.ai_motivational_affinity,
            'ai_experience_relevance': self.ai_experience_relevance,
            'ai_comment': self.ai_comment,
            'created_at': self.created_at
        }