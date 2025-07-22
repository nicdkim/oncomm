from pydantic import BaseModel
from typing import Optional

class TransactionOut(BaseModel):
    id: int
    date: str
    description: str
    amount: float
    company_id: Optional[str]
    category_id: Optional[str]
    category_name: Optional[str]
    classified: bool

    class Config:
        orm_mode = True
