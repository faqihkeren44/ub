from fastapi import APIRouter, Depends, Cookie, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from urllib.parse import quote
from .. import database, models, utils
from .auth import verify_admin
import random

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
    
    gen_id = f"UB-{register.identity_number[-4:]}{random.randint(10, 99)}"
    hashed_pw = utils.hash_password(gen_id)

    new_user = models.User(
        member_id=gen_id,
        hashed_password=hashed_pw,
        full_name=register.full_name,
        birth_info=register.birth_info,
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
    

# @router.post("/update-status/{user_id}")
# def update_user_status(
#     user_id: int,
#     new_status: str = Form(...),
#     request: Request = None,
#     db: Session = Depends(database.get_db)
# ):
#     token_cookie = request.cookies.get("access_token")

#     if not token_cookie:
#         return RedirectResponse(
#             url="auth/login?msg=not_login",
#             status_code=303
#         )

#     try:
#         token = token_cookie.replace("Bearer ", "")
#         payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

#         admin_identifier = payload.get("sub")
#         role = payload.get("role")

#         if role != "superadmin":
#             raise HTTPException(status_code=403, detail="Akses ditolak.")

#         # Ambil admin dari database
#         admin_db = (
#             db.query(models.Admin)
#             .filter(models.Admin.admin_id == admin_identifier)
#             .first()
#         )

#         if not admin_db:
#             raise HTTPException(status_code=404, detail="Admin tidak ditemukan.")

#         # Ambil user yang ingin diubah
#         user = (
#             db.query(models.User)
#             .filter(models.User.id == user_id)
#             .first()
#         )

#         if not user:
#             raise HTTPException(status_code=404, detail="User tidak ditemukan.")

#         # Mapping string ke enum
#         status_mapping = {
#             "APPROVED": models.UserStatus.APPROVED.value,
#             "REJECTED": models.UserStatus.REJECTED.value,
#             "PENDING": models.UserStatus.PENDING.value,
#         }

#         if new_status not in status_mapping:
#             raise HTTPException(status_code=400, detail="Status tidak valid.")

#         # Update status
#         user.status_flags = status_mapping[new_status]
#         user.approved_by = admin_db.admin_id

#         db.commit()

#         return RedirectResponse(
#             url="/admin/dashboard",
#             status_code=303
#         )

#     except ExpiredSignatureError:
#         response = RedirectResponse(
#             url="/auth/login?msg=expired",
#             status_code=303
#         )
#         response.delete_cookie("access_token")
#         return response