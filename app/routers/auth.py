from fastapi import APIRouter, Depends, HTTPException, status, Request, Form, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.service.auth import get_current_user
from app.service import auth
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema, Token, UserVerification, PasswordResetRequest, PasswordReset, UserProfileUpdate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/register", response_model=UserSchema)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    verification_token = auth.generate_verification_token()
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        avatar=user.avatar,
        is_email_verified=False,
        verification_token=verification_token
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    auth.send_verification_email(user.email, verification_token)
    return db_user

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: UserSchema = Depends(auth.get_current_user)):
    return current_user

@router.get("/verify-email")
async def verify_email(email: str, token: str, db: Session = Depends(get_db)):
    if auth.verify_user_email(db, email, token):
        return {"msg": "Email successfully verified"}
    raise HTTPException(status_code=400, detail="Invalid token or email")

@router.post("/password-reset-request")
async def password_reset_request(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Email not registered")
    reset_token = auth.generate_reset_password_token()
    user.reset_password_token = reset_token
    db.commit()
    auth.send_reset_password_email(user.email, reset_token)
    return {"msg": "Password reset email sent"}

@router.post("/reset-password")
async def reset_password(token: str = Form(...), new_password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_password_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    user.hashed_password = auth.get_password_hash(new_password)
    user.reset_password_token = None
    db.commit()
    return {"msg": "Password reset successful"}

@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_form(request: Request, token: str):
    return templates.TemplateResponse("reset_password.html", {"request": request, "token": token})

@router.put("/profile", response_model=UserSchema)
async def update_profile(
    new_username: str = Body(..., alias="new_username"),
    new_photo: str = Body(..., alias="new_photo"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if new_username:
        current_user.username = new_username
        db.commit()
    if new_photo:
        current_user.avatar = new_photo
        db.commit()
    db.commit()
    db.refresh(current_user)
    return current_user