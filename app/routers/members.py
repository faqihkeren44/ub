from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.config import SECRET_KEY
from jose import jwt, ExpiredSignatureError
from .. import models, database

router = APIRouter(
    prefix="/dashboard",
    tags=["Member Area"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/me", response_class=HTMLResponse)
def get_me(
    request: Request, 
    access_token: str = Cookie(None), 
    db: Session = Depends(database.get_db)
):
    if not access_token:
        return RedirectResponse(url="/auth/login?msg=not_login")
    
    try:
        token = access_token.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        member_id = payload.get("sub")

    except ExpiredSignatureError:
        response = RedirectResponse(url="/auth/login?msg=expired", status_code=303)
        response.delete_cookie("access_token")
        return response

    except Exception:
        return RedirectResponse(url="/auth/login?msg=invalid", status_code=303)

    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if member is None:
        return RedirectResponse(url="/auth/login")

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={ 
        "member": member
        }
    )