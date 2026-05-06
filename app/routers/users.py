from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from urllib.parse import quote
from .. import models, schemas, database, utils
import random

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

template = Jinja2Templates(directory="templates")

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
def register_user(
    confirm_password: str = Form(...),
    user_data: schemas.UserCreate = Depends(schemas.UserCreate.as_form),
    db: Session = Depends(database.get_db)):
    
    if user_data.password != confirm_password:
        return RedirectResponse(url="/users/register?msg=password_mismatch", status_code=303)

    if db.query(models.User).filter(models.User.identity_number == user_data.identity_number).first():
        return RedirectResponse(url="/users/register?msg=already_exists", status_code=303)

    data = user_data.model_dump(exclude={'password'})

    data['dkm_group'] = models.KelompokDKM(data['dkm_group'])
    data['mandatory_savings'] = models.SetoranWajib(data['mandatory_savings'])

    hashed_pw = utils.hash_password(user_data.password)
    gen_id = f"UB-{user_data.identity_number[-4:]}{random.randint(10, 99)}"

    new_user = models.User(
        **data,
        member_id=gen_id,
        hashed_password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    teks_sambutan = f"Selamat, {new_user.full_name} sudah berhasil mendaftar!"
    pesan_sukses = quote(teks_sambutan)

    return RedirectResponse(
        url=f"/auth/login?msg={pesan_sukses}&status=sukses", 
        status_code=303
    )