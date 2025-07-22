from fastapi import FastAPI
from app.api.v1.accounting import router as accounting_router

app = FastAPI(title="AI E-Commerce Accounting API")
app.include_router(accounting_router, prefix="/api/v1/accounting")

@app.get("/")
async def root():
    return {
        "msg": "AI 이커머스 경영 경리 프로그램입니다. API 문서는 /docs 에서 확인하세요."
    }