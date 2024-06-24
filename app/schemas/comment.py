from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    teacher_id: int
    user_id: int
    time: datetime

    class Config:
        orm_mode = True


class CommentWithName(Comment):
    username: str
