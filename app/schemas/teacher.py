from pydantic import BaseModel
from typing import List

class TeacherBase(BaseModel):
    name: str
    photo: str
    alma_mater: str
    degree: str
    positions: str
    biography: str

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int
    knowledge_rating: float
    teaching_skill_rating: float
    communication_rating: float
    easiness_rating: float

    class Config:
        orm_mode = True

class TeacherRatingBase(BaseModel):
    knowledge_rating: float
    teaching_skill_rating: float
    communication_rating: float
    easiness_rating: float

class TeacherRatingCreate(TeacherRatingBase):
    teacher_id: int

class TeacherRating(TeacherRatingBase):
    id: int
    teacher_id: int
    user_id: int

    class Config:
        orm_mode = True

class TeacherRequestBase(BaseModel):
    name: str
    photo: str
    alma_mater: str
    degree: str
    positions: str
    biography: str

class TeacherRequestCreate(TeacherRequestBase):
    user_id: int

class TeacherRequest(TeacherRequestBase):
    id: int
    user_id: int
    is_approved: bool

    class Config:
        orm_mode = True