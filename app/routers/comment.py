from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.db.database import get_db
from typing import List
import datetime

from app.service import auth

router = APIRouter()

@router.post("/comments", response_model=schemas.Comment)
async def create_comment(
    comment: schemas.CommentCreate,
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_comment = models.Comment(
        teacher_id=teacher_id,
        user_id=current_user.id,
        content=comment.content,
        time=datetime.datetime.utcnow()
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/teachers/{teacher_id}/comments", response_model=List[schemas.CommentWithName])
async def get_comments(
    teacher_id: int,
    db: Session = Depends(get_db)
):
    comments = db.query(models.Comment).filter(models.Comment.teacher_id == teacher_id).order_by(models.Comment.time.desc()).all()
    comments_with_usernames = []
    for c in comments:
        user = db.query(models.User).filter(models.User.id == c.user_id).first()
        comment_with_username = {
            "id": c.id,
            "teacher_id": c.teacher_id,
            "user_id": c.user_id,
            "content": c.content,
            "time": c.time,
            "username": user.username
        }
        comments_with_usernames.append(comment_with_username)

    return comments_with_usernames