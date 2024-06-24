from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter()

@router.get("/teachers", response_model=List[schemas.Teacher])
async def get_teachers(db: Session = Depends(get_db)):
    teachers = db.query(models.Teacher).all()
    for teacher in teachers:
        teacher.positions_list = teacher.positions.split(',')
    return teachers

@router.get("/teachers/{id}", response_model=schemas.Teacher)
async def get_teacher(id: int, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@router.post("/teachers", response_model=schemas.Teacher, status_code=status.HTTP_201_CREATED)
async def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = models.Teacher(
        name=teacher.name,
        photo=teacher.photo,
        alma_mater=teacher.alma_mater,
        degree=teacher.degree,
        positions=teacher.positions,
        biography=teacher.biography
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher
