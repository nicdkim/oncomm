from fastapi import FastAPI
from app.api.v1.accounting import router as accounting_router

app = FastAPI(title="AI E-Commerce Accounting API")
app.include_router(accounting_router, prefix="/api/v1/accounting")
