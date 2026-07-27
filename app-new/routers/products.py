from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database, models, schemas

router = APIRouter(
    prefix="/products",
    tags=['Products']
)

@router.get("/", response_model=list[schemas.ProductOut])
def get_products(db: Session = Depends(database.get_db)):
    products = db.query(models.Product).all()
    return products

@router.post("/", response_model=schemas.ProductOut)
def input_product(product_data:schemas.ProductCreate, db: Session = Depends(database.get_db)):
    new_product = models.Product(**product_data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product