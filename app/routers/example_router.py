from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..init_db import clear_users_table

router = APIRouter()

@router.get("/users/")
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.post("/clear-users", status_code=204)
async def clear_users(db: Session = Depends(get_db)):
    clear_users_table(db)
    return "ok";