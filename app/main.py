from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app import models, schemas, utils

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

#ENDPOINT PENDAFTARAN
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