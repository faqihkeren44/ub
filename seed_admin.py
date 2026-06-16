from app.database import SessionLocal
from app import models
from app.core import security
from app.database import DATABASE_URL

print(DATABASE_URL)
def seed_admin():
    db = SessionLocal()

    try:
        admin = db.query(models.Admin).filter(
            models.Admin.admin_id == "admin_ub_001"
        ).first()

        if admin:
            print("Admin sudah ada")
            return

        new_admin = models.Admin(
            admin_id="admin_ub_001",
            full_name="Administrator Utama",
            hashed_password=security.hash_password("admin123"),
            role="superadmin"
        )

        db.add(new_admin)
        db.commit()

        print("Admin berhasil dibuat")

    except Exception as e:
        db.rollback()
        print(e)

    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()