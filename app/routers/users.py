from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from urllib.parse import quote
from app import models, database, schemas
from .auth import verify_user
from app.core import security
from datetime import datetime

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

template = Jinja2Templates(directory="templates")

@router.get("/praregister", response_class=HTMLResponse)
def praregister_page(request: Request):
    return template.TemplateResponse("praregister.html", {
        "request": request
    })

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request, msg: str = None):
    display_message = ""
    tipe_pesan = ""

    if msg == "password_mismatch":
        display_message = "Password dan Confirmation Password berbeda. Pastikan isi keduanya dengan nilai yang sama"
        tipe_pesan = "peringatan"        
    elif msg == "invalid_data":
        display_message = "Data tidak sesuai. Pastikan memasukan data sesuai instruksi"
        tipe_pesan = "peringatan"        
    elif msg == "already_exists":
        display_message = "Email yang dimasukan sudah ada. Silahkan coba menggunakan email yang lain"
        tipe_pesan = "peringatan"    

    return template.TemplateResponse("register.html",{
        "request": request, 
        "pesan": display_message,
        "status": tipe_pesan
    })

@router.post("/register")
def register_member(
    member_data: schemas.MemberCreate = Depends(schemas.MemberCreate.as_form),
    db: Session = Depends(database.get_db)):
    
    if db.query(models.Member).filter(models.Member.identity_number == member_data.identity_number).first():
        return RedirectResponse(url="/members/register?msg=already_exists", status_code=303)
    
    if db.query(models.Member).filter(models.Member.identity_number == member_data.identity_number).first():
        return RedirectResponse(url="/members/register?msg=already_exists", status_code=303)
    
    data = member_data.model_dump(exclude={'password'})

    data['dkm_group'] = models.KelompokDKM(data['dkm_group'])
    data['mandatory_savings'] = models.SetoranWajib(data['mandatory_savings'])
    data['submitted_at'] = datetime.now()

    new_member = models.Member(
        **data,
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    teks_sambutan = f"Selamat, {new_member.full_name} sudah berhasil mendaftar!"
    pesan_sukses = quote(teks_sambutan)

    return RedirectResponse(
        url=f"/auth/login?msg={pesan_sukses}&status=sukses", 
        status_code=303
    )

@router.get("/change-password", response_class=HTMLResponse)
def change_password_page(
    request: Request,
):
    return template.TemplateResponse("change_password.html",{
        "request": request,
    })

@router.post("/change-password")
def change_password(
    request: Request,
    db: Session = Depends(database.get_db),
    current_member: models.Member = Depends(verify_user),
    form_data: schemas.PasswordChange = Depends(schemas.get_password_form)
):
    if isinstance(current_member, RedirectResponse):
        return current_member
    
    member = db.query(models.Member).filter(models.Member.id == current_member.id).first()
    if not security.verify_password(form_data.current_password, member.hashed_password):
        raise HTTPException(status_code=400, detail="Password lama salah")
    
    member.temporary_password = None
    member.hashed_password = security.hash_password(form_data.new_password)
    member.must_change_password=False

    db.commit()
    
    return RedirectResponse(
        "/dashboard/me",
        status_code=303
    )