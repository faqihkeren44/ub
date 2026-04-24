from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.config import SECRET_KEY
from jose import jwt
from .. import database, schemas, models, utils
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


router = APIRouter(tags=['Authentication'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
# Ganti schemas.UserLogin dengan OAuth2PasswordRequestForm
def login_user(
    response: Response, 
    user_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # OAuth2PasswordRequestForm menyimpan email di field .username
    user = db.query(models.User).filter(models.User.email == user_data.username).first()
    
    if user is None:
        raise HTTPException(status_code=401, detail="Email atau password salah")

    # Verifikasi password (pakai logika pwd_context kamu)
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email atau password salah")

    # 1. Buat Token JWT
    exp = datetime.utcnow() + timedelta(minutes=30)
    payload = {"sub": str(user.id), "exp": exp}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    # 2. Buat objek RedirectResponse terlebih dahulu
    response = RedirectResponse(url="/me", status_code=status.HTTP_303_SEE_OTHER)

    # 3. Tempelkan Cookie ke objek response tersebut
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {token}", 
        httponly=True,
        max_age=1800, # Token berlaku 30 menit
        samesite="lax" # Agar aman dan bisa terbaca browser
    )

    return response