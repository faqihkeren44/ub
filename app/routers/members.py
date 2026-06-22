from fastapi import APIRouter, Request, Depends, Cookie, Form
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

def get_current_member(access_token: str, db: Session):
    if not access_token:
        return None

    try:
        token = access_token.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        member_id = payload.get("sub")

        member = (
            db.query(models.Member)
            .filter(models.Member.id == member_id)
            .first()
        )

        return member

    except Exception:
        return None


@router.get("/change-profile", response_class=HTMLResponse)
def change_profile_page(
    request: Request,
    access_token: str = Cookie(None),
    db: Session = Depends(database.get_db),
):
    member = get_current_member(access_token, db)

    if member is None:
        return RedirectResponse("/auth/login")

    return templates.TemplateResponse(
        request=request,
        name="change_profile.html",
        context={
            "member": member
        }
    )


@router.post("/edit-profile")
def edit_profile(
    request: Request,
    full_name: str = Form(...),
    birth_place: str = Form(...),
    birth_date: str = Form(...),
    gender: str = Form(...),
    address: str = Form(...),
    family_card_number: str = Form(...),
    identity_number: str = Form(...),
    phone_number: str = Form(...),
    spouse_name: str = Form(""),
    job: str = Form(...),

    access_token: str = Cookie(None),
    db: Session = Depends(database.get_db)
):

    member = get_current_member(access_token, db)

    if member is None:
        return RedirectResponse("/auth/login")

    member.full_name = full_name
    member.birth_place = birth_place
    member.birth_date = birth_date
    member.gender = gender
    member.address = address
    member.family_card_number = family_card_number
    member.identity_number = identity_number
    member.phone_number = phone_number
    member.spouse_name = spouse_name
    member.job = job

    db.commit()

    return templates.TemplateResponse(
        request=request,
        name="/dashboard/me",
        status_code=303
    )