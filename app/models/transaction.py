from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from app.core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    company_id = Column(String, ForeignKey("companies.id"), nullable=True)
    category_id = Column(String, ForeignKey("categories.id"), nullable=True)
    category_name = Column(String, nullable=True)
    raw_data = Column(Text, nullable=True)
    classified = Column(Boolean, default=False)
