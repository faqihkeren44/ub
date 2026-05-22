from fastapi import APIRouter, Depends, status, Response, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.config import SECRET_KEY
from jose import jwt, ExpiredSignatureError
from .. import database, models
from app.core import security

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

templates = Jinja2Templates(directory="templates")

def verify_admin(
    request: Request,
    db: Session = Depends(database.get_db)
):
    token_cookie = request.cookies.get("access_token")

    # Belum login
    if not token_cookie:
        return RedirectResponse(url="/auth/login?msg=not_login", status_code=303)

    try:
        # Hilangkan prefix "Bearer "
        token = token_cookie.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Ambil data dari payload
        admin_identifier = payload.get("sub") # Ini isinya "admin_ub_001"
        role = payload.get("role")

        if role != "superadmin": # Sesuaikan role dengan logic loginmu
            raise HTTPException(status_code=403, detail="Akses ditolak.")

        # Cari admin di database
        admin = (
            db.query(models.Admin)
            .filter(models.Admin.admin_id == payload.get("sub"))
            .first()
        )

        if not admin:
            print(f"LOG: Admin dengan ID {admin_identifier} tidak ada di database!")
            response = RedirectResponse(url="/auth/login?msg=admin_not_found", status_code=303)
            response.delete_cookie("access_token")
            return response
        
        return admin

    except ExpiredSignatureError:
        response = RedirectResponse(url="/auth/login?msg=expired", status_code=303)
        response.delete_cookie("access_token")
        return response
    except Exception as e:
        print(f"LOG ERROR: {e}") # Tambahkan ini agar error muncul di CMD
        return RedirectResponse(url="/auth/login?msg=error", status_code=303)

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, msg: str = None, status: str = "peringatan"):
    display_message = ""
    tipe_pesan = status

    if msg == "success_logout":
        display_message = "Anda telah berhasil keluar secara aman."
        tipe_pesan = "sukses"
    elif msg == "not_login":
        display_message = "Silahkan Login terlebih dahulu."
    elif msg == "invalid":
        display_message = "Username atau Password salah. Silahkan coba kembali."
    elif msg == "expired":
        display_message = "Sesi Anda telah berakhir demi keamanan. Silakan masuk kembali."
    elif msg:
        display_message = msg

    return templates.TemplateResponse("login.html", {
        "request": request, 
        "pesan": display_message,
        "status": tipe_pesan
    })

@router.post("/login")
def login_user(response: Response, user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Pengecekan Admin
    admin = db.query(models.Admin).filter(models.Admin.admin_id == user_data.username).first()
        
    if admin:
        if security.verify_password(user_data.password, admin.hashed_password):
            exp = datetime.utcnow() + timedelta(minutes=30)
            payload = {"sub": str(admin.admin_id), "role": "superadmin", "exp": exp}
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")            
            response = RedirectResponse(url="/admin/dashboard", status_code=303)
            response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
            return response

    # Pengecekan Anggota
    user = db.query(models.User).filter(
        or_(
            models.User.identity_number == user_data.username,
            models.User.member_id == user_data.username
        )
    ).first()
    
    if user is None:
        return RedirectResponse(url="/auth/login?msg=invalid", status_code=303)

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(user_data.password, user.hashed_password):
        return RedirectResponse(url="/auth/login?msg=invalid", status_code=303)

    exp = datetime.now() + timedelta(minutes=30)
    payload = {"sub": str(user.id), "role": "user", "exp": exp}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    response = RedirectResponse(url="/dashboard/me", status_code=status.HTTP_303_SEE_OTHER)

    response.set_cookie(
        key="access_token", 
        value=f"Bearer {token}", 
        httponly=True,
        max_age=1800,
        samesite="lax" 
    )

    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/auth/login?msg=success_logout", status_code=303)
    response.delete_cookie("access_token")
    return response