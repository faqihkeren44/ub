# from fastapi import APIRouter, Depends, Cookie, Request, HTTPException, Form, UploadFile, File
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

# from app.models.member import (
#     Member,
#     KelompokDKM,
#     SetoranWajib,
#     MemberStatus,
# )


# # ==========================================================
# # KONFIGURASI IMPORT
# # ==========================================================

# IMPORT_COLUMN_MAPPING = {
#     "NOMOR ANGGOTA": "member_id",
#     "NAMA": "full_name",
#     "TEMPAT LAHIR": "birth_place",
#     "TANGGAL LAHIR": "birth_date",
#     "JENIS KELAMIN": "gender",
#     "ALAMAT": "address",
#     "NOMOR KARTU KELUARGA": "family_card_number",
#     "NOMOR KTP": "identity_number",
#     "NO TLP / HP": "phone_number",
#     "PEKERJAAN": "job",
#     "NAMA SUAMI / ISTRI": "spouse_name",
#     "KELOMPOK DKM": "dkm_group",
#     "SIMPANAN WAJIB": "mandatory_savings",
#     "TANGGAL MASUK KOPERASI": "submitted_at",
#     "AKTIF / KELUAR": "member_status",
#     "TANGGAL KELUAR": "left_at",
#     "KETERANGAN": "status_note",
# }

# IMPORT_PREVIEW_COLUMNS = [
#     "member_id",
#     "full_name",
#     "birth_place",
#     "birth_date",
#     "gender",
#     "address",
#     "family_card_number",
#     "identity_number",
#     "phone_number",
#     "job",
#     "spouse_name",
#     "dkm_group",
#     "mandatory_savings",
#     "submitted_at",
#     "approved_at",
#     "member_status",
#     "left_at",
#     "status_note",
#     "import_status",
#     "errors",
# ]

# GENDER_MAPPING = {
#     "L": "Pria",
#     "LAKI-LAKI": "Pria",
#     "LAKI LAKI": "Pria",
#     "PRIA": "Pria",
#     "P": "Wanita",
#     "PEREMPUAN": "Wanita",
#     "WANITA": "Wanita",
# }

# STATUS_MAPPING = {
#     "AKTIF": MemberStatus.ACTIVE,
#     "TIDAK AKTIF": MemberStatus.INACTIVE,
#     "KELUAR": MemberStatus.RESIGNED,
# }

# DKM_MAPPING = {
#     item.value.strip().upper(): item
#     for item in KelompokDKM
# }

# SAVINGS_MAPPING = {
#     "25K": SetoranWajib.LEVEL_25K,
#     "50K": SetoranWajib.LEVEL_50K,
#     "100K": SetoranWajib.LEVEL_100K,
#     "250K": SetoranWajib.LEVEL_250K,
#     "500K": SetoranWajib.LEVEL_500K,
# }


# # ==========================================================
# # HELPER
# # ==========================================================

# def _clean_text(value):
#     """Mengubah nilai kosong/NaN menjadi string kosong."""
#     if pd.isna(value):
#         return ""

#     return str(value).strip()


# def _add_import_error(df, mask, message):
#     """Menambahkan pesan error tanpa menghapus error sebelumnya."""
#     if not mask.any():
#         return

#     df.loc[mask, "is_valid"] = False

#     df.loc[mask, "errors"] = df.loc[mask, "errors"].apply(
#         lambda current:
#             f"{current}; {message}"
#             if current
#             else message
#     )


# def _parse_optional_date(df, column, label):
#     """
#     Field tanggal boleh kosong.
#     Tetapi jika diisi dan tidak bisa diparse, baris menjadi invalid.
#     """
#     raw = df[column].copy()
#     non_empty = raw.notna() & raw.astype(str).str.strip().ne("")

#     parsed = pd.to_datetime(
#         raw,
#         errors="coerce",
#         dayfirst=True,
#     )

#     invalid = non_empty & parsed.isna()

#     df[column] = parsed

#     _add_import_error(
#         df,
#         invalid,
#         f"{label} tidak valid"
#     )


# def _normalize_savings(value):
#     """
#     Simpanan wajib boleh kosong.
#     Jika diisi, harus bisa dikenali sebagai enum SetoranWajib.
#     """
#     if value == "":
#         return None

#     # Nilai dari Excel sering terbaca sebagai angka.
#     try:
#         numeric_value = int(float(value))

#         try:
#             return SetoranWajib(numeric_value)
#         except ValueError:
#             pass

#     except (ValueError, TypeError):
#         pass

#     normalized = str(value).upper().strip()

#     return SAVINGS_MAPPING.get(normalized)


# def _prepare_import_dataframe(content, db):
#     """
#     Satu-satunya fungsi yang melakukan:
#     Excel -> cleaning -> normalisasi -> validasi -> duplicate -> statistik.

#     Endpoint preview dan confirm sama-sama menggunakan fungsi ini.
#     """

#     # ------------------------------------------------------
#     # 1. Baca Excel
#     # ------------------------------------------------------

#     try:
#         df = pd.read_excel(
#             BytesIO(content),
#             header=1,
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=400,
#             detail=f"File Excel tidak dapat dibaca: {str(e)}"
#         )

#     # Buang baris yang benar-benar kosong.
#     df = df.dropna(how="all").copy()

#     if df.empty:
#         raise HTTPException(
#             status_code=400,
#             detail="File Excel tidak memiliki data."
#         )

#     # ------------------------------------------------------
#     # 2. Bersihkan nama kolom
#     # ------------------------------------------------------

#     df.columns = (
#         df.columns
#         .astype(str)
#         .str.strip()
#     )

#     missing_columns = [
#         column
#         for column in IMPORT_COLUMN_MAPPING
#         if column not in df.columns
#     ]

#     if missing_columns:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "message": "Kolom Excel tidak lengkap.",
#                 "missing_columns": missing_columns,
#             }
#         )

#     # Hanya ambil kolom yang memang dipakai aplikasi.
#     df = df[
#         list(IMPORT_COLUMN_MAPPING.keys())
#     ].copy()

#     df.rename(
#         columns=IMPORT_COLUMN_MAPPING,
#         inplace=True,
#     )

#     # ------------------------------------------------------
#     # 3. Cleaning
#     # ------------------------------------------------------

#     for column in df.columns:
#         if df[column].dtype == "object":
#             df[column] = (
#                 df[column]
#                 .fillna("")
#                 .astype(str)
#                 .str.strip()
#                 .replace({
#                     "nan": "",
#                     "NaN": "",
#                     "NAN": "",
#                 })
#             )

#     # ------------------------------------------------------
#     # 4. Validasi dasar
#     #
#     # HANYA NAMA YANG WAJIB.
#     #
#     # Field lain boleh kosong.
#     # Kalau diisi, harus valid.
#     # ------------------------------------------------------

#     df["is_valid"] = True
#     df["errors"] = ""

#     empty_name = (
#         df["full_name"].isna()
#         | df["full_name"].astype(str).str.strip().eq("")
#     )

#     _add_import_error(
#         df,
#         empty_name,
#         "Nama kosong"
#     )

#     # ------------------------------------------------------
#     # 5. Gender
#     # ------------------------------------------------------

#     raw_gender = df["gender"].astype(str).str.strip()
#     non_empty_gender = raw_gender.ne("")

#     df["gender"] = (
#         raw_gender
#         .str.upper()
#         .map(GENDER_MAPPING)
#     )

#     invalid_gender = (
#         non_empty_gender
#         & df["gender"].isna()
#     )

#     _add_import_error(
#         df,
#         invalid_gender,
#         "Jenis kelamin tidak valid"
#     )

#     # ------------------------------------------------------
#     # 6. Kelompok DKM
#     # ------------------------------------------------------

#     raw_dkm = df["dkm_group"].astype(str).str.strip()
#     non_empty_dkm = raw_dkm.ne("")

#     df["dkm_group"] = (
#         raw_dkm
#         .str.upper()
#         .map(DKM_MAPPING)
#     )

#     invalid_dkm = (
#         non_empty_dkm
#         & df["dkm_group"].isna()
#     )

#     _add_import_error(
#         df,
#         invalid_dkm,
#         "Kelompok DKM tidak valid"
#     )

#     # ------------------------------------------------------
#     # 7. Simpanan wajib
#     # ------------------------------------------------------

#     raw_savings = df["mandatory_savings"].copy()

#     df["mandatory_savings"] = (
#         raw_savings.apply(_normalize_savings)
#     )

#     invalid_savings = (
#         raw_savings.astype(str).str.strip().ne("")
#         & df["mandatory_savings"].isna()
#     )

#     _add_import_error(
#         df,
#         invalid_savings,
#         "Simpanan wajib tidak valid"
#     )

#     # ------------------------------------------------------
#     # 8. Status anggota
#     # ------------------------------------------------------

#     raw_status = df["member_status"].astype(str).str.strip()
#     non_empty_status = raw_status.ne("")

#     df["member_status"] = (
#         raw_status
#         .str.upper()
#         .map(STATUS_MAPPING)
#     )

#     invalid_status = (
#         non_empty_status
#         & df["member_status"].isna()
#     )

#     _add_import_error(
#         df,
#         invalid_status,
#         "Status anggota tidak valid"
#     )

#     # ------------------------------------------------------
#     # 9. Tanggal
#     # ------------------------------------------------------

#     _parse_optional_date(
#         df,
#         "birth_date",
#         "Tanggal lahir"
#     )

#     _parse_optional_date(
#         df,
#         "submitted_at",
#         "Tanggal masuk koperasi"
#     )

#     _parse_optional_date(
#         df,
#         "left_at",
#         "Tanggal keluar"
#     )

#     # Tanggal approved mengikuti tanggal masuk koperasi.
#     df["approved_at"] = df["submitted_at"]

#     # ------------------------------------------------------
#     # 10. Normalisasi member_id dan KTP
#     # ------------------------------------------------------

#     for column in [
#         "member_id",
#         "identity_number",
#     ]:
#         df[column] = (
#             df[column]
#             .fillna("")
#             .astype(str)
#             .str.strip()
#             .replace({
#                 "nan": "",
#                 "NaN": "",
#                 "NAN": "",
#             })
#         )

#     # ------------------------------------------------------
#     # 11. Duplicate dalam Excel
#     # ------------------------------------------------------

#     duplicate_member_excel = (
#         df["member_id"].ne("")
#         & df["member_id"].duplicated(keep=False)
#     )

#     _add_import_error(
#         df,
#         duplicate_member_excel,
#         "Nomor anggota duplikat dalam Excel"
#     )

#     duplicate_identity_excel = (
#         df["identity_number"].ne("")
#         & df["identity_number"].duplicated(keep=False)
#     )

#     _add_import_error(
#         df,
#         duplicate_identity_excel,
#         "Nomor KTP duplikat dalam Excel"
#     )

#     # ------------------------------------------------------
#     # 12. Duplicate dengan database
#     # ------------------------------------------------------

#     member_ids = (
#         df.loc[
#             df["member_id"].ne(""),
#             "member_id"
#         ]
#         .unique()
#         .tolist()
#     )

#     identity_numbers = (
#         df.loc[
#             df["identity_number"].ne(""),
#             "identity_number"
#         ]
#         .unique()
#         .tolist()
#     )

#     existing_member_ids = set()

#     if member_ids:
#         existing_member_ids = {
#             value
#             for value, in (
#                 db.query(Member.member_id)
#                 .filter(Member.member_id.in_(member_ids))
#                 .all()
#             )
#             if value
#         }

#     existing_identity_numbers = set()

#     if identity_numbers:
#         existing_identity_numbers = {
#             value
#             for value, in (
#                 db.query(Member.identity_number)
#                 .filter(
#                     Member.identity_number.in_(identity_numbers)
#                 )
#                 .all()
#             )
#             if value
#         }

#     duplicate_member_database = (
#         df["member_id"].isin(existing_member_ids)
#     )

#     _add_import_error(
#         df,
#         duplicate_member_database,
#         "Nomor anggota sudah ada di database"
#     )

#     duplicate_identity_database = (
#         df["identity_number"].isin(
#             existing_identity_numbers
#         )
#     )

#     _add_import_error(
#         df,
#         duplicate_identity_database,
#         "Nomor KTP sudah ada di database"
#     )

#     # ------------------------------------------------------
#     # 13. Status import
#     # ------------------------------------------------------

#     df["import_status"] = "BARU"

#     # Invalid selalu tidak boleh diimport.
#     df.loc[
#         ~df["is_valid"],
#         "import_status"
#     ] = "INVALID"

#     # Duplicate diberi status DUPLIKAT.
#     duplicate_mask = (
#         duplicate_member_excel
#         | duplicate_identity_excel
#         | duplicate_member_database
#         | duplicate_identity_database
#     )

#     df.loc[
#         duplicate_mask,
#         "import_status"
#     ] = "DUPLIKAT"

#     # ------------------------------------------------------
#     # 14. Statistik
#     # ------------------------------------------------------

#     total_data = len(df)

#     invalid_data = int(
#         (~df["is_valid"]).sum()
#     )

#     duplicate_data = int(
#         (df["import_status"] == "DUPLIKAT").sum()
#     )

#     new_data = int(
#         (
#             (df["is_valid"])
#             & (df["import_status"] == "BARU")
#         ).sum()
#     )

#     # Data valid berarti valid dan tidak duplicate.
#     valid_data = new_data

#     # ------------------------------------------------------
#     # 15. Siapkan preview
#     # ------------------------------------------------------

#     preview_df = df[IMPORT_PREVIEW_COLUMNS].copy()

#     # Enum -> value untuk JSON.
#     for column in [
#         "dkm_group",
#         "mandatory_savings",
#         "member_status",
#     ]:
#         preview_df[column] = preview_df[column].apply(
#             lambda value:
#                 value.value
#                 if hasattr(value, "value")
#                 else (
#                     "" if pd.isna(value)
#                     else value
#                 )
#         )

#     # Timestamp/date -> string.
#     for column in [
#         "birth_date",
#         "submitted_at",
#         "approved_at",
#         "left_at",
#     ]:
#         preview_df[column] = preview_df[column].apply(
#             lambda value:
#                 value.strftime("%Y-%m-%d")
#                 if pd.notna(value)
#                 else ""
#         )

#     # NaN/NA -> string kosong.
#     preview_df = preview_df.fillna("")

#     preview = preview_df.head(20).to_dict(
#         orient="records"
#     )

#     return {
#         "df": df,
#         "total_data": total_data,
#         "valid_data": valid_data,
#         "invalid_data": invalid_data,
#         "new_data": new_data,
#         "duplicate_data": duplicate_data,
#         "preview": preview,
#     }


# def _optional_value(value):
#     """Mengubah NaN/NaT menjadi None untuk SQLAlchemy."""
#     if value is None or pd.isna(value):
#         return None
#     return value


# # ==========================================================
# # HALAMAN IMPORT
# # ==========================================================

# @router.get("/import", response_class=HTMLResponse)
# async def import_members_page(
#     request: Request,
#     admin: models.Admin = Depends(verify_admin),
# ):
#     return templates.TemplateResponse(
#         request=request,
#         name="admin/member_import.html",
#         context={
#             "admin": admin,
#         }
#     )


# # ==========================================================
# # PREVIEW + VALIDASI
# # ==========================================================

# @router.post("/import")
# async def import_members(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
# ):
#     if not file.filename:
#         raise HTTPException(
#             status_code=400,
#             detail="File belum dipilih."
#         )

#     if not file.filename.lower().endswith(
#         (".xlsx", ".xls")
#     ):
#         raise HTTPException(
#             status_code=400,
#             detail="File harus berupa Excel (.xlsx atau .xls)."
#         )

#     content = await file.read()

#     if not content:
#         raise HTTPException(
#             status_code=400,
#             detail="File kosong."
#         )

#     result = _prepare_import_dataframe(
#         content,
#         db
#     )

#     return {
#         "message": "File berhasil dibaca dan divalidasi.",
#         "filename": file.filename,
#         "total_data": result["total_data"],
#         "valid_data": result["valid_data"],
#         "invalid_data": result["invalid_data"],
#         "new_data": result["new_data"],
#         "duplicate_data": result["duplicate_data"],
#         "preview": result["preview"],
#     }


# # ==========================================================
# # CONFIRM IMPORT KE POSTGRESQL
# # ==========================================================

# @router.post("/import/confirm")
# async def confirm_import(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
# ):
#     if not file.filename:
#         raise HTTPException(
#             status_code=400,
#             detail="File belum dipilih."
#         )

#     if not file.filename.lower().endswith(
#         (".xlsx", ".xls")
#     ):
#         raise HTTPException(
#             status_code=400,
#             detail="File harus berupa Excel (.xlsx atau .xls)."
#         )

#     content = await file.read()

#     if not content:
#         raise HTTPException(
#             status_code=400,
#             detail="File kosong."
#         )

#     # Gunakan validator yang SAMA dengan preview.
#     result = _prepare_import_dataframe(
#         content,
#         db
#     )

#     df = result["df"]

#     # Hanya BARU yang valid yang boleh masuk.
#     rows_to_import = df[
#         (df["is_valid"])
#         & (df["import_status"] == "BARU")
#     ]

#     imported = 0

#     try:
#         for _, row in rows_to_import.iterrows():

#             member = Member(
#                 # Boleh kosong jika kolom database nullable.
#                 member_id=(
#                     row["member_id"]
#                     if row["member_id"]
#                     else None
#                 ),

#                 full_name=row["full_name"],

#                 birth_place=(
#                     row["birth_place"]
#                     if row["birth_place"]
#                     else None
#                 ),

#                 birth_date=_optional_value(
#                     row["birth_date"]
#                 ),

#                 gender=(
#                     row["gender"]
#                     if not pd.isna(row["gender"])
#                     else None
#                 ),

#                 address=(
#                     row["address"]
#                     if row["address"]
#                     else None
#                 ),

#                 family_card_number=(
#                     row["family_card_number"]
#                     if row["family_card_number"]
#                     else None
#                 ),

#                 identity_number=(
#                     row["identity_number"]
#                     if row["identity_number"]
#                     else None
#                 ),

#                 phone_number=(
#                     row["phone_number"]
#                     if row["phone_number"]
#                     else None
#                 ),

#                 job=(
#                     row["job"]
#                     if row["job"]
#                     else None
#                 ),

#                 spouse_name=(
#                     row["spouse_name"]
#                     if row["spouse_name"]
#                     else None
#                 ),

#                 dkm_group=(
#                     row["dkm_group"]
#                     if not pd.isna(row["dkm_group"])
#                     else None
#                 ),

#                 mandatory_savings=(
#                     row["mandatory_savings"]
#                     if not pd.isna(row["mandatory_savings"])
#                     else None
#                 ),

#                 submitted_at=_optional_value(
#                     row["submitted_at"]
#                 ),

#                 approved_at=_optional_value(
#                     row["approved_at"]
#                 ),

#                 member_status=(
#                     row["member_status"]
#                     if not pd.isna(row["member_status"])
#                     else None
#                 ),

#                 left_at=_optional_value(
#                     row["left_at"]
#                 ),

#                 status_note=(
#                     row["status_note"]
#                     if row["status_note"]
#                     else None
#                 ),
#             )

#             db.add(member)
#             imported += 1

#         db.commit()

#     except Exception as e:
#         db.rollback()

#         raise HTTPException(
#             status_code=400,
#             detail=f"Import gagal dan tidak ada data yang disimpan: {str(e)}"
#         )

#     return {
#         "message": "Import data anggota berhasil.",
#         "total_data": result["total_data"],
#         "valid_data": result["valid_data"],
#         "invalid_data": result["invalid_data"],
#         "duplicate_data": result["duplicate_data"],
#         "imported": imported,
#         "skipped": result["total_data"] - imported,
#     }
