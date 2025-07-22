from fastapi import FastAPI
from app.api.v1.accounting import router as accounting_router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI E-Commerce Accounting API")
app.include_router(accounting_router, prefix="/api/v1/accounting")
