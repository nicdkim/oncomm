from sqlalchemy import Column, String
from app.core.database import Base

class Company(Base):
    __tablename__ = "companies"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
