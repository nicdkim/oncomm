from app.models.transaction import Transaction
from app.core.database import SessionLocal
from sqlalchemy.orm import Session

def create_transaction_records(records: list):
    session: Session = SessionLocal()
    try:
        for r in records:
            tx = Transaction(
                date=r["거래일시"],
                description=r["적요"],
                amount=r["금액"],
                company_id=r.get("company_id"),
                category_id=r.get("category_id"),
                category_name=r.get("category_name"),
                raw_data=str(r),
                classified=r.get("classified", False)
            )
            session.add(tx)
        session.commit()
    finally:
        session.close()

def get_transactions_by_company(company_id: str):
    session: Session = SessionLocal()
    try:
        txs = session.query(Transaction).filter(Transaction.company_id == company_id).all()
        return txs
    finally:
        session.close()
