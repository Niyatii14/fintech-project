from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: float
    category: str
    description: str
    type: str

class TransactionResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: str
    type: str
    created_at : datetime

    class Config:
        from_attributes = True
        

