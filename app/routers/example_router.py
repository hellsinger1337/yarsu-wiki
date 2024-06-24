from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..init_db import clear_users_table
from .. import models
from ..service.commits import get_commits, FRONTEND_REPO, BACKEND_REPO, Commit
from datetime import datetime
router = APIRouter()

@router.get("/users/")
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.post("/clear-users", status_code=204)
async def clear_users(db: Session = Depends(get_db)):
    clear_users_table(db)
    return "ok";

@router.delete("/clear", response_model=dict)
async def clear_database(db: Session = Depends(get_db)):
    db.query(models.Teacher).delete()
    db.query(models.TeacherRating).delete()
    db.query(models.Comment).delete()
    db.commit()
    return {"message": "All records cleared"}

@router.get("/commits/frontend", response_model=list[Commit])
def get_frontend_commits():
    since = datetime(2024, 6, 24, 10, 00)
    return get_commits(FRONTEND_REPO, since)

@router.get("/commits/backend", response_model=list[Commit])
def get_backend_commits():
    since = datetime(2024, 6, 24, 10, 00)
    return get_commits(BACKEND_REPO, since)