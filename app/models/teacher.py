from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from . import Base

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    photo = Column(String)
    alma_mater = Column(String)
    degree = Column(String)
    positions = Column(String)  
    biography = Column(String)
    knowledge_rating = Column(Float, default=0)
    teaching_skill_rating = Column(Float, default=0)
    communication_rating = Column(Float, default=0)
    easiness_rating = Column(Float, default=0)

class TeacherRating(Base):
    __tablename__ = "teacher_ratings"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    user_id = Column(Integer)
    knowledge_rating = Column(Float)
    teaching_skill_rating = Column(Float)
    communication_rating = Column(Float)
    easiness_rating = Column(Float)

class TeacherRequest(Base):
    __tablename__ = "teacher_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    photo = Column(String)
    alma_mater = Column(String)
    degree = Column(String)
    positions = Column(String)
    biography = Column(String)
    user_id = Column(Integer)
    is_approved = Column(Boolean, default=False)