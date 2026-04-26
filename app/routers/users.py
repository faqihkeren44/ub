from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from urllib.parse import quote
from .. import models, schemas, database, utils

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
    full_name: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(database.get_db)):
    
    if password != confirm_password:
        return RedirectResponse(url="/users/register?msg=password_mismatch", status_code=303)

    try:
        user_data = schemas.UserCreate(
            full_name=full_name,
            email=username,
            password=password
        )
    except ValueError as e:
        return RedirectResponse(url="/users/register?msg=invalid_data", status_code=303)

    user_exist = db.query(models.User).filter(models.User.email == user_data.email).first()
    if user_exist:
        return RedirectResponse(url="/users/register?msg=already_exists", status_code=303)

    hashed_password = utils.hash_password(user_data.password)

    new_user = models.User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
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