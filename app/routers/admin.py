from fastapi import APIRouter, Depends, Cookie, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.config import SECRET_KEY
from jose import jwt, ExpiredSignatureError
from .. import database, models

router = APIRouter(
    prefix="/admin",
    tags=['Admin Dashboard']
)

templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(
    request: Request, 
    db: Session = Depends(database.get_db)
):
    # 1. Ambil token langsung dari request cookie
    token_cookie = request.cookies.get("access_token")
    
    if not token_cookie:
        return RedirectResponse(url="/auth/login?msg=not_login", status_code=303)

    try:
        # Hapus prefix 'Bearer ' jika ada
        token = token_cookie.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        # Ambil data dari payload
        admin_identifier = payload.get("sub") # Ini isinya "admin_ub_001"
        role = payload.get("role")

        if role != "superadmin": # Sesuaikan role dengan logic loginmu
            raise HTTPException(status_code=403, detail="Akses ditolak.")

        # 2. Query ke tabel Admin menggunakan admin_id (bukan ID auto-increment)
        admin_db = db.query(models.Admin).filter(models.Admin.admin_id == admin_identifier).first()

        if not admin_db:
            print(f"LOG: Admin dengan ID {admin_identifier} tidak ada di database!")
            response = RedirectResponse(url="/auth/login?msg=admin_not_found", status_code=303)
            response.delete_cookie("access_token")
            return response

        # 3. Ambil semua data anggota untuk ditampilkan di dashboard
        all_users = db.query(models.User).all()

        return templates.TemplateResponse("admin.html", {
            "request": request,
            "admin": admin_db,
            "all_users": all_users
        })

    except ExpiredSignatureError:
        response = RedirectResponse(url="/auth/login?msg=expired", status_code=303)
        response.delete_cookie("access_token")
        return response
    except Exception as e:
        print(f"LOG ERROR: {e}") # Tambahkan ini agar error muncul di CMD
        return RedirectResponse(url="/auth/login?msg=error", status_code=303)