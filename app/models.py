from sqlalchemy import Column, Integer, String
from app.database import Base

class TestTable(Base):
    __tablename__ = "test_table"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)