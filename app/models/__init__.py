from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import User
from .teacher import Teacher, TeacherRating,TeacherRequest
from .comment import Comment