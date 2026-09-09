from fastapi import APIRouter, Request, Depends, Cookie, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.config import SECRET_KEY
from jose import jwt, ExpiredSignatureError
from .. import models, database

from app.utils.storage import get_public_url, upload_image, delete_image

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
    
    photo_url = None

    if member.photo:
        photo_url = get_public_url(member.photo, "member-photo")    

    return templates.TemplateResponse(
        request=request,
        name="member/dashboard.html",
        context={ 
            "member": member,
            "photo_url": photo_url,
        }
    )

@router.get("/profile", response_class=HTMLResponse)
def profile(
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
    
    photo_url = None

    if member.photo:
        photo_url = get_public_url(member.photo, "member-photo")

    return templates.TemplateResponse(
        request=request,
        name="member/profile.html",
        context={ 
        "member": member,
        "photo_url": photo_url
        }
    )

def get_current_member(
    access_token: str = Cookie(None),
    db: Session = Depends(database.get_db)
):
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


@router.get("/edit-profile", response_class=HTMLResponse)
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
        name="member/change_profile.html",
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
    dkm_group: str = Form(...),
    mandatory_savings: int = Form(...),
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
    member.dkm_group = models.KelompokDKM(dkm_group)
    member.mandatory_savings = models.SetoranWajib(mandatory_savings)

    db.commit()

    return RedirectResponse(
        "/dashboard/me",
        status_code=303
    )

from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from app.utils.storage import upload_image, delete_image

@router.post("/profile/photo")
async def update_photo(
    photo: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.Member = Depends(get_current_member)
):
    member = db.query(models.Member).filter(
        models.Member.id == current_user.id
    ).first()

    if member.photo:
        delete_image(member.photo)

    new_photo = await upload_image(photo)

    member.photo = new_photo

    print("Photo di DB:", member.photo)
    
    db.commit()

    return RedirectResponse(
        "/dashboard/me",
        status_code=303
    )

# https://chwgvqetsfxcedlkztky.supabase.co/storage/v1/object/public/member-photo/member/cf668b06-85b8-4bcc-95da-25f9d0723725.png
# member/e44113b1-2882-4963-8f75-14e9a47e73b2.png
# member/cf668b06-85b8-4bcc-95da-25f9d0723725.png