from sqlalchemy import Column, Integer, String, Numeric, Text
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    price = Column(Numeric, nullable=False)
    stock = Column(Integer, default=0)