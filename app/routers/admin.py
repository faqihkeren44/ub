from fastapi import APIRouter, Depends, Cookie, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from app import database, models
from app.core import security, password
from app import models
from .auth import verify_admin

from typing import Optional
from sqlalchemy import extract

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
    message = ""
    if msg =="success":
        message = "Anggota sudah disetujui"
    
    registers = (
        db.query(models.Member)
        .filter(models.Member.member_status == models.MemberStatus.PENDING)
        .order_by(models.Member.submitted_at.desc())
        .limit(5)
        .all()
    )
    
    all_members = (
        db.query(models.Member)
        .filter(models.Member.member_status == models.MemberStatus.ACTIVE)
        .filter(extract("year", models.Member.approved_at) == 2026)
        .order_by(models.Member.approved_at.desc())
        .limit(5)
        .all()
    )

    # Menghitung total member aktif
    total_active_members = (
        db.query(models.Member)
        .filter(models.Member.member_status == models.MemberStatus.ACTIVE) # sesuaikan jika namanya ACTIVE
        .count()
    )

    # Menghitung total member tidak aktif / pending / ditolak
    total_inactive_members = (
        db.query(models.Member)
        .filter(models.Member.member_status != models.MemberStatus.ACTIVE) # selain yang aktif
        .count()
    )
    
    # Menghitung keseluruhan member tanpa filter status
    total_all_members = db.query(models.Member).count()

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "admin": admin,
            "registers": registers,
            "all_members": all_members,
            "message": message,
            "total_active": total_active_members,
            "total_inactive": total_inactive_members,
            "total_all": total_all_members
        }
    )

@router.get("/members/list", response_class=HTMLResponse)
def members_list(
    request: Request,
    dkm_group: Optional[str] = None,
    name: Optional[str] = None,
    year: str | None = None,
    db: Session = Depends(database.get_db),
    admin: models.Admin = Depends(verify_admin)
):
    query = db.query(models.Member)
    # .filter(models.Member.member_status == models.MemberStatus.ACTIVE)

    if dkm_group:
        query = query.filter(
            models.Member.dkm_group == models.KelompokDKM[dkm_group]
        )

    if name:
        query = query.filter(
            models.Member.full_name.ilike(f"%{name}%")
        )

    # Filter tahun
    current_year = datetime.now().year

    if year == "all":
        selected_year = "all"

    elif year:
        selected_year = int(year)
        query = query.filter(
            extract("year", models.Member.approved_at) == selected_year
        )

    else:
        selected_year = current_year
        query = query.filter(
            extract("year", models.Member.approved_at) == current_year
        )

    all_members = (
        query
        .order_by(models.Member.full_name.asc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="members_list.html",
        context={
            "admin": admin,
            "all_members": all_members,
            "dkm_groups": models.KelompokDKM,
            "selected_dkm": dkm_group,
            "selected_year": selected_year,
            "search_name": name,
        }
    )

@router.get("/members/{member_id}", response_class=HTMLResponse)
def member_detail(
    member_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
    admin: models.Admin = Depends(verify_admin)
):
    member = (db.query(models.Member).filter(models.Member.id == member_id)).first()

    if not member:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan") 
    
    is_registration = (
        member.member_status == models.MemberStatus.PENDING
    )
    
    return templates.TemplateResponse(
        request=request,
        name="admin_member_detail.html",
        context={
            "request": request,
            "admin": admin,
            "member": member,
            "is_registration": is_registration,
        }
    )

# ==========================================================
# PERSETUJUAN REGISTRASI
# ==========================================================
@router.post("/members/{member_id}/approve", response_class=HTMLResponse)
def approve_registration(
    member_id: int,
    db: Session = Depends(database.get_db),
    admin: models.Admin = Depends(verify_admin)
):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()

    if member.member_status != models.MemberStatus.PENDING:
        raise HTTPException(status_code=400, detail="Data pendaftar tidak ditemukan")
    
    year = datetime.now().year
    gen_id = f"UB{year}-{member.id:03d}"
    temporary_password = (password.generate_password(8))
    hashed_pw = security.hash_password(temporary_password)

    member.member_id = gen_id
    member.hashed_password = hashed_pw
    member.temporary_password = temporary_password
    member.must_change_password = True
    member.member_status = models.MemberStatus.ACTIVE
    member.approved_by = admin.admin_id
    member.approved_at = datetime.now()

    db.commit()
    db.refresh(member)

    return RedirectResponse(
        "/admin/dashboard", 
        status_code=303
    )
    
@router.post("/members/{member_id}/delete", response_class=HTMLResponse)
def delete_member(
    member_id: int,
    db: Session = Depends(database.get_db),
    admin: models.Admin = Depends(verify_admin)
):
    # Cari anggota berdasarkan ID
    member = db.query(models.Member).filter(models.Member.id == member_id).first()

    # Jika anggota tidak ditemukan, lemparkan error 404
    if not member:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")
    
    # Proses penghapusan data dari database
    db.delete(member)
    db.commit()

    # Redirect kembali ke halaman dashboard utama admin
    return RedirectResponse(
        url="/admin/dashboard?msg=deleted", 
        status_code=303
    )

# ==========================================================
# RESET PASSWORD
# ==========================================================

@router.post("/members/{member_id}/reset-password", response_class=HTMLResponse)
def reset_password(
    member_id: int,
    db: Session = Depends(database.get_db),
    admin: models.Admin = Depends(verify_admin)
):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()

    if not member:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")
    
    new_password = password.generate_password(8)

    member.hashed_password = security.hash_password(new_password)
    member.temporary_password = new_password
    member.must_change_password = True

    db.commit()

    return RedirectResponse(
        url=f"/admin/members/{member_id}",
        status_code=303
    )

# ==========================================================
# GENERATE PDF FORMULIR
# ==========================================================

from fastapi import APIRouter, Response
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.pdf_generator import generate_member_pdf

@router.get("/member/{member_id}/preview")
async def preview_member_pdf(member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()

    try:
        pdf_bytes = generate_member_pdf(member)
        return Response(
            content=bytes(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename=Form_Pendaftaran_{member.id}.pdf"
            }
        )
    except Exception as e:    
        return {"status": "error", "detail_kesalahan": str(e)}


# ==========================================================
# EDIT PROFILE ANGGOTA
# ==========================================================
from app.core.config import SECRET_KEY
from jose import jwt

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
    
@router.get("/members/{member_id}/edit-profile", response_class=HTMLResponse)
def change_profile_page(
    member_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
    admin: models.Admin = Depends(verify_admin)
):
    member = (db.query(models.Member).filter(models.Member.id == member_id)).first()

    if not member:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan") 
    
    return templates.TemplateResponse(
        request=request,
        name="change_profile_admin.html",
        context={
            "request": request,
            "admin": admin,
            "member": member
        }
    )


@router.post("/members/{member_id}/edit-profile")
def edit_profile(
    member_id: int,
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
    member_status: str = Form(...),
    db: Session = Depends(database.get_db)
):
    member = (db.query(models.Member).filter(models.Member.id == member_id)).first()

    if not member:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan") 

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
    member.member_status = models.MemberStatus(member_status)

    db.commit()

    return RedirectResponse(
        "/admin/dashboard",
        status_code=303
    )