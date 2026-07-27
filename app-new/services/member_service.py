from fastapi import Depends
from sqlalchemy.orm import Session
from app import database, models
from app.core import password, security

# ==========================================================
# RESET PASSWORD
# ==========================================================

def reset_password_member(
    db: Session,
    member: models.Member
) -> str:
    new_password = password.generate_password(8)
    member.hashed_password = security.hash_password(new_password)
    member.temporary_password = new_password
    member.must_change_password = True

    db.commit()

    return new_password