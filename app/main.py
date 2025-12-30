from fastapi import FastAPI
from app.routes import accounts, transactions, auth

app = FastAPI(
    title="Banking API",
    description="Early-stage banking system migrated to FastAPI",
    version="0.1.0"
)


app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"status": "running"}


