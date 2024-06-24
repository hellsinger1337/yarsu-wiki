from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from . import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    avatar = Column(String, nullable=True)
    is_email_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True) 
    reset_password_token = Column(String, nullable=True) 