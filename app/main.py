from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.config import SECRET_KEY
from app import models, schemas, utils
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from .routers import products

app = FastAPI ()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(products.router)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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

def check_admin_role(db: Session = Depends(get_db)):
     if current_user == True:
          pass
     else:
          raise HTTPException(status_code=304, detail="Access is forbidden")