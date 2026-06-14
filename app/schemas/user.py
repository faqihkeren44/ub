from pydantic import BaseModel, field_validator, model_validator
from fastapi import Form
from typing import Optional
from decimal import Decimal
from datetime import date
import re

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
    job: str
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
        job: str = Form(...),        
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
            job=job,
            dkm_group=dkm_group,
            mandatory_savings=mandatory_savings
        )

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password minimal 8 karakter")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Harus mengandung huruf besar")
        if not re.search(r"[a-z]", value):
            raise ValueError("Harus mengandung huruf kecil")
        if not re.search(r"\d", value):
            raise ValueError("Harus mengandung angka")
        return value

    @model_validator(mode="after")
    def verify_password_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("Konfirmasi password baru tidak cocok")
        if self.current_password == self.new_password:
            raise ValueError("Password baru tidak boleh sama dengan password lama")
        return self

def get_password_form(
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
) -> PasswordChange:
    return PasswordChange(
        current_password=current_password,
        new_password=new_password,
        confirm_password=confirm_password
    )