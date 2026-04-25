from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.config import SECRET_KEY
from jose import jwt
from .. import models, database

router = APIRouter(
    prefix="/dashboard",
    tags=["Member Area"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/me", response_class=HTMLResponse)
def get_me(request: Request, access_token: str = Cookie(None), db: Session = Depends(database.get_db)):
    print(f"Token yang diterima: {access_token}")
    if not access_token:
        return RedirectResponse(url="/login")
    
    try:
        token = access_token.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return RedirectResponse(url="users/login")

    user_id = payload.get("sub")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        return RedirectResponse(url="users/login")

    return templates.TemplateResponse("profile.html", {
        "request": request, 
        "user": user
    })

# Cara menghandle jika token expired