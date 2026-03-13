from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import user, transaction
from app.routes.auth import router as auth_router
from app.routes.transactions import router as transaction_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Server is running"}

app.include_router(transaction_router)
