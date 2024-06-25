from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas
from app.database import get_db
from app.service import auth

router = APIRouter()

@router.post("/teacher-ratings", response_model=schemas.Teacher)
async def rate_teacher(
    rating: schemas.TeacherRatingCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    existing_rating = db.query(models.TeacherRating).filter(
        models.TeacherRating.teacher_id == rating.teacher_id,
        models.TeacherRating.user_id == current_user.id
    ).first()

    if existing_rating:
        existing_rating.knowledge_rating = rating.knowledge_rating
        existing_rating.teaching_skill_rating = rating.teaching_skill_rating
        existing_rating.communication_rating = rating.communication_rating
        existing_rating.easiness_rating = rating.easiness_rating
        db.commit()
    else:
        new_rating = models.TeacherRating(
            teacher_id=rating.teacher_id,
            user_id=current_user.id,
            knowledge_rating=rating.knowledge_rating,
            teaching_skill_rating=rating.teaching_skill_rating,
            communication_rating=rating.communication_rating,
            easiness_rating=rating.easiness_rating
        )
        db.add(new_rating)
        db.commit()

    average_ratings = db.query(
        func.avg(models.TeacherRating.knowledge_rating).label("knowledge_rating"),
        func.avg(models.TeacherRating.teaching_skill_rating).label("teaching_skill_rating"),
        func.avg(models.TeacherRating.communication_rating).label("communication_rating"),
        func.avg(models.TeacherRating.easiness_rating).label("easiness_rating")
    ).filter(models.TeacherRating.teacher_id == rating.teacher_id).first()

    teacher = db.query(models.Teacher).filter(models.Teacher.id == rating.teacher_id).first()
    if teacher:
        teacher.knowledge_rating = average_ratings.knowledge_rating
        teacher.teaching_skill_rating = average_ratings.teaching_skill_rating
        teacher.communication_rating = average_ratings.communication_rating
        teacher.easiness_rating = average_ratings.easiness_rating
        db.commit()

    return teacher