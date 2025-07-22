from fastapi import APIRouter

router = APIRouter()

@router.post("/process")
async def process_accounting():
    return {"msg": "구현 해야함"}

@router.get("/records")
async def get_records(companyId: str):
    return {"msg": f"구현 해야함, companyId={companyId}"}
