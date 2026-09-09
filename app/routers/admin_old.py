# from fastapi import APIRouter, Depends, Cookie, Request, HTTPException, Form
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.templating import Jinja2Templates
# from sqlalchemy.orm import Session
# from datetime import datetime
# from app import database, models
# from app.core import security, password
# from app import models
# from .auth import verify_admin

# from typing import Optional
# from sqlalchemy import extract

# from app.utils.storage import get_public_url, upload_image, delete_image

# router = APIRouter(
#     prefix="/admin",
#     tags=['Admin Dashboard'],
#     dependencies=[Depends(verify_admin)]
# )

# templates = Jinja2Templates(directory="templates")

# # ==========================================================
# # DASHBOARD ADMIN
# # ==========================================================
# @router.get("/dashboard", response_class=HTMLResponse)
# def admin_dashboard(
#     request: Request,
#     db: Session = Depends(database.get_db),
#     msg: str = None,
#     admin: models.Admin = Depends(verify_admin)
# ):
#     message = ""
#     if msg =="success":
#         message = "Anggota sudah disetujui"
    
#     registers = (
#         db.query(models.Member)
#         .filter(models.Member.member_status == models.MemberStatus.PENDING)
#         .order_by(models.Member.submitted_at.desc())
#         .limit(5)
#         .all()
#     )
    
#     all_members = (
#         db.query(models.Member)
#         .filter(models.Member.member_status == models.MemberStatus.ACTIVE)
#         .filter(extract("year", models.Member.approved_at) == 2026)
#         .order_by(models.Member.approved_at.desc())
#         .limit(5)
#         .all()
#     )

#     # Menghitung total member aktif
#     total_active_members = (
#         db.query(models.Member)
#         .filter(models.Member.member_status == models.MemberStatus.ACTIVE) # sesuaikan jika namanya ACTIVE
#         .count()
#     )

#     # Menghitung total member tidak aktif / pending / ditolak
#     total_inactive_members = (
#         db.query(models.Member)
#         .filter(models.Member.member_status != models.MemberStatus.ACTIVE) # selain yang aktif
#         .count()
#     )

#     total_registers = (
#         db.query(models.Member)
#         .filter(models.Member.member_status != models.MemberStatus.PENDING) # selain yang aktif
#         .count()
#     )
    
#     # Menghitung keseluruhan member tanpa filter status
#     total_all_members = db.query(models.Member).count()

#     return templates.TemplateResponse(
#         request=request,
#         name="admin/dashboard.html",
#         context={
#             "admin": admin,
#             "registers": registers,
#             "all_members": all_members,
#             "message": message,
#             "total_active": total_active_members,
#             "total_inactive": total_inactive_members,
#             "total_registers": total_registers,
#             "total_all": total_all_members
#         }
#     )

# @router.get("/members/list", response_class=HTMLResponse)
# def members_list(
#     request: Request,
#     dkm_group: Optional[str] = None,
#     name: Optional[str] = None,
#     year: str | None = None,
#     db: Session = Depends(database.get_db),
#     admin: models.Admin = Depends(verify_admin)
# ):
#     query = db.query(models.Member)
#     # .filter(models.Member.member_status == models.MemberStatus.ACTIVE)

#     if dkm_group:
#         query = query.filter(
#             models.Member.dkm_group == models.KelompokDKM[dkm_group]
#         )

#     if name:
#         query = query.filter(
#             models.Member.full_name.ilike(f"%{name}%")
#         )

#     # Filter tahun
#     current_year = datetime.now().year

#     if year == "all":
#         selected_year = "all"

#     elif year:
#         selected_year = int(year)
#         query = query.filter(
#             extract("year", models.Member.approved_at) == selected_year
#         )

#     else:
#         selected_year = current_year
#         query = query.filter(
#             extract("year", models.Member.approved_at) == current_year
#         )

#     all_members = (
#         query
#         .order_by(models.Member.full_name.asc())
#         .all()
#     )

#     return templates.TemplateResponse(
#         request=request,
#         name="admin/member_list.html",
#         context={
#             "admin": admin,
#             "all_members": all_members,
#             "dkm_groups": models.KelompokDKM,
#             "selected_dkm": dkm_group,
#             "selected_year": selected_year,
#             "search_name": name,
#         }
#     )

# @router.get("/members/{member_id}", response_class=HTMLResponse)
# def member_detail(
#     member_id: int,
#     request: Request,
#     db: Session = Depends(database.get_db),
#     admin: models.Admin = Depends(verify_admin)
# ):
#     member = (db.query(models.Member).filter(models.Member.id == member_id)).first()

#     if not member:
#         raise HTTPException(status_code=404, detail="Anggota tidak ditemukan") 

#     photo_url = None

#     if member.photo:
#         photo_url = get_public_url(member.photo, "member-photo")
    
#     if member.photo_ktp:
#         photo_ktp_url = get_public_url(member.photo_ktp, "photo_ktp")
    
#     if member.photo_kk:
#         photo_kk_url = get_public_url(member.photo_kk, "photo_kk")

#     is_registration = (
#         member.member_status == models.MemberStatus.PENDING
#     )
    
#     return templates.TemplateResponse(
#         request=request,
#         name="admin/member_details.html",
#         context={
#             "request": request,
#             "admin": admin,
#             "member": member,
#             "photo_url": photo_url,
#             "photo_ktp_url": photo_ktp_url,
#             "photo_kk_url": photo_kk_url,
#             "is_registration": is_registration,
#         }
#     )

# from fastapi import UploadFile
# from fastapi import File
# from fastapi import Form
# from app.utils.storage import upload_image, delete_image

# @router.post("/members/{member_id}/photo", response_class=HTMLResponse)
# async def update_photo(
#     member_id: int,
#     request: Request,
#     db: Session = Depends(database.get_db),
#     admin: models.Admin = Depends(verify_admin),  
#     photo: UploadFile = File(...)
# ):
#     member = (db.query(models.Member).filter(models.Member.id == member_id)).first()

#     if not member:
#         raise HTTPException(status_code=404, detail="Anggota tidak ditemukan") 
    
#     if member.photo:
#         delete_image(member.photo)

#     new_photo = await upload_image(photo)

#     member.photo = new_photo

#     print("Photo di DB:", member.photo)
    
#     db.commit()

#     return RedirectResponse(
#         f"/admin/members/{member_id}",
#         status_code=303
#     )

# # ==========================================================
# # PERSETUJUAN REGISTRASI
# # ==========================================================
# @router.post("/members/{member_id}/approve", response_class=HTMLResponse)
# def approve_registration(
#     member_id: int,
#     db: Session = Depends(database.get_db),
#     admin: models.Admin = Depends(verify_admin)
# ):
#     member = (
#         db.query(models.Member)
#         .filter(models.Member.id == member_id)
#         .first()
#     )

#     if not member:
#         raise HTTPException(
#             status_code=404,
#             detail="Member tidak ditemukan"
#         )

#     if member.member_status != models.MemberStatus.PENDING:
#         raise HTTPException(
#             status_code=400,
#             detail="Data pendaftar tidak ditemukan"
#         )

#     year = datetime.now().year
#     gen_id = f"UB{year}-{member.id:03d}"

#     temporary_password = password.generate_password(8)
#     hashed_pw = security.hash_password(temporary_password)

#     member.member_id = gen_id
#     member.hashed_password = hashed_pw
#     member.temporary_password = temporary_password
#     member.must_change_password = True
#     member.member_status = models.MemberStatus.ACTIVE
#     member.approved_by = admin.admin_id
#     member.approved_at = datetime.now()

#     db.commit()
#     db.refresh(member)

#     return RedirectResponse(
#         "/admin/dashboard",
#         status_code=303
#     )

# @router.post("/members/{member_id}/delete", response_class=HTMLResponse)
# def delete_member(
#     member_id: int,
#     db: Session = Depends(database.get_db),
#     admin: models.Admin = Depends(verify_admin)
# ):
#     # Cari anggota berdasarkan ID
#     member = db.query(models.Member).filter(models.Member.id == member_id).first()

#     # Jika anggota tidak ditemukan, lemparkan error 404
#     if not member:
#         raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")
    
#     if member.photo:
#         delete_image(member.photo)
    
#     # Proses penghapusan data dari database
#     db.delete(member)
#     db.commit()

#     # Redirect kembali ke halaman dashboard utama admin
#     return RedirectResponse(
#         url="/admin/dashboard?msg=deleted", 
#         status_code=303
#     )

# # ==========================================================
# # RESET PASSWORD
# # ==========================================================

# @router.post("/members/{member_id}/reset-password", response_class=HTMLResponse)
# def reset_password(
#     member_id: int,
#     db: Session = Depends(database.get_db),
#     admin: models.Admin = Depends(verify_admin)
# ):
#     member = db.query(models.Member).filter(models.Member.id == member_id).first()

#     if not member:
#         raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")
    
#     new_password = password.generate_password(8)

#     member.hashed_password = security.hash_password(new_password)
#     member.temporary_password = new_password
#     member.must_change_password = True

#     db.commit()

#     return RedirectResponse(
#         url=f"/admin/members/{member_id}",
#         status_code=303
#     )

# # ==========================================================
# # GENERATE PDF FORMULIR
# # ==========================================================

# from fastapi import APIRouter, Response
# from fastapi import Depends
# from fastapi import HTTPException
# from fastapi.responses import FileResponse
# from sqlalchemy.orm import Session

# from app.database import get_db
# from app.services.pdf_generator import generate_member_pdf

# @router.get("/member/{member_id}/preview")
# async def preview_member_pdf(member_id: int, db: Session = Depends(get_db)):
#     member = db.query(models.Member).filter(models.Member.id == member_id).first()

#     try:
#         pdf_bytes = generate_member_pdf(member)
#         return Response(
#             content=bytes(pdf_bytes),
#             media_type="application/pdf",
#             headers={
#                 "Content-Disposition": f"inline; filename=Form_Pendaftaran_{member.id}.pdf"
#             }
#         )
#     except Exception as e:    
#         return {"status": "error", "detail_kesalahan": str(e)}


# # ==========================================================
# # EDIT PROFILE ANGGOTA
# # ==========================================================
# from app.core.config import SECRET_KEY
# from jose import jwt

# def get_current_member(access_token: str, db: Session):
#     if not access_token:
#         return None

#     try:
#         token = access_token.split(" ")[1]
#         payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         member_id = payload.get("sub")

#         member = (
#             db.query(models.Member)
#             .filter(models.Member.id == member_id)
#             .first()
#         )

#         return member

#     except Exception:
#         return None
    
# @router.get("/members/{member_id}/edit-profile", response_class=HTMLResponse)
# def change_profile_page(
#     member_id: int,
#     request: Request,
#     db: Session = Depends(database.get_db),
#     admin: models.Admin = Depends(verify_admin)
# ):
#     member = (db.query(models.Member).filter(models.Member.id == member_id)).first()

#     if not member:
#         raise HTTPException(status_code=404, detail="Anggota tidak ditemukan") 
    
#     return templates.TemplateResponse(
#         request=request,
#         name="admin/change_profile.html",
#         context={
#             "request": request,
#             "admin": admin,
#             "member": member
#         }
#     )


# @router.post("/members/{member_id}/edit-profile")
# def edit_profile(
#     member_id: int,
#     request: Request,
#     full_name: str = Form(...),
#     birth_place: str = Form(...),
#     birth_date: str = Form(...),
#     gender: str = Form(...),
#     address: str = Form(...),
#     family_card_number: str = Form(...),
#     identity_number: str = Form(...),
#     phone_number: str = Form(...),
#     spouse_name: str = Form(""),
#     job: str = Form(...),
#     dkm_group: str = Form(...),
#     mandatory_savings: int = Form(...),
#     member_status: str = Form(...),
#     db: Session = Depends(database.get_db)
# ):
#     member = (db.query(models.Member).filter(models.Member.id == member_id)).first()

#     if not member:
#         raise HTTPException(status_code=404, detail="Anggota tidak ditemukan") 

#     member.full_name = full_name
#     member.birth_place = birth_place
#     member.birth_date = birth_date
#     member.gender = gender
#     member.address = address
#     member.family_card_number = family_card_number
#     member.identity_number = identity_number
#     member.phone_number = phone_number
#     member.spouse_name = spouse_name
#     member.job = job
#     member.dkm_group = models.KelompokDKM(dkm_group)
#     member.mandatory_savings = models.SetoranWajib(mandatory_savings)
#     member.member_status = models.MemberStatus(member_status)

#     db.commit()

#     return RedirectResponse(
#         "/admin/dashboard",
#         status_code=303
#     )

# # ==========================================================
# # IMPORT DATA ANGGOTA
# # ==========================================================

# import pandas as pd
# from io import BytesIO

# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models.member import Member

# from app.models.member import (
#     KelompokDKM,
#     SetoranWajib,
#     MemberStatus,
# )

# @router.get("/import")
# async def import_members_page(request: Request):

#     return templates.TemplateResponse(
#         "admin/member_import.html",
#         {
#             "request": request
#         }
#     )

# @router.post("/import")
# async def import_members(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):

#     # ==================================================
#     # 1. Validasi ekstensi file
#     # ==================================================

#     if not file.filename.lower().endswith((".xlsx", ".xls")):
#         raise HTTPException(
#             status_code=400,
#             detail="File harus berupa Excel (.xlsx atau .xls)"
#         )


#     # ==================================================
#     # 2. Baca file
#     # ==================================================

#     content = await file.read()

#     try:
#         df = pd.read_excel(
#             BytesIO(content),
#             header=1
#         )

#         df = df.dropna(
#             how="all"
#         )

#         df = df[
#             df["NOMOR ANGGOTA"].notna()
#         ]

#     except Exception as e:
#         print("ERROR EXCEL:", repr(e))

#         raise HTTPException(
#             status_code=400,
#             detail=f"File Excel tidak dapat dibaca: {str(e)}"
#         )


#     # ==================================================
#     # 3. Bersihkan nama kolom
#     # ==================================================

#     df.columns = (
#         df.columns
#         .astype(str)
#         .str.strip()
#     )


#     print("COLUMNS:", df.columns.tolist())


#     # ==================================================
#     # 4. Mapping kolom Excel → Member
#     # ==================================================

#     column_mapping = {

#         "NOMOR ANGGOTA": "member_id",

#         "NAMA": "full_name",

#         "TEMPAT LAHIR": "birth_place",

#         "TANGGAL LAHIR": "birth_date",

#         "JENIS KELAMIN": "gender",

#         "ALAMAT": "address",

#         "NOMOR KARTU KELUARGA": "family_card_number",

#         "NOMOR KTP": "identity_number",

#         "NO TLP / HP": "phone_number",

#         "PEKERJAAN": "job",

#         "NAMA SUAMI / ISTRI": "spouse_name",

#         "KELOMPOK DKM": "dkm_group",

#         "SIMPANAN WAJIB": "mandatory_savings",

#         "TANGGAL MASUK KOPERASI": "submitted_at",

#         "AKTIF / KELUAR": "member_status",

#         "TANGGAL KELUAR": "left_at",

#         "KETERANGAN": "status_note"
#     }


#     # ==================================================
#     # 5. Kolom yang wajib ada
#     # ==================================================

#     required_columns = list(
#         column_mapping.keys()
#     )


#     missing_columns = [
#         column
#         for column in required_columns
#         if column not in df.columns
#     ]


#     if missing_columns:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "message": "Kolom Excel tidak lengkap",
#                 "missing_columns": missing_columns
#             }
#         )


#     # ==================================================
#     # 6. Ambil hanya kolom yang diperlukan
#     # ==================================================

#     df = df[
#         required_columns
#     ].copy()


#     # ==================================================
#     # 7. Rename kolom
#     # ==================================================

#     df.rename(
#         columns=column_mapping,
#         inplace=True
#     )


#     # ==================================================
#     # 8. Bersihkan data
#     # ==================================================

#     for column in df.columns:

#         if df[column].dtype == "object":

#             df[column] = (
#                 df[column]
#                 .fillna("")
#                 .astype(str)
#                 .str.strip()
#             )


#     # ==================================================
#     # 9. Normalisasi Gender
#     # ==================================================

#     gender_mapping = {

#         "L": "Pria",
#         "LAKI-LAKI": "Pria",
#         "LAKI LAKI": "Pria",
#         "PRIA": "Pria",

#         "P": "Wanita",
#         "PEREMPUAN": "Wanita",
#         "WANITA": "Wanita"
#     }


#     df["gender"] = (
#         df["gender"]
#         .str.upper()
#         .map(gender_mapping)
#         .fillna(df["gender"])
#     )


#     # ==================================================
#     # 10. Normalisasi Status
#     #
#     # HANYA menggunakan AKTIF / KELUAR
#     # STATUS ANGGOTA diabaikan
#     # ==================================================

#     status_mapping = {

#         "AKTIF": MemberStatus.ACTIVE.value,

#         "KELUAR": MemberStatus.RESIGNED.value,

#         "TIDAK AKTIF": MemberStatus.INACTIVE.value
#     }


#     df["member_status"] = (
#         df["member_status"]
#         .str.upper()
#         .map(status_mapping)
#         .fillna(df["member_status"])
#     )


#     # ==================================================
#     # 11. Normalisasi Kelompok DKM
#     # ==================================================

#     valid_dkm = {
#         item.value
#         for item in KelompokDKM
#     }


#     # ==================================================
#     # 12. Normalisasi Simpanan Wajib
#     # ==================================================

#     def normalize_savings(value):

#         if value == "":
#             return ""

#         try:
#             value = float(value)

#             return int(value)

#         except (ValueError, TypeError):

#             value = str(value).upper().strip()

#             mapping = {
#                 "25K": 25000,
#                 "50K": 50000,
#                 "100K": 100000,
#                 "250K": 250000,
#                 "500K": 500000
#             }

#             return mapping.get(
#                 value,
#                 value
#             )


#     df["mandatory_savings"] = (
#         df["mandatory_savings"]
#         .apply(normalize_savings)
#     )


#     valid_savings = {
#         item.value
#         for item in SetoranWajib
#     }


#     # ==================================================
#     # 13. Konversi tanggal
#     # ==================================================

#     date_columns = [
#         "birth_date",
#         "submitted_at",
#         "left_at"
#     ]


#     for column in date_columns:

#         df[column] = pd.to_datetime(
#             df[column],
#             errors="coerce",
#             format="%d/%m/%Y",
#             dayfirst=True
#         )


#     # ==================================================
#     # 14. approved_at = submitted_at
#     # ==================================================

#     df["approved_at"] = df["submitted_at"]


#     # ==================================================
#     # 15. Validasi
#     # ==================================================

#     df["is_valid"] = True

#     df["errors"] = ""


#     def add_error(mask, message):

#         df.loc[
#             mask,
#             "is_valid"
#         ] = False

#         df.loc[
#             mask,
#             "errors"
#         ] = (
#             df.loc[
#                 mask,
#                 "errors"
#             ]
#             .apply(
#                 lambda x:
#                 f"{x}; {message}"
#                 if x
#                 else message
#             )
#         )


#     # ==================================================
#     # 16. Validasi field wajib
#     # ==================================================

#     required_data = [
#         "member_id",
#         "full_name",
#         "gender",
#         "dkm_group",
#         "mandatory_savings",
#         "submitted_at",
#         "member_status"
#     ]


#     for column in required_data:

#         mask = (
#             df[column].isna()
#             | df[column].astype(str).str.strip().eq("")
#         )

#         add_error(
#             mask,
#             f"{column} kosong"
#         )


#     # ==================================================
#     # 17. Validasi gender
#     # ==================================================

#     invalid_gender = (
#         ~df["gender"].isin({
#             "Pria",
#             "Wanita"
#         })
#     )


#     add_error(
#         invalid_gender,
#         "Jenis kelamin tidak valid"
#     )


#     # ==================================================
#     # 18. Validasi DKM
#     # ==================================================

#     invalid_dkm = (
#         ~df["dkm_group"].isin(valid_dkm)
#     )


#     add_error(
#         invalid_dkm,
#         "Kelompok DKM tidak valid"
#     )


#     # ==================================================
#     # 19. Validasi Simpanan Wajib
#     # ==================================================

#     invalid_savings = (
#         ~df["mandatory_savings"].isin(
#             valid_savings
#         )
#     )


#     add_error(
#         invalid_savings,
#         "Simpanan wajib tidak valid"
#     )


#     # ==================================================
#     # 20. Validasi Status
#     # ==================================================

#     valid_statuses = {
#         MemberStatus.ACTIVE.value,
#         MemberStatus.INACTIVE.value,
#         MemberStatus.RESIGNED.value
#     }


#     invalid_status = (
#         ~df["member_status"].isin(
#             valid_statuses
#         )
#     )


#     add_error(
#         invalid_status,
#         "Status anggota tidak valid"
#     )


#     # ==================================================
#     # 21. Validasi tanggal lahir
#     # ==================================================

#     invalid_birth_date = (
#         df["birth_date"].isna()
#     )


#     add_error(
#         invalid_birth_date,
#         "Tanggal lahir tidak valid"
#     )


#     # ==================================================
#     # 22. Validasi tanggal masuk
#     # ==================================================

#     invalid_submitted_at = (
#         df["submitted_at"].isna()
#     )


#     add_error(
#         invalid_submitted_at,
#         "Tanggal masuk koperasi tidak valid"
#     )


#     # ==================================================
#     # 23. Duplicate member_id dalam Excel
#     # ==================================================

#     duplicate_member_id = (
#         df["member_id"].ne("")
#         & df["member_id"].duplicated(
#             keep=False
#         )
#     )


#     add_error(
#         duplicate_member_id,
#         "Nomor anggota duplikat dalam Excel"
#     )


#     # ==================================================
#     # 24. Duplicate identity_number dalam Excel
#     # ==================================================

#     duplicate_identity = (
#         df["identity_number"].ne("")
#         & df["identity_number"].duplicated(
#             keep=False
#         )
#     )


#     add_error(
#         duplicate_identity,
#         "Nomor KTP duplikat dalam Excel"
#     )

#     # ==================================================
#     # Cek duplicate dengan database
#     # ==================================================

#     member_ids = (
#         df["member_id"]
#         .dropna()
#         .astype(str)
#         .str.strip()
#     )

#     identity_numbers = (
#         df["identity_number"]
#         .dropna()
#         .astype(str)
#         .str.strip()
#     )


#     # Ambil member_id yang sudah ada
#     existing_member_ids = {
#         member_id
#         for member_id, in db.query(
#             Member.member_id
#         )
#         .filter(
#             Member.member_id.in_(
#                 member_ids.tolist()
#             )
#         )
#         .all()
#     }


#     # Ambil nomor KTP yang sudah ada
#     existing_identity_numbers = {
#         identity_number
#         for identity_number, in db.query(
#             Member.identity_number
#         )
#         .filter(
#             Member.identity_number.in_(
#                 identity_numbers.tolist()
#             )
#         )
#         .all()
#     }


#     # ==================================================
#     # Tandai member_id yang sudah ada
#     # ==================================================

#     duplicate_member_database = (
#         df["member_id"].isin(
#             existing_member_ids
#         )
#     )


#     add_error(
#         duplicate_member_database,
#         "Nomor anggota sudah ada di database"
#     )


#     # ==================================================
#     # Tandai KTP yang sudah ada
#     # ==================================================

#     duplicate_identity_database = (
#         df["identity_number"].isin(
#             existing_identity_numbers
#         )
#     )


#     add_error(
#         duplicate_identity_database,
#         "Nomor KTP sudah ada di database"
#     )

#     # ==================================================
#     # Status import
#     # ==================================================

#     df["import_status"] = "BARU"


#     # Jika member_id sudah ada di database
#     df.loc[
#         duplicate_member_database,
#         "import_status"
#     ] = "DUPLIKAT"


#     # Jika nomor KTP sudah ada di database
#     df.loc[
#         duplicate_identity_database,
#         "import_status"
#     ] = "DUPLIKAT"

#     # ==================================================
#     # 25. Format tanggal untuk JSON
#     # ==================================================

#     for column in [
#         "birth_date",
#         "submitted_at",
#         "approved_at",
#         "left_at"
#     ]:

#         df[column] = (
#             df[column]
#             .dt.strftime("%Y-%m-%d")
#             .fillna("")
#         )

#     # ==================================================
#     # Statistik
#     # ==================================================

#     total_data = len(df)


#     valid_data = int(
#         df["is_valid"].sum()
#     )


#     invalid_data = (
#         total_data - valid_data
#     )


#     new_data = int(
#         (
#             df["import_status"] == "BARU"
#         ).sum()
#     )


#     duplicate_data = int(
#         (
#             df["import_status"] == "DUPLIKAT"
#         ).sum()
#     )


#     # ==================================================
#     # 27. Preview
#     # ==================================================

#     preview_columns = [
#         "member_id",
#         "full_name",
#         "birth_place",
#         "birth_date",
#         "gender",
#         "address",
#         "family_card_number",
#         "identity_number",
#         "phone_number",
#         "job",
#         "spouse_name",
#         "dkm_group",
#         "mandatory_savings",
#         "submitted_at",
#         "approved_at",
#         "member_status",
#         "left_at",
#         "status_note",
#         "is_valid",
#         "errors"
#     ]


#     preview = (
#         df[
#             preview_columns
#         ]
#         .head(5)
#         .fillna("")
#         .to_dict(
#             orient="records"
#         )
#     )


#     # ==================================================
#     # Response
#     # ==================================================

#     return {

#         "message":
#             "File berhasil diupload dan divalidasi",

#         "filename":
#             file.filename,

#         "total_data":
#             total_data,

#         "valid_data":
#             valid_data,

#         "invalid_data":
#             invalid_data,

#         "new_data":
#             new_data,

#         "duplicate_data":
#             duplicate_data,

#         "preview":
#             preview
#     }

# from fastapi import (
#     APIRouter,
#     UploadFile,
#     File,
#     Depends,
#     HTTPException
# )

# from sqlalchemy.orm import Session

# import pandas as pd

# from io import BytesIO

# from app.database import get_db

# from app.models.member import (
#     Member,
#     KelompokDKM,
#     SetoranWajib,
#     MemberStatus
# )

# @router.post("/import/confirm")
# async def confirm_import(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):

#     # ==================================================
#     # 1. VALIDASI FILE
#     # ==================================================

#     if not file.filename.lower().endswith((".xlsx", ".xls")):

#         raise HTTPException(
#             status_code=400,
#             detail="File harus berupa Excel (.xlsx atau .xls)"
#         )


#     content = await file.read()


#     # ==================================================
#     # 2. BACA EXCEL
#     # ==================================================

#     try:

#         df = pd.read_excel(
#             BytesIO(content),
#             header=1
#         )

#     except Exception as e:

#         raise HTTPException(
#             status_code=400,
#             detail=f"File Excel tidak dapat dibaca: {str(e)}"
#         )


#     # ==================================================
#     # 3. BERSIHKAN DATA
#     # ==================================================

#     df = df.dropna(how="all")


#     df.columns = (
#         df.columns
#         .astype(str)
#         .str.strip()
#     )


#     if "NOMOR ANGGOTA" not in df.columns:

#         raise HTTPException(
#             status_code=400,
#             detail="Kolom NOMOR ANGGOTA tidak ditemukan"
#         )


#     # Hanya baris yang mempunyai nomor anggota
#     df = df[
#         df["NOMOR ANGGOTA"].notna()
#     ]


#     # ==================================================
#     # 4. MAPPING KOLOM EXCEL
#     # ==================================================

#     column_mapping = {

#         "NOMOR ANGGOTA":
#             "member_id",

#         "NAMA":
#             "full_name",

#         "TEMPAT LAHIR":
#             "birth_place",

#         "TANGGAL LAHIR":
#             "birth_date",

#         "JENIS KELAMIN":
#             "gender",

#         "ALAMAT":
#             "address",

#         "NOMOR KARTU KELUARGA":
#             "family_card_number",

#         "NOMOR KTP":
#             "identity_number",

#         "NO TLP / HP":
#             "phone_number",

#         "PEKERJAAN":
#             "job",

#         "NAMA SUAMI / ISTRI":
#             "spouse_name",

#         "KELOMPOK DKM":
#             "dkm_group",

#         "SIMPANAN WAJIB":
#             "mandatory_savings",

#         "TANGGAL MASUK KOPERASI":
#             "submitted_at",

#         "AKTIF / KELUAR":
#             "member_status",

#         "TANGGAL KELUAR":
#             "left_at",

#         "KETERANGAN":
#             "status_note"
#     }


#     # ==================================================
#     # 5. CEK KOLOM
#     # ==================================================

#     missing_columns = [

#         column

#         for column in column_mapping

#         if column not in df.columns
#     ]


#     if missing_columns:

#         raise HTTPException(

#             status_code=400,

#             detail={
#                 "message":
#                     "Kolom Excel tidak lengkap",

#                 "missing_columns":
#                     missing_columns
#             }
#         )


#     # ==================================================
#     # 6. AMBIL KOLOM YANG DIPERLUKAN
#     # ==================================================

#     df = df[
#         list(column_mapping.keys())
#     ].copy()


#     # ==================================================
#     # 7. RENAME KOLOM
#     # ==================================================

#     df.rename(

#         columns=column_mapping,

#         inplace=True
#     )


#     # ==================================================
#     # 8. CLEANING
#     # ==================================================

#     for column in df.columns:

#         df[column] = (
#             df[column]
#             .fillna("")
#         )


#         if df[column].dtype == "object":

#             df[column] = (
#                 df[column]
#                 .astype(str)
#                 .str.strip()
#             )


#             df[column] = (
#                 df[column]
#                 .replace(
#                     [
#                         "nan",
#                         "NaN",
#                         "NAN"
#                     ],
#                     ""
#                 )
#             )


#     # ==================================================
#     # 9. GENDER
#     # ==================================================

#     gender_mapping = {

#         "L":
#             "Pria",

#         "LAKI-LAKI":
#             "Pria",

#         "LAKI LAKI":
#             "Pria",

#         "PRIA":
#             "Pria",

#         "P":
#             "Wanita",

#         "PEREMPUAN":
#             "Wanita",

#         "WANITA":
#             "Wanita"
#     }


#     df["gender"] = (

#         df["gender"]
#         .str.upper()
#         .map(gender_mapping)

#     )


#     # ==================================================
#     # 10. DKM
#     # ==================================================

#     dkm_mapping = {

#         "DKM DARUSSALAM - GUNUNG GEDE":
#             KelompokDKM.DARUSSALAM,

#         "DKM AL BAROKAH - PONDOK RUMPUT":
#             KelompokDKM.AL_BAROKAH,

#         "DKM DARUL HIKMAH - GREEN AROFAH":
#             KelompokDKM.DARUL_HIKMAH,

#         "DKM AR-RAUDHOH - PAKUAN":
#             KelompokDKM.AR_RAUDHOH,

#         "DKM BAITUL IZZA - TAJUR":
#             KelompokDKM.BAITUL_IZZA,

#         "DKM AN-NASHR - CIKARET":
#             KelompokDKM.AN_NASHR,

#         "DKM AR-ROHMAN - CIAPUS":
#             KelompokDKM.AR_ROHMAN
#     }


#     df["dkm_group"] = (

#         df["dkm_group"]
#         .str.upper()
#         .map(dkm_mapping)

#     )


#     # ==================================================
#     # 11. SIMPANAN WAJIB
#     # ==================================================

#     def normalize_savings(value):

#         if value == "":
#             return None


#         try:

#             return SetoranWajib(
#                 int(float(value))
#             )


#         except (
#             ValueError,
#             TypeError
#         ):

#             mapping = {

#                 "25K":
#                     SetoranWajib.LEVEL_25K,

#                 "50K":
#                     SetoranWajib.LEVEL_50K,

#                 "100K":
#                     SetoranWajib.LEVEL_100K,

#                 "250K":
#                     SetoranWajib.LEVEL_250K,

#                 "500K":
#                     SetoranWajib.LEVEL_500K
#             }


#             return mapping.get(

#                 str(value)
#                 .upper()
#                 .strip()

#             )


#     df["mandatory_savings"] = (

#         df["mandatory_savings"]
#         .apply(normalize_savings)

#     )


#     # ==================================================
#     # 12. MEMBER STATUS
#     #
#     # HANYA MENGGUNAKAN
#     # KOLOM AKTIF / KELUAR
#     # ==================================================

#     status_mapping = {

#         "AKTIF":
#             MemberStatus.ACTIVE,

#         "TIDAK AKTIF":
#             MemberStatus.INACTIVE,

#         "KELUAR":
#             MemberStatus.RESIGNED
#     }


#     df["member_status"] = (

#         df["member_status"]
#         .str.upper()
#         .map(status_mapping)

#     )


#     # ==================================================
#     # 13. TANGGAL
#     # ==================================================

#     date_columns = [

#         "birth_date",

#         "submitted_at",

#         "left_at"
#     ]


#     for column in date_columns:

#         df[column] = pd.to_datetime(

#             df[column],

#             errors="coerce",

#             dayfirst=True

#         )


#     # ==================================================
#     # 14. APPROVED AT
#     #
#     # Tanggal masuk koperasi
#     # digunakan untuk:
#     #
#     # submitted_at
#     # approved_at
#     # ==================================================

#     df["approved_at"] = (
#         df["submitted_at"]
#     )


#     # ==================================================
#     # 15. AMBIL MEMBER ID DARI DATABASE
#     # ==================================================

#     member_ids = (

#         df["member_id"]
#         .astype(str)
#         .str.strip()
#         .tolist()

#     )


#     identity_numbers = (

#         df["identity_number"]
#         .astype(str)
#         .str.strip()
#         .tolist()

#     )


#     # Jangan masukkan string kosong
#     identity_numbers = [

#         value

#         for value in identity_numbers

#         if value
#     ]


#     # ==================================================
#     # 16. MEMBER ID YANG SUDAH ADA
#     # ==================================================

#     existing_member_ids = {

#         value

#         for value, in (

#             db.query(
#                 Member.member_id
#             )

#             .filter(
#                 Member.member_id.in_(
#                     member_ids
#                 )
#             )

#             .all()

#         )

#     }


#     # ==================================================
#     # 17. NOMOR KTP YANG SUDAH ADA
#     # ==================================================

#     existing_identity_numbers = {

#         value

#         for value, in (

#             db.query(
#                 Member.identity_number
#             )

#             .filter(
#                 Member.identity_number.in_(
#                     identity_numbers
#                 )
#             )

#             .all()

#         )

#     }


#     # ==================================================
#     # 18. IMPORT
#     # ==================================================

#     imported = 0

#     skipped = 0


#     # Untuk mencegah duplicate
#     # antar baris Excel
#     processed_member_ids = set()

#     processed_identity_numbers = set()


#     for _, row in df.iterrows():

#         member_id = row["member_id"]


#         identity_number = (
#             row["identity_number"]
#         )


#         # ==============================================
#         # MEMBER ID KOSONG
#         # ==============================================

#         if not member_id:

#             skipped += 1

#             continue


#         # ==============================================
#         # DUPLICATE MEMBER ID DATABASE
#         # ==============================================

#         if member_id in existing_member_ids:

#             skipped += 1

#             continue


#         # ==============================================
#         # DUPLICATE MEMBER ID EXCEL
#         # ==============================================

#         if member_id in processed_member_ids:

#             skipped += 1

#             continue


#         # ==============================================
#         # DUPLICATE KTP DATABASE
#         # ==============================================

#         if (

#             identity_number

#             and identity_number
#             in existing_identity_numbers

#         ):

#             skipped += 1

#             continue


#         # ==============================================
#         # DUPLICATE KTP EXCEL
#         # ==============================================

#         if (

#             identity_number

#             and identity_number
#             in processed_identity_numbers

#         ):

#             skipped += 1

#             continue


#         # ==============================================
#         # DATA WAJIB
#         # ==============================================

#         if not row["full_name"]:

#             skipped += 1

#             continue


#         if pd.isna(
#             row["birth_date"]
#         ):

#             skipped += 1

#             continue


#         if not row["gender"]:

#             skipped += 1

#             continue


#         if not row["dkm_group"]:

#             skipped += 1

#             continue


#         if not row["mandatory_savings"]:

#             skipped += 1

#             continue


#         if pd.isna(
#             row["submitted_at"]
#         ):

#             skipped += 1

#             continue


#         if not row["member_status"]:

#             skipped += 1

#             continue


#         # ==============================================
#         # BUAT MEMBER
#         # ==============================================

#         member = Member(

#             member_id=
#                 member_id,

#             full_name=
#                 row["full_name"],

#             birth_place=
#                 row["birth_place"],

#             birth_date=
#                 row["birth_date"],

#             gender=
#                 row["gender"],

#             address=
#                 row["address"],

#             family_card_number=
#                 row["family_card_number"],

#             identity_number=
#                 identity_number
#                 or None,

#             phone_number=
#                 row["phone_number"],

#             job=
#                 row["job"],

#             spouse_name=
#                 row["spouse_name"],

#             dkm_group=
#                 row["dkm_group"],

#             mandatory_savings=
#                 row["mandatory_savings"],

#             submitted_at=
#                 row["submitted_at"],

#             approved_at=
#                 row["approved_at"],

#             member_status=
#                 row["member_status"],

#             left_at=(

#                 row["left_at"]

#                 if not pd.isna(
#                     row["left_at"]
#                 )

#                 else None

#             ),

#             status_note=
#                 row["status_note"]
#         )


#         db.add(member)


#         # Tandai sudah diproses
#         processed_member_ids.add(
#             member_id
#         )


#         if identity_number:

#             processed_identity_numbers.add(
#                 identity_number
#             )


#         imported += 1


#     # ==================================================
#     # 19. COMMIT
#     # ==================================================

#     try:

#         db.commit()

#     except Exception as e:

#         db.rollback()

#         raise HTTPException(

#             status_code=400,

#             detail=f"Import gagal: {str(e)}"

#         )


#     # ==================================================
#     # 20. RESPONSE
#     # ==================================================

#     return {

#         "message":
#             "Import data anggota berhasil",

#         "total_data":
#             len(df),

#         "imported":
#             imported,

#         "skipped":
#             skipped
#     }