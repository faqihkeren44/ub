import enum
from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, Enum
from enum import IntFlag
from app.database import Base

class TestTable(Base):
    __tablename__ = "test_table"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class KelompokDKM(enum.Enum):
    DARUSSALAM = "DKM DARUSSALAM - Gunung Gede"
    AL_BAROKAH = "DKM AL BAROKAH - Pondok Rumput"
    DARUL_HIKMAH = "DKM DARUL HIKMAH - Green Arofah"
    AR_RAUDHOH = "DKM AR-RAUDHOH - Pakuan"
    BAITUL_IZZA = "DKM BAITUL IZZA - Tajur"
    AN_NASHR = "DKM AN-NASHR - Cikaret"
    AR_ROHMAN = "DKM AR-ROHMAN - Ciapus"

class SetoranWajib(enum.IntEnum):
    LEVEL_25K = 25000
    LEVEL_50K = 50000
    LEVEL_100K = 100000
    LEVEL_250K = 250000
    LEVEL_500K = 500000

class GenderType(enum.Enum):
    MALE = "Pria"
    FEMALE = "Wanita"

class UserStatus(IntFlag):
    PENDING = 1
    APPROVED = 2
    REJECTED = 4

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)

    # Data Identitas
    full_name = Column(String, nullable=False)
    birth_info = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    address = Column(String, nullable=False)
    family_card_number = Column(String, nullable=False) # No KK
    identity_number = Column(String, unique=True, nullable=False) # No KTP
    phone_number = Column(String, nullable=False)
    spouse_name = Column(String, nullable=True) # Nama Pasangan

    # Pilihan Terbatas
    dkm_group = Column(Enum(KelompokDKM), nullable=False)
    mandatory_savings = Column(Enum(SetoranWajib), nullable=False)

    # Akun Anggota
    member_id = Column(String, unique=True, nullable=True) 
    hashed_password = Column(String, nullable=True)

    # Status
    status_flags = Column(Integer, default=UserStatus.PENDING.value)
    approved_by = Column(String, nullable=True)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    price = Column(Numeric, nullable=False)
    stock = Column(Integer, default=0)