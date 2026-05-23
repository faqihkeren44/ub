from pydantic import BaseModel, EmailStr, Field
from fastapi import Form
from typing import Optional
from decimal import Decimal
from datetime import date

class UserCreate(BaseModel):
    full_name: str
    birth_date: date
    birth_place: str
    gender: str
    address: str
    family_card_number: str
    identity_number: str
    phone_number: str
    spouse_name: Optional[str] = None
    dkm_group: str
    mandatory_savings: int

    @classmethod
    def as_form(
        cls,
        full_name: str = Form(...),
        birth_date: date = Form(...),
        birth_place: str = Form(...),
        gender: str = Form(...),
        address: str = Form(...),
        family_card_number: str = Form(...),
        identity_number: str = Form(...),
        phone_number: str = Form(...),
        spouse_name: Optional[str] = Form(None),
        dkm_group: str = Form(...),
        mandatory_savings: int = Form(...)
    ):
        return cls(
            full_name=full_name,
            birth_date=birth_date,
            birth_place=birth_place,
            gender=gender,
            address=address,
            family_card_number=family_card_number,
            identity_number=identity_number,
            phone_number=phone_number,
            spouse_name=spouse_name,
            dkm_group=dkm_group,
            mandatory_savings=mandatory_savings
        )

