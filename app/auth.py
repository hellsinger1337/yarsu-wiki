from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .database import get_db
from .models.user import User
from .schemas.user import TokenData
import requests
from .config import settings
import random
import string
import smtplib
import hashlib
import os
from email.mime.text import MIMEText

# Конфигурация для JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30000000

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def generate_verification_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def send_verification_email(email: str, token: str):
    smtp_server = settings.yandex_smtp_server
    smtp_port = settings.yandex_smtp_port
    smtp_username = settings.yandex_email
    smtp_password = settings.yandex_password
    print(settings.yandex_smtp_server)
    print(settings.yandex_smtp_port)
    print(settings.yandex_email)

    verification_url = f"https://hellsinger1337-yarsu-wiki-0893.twc1.net/auth/verify-email?email={email}&token={token}"
    html_content = f"""
    <html>
    <body>
        <p>Thank you for registering!<br>
        Please click the link below to verify your email address:<br>
        <a href="{verification_url}">Verify Email</a>
        </p>
    </body>
    </html>
    """

    msg = MIMEText(html_content, "html")
    msg['Subject'] = 'Verify your email'
    msg['From'] = smtp_username
    msg['To'] = email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, [email], msg.as_string())

def verify_user_email(db: Session, email: str, token: str):
    user = get_user_by_email(db, email)
    if user and user.verification_token == token:
        user.is_email_verified = True
        user.verification_token = None
        db.commit()
        db.refresh(user)
        return True
    return False

def generate_reset_password_token() -> str:
    return hashlib.sha256(os.urandom(60)).hexdigest()

def send_reset_password_email(email: str, token: str):
    smtp_server = settings.yandex_smtp_server
    smtp_port = settings.yandex_smtp_port
    smtp_username = settings.yandex_email
    smtp_password = settings.yandex_password

    reset_url = f"https://hellsinger1337-yarsu-wiki-0893.twc1.net/auth/reset-password?token={token}"
    html_content = f"""
    <html>
    <body>
        <p>You requested a password reset.<br>
        Please click the link below to reset your password:<br>
        <a href="{reset_url}">Reset Password</a>
        </p>
    </body>
    </html>
    """

    msg = MIMEText(html_content, "html")
    msg['Subject'] = 'Reset your password'
    msg['From'] = smtp_username
    msg['To'] = email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, [email], msg.as_string())