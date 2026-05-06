from pydantic import BaseModel, EmailStr, Field
from fastapi import Form
from typing import Optional
from decimal import Decimal

class UserCreate(BaseModel):
    full_name: str
    birth_info: str
    gender: str
    address: str
    family_card_number: str
    identity_number: str
    phone_number: str
    spouse_name: Optional[str] = None
    dkm_group: str
    mandatory_savings: int
    password: str

    @classmethod
    def as_form(
        cls,
        full_name: str = Form(...),
        birth_info: str = Form(...),
        gender: str = Form(...),
        address: str = Form(...),
        family_card_number: str = Form(...),
        identity_number: str = Form(...),
        phone_number: str = Form(...),
        spouse_name: Optional[str] = Form(None),
        dkm_group: str = Form(...),
        mandatory_savings: int = Form(...),
        password: str = Form(...)
    ):
        return cls(
            full_name=full_name,
            birth_info=birth_info,
            gender=gender,
            address=address,
            family_card_number=family_card_number,
            identity_number=identity_number,
            phone_number=phone_number,
            spouse_name=spouse_name,
            dkm_group=dkm_group,
            mandatory_savings=mandatory_savings,
            password=password
        )

class UserOut(BaseModel):
    identity_number: str
    member_id: str
    full_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

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