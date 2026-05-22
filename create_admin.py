from app.database import SessionLocal
from app import models
from app.core import security

# Gunakan huruf kapital untuk menandakan ini adalah Konstanta/Konfigurasi
ADMIN_ID = "admin_ub_001"
ADMIN_PWD = "admin123"

def create_initial_admin():
    db = SessionLocal()
    try:
        existing_admin = db.query(models.Admin).filter(models.Admin.admin_id == ADMIN_ID).first()
        
        if existing_admin:
            print(f"INFO: Admin {ADMIN_ID} sudah ada di database")
            return

        hashed_pw = security.hash_password(ADMIN_PWD)
        new_admin = models.Admin(
            admin_id=ADMIN_ID,
            full_name="Administrator Utama",
            hashed_password=hashed_pw,
            role="superadmin"
        )
        
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        print(f"SUKSES: Admin {ADMIN_ID} berhasil dibuat!")
        
    except Exception as e:
        print(f"ERROR: Terjadi kesalahan: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_admin()