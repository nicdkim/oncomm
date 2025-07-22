from sqlalchemy import Column, String, ForeignKey
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    company_id = Column(String, ForeignKey("companies.id"))
