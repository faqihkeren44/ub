from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database, utils

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/register", response_model=schemas.UserOut)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user_exist = db.query(models.User).filter(models.User.email == user_data.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    hashed_password = utils.hash_password(user_data.password)

    new_user = models.User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user