import enum
from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, Enum, DateTime, Date, func
from enum import IntFlag
from app.database import Base

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

class MemberStatus(enum.Enum):
    PENDING = "DITUNDA"
    REJECTED = "DITOLAK"
    ACTIVE = "AKTIF"
    INACTIVE = "TIDAK AKTIF"
    RESIGNED = "KELUAR"

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)

    member_id = Column(String, unique=True, nullable=True, index=True) 
    hashed_password = Column(String, nullable=True)
    temporary_password = Column(String, nullable=True)
    must_change_password = Column(Boolean, default=True)

    full_name = Column(String)
    birth_place = Column(String)
    birth_date = Column(Date)
    gender = Column(String, nullable=False)
    address = Column(String)
    family_card_number = Column(String)
    identity_number = Column(String, unique=True)
    phone_number = Column(String)
    spouse_name = Column(String)
    job = Column(String)

    dkm_group = Column(Enum(KelompokDKM), nullable=False)
    mandatory_savings = Column(Enum(SetoranWajib))
    submitted_at = Column(DateTime)

    approved_at = Column(DateTime, server_default=func.now())
    approved_by = Column(String)

    member_status = Column(Enum(MemberStatus), index=True, default=MemberStatus.PENDING)
    left_at = Column(DateTime)
    status_note = Column(Text)