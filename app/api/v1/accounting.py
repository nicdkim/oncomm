from fastapi import APIRouter, UploadFile, File, Query
from app.services.classify import process_transactions
from app.schemas.process import ProcessResponse
from app.schemas.transaction import TransactionOut
from app.crud.transaction import get_transactions_by_company

router = APIRouter()

@router.post("/process", response_model=ProcessResponse)
async def process_accounting(
    bank_csv: UploadFile = File(...),
    rules_json: UploadFile = File(...)
):
    summary = await process_transactions(bank_csv, rules_json)
    return summary

@router.get("/records", response_model=list[TransactionOut])
def get_records(
    companyId: str = Query(...),
):
    return get_transactions_by_company(companyId)
