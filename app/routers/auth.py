from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.config import SECRET_KEY
from jose import jwt, ExpiredSignatureError, JWTError
from app import database, models
from app.core import security


# ============================================================
# Custom exception untuk redirect autentikasi.
# Digunakan agar FastAPI dapat mengembalikan RedirectResponse
# dari dependency injection dengan benar (raise, bukan return).
# FastAPI TIDAK otomatis return Response object dari dependency;
# endpoint akan menerimanya sebagai parameter biasa → crash.
# ============================================================
class RedirectException(Exception):
    """Exception yang dikonversi menjadi RedirectResponse oleh handler di main.py."""
    def __init__(self, url: str, status_code: int = 303, delete_cookies: list = None):
        self.url = url
        self.status_code = status_code
        self.delete_cookies = delete_cookies or []


router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

templates = Jinja2Templates(directory="templates")


def verify_admin(
    request: Request,
    db: Session = Depends(database.get_db)
):
    """
    Dependency untuk endpoint admin.
    Mengembalikan objek Admin jika terautentikasi.
    Melempar RedirectException jika tidak terautentikasi.
    """
    token_cookie = request.cookies.get("access_token")

    if not token_cookie:
        raise RedirectException(url="/auth/login?msg=not_login")

    try:
        token = token_cookie.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        admin_identifier = payload.get("sub")
        role = payload.get("role")

        if role != "superadmin":
            raise RedirectException(url="/auth/login?msg=not_login")

        admin = (
            db.query(models.Admin)
            .filter(models.Admin.admin_id == admin_identifier)
            .first()
        )

        if not admin:
            print(f"LOG: Admin dengan ID {admin_identifier} tidak ada di database!")
            raise RedirectException(
                url="/auth/login?msg=admin_not_found",
                delete_cookies=["access_token"]
            )

        return admin

    except RedirectException:
        raise

    except ExpiredSignatureError:
        raise RedirectException(
            url="/auth/login?msg=expired",
            delete_cookies=["access_token"]
        )

    except JWTError as e:
        print(f"LOG JWT ERROR: {e}")
        raise RedirectException(url="/auth/login?msg=error")


def verify_user(
    request: Request,
    db: Session = Depends(database.get_db)
):
    """
    Dependency untuk endpoint anggota (member).
    Mengembalikan objek Member jika terautentikasi.
    Melempar RedirectException jika tidak terautentikasi.
    """
    token_cookie = request.cookies.get("access_token")

    if not token_cookie:
        raise RedirectException(url="/auth/login?msg=not_login")

    try:
        token = token_cookie.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")

        if user_id is None:
            raise RedirectException(url="/auth/login?msg=not_login")

        user = db.query(models.Member).filter(models.Member.id == user_id).first()
        if not user:
            raise RedirectException(
                url="/auth/login?msg=not_found",
                delete_cookies=["access_token"]
            )

        return user

    except RedirectException:
        raise

    except ExpiredSignatureError:
        raise RedirectException(
            url="/auth/login?msg=expired",
            delete_cookies=["access_token"]
        )

    except Exception as e:
        print(f"LOG ERROR verify_user: {e}")
        raise RedirectException(url="/auth/login?msg=error")


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

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "pesan": display_message,
            "status": tipe_pesan
        }
    )


@router.post("/login")
def login_user(
    response: Response,
    user_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
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
    user = db.query(models.Member).filter(
        or_(
            models.Member.identity_number == user_data.username,
            models.Member.member_id == user_data.username
        )
    ).first()

    if user is None:
        return RedirectResponse(url="/auth/login?msg=invalid", status_code=303)

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(user_data.password, user.hashed_password):
        return RedirectResponse(url="/auth/login?msg=invalid", status_code=303)

    exp = datetime.utcnow() + timedelta(minutes=30)
    payload = {"sub": str(user.id), "role": "user", "exp": exp}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    response = RedirectResponse(url="/dashboard/me", status_code=303)
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