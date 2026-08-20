from fastapi import FastAPI

from app.routers import health, transactions


app = FastAPI(
    title="Investment AI API",
    description="API para gestionar inversiones y consultar información financiera autorizada.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(transactions.router)
