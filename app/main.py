from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.config import SECRET_KEY
from app import models, schemas, utils
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

app = FastAPI ()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}

@app.post("/register", response_model=schemas.UserOut)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Cek apakah email sudah terdaftar
    user_exist = db.query(models.User).filter(models.User.email == user_data.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    # Hashing password
    hashed_password = utils.hash_password(user_data.password)

    #Objek User baru untuk disimpan
    new_user = models.User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )

    # Simpan ke database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login")
def login_user(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Email atau password salah")

    plain_password = user_data.password
    hashed_password = user.hashed_password
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(plain_password, hashed_password):
        raise HTTPException(status_code=401, detail="Email atau password salah")

    exp = datetime.utcnow()+ timedelta(minutes=30)
    payload = {"sub": str(user.id), "exp": exp}
    
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/me")
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = payload["sub"]

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return {
        "id": user.id,
        "email": user.email
    }