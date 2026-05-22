from fastapi import APIRouter, Depends, Cookie, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from app import database, models
from app.core import security, password
from app import models
from .auth import verify_admin

router = APIRouter(
    prefix="/admin",
    tags=['Admin Dashboard'],
    dependencies=[Depends(verify_admin)]
)

templates = Jinja2Templates(directory="templates")

# ==========================================================
# DASHBOARD ADMIN
# ==========================================================
@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(
    request: Request,
    db: Session = Depends(database.get_db),
    msg: str = None,
    admin: models.Admin = Depends(verify_admin)
):
    if msg =="success":
        message = "Anggota sudah disetujui"
    
    registers = db.query(models.Registration).order_by(models.Registration.submitted_at.desc()).all()
    all_users = (
        db.query(models.User)
        .order_by(models.User.approved_at.desc())
        .limit(5)
        .all()
    )

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "admin": admin,
            "registers": registers,
            "all_users": all_users
        }
    )

@router.get("/users/{user_id}", response_class=HTMLResponse)
def user_detail(
    user_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
    admin: models.Admin = Depends(verify_admin)
):
    user = (db.query(models.User).filter(models.User.id == user_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan") 
    
    return templates.TemplateResponse(
        "admin_user_detail.html",
        {
            "request": request,
            "admin": admin,
            "user": user
        }
    )

@router.get("/register/{user_id}", response_class=HTMLResponse)
def register_detail(
    user_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
    admin: models.Admin = Depends(verify_admin)
):
    user = db.query(models.Registration).filter(models.Registration.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan") 
    
    return templates.TemplateResponse(
        "admin_user_detail.html",
        {
            "request": request,
            "admin": admin,
            "user": user
        }
    )


# ==========================================================
# PERSETUJUAN REGISTRASI
# ==========================================================
@router.post("/registrations/{user_id}/approve", response_class=HTMLResponse)
def approve_registration(
    user_id: int,
    db: Session = Depends(database.get_db),
    admin: models.Admin = Depends(verify_admin)
):
    register = db.query(models.Registration).filter(models.Registration.id == user_id).first()

    if not register:
        raise HTTPException(status_code=400, detail="Data pendaftar tidak ditemukan")
    
    existing_user = db.query(models.User).filter(models.User.identity_number == register.identity_number).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User dengan NIK tersebut sudah terdaftar")
    
    year = datetime.now().year
    gen_id = f"UB{year}-{register.id:03d}"
    temporary_password = (password.generate_password(8))
    hashed_pw = security.hash_password(temporary_password)

    new_user = models.User(
        member_id=gen_id,
        temporary_password=temporary_password,
        must_change_password=True,
        hashed_password=hashed_pw,
        full_name=register.full_name,
        birth_date=register.birth_date,
        birth_place=register.birth_place,
        gender=register.gender,
        address=register.address,
        family_card_number=register.family_card_number,
        identity_number=register.identity_number,
        phone_number=register.phone_number,
        spouse_name=register.spouse_name,
        dkm_group=register.dkm_group,
        mandatory_savings=register.mandatory_savings,
        approved_by=admin.admin_id
    )

    db.add(new_user)
    db.delete(register)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(
        "/admin/dashboard", 
        status_code=303
    )