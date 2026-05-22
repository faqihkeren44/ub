from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from urllib.parse import quote
from app import models, database
from app.schemas.user import UserCreate

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
    user_data: UserCreate = Depends(UserCreate.as_form),
    db: Session = Depends(database.get_db)):
    
    if db.query(models.User).filter(models.User.identity_number == user_data.identity_number).first():
        return RedirectResponse(url="/users/register?msg=already_exists", status_code=303)
    
    if db.query(models.User).filter(models.Registration.identity_number == user_data.identity_number).first():
        return RedirectResponse(url="/users/register?msg=already_exists", status_code=303)
    

    data = user_data.model_dump(exclude={'password'})

    data['dkm_group'] = models.user.KelompokDKM(data['dkm_group'])
    data['mandatory_savings'] = models.user.SetoranWajib(data['mandatory_savings'])


    new_user = models.Registration(
        **data,
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