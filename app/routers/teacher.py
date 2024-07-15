from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.db.database import get_db

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

@router.post("/teacher_requests", response_model=schemas.TeacherRequest, status_code=status.HTTP_201_CREATED)
async def create_teacher_request(request: schemas.TeacherRequestCreate, db: Session = Depends(get_db)):
    db_request = models.TeacherRequest(
        name=request.name,
        photo=request.photo,
        alma_mater=request.alma_mater,
        degree=request.degree,
        positions=request.positions,
        biography=request.biography,
        user_id=request.user_id
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.post("/approve_teacher_request/{request_id}", response_model=schemas.Teacher)
async def approve_teacher_request(request_id: int, db: Session = Depends(get_db)):
    db_request = db.query(models.TeacherRequest).filter(models.TeacherRequest.id == request_id).first()
    
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")

    if db_request.is_approved:
        raise HTTPException(status_code=400, detail="Request already approved")

    db_teacher = models.Teacher(
        name=db_request.name,
        photo=db_request.photo,
        alma_mater=db_request.alma_mater,
        degree=db_request.degree,
        positions=db_request.positions,
        biography=db_request.biography
    )
    db.add(db_teacher)
    db_request.is_approved = True
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.get("/teacher_requests", response_model=List[schemas.TeacherRequest])
async def get_teacher_requests(db: Session = Depends(get_db)):
    requests = db.query(models.TeacherRequest).all()
    return requests