from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class ProductBase(BaseModel):
    name: str = Field(..., min_length=3)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    
    class Config:
        from_attributes = True